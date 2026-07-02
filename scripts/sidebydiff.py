#!/usr/bin/env python3
"""
Generate side-by-side diff PDF for the FULL proposal (paragraph-level),
concatenating all chapter files in main.tex.template's include order into
one continuous document per git ref, then diffing paragraph-by-paragraph.

Both sides always show their FULL text (compiled, live LaTeX -- not
escaped, not omitted). Diffing works in two passes, matching how VSCode's
split diff editor behaves:

  1. Paragraph-level LCS aligns "this old paragraph" with "this new
     paragraph" (or flags it as pure delete / pure insert).
  2. For any paragraph that changed, a SECOND word-level LCS pass finds
     exactly which words differ. Only those words get a soft background
     highlight (\colorbox) -- red on the left, green on the right.
     Everything else renders as plain, normal-colored text, same as an
     unchanged paragraph would.
"""

import os
import re
import subprocess
import sys
import shutil

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
    res = subprocess.run(["git", "rev-parse", "--verify", ref], capture_output=True)
    if res.returncode == 0:
        return ref
    if not ref.startswith("proposal/"):
        alt_ref = f"proposal/{ref}"
        res = subprocess.run(["git", "rev-parse", "--verify", alt_ref], capture_output=True)
        if res.returncode == 0:
            return alt_ref
    return ref


def clean_latex_for_diff(text):
    """Strip page-level/environment structures that cross paragraph boundaries or break minipages."""
    text = replace_title_page(text)
    text = re.sub(r'(?<!\\)%.*', '', text)
    text = re.sub(r'\\newpage\b', '', text)
    text = re.sub(r'\\clearpage\b', '', text)
    text = re.sub(r'\\begin\{spacing\}\{[^{}]*\}', '', text)
    text = re.sub(r'\\end\{spacing\}', '', text)
    text = re.sub(r'\\begin\{center\}', '', text)
    text = re.sub(r'\\end\{center\}', '', text)
    text = re.sub(r'\\begin\{minipage\}(\[[^\]]*\])?\{[^{}]*\}', '', text)
    text = re.sub(r'\\end\{minipage\}', '', text)
    text = re.sub(r'\\hfill\b', '', text)
    return text


def find_git_path(ref, filename):
    """Find the path of filename in a given git ref dynamically."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if line.endswith(filename):
            return line
    return None


def get_template_inputs(ref):
    """
    Extract list of tex filenames included via \\input in main.tex.template of the ref.
    """
    path = find_git_path(ref, "main.tex.template")
    if not path:
        return [
            "00-frontmatter.tex",
            "01-pendahuluan.tex",
            "02-tinjauan-pustaka.tex",
            "03-metodologi.tex",
            "04-jadwal.tex",
        ]
    content = get_git_content(ref, path)
    matches = re.findall(r'\\input\{([^}]+)\}', content)
    filenames = []
    for m in matches:
        m = m.strip()
        if not m.endswith(".tex"):
            m = m + ".tex"
        filenames.append(os.path.basename(m))
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
        if any(pat in line_strip for pat in ["\\thesection", "\\titleformat{\\section}", "\\titleformat{\\subsection}", "\\titleformat{\\subsubsection}"]):
            commands.append(line_strip)
    return "\n  ".join(commands)


def build_full_proposal(ref):
    """
    Concatenate all chapter files for a given git ref, in the exact order
    main.tex.template \\input's them, into one continuous LaTeX string --
    this is the "whole proposal compiled as one file" the diff runs against,
    not a per-file diff with separate sections per chapter.
    """
    parts = []
    filenames = get_template_inputs(ref)
    for fname in filenames:
        path = find_git_path(ref, fname)
        if path:
            content = get_git_content(ref, path)
            if content:
                parts.append(content.strip())
    full_text = "\n\n".join(parts)
    return clean_latex_for_diff(full_text)


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
    # Build a flat stream of ('W', word) / ('NL', None) first.
    stream = []
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if idx > 0:
            stream.append(("NL", None))
        for word in line.split():
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
            if any(env in val for env in ["\\begin{equation}", "\\begin{multline}", "\\begin{align}", "\\begin{gather}", "\\["]):
                display_math = True
            
            # Count unescaped braces
            unescaped_opens = len(re.findall(r'(?<!\\)\{', val))
            unescaped_closes = len(re.findall(r'(?<!\\)\}', val))
            brace_balance += unescaped_opens - unescaped_closes
            
            # Count unescaped dollars to toggle math mode
            unescaped_dollars = len(re.findall(r'(?<!\\)\$', val))
            if unescaped_dollars % 2 != 0:
                math_mode = not math_mode
                
            if any(env in val for env in ["\\end{equation}", "\\end{multline}", "\\end{align}", "\\end{gather}", "\\]"]):
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
    val_strip = val.strip()
    val_clean = re.sub(r'[\.,;\?!\)]+$', '', val_strip)
    val_clean = re.sub(r'^\(', '', val_clean)
    
    if re.match(r'^\$(.*)\$$', val_clean):
        if is_safe_to_highlight_token(val, is_math=True):
            return style + "_math"
        return None
        
    if re.match(r'^\\(textit|textbf|emph|underline|section|subsection|subsubsection)\{.*\}$', val_clean):
        if is_safe_to_highlight_token(val):
            return style + "_format"
        return None
        
    if re.match(r'^\\(parencite|cite|textcite|citeauthor|citeyear)\{.*\}$', val_clean):
        return None
        
    if re.match(r'^\\(texttt)\{.*\}$', val_clean):
        if is_safe_to_highlight_token(val, is_box=True):
            return style + "_box"
        return None
        
    if is_safe_to_highlight_token(val):
        return style + "_text"
        
    return None


def apply_highlight(style, text):
    if not style:
        return text + " "
    
    color = "delhl" if style.startswith("delhl") else "inshl"
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
        pattern = r'^\\(textit|textbf|emph|underline|section|subsection|subsubsection)\{(.*)\}$'
        match = re.match(pattern, val_strip)
        if match:
            macro_name = match.group(1)
            content = match.group(2)
            inner_style = classify_token_style(color, content)
            return f"{punc_start}\\{macro_name}{{{apply_highlight(inner_style, content).strip()}}}{punc_end} "
            
    if style.endswith("_box"):
        return f"{punc_start}\\colorbox{{{color}}}{{{val_strip}}}{punc_end} "
            
    if style.endswith("_math"):
        math_pattern = r'^\$(.*)\$$'
        match = re.match(math_pattern, val_strip)
        if match:
            content = match.group(1)
            return f"{punc_start}\\colorbox{{{color}}}{{\\ensuremath{{{content}}}}}{punc_end} "
            
    if style.endswith("_text"):
        hl_cmd = "delhighlight" if color == "delhl" else "inhighlight"
        return f"{punc_start}\\{hl_cmd}{{{val_strip}}}{punc_end} "
        
    return text + " "


def word_level_render(old_text, new_text):
    """
    Run word-level LCS between old_text and new_text. Return
    (old_rendered, new_rendered) where only the differing words are
    wrapped in highlight commands (when safe to do so)
    -- everything matching stays plain text on BOTH sides, exactly like
    VSCode's inline word diff.
    """
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
                old_actions.append((classify_token_style("delhl", value), value))
        elif kind == "insert":
            if kind_type == "NL":
                new_actions.append((None, "\n"))
            else:
                new_actions.append((classify_token_style("inshl", value), value))

    def merge_runs(actions):
        if not actions:
            return []
        merged = []
        cur_style, val = actions[0]
        cur_list = [val]
        for style, val in actions[1:]:
            if style == cur_style and val != "\n" and cur_list[-1] != "\n":
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
        for style, val in runs:
            if val == "\n":
                parts.append("\n")
            else:
                parts.append(apply_highlight(style, val))
        return "".join(parts)

    return render_merged(old_merged), render_merged(new_merged)


def render_pair(old_text, new_text):
    """
    Render one paragraph slot side-by-side.
    """
    old_rendered, new_rendered = word_level_render(old_text, new_text)

    return (
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\setlength{\\textwidth}{\\linewidth}\n"
        "\\begin{leftside}\n"
        f"\\raggedright {old_rendered}\n"
        "\\end{leftside}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\setlength{\\textwidth}{\\linewidth}\n"
        "\\begin{rightside}\n"
        f"\\raggedright {new_rendered}\n"
        "\\end{rightside}\n"
        "\\end{minipage}\n"
        "\\par\\vspace{0.4cm}\\hrule\\vspace{0.4cm}\n"
    )

def render_equal(text):
    """Paragraph unchanged in both versions -- word-level render, no
    highlight, so \\newline / unsafe constructs are handled properly
    instead of being dumped raw into restricted h-mode minipage."""
    rendered = "".join(render_token(t, highlight=None) for t in tokenize_words(text))
    return (
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\setlength{\\textwidth}{\\linewidth}\n"
        "\\begin{leftside}\n"
        f"\\raggedright {rendered}\n"
        "\\end{leftside}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\setlength{\\textwidth}{\\linewidth}\n"
        "\\begin{rightside}\n"
        f"\\raggedright {rendered}\n"
        "\\end{rightside}\n"
        "\\end{minipage}\n"
        "\\par\\vspace{0.4cm}\\hrule\\vspace{0.4cm}\n"
    )


def render_ops(ops):
    """Pair up consecutive delete/insert runs as 'changed paragraph';
    leftover delete-only or insert-only paragraphs render with an empty
    opposite column."""
    out = []
    pending_delete, pending_insert = [], []

    def flush():
        n = max(len(pending_delete), len(pending_insert))
        for k in range(n):
            old_p = pending_delete[k] if k < len(pending_delete) else ""
            new_p = pending_insert[k] if k < len(pending_insert) else ""
            out.append(render_pair(old_p, new_p))
        pending_delete.clear()
        pending_insert.clear()

    for kind, text in ops:
        if kind == "equal":
            flush()
            out.append(render_equal(text))
        elif kind == "delete":
            pending_delete.append(text)
        elif kind == "insert":
            pending_insert.append(text)
    flush()
    return "".join(out)


def load_env_macros():
    # Try .env.local first, then .env.example
    env_path = ".env.local" if os.path.exists(".env.local") else ".env.example"
    macros = []
    defaults = {
        "RESEARCHER_NAME": "[Nama Peneliti]",
        "RESEARCHER_NIM": "[NIM]",
        "INSTITUTION_NAME": "[Institusi]",
        "FACULTY_NAME": "[Fakultas]",
        "DEPARTMENT_NAME": "[Jurusan]",
        "PROGRAM_STUDY": "[Program Studi]",
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

    macros.append(rf"\newcommand{{\researchername}}{{{defaults.get('RESEARCHER_NAME', '[Nama Peneliti]')}}}")
    macros.append(rf"\newcommand{{\researchernim}}{{{defaults.get('RESEARCHER_NIM', '[NIM]')}}}")
    macros.append(rf"\newcommand{{\institutionname}}{{{defaults.get('INSTITUTION_NAME', '[Institusi]')}}}")
    macros.append(rf"\newcommand{{\facultyname}}{{{defaults.get('FACULTY_NAME', '[Fakultas]')}}}")
    macros.append(rf"\newcommand{{\departmentname}}{{{defaults.get('DEPARTMENT_NAME', '[Jurusan]')}}}")
    macros.append(rf"\newcommand{{\programstudy}}{{{defaults.get('PROGRAM_STUDY', '[Program Studi]')}}}")
    macros.append(rf"\newcommand{{\advisoracademic}}{{{defaults.get('ADVISOR_ACADEMIC', '[Dosen Pembimbing Akademik]')}}}")
    macros.append(rf"\newcommand{{\advisoracademicnip}}{{{defaults.get('ADVISOR_ACADEMIC_NIP', '[NIP]')}}}")
    macros.append(rf"\newcommand{{\advisorthesis}}{{{defaults.get('ADVISOR_THESIS', '[Dosen Pembimbing Skripsi]')}}}")
    macros.append(rf"\newcommand{{\advisorthesisnip}}{{{defaults.get('ADVISOR_THESIS_NIP', '[NIP]')}}}")
    macros.append(rf"\newcommand{{\examinerone}}{{{defaults.get('EXAMINER_1', '[Penguji 1]')}}}")
    macros.append(rf"\newcommand{{\examineronenip}}{{{defaults.get('EXAMINER_1_NIP', '[NIP]')}}}")
    macros.append(rf"\newcommand{{\examinertwo}}{{{defaults.get('EXAMINER_2', '[Penguji 2]')}}}")
    macros.append(rf"\newcommand{{\examinertwonip}}{{{defaults.get('EXAMINER_2_NIP', '[NIP]')}}}")
    return "\n".join(macros)


def replace_title_page(text):
    idx = 0
    while True:
        match = re.search(r'\\makeisititle\b', text[idx:])
        if not match:
            break
        start_pos = idx + match.start()
        args = []
        pos = start_pos + len("\\makeisititle")
        success = True
        for _ in range(5):
            while pos < len(text) and text[pos].isspace():
                pos += 1
            if pos >= len(text) or text[pos] != '{':
                success = False
                break
            balance = 1
            arg_start = pos + 1
            pos += 1
            while pos < len(text) and balance > 0:
                if text[pos] == '{':
                    balance += 1
                elif text[pos] == '}':
                    balance -= 1
                pos += 1
            if balance > 0:
                success = False
                break
            args.append(text[arg_start:pos-1])
        
        if success:
            replacement = (
                f"\\section*{{Judul Proposal}}\n{args[0]}\n\n"
                f"\\section*{{Peneliti}}\n{args[1]} (NIM: {args[2]})\n\n"
                f"\\section*{{Pendaftaran}}\n{args[3]} -- {args[4]}\n\n"
            )
            text = text[:start_pos] + replacement + text[pos:]
            idx = start_pos + len(replacement)
        else:
            idx = start_pos + 1
    return text


def extract_citation_keys(text):
    matches = re.findall(r'\\(?:parencite|cite|textcite|nocite)\{([^}]+)\}', text)
    keys = set()
    for match in matches:
        for key in match.split(','):
            keys.add(key.strip())
    return sorted(list(keys))

def generate_diff_latex(tag1, tag2, outdir):
    os.makedirs(outdir, exist_ok=True)
    # Clean old temp files to ensure biber runs correctly
    for ext in ["aux", "log", "bcf", "bbl", "blg", "run.xml", "pdf", "tex", "fdb_latexmk", "fls"]:
        path = os.path.join(outdir, f"proposal_diff.{ext}")
        if os.path.exists(path):
            os.remove(path)

    old_full = build_full_proposal(tag1)
    new_full = build_full_proposal(tag2)

    left_formatting = extract_section_formatting(tag1)
    right_formatting = extract_section_formatting(tag2)

    # Extract citations
    v1_keys = extract_citation_keys(old_full)
    v2_keys = extract_citation_keys(new_full)

    # Bibliography diff block
    bib_diff = []
    if v1_keys or v2_keys:
        v1_nocite = f"\\nocite{{{', '.join(v1_keys)}}}" if v1_keys else ""
        v2_nocite = f"\\nocite{{{', '.join(v2_keys)}}}" if v2_keys else ""
        bib_diff = [
            r"\newpage",
            r"\section*{Daftar Pustaka / References}",
            r"\noindent",
            r"\begin{minipage}[t]{0.48\textwidth}",
            r"\setlength{\textwidth}{\linewidth}",
            r"\raggedright",
            r"\begin{refsection}",
            v1_nocite,
            r"\printbibliography[heading=none]" if v1_keys else "",
            r"\end{refsection}",
            r"\end{minipage}\hfill",
            r"\begin{minipage}[t]{0.48\textwidth}",
            r"\setlength{\textwidth}{\linewidth}",
            r"\raggedright",
            r"\begin{refsection}",
            v2_nocite,
            r"\printbibliography[heading=none]" if v2_keys else "",
            r"\end{refsection}",
            r"\end{minipage}"
        ]

    ops = compute_diff(split_paragraphs(old_full), split_paragraphs(new_full))
    body = render_ops(ops) + "\n" + "\n".join(bib_diff)

    # Pull class/bib/logo assets so the diff compiles with the real
    # proposal styling instead of a bare article class.
    cls_path2 = find_git_path(tag2, "isi-proposal.cls")
    cls_path1 = find_git_path(tag1, "isi-proposal.cls")
    cls_content = get_git_content(tag2, cls_path2) if cls_path2 else ""
    if not cls_content and cls_path1:
        cls_content = get_git_content(tag1, cls_path1)
    with open(os.path.join(outdir, "isi-proposal.cls"), "w") as f:
        f.write(cls_content)

    bib_path2 = find_git_path(tag2, "references.bib")
    bib_path1 = find_git_path(tag1, "references.bib")
    bib_content = get_git_content(tag2, bib_path2) if bib_path2 else ""
    if not bib_content and bib_path1:
        bib_content = get_git_content(tag1, bib_path1)
    with open(os.path.join(outdir, "references.bib"), "w") as f:
        f.write(bib_content)

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
        r"\geometry{a3paper, margin=1.5cm}", # Set to A3 with generous margins
        r"\usepackage{tikz}",
        r"\usetikzlibrary{shapes.geometric, arrows}",
        r"\addbibresource{references.bib}",
        # Load local env macros dynamically
        load_env_macros(),
        # Counters for side-by-side sync
        r"\newcounter{leftsection}",
        r"\newcounter{leftsubsection}",
        r"\newcounter{leftsubsubsection}",
        r"\newcounter{rightsection}",
        r"\newcounter{rightsubsection}",
        r"\newcounter{rightsubsubsection}",
        r"\newenvironment{leftside}{%",
        r"  \setcounter{section}{\value{leftsection}}%",
        r"  \setcounter{subsection}{\value{leftsubsection}}%",
        r"  \setcounter{subsubsection}{\value{leftsubsubsection}}%",
        f"  {left_formatting}%",
        r"}{%",
        r"  \setcounter{leftsection}{\value{section}}%",
        r"  \setcounter{leftsubsection}{\value{subsection}}%",
        r"  \setcounter{leftsubsubsection}{\value{subsubsection}}%",
        r"}",
        r"\newenvironment{rightside}{%",
        r"  \setcounter{section}{\value{rightsection}}%",
        r"  \setcounter{subsection}{\value{rightsubsection}}%",
        r"  \setcounter{subsubsection}{\value{rightsubsubsection}}%",
        f"  {right_formatting}%",
        r"}{%",
        r"  \setcounter{rightsection}{\value{section}}%",
        r"  \setcounter{rightsubsection}{\value{subsection}}%",
        r"  \setcounter{rightsubsubsection}{\value{subsubsection}}%",
        r"}",
        # Redefine MakeUppercase to do nothing so colorbox inside it doesn't crash
        r"\renewcommand{\MakeUppercase}[1]{#1}",
        # Redefine page-breaking/floating environments to prevent compile crashes inside minipages
        r"\renewenvironment{table}[1][]{}{}",
        r"\renewenvironment{figure}[1][]{}{}",
        r"\renewcommand{\caption}[1]{\par\vspace{0.2cm}\noindent\textbf{Caption:} #1\par}",
        r"\renewcommand{\makeisititle}[5]{%",
        r"  {\centering",
        r"    {\Large \textbf{#1}}\par\vspace{1em}",
        r"    \textbf{#2} (\texttt{#3})\par\vspace{1em}",
        r"    #4\par\vspace{1em}",
        r"    #5\par}",
        r"}",
        # Soft pastel backgrounds for word-level highlighting, matching
        # GitHub/VSCode diff colors -- NOT full-text coloring anymore.
        r"\definecolor{delhl}{RGB}{255,214,214}",
        r"\definecolor{inshl}{RGB}{204,244,206}",
        # Use soul for line-wrapping highlights
        r"\usepackage{soul}",
        r"\sethlcolor{delhl}",
        r"\newcommand{\delhighlight}[1]{{\sethlcolor{delhl}\hl{#1}}}",
        r"\newcommand{\inhighlight}[1]{{\sethlcolor{inshl}\hl{#1}}}",
        r"\begin{document}",
        r"\thispagestyle{empty}",
        r"\begin{center}",
        r"{\Large \textbf{Proposal Diff Report}}\\[0.5em]",
        rf"\texttt{{{tag1} $\rightarrow$ {tag2}}}\\[0.5em]",
        r"\today",
        r"\end{center}",
        # Continuous flow, no newpage
        body,
        r"\end{document}",
    ]

    tex_path = os.path.join(outdir, "proposal_diff.tex")
    with open(tex_path, "w") as f:
        f.write("\n".join(latex))
    return tex_path


def latex_to_pdf(tex_path, outdir):
    """Use latexmk (not a bare pdflatex loop) so biber/citation passes
    that \\parencite needs actually run before the final PDF is produced.
    Runs inside outdir to prevent latexmk from losing the relative path on reruns."""
    filename = os.path.basename(tex_path)
    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode",
         "-e", "$aux_dir='.';$out_dir='.'",
         filename],
        cwd=outdir,
        capture_output=True, text=True
    )
    pdf_path = os.path.join(outdir, "proposal_diff.pdf")
    if result.returncode != 0 and not os.path.exists(pdf_path):
        print(result.stdout[-3000:])
        print(result.stderr[-3000:])
    return pdf_path if os.path.exists(pdf_path) else None


def main():
    tag1 = sys.argv[1] if len(sys.argv) > 1 else "proposal/v1"
    tag2 = sys.argv[2] if len(sys.argv) > 2 else "proposal/v2"
    tag1 = resolve_git_ref(tag1)
    tag2 = resolve_git_ref(tag2)
    outdir = sys.argv[3] if len(sys.argv) > 3 else "scratch"

    print(f"=== Building full proposal diff: {tag1} -> {tag2} ===")
    tex_path = generate_diff_latex(tag1, tag2, outdir)

    print("=== Compiling PDF ===")
    pdf_path = latex_to_pdf(tex_path, outdir)

    if pdf_path:
        size = os.path.getsize(pdf_path)
        print(f"=== Done: {pdf_path} ({size} bytes) ===")
    else:
        print(f"PDF not generated -- check {outdir}/proposal_diff.log")


if __name__ == "__main__":
    main()
