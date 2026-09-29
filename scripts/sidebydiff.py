#!/usr/bin/env python3
r"""
Generate a section-aligned side-by-side diff of committed manuscripts.
Read chapters, nested inputs, and cover wording from each source version.
Align existing headings, then compare paragraphs and words within each
section. Columns flow across pages and synchronize at section boundaries.
Both sides retain their full text; only changed words receive highlights.
"""

from difflib import SequenceMatcher
import os
import re
import subprocess
import sys
import shutil
import tempfile

from build_pdf import compile_pdf

CHAPTER_ORDER = [
    "docs/proposal-phase/proposal/chapters/00-frontmatter.tex",
    "docs/proposal-phase/proposal/chapters/01-pendahuluan.tex",
    "docs/proposal-phase/proposal/chapters/02-tinjauan-pustaka.tex",
    "docs/proposal-phase/proposal/chapters/03-metodologi.tex",
    "docs/proposal-phase/proposal/chapters/04-jadwal.tex",
]

CLASS_PATH = "docs/proposal-phase/assets/isi-proposal.cls"
BIB_PATH = "docs/proposal-phase/assets/references.bib"
LOGO_PATH = "docs/proposal-phase/assets/logo-isi.png"

# Placeholders are dynamically loaded from env files.


def get_git_content(ref, path):
    """Get file content from a git tag/commit. Empty string if missing."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def resolve_git_ref(ref):
    # Accept the convenient lowercase spelling without requiring a tag.
    if ref.lower() == "head":
        ref = "HEAD"
    candidates = [ref]
    for prefix in ["thesis/", "proposal/"]:
        if not ref.startswith(prefix):
            candidates.append(f"{prefix}{ref}")
    for candidate in candidates:
        res = subprocess.run(
            ["git", "rev-parse", "--verify", "--end-of-options", f"{candidate}^{{commit}}"],
            capture_output=True, text=True,
        )
        if res.returncode == 0:
            tag = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/tags/{candidate}"],
                capture_output=True,
            )
            return candidate if tag.returncode == 0 else res.stdout.strip()
    raise ValueError(f"Unknown Git ref: {ref}")


def clean_latex_for_diff(text, class_source=None):
    """Preserve source page boundaries, wording, and local formatting."""
    text = replace_title_page(text, class_source)
    text = re.sub(r'(?<!\\)%.*', '', text)
    # The renderer handles page boundaries outside the comparison columns.
    text = text.replace(r"\begin{titlepage}", r"\begingroup")
    text = text.replace(r"\end{titlepage}", "\\endgroup\n\\newpage")
    text = re.sub(r'\\vfill\b|\\vspace\*\{\\fill\}', '', text)
    # A source page number must not reset the comparison's page counter.
    text = re.sub(r'\\setcounter\{page\}\{[^{}]*\}', '', text)
    return text


def find_git_path(ref, filename):
    """Find the path of filename in a given git ref dynamically."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    paths = result.stdout.splitlines()
    if filename == "main.tex.template":
        proposal_templates = [
            "docs/proposal-phase/proposal/main.tex.template",
            "thesis/proposal/main.tex.template",
        ]
        thesis_templates = ["docs/final-thesis/thesis/main.tex.template"]
        candidates = (proposal_templates + thesis_templates
                      if ref.startswith("proposal/")
                      else thesis_templates + proposal_templates)
        for path in candidates:
            if path in paths:
                return path
        raise ValueError(f"No manuscript template found at {ref}")
    for line in paths:
        if os.path.basename(line) == filename:
            return line
    return None


def get_template_inputs(ref):
    """
    Extract exact chapter paths relative to the selected manuscript template.
    """
    path = find_git_path(ref, "main.tex.template")
    content = get_git_content(ref, path)
    matches = re.findall(r'\\input\{([^}]+)\}', content)
    filenames = []
    for m in matches:
        m = m.strip()
        if not m.endswith(".tex"):
            m = m + ".tex"
        filenames.append(os.path.normpath(os.path.join(os.path.dirname(path), m)))
    return filenames


def extract_section_formatting(ref):
    """
    Find main.tex.template in git ref, and extract formatting commands:
    \\renewcommand{\\thesection}...
    \\titleformat{\\section}...
    \\titleformat{\\subsection}...
    \\titleformat{\\subsubsection}...
    """
    path = find_git_path(ref, "main.tex.template")
    if not path:
        return ""
    content = get_git_content(ref, path)
    commands = []
    for line in content.splitlines():
        line_strip = line.strip()
        if any(pat in line_strip for pat in ["\\thesection", "\\titleformat{\\section}", "\\titleformat{\\subsection}", "\\titleformat{\\subsubsection}", "\\renewcommand{\\figurename}", "\\renewcommand{\\tablename}"]):
            commands.append(line_strip)
        elif re.match(r'\\(?:tolerance|emergencystretch|hyphenpenalty|exhyphenpenalty)\s*=', line_strip):
            commands.append(line_strip)
        elif line_strip in (r"\doublespacing", r"\onehalfspacing", r"\singlespacing"):
            commands.append(line_strip)
    chapter_definition = re.search(r'\\newcommand\{\\thesischapter\}\[2\]', content)
    if chapter_definition:
        body, _ = read_braced_argument(content, chapter_definition.end())
        body = re.sub(r'\\clearpage\b', '', body)
        body = re.sub(r'\\addcontentsline\{[^{}]*\}\{[^{}]*\}\{[^{}]*\}', '', body)
        body = re.sub(r'(?<!\\)%.*', '', body)
        commands.append(r"\def\thesischapter#1#2{" + body + "}")
    return "\n  ".join(commands)


def build_full_proposal(ref):
    """
    Concatenate all chapter files for a given git ref, in the exact order
    main.tex.template \\input's them, into one continuous LaTeX string --
    this is the "whole proposal compiled as one file" the diff runs against,
    not a per-file diff with separate sections per chapter.
    """
    parts = []
    template_path = find_git_path(ref, "main.tex.template")
    template = get_git_content(ref, template_path)
    document_root = os.path.dirname(template_path)

    def read_input(path, stack=()):
        if path in stack:
            raise ValueError(f"Recursive LaTeX input at {ref}:{path}")
        content = get_git_content(ref, path)
        if not content:
            raise ValueError(f"Missing or empty LaTeX input at {ref}:{path}")

        def expand(match):
            name = match.group(1).strip()
            if not name.endswith(".tex"):
                name += ".tex"
            nested_path = os.path.normpath(os.path.join(document_root, name))
            return read_input(nested_path, (*stack, path))

        return re.sub(r'\\input\{([^}]+)\}', expand, content)

    # Keep chapter headings from the template in their original input order.
    template_body = template.split(r"\begin{document}", 1)[-1]
    chapter_break = re.search(r'\\newcommand\{\\thesischapter\}\[2\]', template)
    chapter_body = read_braced_argument(template, chapter_break.end())[0] if chapter_break else ""
    for match in re.finditer(r'\\input\{([^}]+)\}|\\thesischapter\{([^}]+)\}\{([^}]+)\}|\\(?:newpage|clearpage)\b', template_body):
        if match.group(1):
            name = match.group(1).strip()
            if not name.endswith(".tex"):
                name += ".tex"
            parts.append(read_input(os.path.normpath(os.path.join(document_root, name))).strip())
        else:
            if match.group(2) and re.search(r'\\(?:newpage|clearpage)\b', chapter_body):
                parts.append(r"\clearpage")
            parts.append(match.group(0))
    full_text = "\n\n".join(parts)
    class_path = find_git_path(ref, "isi-proposal.cls")
    class_source = get_git_content(ref, class_path) if class_path else ""
    return clean_latex_for_diff(full_text, class_source)


def split_paragraphs(content):
    """Split into paragraph blocks, separated by 1+ blank lines. Respects tikzpicture blocks to prevent formatting/compilation issues."""
    if not content:
        return []
    normalized = content.replace("\r\n", "\n")
    paragraphs = []
    current_para_lines = []
    in_tikz = False
    
    lines = normalized.split("\n")
    for line in lines:
        line_strip = line.strip()
        if "\\begin{tikzpicture}" in line_strip:
            in_tikz = True
        
        if not line_strip and not in_tikz:
            if current_para_lines:
                paragraphs.append("\n".join(current_para_lines).strip())
                current_para_lines = []
        else:
            current_para_lines.append(line)
            
        if "\\end{tikzpicture}" in line_strip:
            in_tikz = False
            
    if current_para_lines:
        paragraphs.append("\n".join(current_para_lines).strip())
        
    return [p for p in paragraphs if p]


def compute_lcs(a, b):
    """Longest Common Subsequence, run at paragraph level (not line level)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            lcs.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs.reverse()
    return lcs


def compute_diff(old_paragraphs, new_paragraphs):
    """Return list of ('equal' | 'delete' | 'insert', paragraph_text)."""
    lcs = compute_lcs(old_paragraphs, new_paragraphs)
    ops = []
    i = j = 0
    lcs_idx = 0
    while i < len(old_paragraphs) or j < len(new_paragraphs):
        if (lcs_idx < len(lcs)
                and i < len(old_paragraphs)
                and old_paragraphs[i] == lcs[lcs_idx]
                and j < len(new_paragraphs)
                and new_paragraphs[j] == lcs[lcs_idx]):
            ops.append(("equal", old_paragraphs[i]))
            i += 1
            j += 1
            lcs_idx += 1
        elif i < len(old_paragraphs) and (
            lcs_idx >= len(lcs) or old_paragraphs[i] != lcs[lcs_idx]
        ):
            ops.append(("delete", old_paragraphs[i]))
            i += 1
        elif j < len(new_paragraphs) and (
            lcs_idx >= len(lcs) or new_paragraphs[j] != lcs[lcs_idx]
        ):
            ops.append(("insert", new_paragraphs[j]))
            j += 1
        else:
            i += 1
            j += 1
    return ops


# ---------------------------------------------------------------------------
# Word-level diff (second pass). Same LCS machinery as paragraph-level,
# just fed tokens instead of whole paragraphs.
#
# IMPORTANT: naive whitespace tokenization is UNSAFE for LaTeX source.
# A "word" split purely on spaces can land mid-macro-argument, e.g.
# `\makeisititle{...}{Semester Ganjil 2026/2027}{2026}` whitespace-splits
# into a token like `2026/2027}{2026}` which has unbalanced braces on
# its own. Wrapping that fragment in \colorbox{color}{...} desyncs brace
# matching for the REST of the document and cascades into a fatal
# "Missing \endgroup" / "Emergency stop" error.
#
# Fix: after whitespace-splitting, merge adjacent tokens until the
# running brace balance returns to zero, so every token handed to
# \colorbox is guaranteed self-balanced. This trades some highlight
# granularity (a whole macro-argument may light up as one chunk instead
# of word-by-word) for a document that actually compiles.
# ---------------------------------------------------------------------------

DISPLAY_MATH_ENVIRONMENTS = r"(?:equation|multline|align|alignat|flalign|gather|displaymath)\*?"
DISPLAY_MATH_START = re.compile(r'\\begin\{' + DISPLAY_MATH_ENVIRONMENTS + r'\}|\\\[')
DISPLAY_MATH_END = re.compile(r'\\end\{' + DISPLAY_MATH_ENVIRONMENTS + r'\}|\\\]')


UNSAFE_HIGHLIGHT_PATTERNS = (
    "\\\\",       # row breaks (tabularx, tikz) -- illegal in restricted h-mode
    "\\begin",
    "\\end",
    "\\newpage",
    "\\item",
    "&",          # alignment tab -- illegal in boxes
    "\\hline",    # table lines
    "\\cline",
    "\\cellcolor", # table cell coloring
    "\\multicolumn",
)


def _is_safe_to_highlight(token_text):
    """
    Refuse to wrap a token in \\colorbox if it contains constructs that
    are illegal inside a restricted-horizontal-mode box (\\colorbox is
    built on \\getitemize), even when its braces are balanced. \\\\ / \\begin
    / \\end / \\newpage all require paragraph or vertical mode.
    """
    if any(pat in token_text for pat in UNSAFE_HIGHLIGHT_PATTERNS):
        return False
    if re.search(r'\\[^%_#$]', token_text):
        return False
    if re.search(r'(?<!\\)%', token_text):
        return False
    if re.search(r'(?<!\\)_', token_text):
        return False
    if re.search(r'(?<!\\)\^', token_text):
        return False
    if re.search(r'(?<!\\)\$', token_text):
        return False
    return True


def tokenize_words(text):
    """
    Split a paragraph into brace-safe and math-safe tokens.

    Pass 1: split on whitespace, tracking newlines as boundaries.
    Pass 2: merge consecutive word-tokens whenever the running
            '{' minus '}' count is nonzero, unescaped '$' is unbalanced, or
            inside a display math environment, so every emitted token is
            individually brace-balanced and math-balanced.
    """
    # Keep compact environment wrappers separate from visible heading words.
    # Include begin arguments so highlights cannot replace an environment's size.
    text = re.sub(r'\\begin\{[^{}]+\}(?:\[[^\]]*\])?(?:\{[^{}]*\})*|\\end\{[^{}]+\}|\\(?:begingroup|endgroup)\b',
                  lambda match: " " + match.group(0) + " ", text)
    # Build a flat stream of ('W', word) / ('NL', None) first.
    stream = []
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if idx > 0:
            stream.append(("NL", None))
        for word in line.split():
            # Keep attached punctuation with inline math; splitting ($x$)
            # into three words invents spaces next to the parentheses.
            stream.append(("W", word))

    merged = []
    buf = []
    brace_balance = 0
    math_mode = False
    display_math = False

    def flush():
        if buf:
            merged.append(("W", " ".join(buf)))
            buf.clear()

    for kind, val in stream:
        if kind == "NL":
            if math_mode or display_math or brace_balance != 0:
                # Mid-merge: fold newline into space
                continue
            flush()
            merged.append(("NL", None))
        else:
            buf.append(val)
            
            # Check display math start/end
            if DISPLAY_MATH_START.search(val):
                display_math = True
            
            # Count unescaped braces
            unescaped_opens = len(re.findall(r'(?<!\\)\{', val))
            unescaped_closes = len(re.findall(r'(?<!\\)\}', val))
            brace_balance += unescaped_opens - unescaped_closes
            
            # Count unescaped dollars to toggle math mode
            unescaped_dollars = len(re.findall(r'(?<!\\)\$', val))
            if unescaped_dollars % 2 != 0:
                math_mode = not math_mode
                
            if DISPLAY_MATH_END.search(val):
                display_math = False
                
            if brace_balance <= 0 and not math_mode and not display_math:
                flush()
                brace_balance = 0
    flush()
    return merged


def render_token(token, highlight=None):
    """Render a single token. `highlight` is a color name or None."""
    kind, value = token
    if kind == "NL":
        return "\n"
    if highlight and _is_safe_to_highlight(value):
        return f"\\colorbox{{{highlight}}}{{{value}}} "
    return f"{value} "


def is_safe_to_highlight_token(val, is_math=False, is_box=False):
    # A trailing TeX space escape would escape the highlight's closing brace.
    if val.endswith("\\"):
        return False
    if is_math:
        if any(pat in val for pat in ["\\begin{equation}", "\\begin{multline}", "\\begin{align}", "\\begin{gather}"]):
            return False
        return True
        
    if any(pat in val for pat in UNSAFE_HIGHLIGHT_PATTERNS):
        return False
        
    if re.search(r'(?<!\\)%', val):
        return False
        
    if not is_box:
        if re.search(r'(?<!\\)_', val) or re.search(r'(?<!\\)\^', val) or re.search(r'(?<!\\)\$', val):
            return False
            
    macros = re.findall(r'\\([a-zA-Z\*]+)', val)
    allowed_macros = {
        "textit", "textbf", "emph", "underline", "section", "subsection", "subsubsection",
        "parencite", "cite", "textcite", "citeauthor", "citeyear", "texttt"
    }
    for macro in macros:
        if macro not in allowed_macros:
            return False
            
    return True


def classify_token_style(style, val):
    if not style:
        return None
    # Display math needs a block background, preserving AMS layout and row breaks.
    if DISPLAY_MATH_START.search(val) and DISPLAY_MATH_END.search(val):
        return style + "_display"
    val_strip = val.strip()
    val_clean = re.sub(r'[\.,;\?!\)]+$', '', val_strip)
    val_clean = re.sub(r'^\(', '', val_clean)
    
    if re.match(r'^\$([^$]*)\$$', val_clean):
        if is_safe_to_highlight_token(val, is_math=True):
            return style + "_math"
        return None
        
    if re.match(r'^\\(section|subsection|subsubsection)\{.*\}$', val_clean):
        if is_safe_to_highlight_token(val):
            return style + "_format"
        return None
        
    if re.match(r'^\\(parencite|cite|textcite|citeauthor|citeyear)\{.*\}$', val_clean):
        if is_safe_to_highlight_token(val, is_box=True):
            # Citation expansion is unsafe inside soul's text reconstruction.
            return style + "_box"
        return None
        
    if is_safe_to_highlight_token(val):
        return style + "_text"
        
    return None


def highlight_prose(text, command):
    """Paint words and their connecting glue inside the source formatting."""
    parts = []
    pos = 0
    formatting = re.compile(r'\\(?:textit|textbf|emph|underline|texttt)\{|(?<!\\)\{')
    color = "delhl" if command == "delhighlight" else "inshl"

    def paint_words(plain):
        return "".join(f"\\diffspace{{{color}}}" if piece.isspace() else f"\\{command}{{{piece}}}"
                       for piece in re.split(r'(\s+)', plain) if piece)

    while match := formatting.search(text, pos):
        parts.append(paint_words(text[pos:match.start()]))
        content, end = read_braced_argument(text, match.end() - 1)
        parts.append(text[match.start():match.end()] + highlight_prose(content, command) + "}")
        pos = end
    parts.append(paint_words(text[pos:]))
    return "".join(parts)


def apply_highlight(style, text):
    if not style:
        return text + " "
    
    color = "delhl" if style.startswith("delhl") else "inshl"
    if style.endswith("_display"):
        return f"\\begin{{diffmath}}{{{color}}}\n{text}\n\\end{{diffmath}}\n"
    if style.endswith("_text"):
        hl_cmd = "delhighlight" if color == "delhl" else "inhighlight"
        # Parentheses and punctuation belong to the changed text as well.
        return highlight_prose(text.strip(), hl_cmd) + " "
    val_strip = text.strip()
    punc_start = ""
    if val_strip.startswith("("):
        punc_start = "("
        val_strip = val_strip[1:]
    punc_end = ""
    punc_match = re.search(r'[\.,;\?!\)]+$', val_strip)
    if punc_match:
        punc_end = punc_match.group(0)
        val_strip = val_strip[:-len(punc_end)]
    
    if style.endswith("_format"):
        pattern = r'^\\(section|subsection|subsubsection)\{(.*)\}$'
        match = re.match(pattern, val_strip)
        if match:
            macro_name = match.group(1)
            content = match.group(2)
            the_cmd = f"\\the{macro_name}"
            return (
                f"{punc_start}"
                f"{{\\let\\origthe{the_cmd}"
                f"\\renewcommand{{{the_cmd}}}{{\\colorbox{{{color}}}{{\\origthe}}}}"
                f"\\{macro_name}{{\\colorbox{{{color}}}{{{content}}}}}}}"
                f"{punc_end} "
            )
            
    if style.endswith("_box"):
        return f"\\diffinline{{{color}}}{{{punc_start}{val_strip}{punc_end}}} "
            
    if style.endswith("_math"):
        math_pattern = r'^\$([^$]*)\$$'
        match = re.match(math_pattern, val_strip)
        if match:
            content = match.group(1)
            return f"\\diffinline{{{color}}}{{{punc_start}\\ensuremath{{{content}}}{punc_end}}} "
        
    return text + " "


def word_level_render(old_text, new_text):
    """
    Run word-level LCS between old_text and new_text. Return
    (old_rendered, new_rendered) where only the differing words are
    wrapped in highlight commands (when safe to do so)
    -- everything matching stays plain text on BOTH sides, exactly like
    VSCode's inline word diff.
    """
    # A matched heading is a container, not one changed word. Compare its
    # title separately so formatting changes do not color its unchanged
    # wording or automatically generated section number.
    heading_pattern = r'^(\s*\\(section|subsection|subsubsection)\*?(?:\[[^\]]*\])?)\{'
    old_heading = re.match(heading_pattern, old_text)
    new_heading = re.match(heading_pattern, new_text)
    if old_heading and new_heading and old_heading.group(2) == new_heading.group(2):
        old_title, old_end = read_braced_argument(old_text, old_heading.end() - 1)
        new_title, new_end = read_braced_argument(new_text, new_heading.end() - 1)
        left_title, right_title = word_level_render(old_title, new_title)
        left_body, right_body = word_level_render(old_text[old_end:], new_text[new_end:])
        return (
            old_heading.group(1) + "{" + left_title.rstrip() + "}" + left_body,
            new_heading.group(1) + "{" + right_title.rstrip() + "}" + right_body,
        )

    old_tokens = tokenize_words(old_text)
    new_tokens = tokenize_words(new_text)
    ops = compute_diff(old_tokens, new_tokens)

    old_actions = []
    new_actions = []

    for kind, tok in ops:
        kind_type, value = tok
        if kind == "equal":
            if kind_type == "NL":
                old_actions.append((None, "\n"))
                new_actions.append((None, "\n"))
            else:
                old_actions.append((None, value))
                new_actions.append((None, value))
        elif kind == "delete":
            if kind_type == "NL":
                old_actions.append((None, "\n"))
            else:
                act_style = classify_token_style("delhl", value)
                val_to_use = value
                if act_style == "delhl_text" and re.match(r'^\\(parencite|cite|textcite|citeauthor|citeyear)\{.*\}$', re.sub(r'[\.,;\?!\)]+$', '', value.strip()).strip()):
                    val_to_use = f"\\mbox{{{value}}}"
                old_actions.append((act_style, val_to_use))
        elif kind == "insert":
            if kind_type == "NL":
                new_actions.append((None, "\n"))
            else:
                act_style = classify_token_style("inshl", value)
                val_to_use = value
                if act_style == "inshl_text" and re.match(r'^\\(parencite|cite|textcite|citeauthor|citeyear)\{.*\}$', re.sub(r'[\.,;\?!\)]+$', '', value.strip()).strip()):
                    val_to_use = f"\\mbox{{{value}}}"
                new_actions.append((act_style, val_to_use))

    def merge_runs(actions):
        if not actions:
            return []
        merged = []
        cur_style, val = actions[0]
        cur_list = [val]
        for style, val in actions[1:]:
            # Keep highlighted tokens separate so ordinary inter-word glue can
            # stretch and break under the source's justification settings. A
            # long soul run otherwise overflows with \emergencystretch=\maxdimen.
            if (style is None and cur_style is None
                    and val != "\n" and cur_list[-1] != "\n"):
                cur_list.append(val)
            else:
                merged.append((cur_style, " ".join(cur_list)))
                cur_style = style
                cur_list = [val]
        merged.append((cur_style, " ".join(cur_list)))
        return merged

    old_merged = merge_runs(old_actions)
    new_merged = merge_runs(new_actions)

    def render_merged(runs):
        parts = []
        joined_newlines = set()

        def inline_color(style):
            if style and style.endswith(("_text", "_math", "_box")):
                return "delhl" if style.startswith("delhl") else "inshl"
            return None

        for index, (style, val) in enumerate(runs):
            if val == "\n":
                parts.append("%\n" if index in joined_newlines else "\n")
            else:
                rendered = apply_highlight(style, val)
                color = inline_color(style)
                following = index + 1
                if following < len(runs) and runs[following][1] == "\n":
                    following += 1
                if (color and following < len(runs)
                        and color == inline_color(runs[following][0])):
                    # Leaders paint the entire justified space and disappear
                    # at a line break; they never box the surrounding phrase.
                    rendered = rendered.removesuffix(" ") + f"\\diffspace{{{color}}}"
                    if following == index + 2:
                        joined_newlines.add(index + 1)
                parts.append(rendered)
        return "".join(parts)

    return render_merged(old_merged), render_merged(new_merged)


PAGE_BREAK = re.compile(r'\\(?:newpage|clearpage)\b')


def frontmatter_identity(text):
    """Match source roles independently of a visible heading or its TeX styling."""
    plain = re.sub(r'\\(?:begin|end)\{[^{}]*\}', '', text)
    plain = re.sub(r'\\[a-zA-Z]+\*?', '', plain)
    plain = re.sub(r'[{}]', '', plain).casefold()
    if re.search(r'^\s*abstrak\s*$|\bkata kunci\s*:', plain, re.MULTILINE):
        return ("frontmatter", "abstract-id")
    if re.search(r'^\s*abstract\s*$|\bkeywords\s*:', plain, re.MULTILINE):
        return ("frontmatter", "abstract-en")
    if "halaman pengesahan" in plain:
        return ("frontmatter", "approval")
    if r"\begingroup" in text and ("skripsi" in plain or "cover" in plain):
        return ("frontmatter", "cover")
    return None


def split_sections(content):
    """Parse source pages and headings, keeping front-matter roles separate."""
    sections = []
    parent = ""
    subsection = ""
    continuation = ("frontmatter",)
    pending_break = ""
    # Keep page commands as metadata on the next block, never as displayed text.
    source_pages = PAGE_BREAK.split(content)
    source_breaks = PAGE_BREAK.findall(content)
    for page_index, page in enumerate(source_pages):
        if page_index:
            pending_break = source_breaks[page_index - 1]
        boundaries = list(re.finditer(
            r'^\s*\\(?:section|subsection|subsubsection)\*?\{[^\n]*|^\s*\\thesischapter\{[^\n]*',
            page, re.MULTILINE,
        ))
        start = 0
        key = frontmatter_identity(page[:boundaries[0].start()] if boundaries else page) or continuation

        def append(end):
            nonlocal pending_break
            text = page[start:end].strip()
            if text:
                sections.append((key, (pending_break + "\n" + text).strip()))
                pending_break = ""

        for match in boundaries:
            append(match.start())
            heading = match.group(0).strip()
            if heading.startswith(r"\thesischapter"):
                parent = subsection = ""
                key = ("chapter", heading)
            elif heading.startswith(r"\section"):
                parent = heading
                subsection = ""
                key = frontmatter_identity(heading) or ("section", parent)
            elif heading.startswith(r"\subsection"):
                subsection = heading
                key = ("subsection", parent, subsection)
            else:
                key = ("subsubsection", parent, subsection, heading)
            start = match.start()
        append(len(page))
        if sections:
            continuation = sections[-1][0]
    return sections


def align_sections(old_sections, new_sections):
    """Keep inserted sections separate instead of shifting subsequent matches."""
    matcher = SequenceMatcher(None, [key for key, _ in old_sections],
                              [key for key, _ in new_sections], autojunk=False)
    pairs = []
    for _, i, end_i, j, end_j in matcher.get_opcodes():
        old_run, new_run = old_sections[i:end_i], new_sections[j:end_j]
        for index in range(max(len(old_run), len(new_run))):
            old = old_run[index][1] if index < len(old_run) else ""
            new = new_run[index][1] if index < len(new_run) else ""
            pairs.append((old, new))
    return pairs


def render_section_text(old_text, new_text):
    """Highlight changed paragraphs without boxing or synchronizing each one."""
    ops = compute_diff(split_paragraphs(old_text), split_paragraphs(new_text))
    left, right = [], []
    deletes, inserts = [], []

    def flush():
        for index in range(max(len(deletes), len(inserts))):
            old = deletes[index] if index < len(deletes) else ""
            new = inserts[index] if index < len(inserts) else ""
            rendered_old, rendered_new = word_level_render(old, new)
            if old:
                left.append(rendered_old)
            if new:
                right.append(rendered_new)
        deletes.clear()
        inserts.clear()

    for kind, text in ops:
        if kind == "equal":
            flush()
            left.append(text)
            right.append(text)
        elif kind == "delete":
            deletes.append(text)
        else:
            inserts.append(text)
    flush()
    return "\n\n".join(left), "\n\n".join(right)


def render_sections(old_full, new_full):
    """Align source sections and honor a page boundary requested by either side."""
    out = [r"\begin{paracol}{2}"]
    has_content = False
    for old_text, new_text in align_sections(split_sections(old_full), split_sections(new_full)):
        if has_content and (PAGE_BREAK.search(old_text) or PAGE_BREAK.search(new_text)):
            out.extend([r"\end{paracol}", r"\newpage", r"\begin{paracol}{2}"])
        left, right = render_section_text(PAGE_BREAK.sub('', old_text).strip(),
                                          PAGE_BREAK.sub('', new_text).strip())
        out.extend([
            r"\begin{leftside}", left, r"\par\end{leftside}",
            r"\switchcolumn", r"\begin{rightside}", right,
            r"\par\end{rightside}", r"\switchcolumn*",
        ])
        has_content = True
    out.append(r"\end{paracol}")
    # A trailing source break still precedes the bibliography.
    if re.search(r'\\(?:newpage|clearpage)\s*$', old_full.strip()) or re.search(r'\\(?:newpage|clearpage)\s*$', new_full.strip()):
        out.append(r"\newpage")
    return "\n".join(out)


def load_env_macros():
    # Try .env.local first, then .env.example
    env_path = ".env.local" if os.path.exists(".env.local") else ".env.example"
    macros = []
    defaults = {
        "THESIS_TITLE": "EVALUASI AKURASI KAIDAH HARMONI FUNGSIONAL PADA MUSIK SIMBOLIK HASIL GENERASI LSTM, CNN, DAN TRANSFORMER",
        "RESEARCHER_NAME": "[Nama Peneliti]",
        "RESEARCHER_NIM": "[NIM]",
        "INSTITUTION_NAME": "[Institusi]",
        "FACULTY_NAME": "[Fakultas]",
        "DEPARTMENT_NAME": "[Jurusan]",
        "PROGRAM_STUDY": "[Program Studi]",
        "CITY_NAME": "[Kota]",
        "SUBMISSION_DATE": "[Tanggal Pengesahan]",
        "ACADEMIC_YEAR": "[Tahun Akademik]",
        "GRADUATION_YEAR": "[Tahun Lulus]",
        "ADVISOR_ACADEMIC": "[Dosen Pembimbing Akademik]",
        "ADVISOR_ACADEMIC_NIP": "[NIP]",
        "ADVISOR_THESIS": "[Dosen Pembimbing Skripsi]",
        "ADVISOR_THESIS_NIP": "[NIP]",
        "EXAMINER_1": "[Penguji 1]",
        "EXAMINER_1_NIP": "[NIP]",
        "EXAMINER_2": "[Penguji 2]",
        "EXAMINER_2_NIP": "[NIP]"
    }
    
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if v:
                        defaults[k] = v

    macros.append(rf"\newcommand{{\thesistitle}}{{{defaults.get('THESIS_TITLE', 'EVALUASI AKURASI KAIDAH HARMONI FUNGSIONAL PADA MUSIK SIMBOLIK HASIL GENERASI LSTM, CNN, DAN TRANSFORMER')}}}")
    macros.append(rf"\newcommand{{\researchername}}{{{defaults.get('RESEARCHER_NAME', '[Nama Peneliti]')}}}")
    macros.append(rf"\newcommand{{\researchernim}}{{{defaults.get('RESEARCHER_NIM', '[NIM]')}}}")
    macros.append(rf"\newcommand{{\institutionname}}{{{defaults.get('INSTITUTION_NAME', '[Institusi]')}}}")
    macros.append(rf"\newcommand{{\facultyname}}{{{defaults.get('FACULTY_NAME', '[Fakultas]')}}}")
    macros.append(rf"\newcommand{{\departmentname}}{{{defaults.get('DEPARTMENT_NAME', '[Jurusan]')}}}")
    macros.append(rf"\newcommand{{\programstudy}}{{{defaults.get('PROGRAM_STUDY', '[Program Studi]')}}}")
    macros.append(rf"\newcommand{{\cityname}}{{{defaults.get('CITY_NAME', '[Kota]')}}}")
    macros.append(rf"\newcommand{{\submissiondate}}{{{defaults.get('SUBMISSION_DATE', '[Tanggal Pengesahan]')}}}")
    macros.append(rf"\newcommand{{\academicyear}}{{{defaults.get('ACADEMIC_YEAR', '[Tahun Akademik]')}}}")
    macros.append(rf"\newcommand{{\graduationyear}}{{{defaults.get('GRADUATION_YEAR', '[Tahun Lulus]')}}}")
    macros.append(rf"\newcommand{{\advisoracademic}}{{{defaults.get('ADVISOR_ACADEMIC', '[Dosen Pembimbing Akademik]')}}}")
    macros.append(rf"\newcommand{{\advisoracademicnip}}{{{defaults.get('ADVISOR_ACADEMIC_NIP', '[NIP]')}}}")
    macros.append(rf"\newcommand{{\advisorthesis}}{{{defaults.get('ADVISOR_THESIS', '[Dosen Pembimbing Skripsi]')}}}")
    macros.append(rf"\newcommand{{\advisorthesisnip}}{{{defaults.get('ADVISOR_THESIS_NIP', '[NIP]')}}}")
    macros.append(rf"\newcommand{{\examinerone}}{{{defaults.get('EXAMINER_1', '[Penguji 1]')}}}")
    macros.append(rf"\newcommand{{\examineronenip}}{{{defaults.get('EXAMINER_1_NIP', '[NIP]')}}}")
    macros.append(rf"\newcommand{{\examinertwo}}{{{defaults.get('EXAMINER_2', '[Penguji 2]')}}}")
    macros.append(rf"\newcommand{{\examinertwonip}}{{{defaults.get('EXAMINER_2_NIP', '[NIP]')}}}")
    return "\n".join(macros)


def read_braced_argument(text, pos):
    """Read a nested TeX argument without treating escaped braces as groups."""
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != "{":
        raise ValueError("Expected a braced LaTeX argument")
    start = pos + 1
    balance = 1
    pos += 1
    while pos < len(text):
        if text[pos] == "\\":
            pos += 2
            continue
        if text[pos] == "{":
            balance += 1
        elif text[pos] == "}":
            balance -= 1
            if balance == 0:
                return text[start:pos], pos + 1
        pos += 1
    raise ValueError("Unclosed LaTeX argument")


def replace_title_page(text, class_source=None):
    """Expand the cover from its version's class; never invent cover labels."""
    if r"\makeisititle" not in text:
        return text
    if class_source is None:
        with open(CLASS_PATH) as source:
            class_source = source.read()
    definition = re.search(r'\\newcommand\{\\makeisititle\}\[5\]', class_source)
    if not definition:
        raise ValueError("Source class has no five-argument makeisititle definition")
    body, _ = read_braced_argument(class_source, definition.end())
    idx = 0
    while (match := re.search(r'\\makeisititle\b', text[idx:])):
        start = idx + match.start()
        pos = start + len(r"\makeisititle")
        args = []
        for _ in range(5):
            arg, pos = read_braced_argument(text, pos)
            args.append(arg)
        replacement = re.sub(r'#([1-5])', lambda m: args[int(m.group(1)) - 1], body)
        text = text[:start] + replacement + text[pos:]
        idx = start + len(replacement)
    return text


def extract_citation_keys(text, suffix=""):
    matches = re.findall(r'\\(?:parencite|cite|textcite|nocite)\{([^}]+)\}', text)
    keys = set()
    for match in matches:
        for key in match.split(','):
            k = key.strip()
            if k:
                keys.add(k + suffix)
    return sorted(list(keys))

def parse_bib(content):
    entries = {}
    idx = 0
    while True:
        idx = content.find('@', idx)
        if idx == -1: break
        brace_idx = content.find('{', idx)
        if brace_idx == -1: break
        entry_type = content[idx+1:brace_idx].strip()
        comma_idx = content.find(',', brace_idx)
        if comma_idx == -1: break
        key = content[brace_idx+1:comma_idx].strip()
        balance = 1
        pos = comma_idx + 1
        while pos < len(content) and balance > 0:
            if content[pos] == '{': balance += 1
            elif content[pos] == '}': balance -= 1
            pos += 1
        if balance == 0:
            fields_text = content[comma_idx+1:pos-1]
            entries[key] = {
                'type': entry_type,
                'fields_text': fields_text,
                'raw': content[idx:pos]
            }
        idx = pos
    return entries

def parse_fields_text(text):
    fields = {}
    idx = 0
    while idx < len(text):
        eq_idx = text.find('=', idx)
        if eq_idx == -1: break
        name = text[idx:eq_idx].strip().split(',')[-1].strip().lower()
        idx = eq_idx + 1
        while idx < len(text) and text[idx] in ' \t\n\r': idx += 1
        if idx == len(text): break
        if text[idx] == '{':
            balance = 1
            pos = idx + 1
            while pos < len(text) and balance > 0:
                if text[pos] == '{': balance += 1
                elif text[pos] == '}': balance -= 1
                pos += 1
            val = text[idx+1:pos-1]
            fields[name] = val
            idx = pos
        elif text[idx] == '"':
            pos = idx + 1
            while pos < len(text) and text[pos] != '"': pos += 1
            val = text[idx+1:pos]
            fields[name] = val
            idx = pos + 1
        else:
            pos = idx
            while pos < len(text) and text[pos] not in ',\n}': pos += 1
            val = text[idx:pos].strip()
            fields[name] = val
            idx = pos
    return fields

def diff_bib_files(bib1_str, bib2_str, keys1, keys2):
    e1 = parse_bib(bib1_str)
    e2 = parse_bib(bib2_str)
    out1 = []
    out2 = []
    for key in set(keys1) | set(keys2):
        if key in keys1 and key not in keys2:
            if key in e1:
                raw = e1[key]['raw'].strip()
                raw = raw[:-1].rstrip() + ',\n  keywords = {v1},\n  userc = {del}\n}'
                out1.append(raw)
        elif key in keys2 and key not in keys1:
            if key in e2:
                raw = e2[key]['raw'].strip()
                raw = raw[:-1].rstrip() + ',\n  keywords = {v2},\n  userc = {ins}\n}'
                out2.append(raw)
        else:
            if key in e1 and key in e2:
                fields1 = parse_fields_text(e1[key]['fields_text'])
                fields2 = parse_fields_text(e2[key]['fields_text'])
                new_f1 = []
                new_f2 = []
                all_fields = set(fields1.keys()) | set(fields2.keys())
                for f in sorted(list(all_fields)):
                    v1 = fields1.get(f)
                    v2 = fields2.get(f)
                    if v1 == v2:
                        if v1 is not None:
                            new_f1.append(f"{f} = {{{v1}}}")
                            new_f2.append(f"{f} = {{{v1}}}")
                    else:
                        if v1 is not None:
                            new_f1.append(f"{f} = {{\\textcolor{{deltext}}{{{v1}}}}}")
                        if v2 is not None:
                            new_f2.append(f"{f} = {{\\textcolor{{instext}}{{{v2}}}}}")
                new_f1.append('keywords = {v1}')
                new_f2.append('keywords = {v2}')
                # Set userc so tcolorbox opens for modified entries too
                new_f1.append('userc = {mod}')
                new_f2.append('userc = {mod}')
                out1.append(f"@{e1[key]['type']}{{{key},\n  " + ",\n  ".join(new_f1) + "\n}")
                out2.append(f"@{e2[key]['type']}{{{key},\n  " + ",\n  ".join(new_f2) + "\n}")
    return "\n".join(out1), "\n".join(out2)

def diff_output_stem(ref1, ref2):
    """Keep resolved ref labels in filenames without creating tag subfolders."""
    names = [re.sub(r'[^A-Za-z0-9._-]', '_', ref) for ref in (ref1, ref2)]
    return f"proposal_diff_{names[0]}_{names[1]}"


def generate_diff_latex(tag1, tag2, outdir):
    os.makedirs(outdir, exist_ok=True)
    stem = diff_output_stem(tag1, tag2)
    bib_filename1 = f"{stem}_references_v1.bib"
    bib_filename2 = f"{stem}_references_v2.bib"
    # Clean old temp files to ensure biber runs correctly
    for ext in ["aux", "log", "bcf", "bbl", "blg", "run.xml", "pdf", "tex", "fdb_latexmk", "fls"]:
        path = os.path.join(outdir, f"{stem}.{ext}")
        if os.path.exists(path):
            os.remove(path)

    old_full = build_full_proposal(tag1)
    new_full = build_full_proposal(tag2)

    # Definitions nested inside newenvironment need doubled parameter markers.
    left_formatting = re.sub(r'(?<!\\)#', "##", extract_section_formatting(tag1))
    right_formatting = re.sub(r'(?<!\\)#', "##", extract_section_formatting(tag2))

    # Extract citations
    pure_v1_keys = extract_citation_keys(old_full)
    v1_keys = extract_citation_keys(old_full, suffix="_v1")
    v2_keys = extract_citation_keys(new_full)

    # Bibliography diff block
    bib_diff = []
    if v1_keys or v2_keys:
        v1_nocite = f"\\nocite{{{', '.join(v1_keys)}}}" if v1_keys else ""
        v2_nocite = f"\\nocite{{{', '.join(v2_keys)}}}" if v2_keys else ""
        bib_diff = [
            v1_nocite,
            v2_nocite,
            r"\begin{paracol}{2}",
            r"\section*{DAFTAR PUSTAKA}",
            r"\printbibliography[heading=none, keyword=v1]" if v1_keys else "",
            r"\switchcolumn",
            r"\section*{DAFTAR PUSTAKA}",
            r"\printbibliography[heading=none, keyword=v2]" if v2_keys else "",
            r"\end{paracol}",
        ]

    body = render_sections(old_full, new_full)
    
    # Append _v1 to citation commands specifically inside the left column 
    # to avoid biber duplicate key merging issues for v1
    def leftside_repl(match):
        content = match.group(1)
        def cite_repl(m2):
            cmd = m2.group(1)
            keys = m2.group(2)
            new_keys = ", ".join([k.strip() + "_v1" if k.strip() else "" for k in keys.split(",")])
            return f"\\{cmd}{{{new_keys}}}"
        new_content = re.sub(r'\\(parencite|cite|textcite|nocite|citeauthor|citeyear)\{([^}]+)\}', cite_repl, content)
        return f"\\begin{{leftside}}{new_content}\\end{{leftside}}"
    
    body = re.sub(r'\\begin\{leftside\}(.*?)\\end\{leftside\}', leftside_repl, body, flags=re.DOTALL)
    body = body + "\n" + "\n".join(bib_diff)

    # Pull class/bib/logo assets so the diff compiles with the real
    # proposal styling instead of a bare article class.
    local_cls = os.path.join("docs", "proposal-phase", "assets", "isi-proposal.cls")
    if os.path.exists(local_cls):
        shutil.copy(local_cls, os.path.join(outdir, "isi-proposal.cls"))
    else:
        cls_path2 = find_git_path(tag2, "isi-proposal.cls")
        cls_path1 = find_git_path(tag1, "isi-proposal.cls")
        cls_content = get_git_content(tag2, cls_path2) if cls_path2 else ""
        if not cls_content and cls_path1:
            cls_content = get_git_content(tag1, cls_path1)
        with open(os.path.join(outdir, "isi-proposal.cls"), "w") as f:
            f.write(cls_content)

    # Write references_v1.bib (from tag1)
    bib_path1 = find_git_path(tag1, "references.bib")
    bib_content_v1 = get_git_content(tag1, bib_path1) if bib_path1 else ""

    # Write references_v2.bib (from tag2 git state; fallback to local if not in git)
    bib_path2 = find_git_path(tag2, "references.bib")
    bib_content_v2 = get_git_content(tag2, bib_path2) if bib_path2 else ""
    if not bib_content_v2:
        local_bib = os.path.join("docs", "proposal-phase", "assets", "references.bib")
        if os.path.exists(local_bib):
            with open(local_bib, "r") as f:
                bib_content_v2 = f.read()
        
    bib_content_v1, bib_content_v2 = diff_bib_files(bib_content_v1, bib_content_v2, pure_v1_keys, v2_keys)
    
    bib_content_v1 = re.sub(r'(@[a-zA-Z]+\s*\{)\s*([^,]+)\s*(,)', lambda m: f"{m.group(1)}{m.group(2).strip()}_v1{m.group(3)}", bib_content_v1)

    with open(os.path.join(outdir, bib_filename1), "w") as f:
        f.write(bib_content_v1)

    with open(os.path.join(outdir, bib_filename2), "w") as f:
        f.write(bib_content_v2)

    # Find logo locally
    local_logo_path = None
    for root, dirs, files in os.walk("."):
        if "logo-isi.png" in files:
            local_logo_path = os.path.join(root, "logo-isi.png")
            break
    if local_logo_path:
        shutil.copy(local_logo_path, os.path.join(outdir, "logo-isi.png"))

    latex = [
        r"\documentclass{isi-proposal}",
        r"\geometry{a3paper,landscape}", # Two A4 page areas; inherit the source class margins
        r"\usepackage{tikz}",
        r"\usetikzlibrary{shapes.geometric, arrows}",
        r"\usepackage{paracol}",
        r"\usepackage{xurl}",
        r"\usepackage{etoolbox}",
        r"\usepackage[most]{tcolorbox}",
        # Define diff colors early so defbibenvironment can reference them
        r"\definecolor{delhl}{RGB}{255,214,214}",
        r"\definecolor{inshl}{RGB}{204,244,206}",
        r"\definecolor{deltext}{RGB}{180,0,0}",
        r"\definecolor{instext}{RGB}{0,120,0}",
        r"\newcommand{\diffinline}[2]{{\setlength{\fboxsep}{0pt}\colorbox{#1}{\strut #2}}}",
        # No inset or added caption: retain the source equation's usable width.
        r"\newtcolorbox{diffmath}[1]{enhanced,breakable,colback=#1,colframe=#1,boxrule=0pt,arc=0pt,boxsep=0pt,left=0pt,right=0pt,top=0pt,bottom=0pt,before skip=0pt,after skip=0pt}",
        rf"\addbibresource{{{bib_filename1}}}",
        rf"\addbibresource{{{bib_filename2}}}",
        r"\AtEveryBibitem{\clearfield{extradate}\clearfield{extrayear}\clearfield{extraalpha}}",
        r"\AtEveryCitekey{\clearfield{extradate}\clearfield{extrayear}\clearfield{extraalpha}}",
        # Custom bibliography environment: tcolorbox wraps del/ins entries for background highlight
        r"\newcommand{\bibdelbegin}{\begin{tcolorbox}[enhanced,breakable,colback=delhl,colframe=delhl,boxrule=0pt,arc=1pt,boxsep=0pt,left=3pt,right=3pt,top=0pt,bottom=0pt,before=\noindent,after=\par,grow to left by=\bibhang]\color{deltext}\noindent\hangindent=\bibhang\hangafter=1}",
        r"\newcommand{\bibinsbegin}{\begin{tcolorbox}[enhanced,breakable,colback=inshl,colframe=inshl,boxrule=0pt,arc=1pt,boxsep=0pt,left=3pt,right=3pt,top=0pt,bottom=0pt,before=\noindent,after=\par,grow to left by=\bibhang]\color{instext}\noindent\hangindent=\bibhang\hangafter=1}",
        r"\newcommand{\bibtcbend}{\end{tcolorbox}}",
        r"\defbibenvironment{bibliography}{\list{}{\setlength{\leftmargin}{\bibhang}\setlength{\itemindent}{-\leftmargin}\setlength{\itemsep}{4pt}\setlength{\parsep}{0pt}}}{\endlist}{\item}",
        r"\renewbibmacro*{begentry}{%",
        r"  \iffieldequalstr{userc}{del}{\bibdelbegin}{}%",
        r"  \iffieldequalstr{userc}{ins}{\bibinsbegin}{}%",
        r"}",
        r"\renewbibmacro*{finentry}{%",
        r"  \finentry",
        r"  \iffieldequalstr{userc}{del}{\bibtcbend}{}%",
        r"  \iffieldequalstr{userc}{ins}{\bibtcbend}{}%",
        r"}",

        # Load local env macros dynamically
        load_env_macros(),
        # Counters for side-by-side sync
        r"\newcounter{leftsection}",
        r"\newcounter{leftsubsection}",
        r"\newcounter{leftsubsubsection}",
        r"\newcounter{lefttable}",
        r"\newcounter{leftfigure}",
        r"\newcounter{leftequation}",
        r"\newcounter{rightsection}",
        r"\newcounter{rightsubsection}",
        r"\newcounter{rightsubsubsection}",
        r"\newcounter{righttable}",
        r"\newcounter{rightfigure}",
        r"\newcounter{rightequation}",
        r"\newenvironment{leftside}{%",
        r"  \setlength{\textwidth}{\linewidth}%",
        r"  \setcounter{section}{\value{leftsection}}%",
        r"  \setcounter{subsection}{\value{leftsubsection}}%",
        r"  \setcounter{subsubsection}{\value{leftsubsubsection}}%",
        r"  \setcounter{table}{\value{lefttable}}%",
        r"  \setcounter{figure}{\value{leftfigure}}%",
        r"  \setcounter{equation}{\value{leftequation}}%",
        f"  {left_formatting}%",
        r"}{%",
        r"  \setcounter{leftsection}{\value{section}}%",
        r"  \setcounter{leftsubsection}{\value{subsection}}%",
        r"  \setcounter{leftsubsubsection}{\value{subsubsection}}%",
        r"  \setcounter{lefttable}{\value{table}}%",
        r"  \setcounter{leftfigure}{\value{figure}}%",
        r"  \setcounter{leftequation}{\value{equation}}%",
        r"}",
        r"\newenvironment{rightside}{%",
        r"  \setlength{\textwidth}{\linewidth}%",
        r"  \setcounter{section}{\value{rightsection}}%",
        r"  \setcounter{subsection}{\value{rightsubsection}}%",
        r"  \setcounter{subsubsection}{\value{rightsubsubsection}}%",
        r"  \setcounter{table}{\value{righttable}}%",
        r"  \setcounter{figure}{\value{rightfigure}}%",
        r"  \setcounter{equation}{\value{rightequation}}%",
        f"  {right_formatting}%",
        r"}{%",
        r"  \setcounter{rightsection}{\value{section}}%",
        r"  \setcounter{rightsubsection}{\value{subsection}}%",
        r"  \setcounter{rightsubsubsection}{\value{subsubsection}}%",
        r"  \setcounter{righttable}{\value{table}}%",
        r"  \setcounter{rightfigure}{\value{figure}}%",
        r"  \setcounter{rightequation}{\value{equation}}%",
        r"}",
        # Retain native caption wording/numbering without floating out of columns.
        r"\makeatletter",
        r"\renewenvironment{table}[1][]{\def\@captype{table}}{}",
        r"\renewenvironment{figure}[1][]{\def\@captype{figure}}{}",
        r"\makeatother",
        # (colors already defined earlier in preamble for defbibenvironment)
        # Use soul for line-wrapping highlights
        r"\usepackage{soul}",
        r"\soulregister{\parencite}{1}",
        r"\soulregister{\cite}{1}",
        r"\soulregister{\textcite}{1}",
        r"\soulregister{\citeauthor}{1}",
        r"\soulregister{\citeyear}{1}",
        r"\soulregister{\texttt}{1}",
        # Words and connecting spaces share the current font's strut bounds.
        # An explicit legal break before the leaders retains normal wrapping
        # even with the source's extremely large emergency stretch.
        r"\makeatletter",
        r"\def\SOUL@hlpreamble{\SOUL@uldp=\dp\strutbox\SOUL@ulht=\ht\strutbox\let\SOUL@ulcolor\SOUL@hlcolor\spaceskip\SOUL@spaceskip}",
        r"\newcommand{\diffspace}[1]{{\color{#1}\penalty0\leaders\hrule height\ht\strutbox depth\dp\strutbox\hskip\fontdimen2\font plus\fontdimen3\font minus\fontdimen4\font}}",
        r"\makeatother",
        r"\sethlcolor{delhl}",
        r"\newcommand{\delhighlight}[1]{{\sethlcolor{delhl}\hl{#1}}}",
        r"\newcommand{\inhighlight}[1]{{\sethlcolor{inshl}\hl{#1}}}",
        r"\begin{document}",
        r"\thispagestyle{empty}",
        r"\setlength{\columnsep}{\dimexpr\paperwidth-\textwidth\relax}",
        r"\setlength{\columnseprule}{0.3pt}",
        r"\begin{paracol}{2}",
        rf"\noindent\texttt{{{tag1}}}",
        r"\switchcolumn",
        rf"\noindent\texttt{{{tag2}}}",
        r"\end{paracol}",
        body,
        r"\end{document}",
    ]

    tex_path = os.path.join(outdir, f"{stem}.tex")
    with open(tex_path, "w") as f:
        f.write("\n".join(latex))
    return tex_path


def latex_to_pdf(tex_path, outdir):
    """Compile with the same temporary-output workflow as proposal builds."""
    pdf_path = os.path.join(outdir, os.path.splitext(os.path.basename(tex_path))[0] + ".pdf")
    return compile_pdf(tex_path, pdf_path)


def main():
    tag1 = sys.argv[1] if len(sys.argv) > 1 else "proposal/v1"
    tag2 = sys.argv[2] if len(sys.argv) > 2 else "proposal/v2"
    tag1 = resolve_git_ref(tag1)
    tag2 = resolve_git_ref(tag2)
    outdir = sys.argv[3] if len(sys.argv) > 3 else "scratch"

    print(f"=== Building full proposal diff: {tag1} -> {tag2} ===")
    os.makedirs(outdir, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="diff-", dir=outdir) as temporary:
        tex_path = generate_diff_latex(tag1, tag2, temporary)
        print("=== Compiling PDF ===")
        pdf_path = latex_to_pdf(tex_path, outdir)

    if pdf_path:
        size = os.path.getsize(pdf_path)
        print(f"=== Done: {pdf_path} ({size} bytes) ===")
    else:
        print(f"PDF not generated -- check {outdir}/{diff_output_stem(tag1, tag2)}.log")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
