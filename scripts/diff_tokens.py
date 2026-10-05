r"""
Tokenize LaTeX prose and render word-level highlights for one compared pair.

Each side is rendered from its own source tokens, so braces and environments
stay balanced; only changed words, formulas, and citations are wrapped.
Strong colors (delhl/inshl) mark words changed inside text that has a
counterpart. Pale colors (delpl/inspl) mark text without a counterpart.
"""

import re

# Highlight colors and the soul commands that paint prose in each color.
STRONG = ("delhl", "inshl")
PALE = ("delpl", "inspl")
HIGHLIGHT_COMMANDS = {"delhl": "delhighlight", "inshl": "inhighlight",
                      "delpl": "delpale", "inspl": "inspale"}


def tone_colors(tone):
    """Return the (deleted, inserted) color names of a highlight tone."""
    return PALE if tone == "pale" else STRONG


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
OPTIONAL_ARGUMENT = re.compile(r'\\[A-Za-z]+\*?(?:\{[^{}]*\})?\[')
# These environments contain syntax that must stay whole. A changed path,
# alignment rule, or verbatim line cannot be wrapped as though it were prose.
ATOMIC_BLOCK = re.compile(
    r'\\begin\{(?:tikzpicture|verbatim|Verbatim|lstlisting|minted|tabular|tabularx|longtable|array)\*?\}')
VERBATIM_BLOCK = re.compile(r'\\begin\{(?:verbatim|Verbatim|lstlisting|minted)\*?\}')
CONTAINER_COMMAND = re.compile(r'^\s*\\(captionof|caption|footnotetext|footnote|href|hyperref)\*?(?![A-Za-z])')
INLINE_VISIBLE_COMMAND = re.compile(
    r'(?<!\\)\\(footnotetext|footnote|href|hyperref|ref|pageref|eqref|autoref|nameref|cref|Cref|url|nolinkurl)\*?(?![A-Za-z])')
GRAPHIC_START = re.compile(r'(?<!\\)\\includegraphics\*?(?![A-Za-z])')


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
    # Line breaks and paragraph ends are structure: a word before them still compares.
    text = isolate_graphics(text)
    text = re.sub(r'\\begin\{[^{}]+\}(?:\[[^\]]*\])?(?:\{[^{}]*\})*|\\end\{[^{}]+\}|\\(?:begingroup|endgroup|par)\b'
                  r'|\\\\\*?(?:\[[^\]]*\])?',
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

            # Optional titles, citation pages, and graphic options can contain
            # spaces too; preserve them as part of their owning command.
            if (brace_balance <= 0 and not math_mode and not display_math
                    and not unfinished_optional_argument(" ".join(buf))):
                flush()
                brace_balance = 0
    flush()
    return merged



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
    if inline_parts(val_strip):
        return style + "_compound"
    if container_parts(val_strip):
        return style + "_container"
    val_clean = re.sub(r'[\.,;:\?!\)]+$', '', val_strip)
    val_clean = re.sub(r'^\(', '', val_clean)

    if graphic_end(val_clean) == len(val_clean):
        return style + "_object"

    if re.match(r'^\$([^$]*)\$$', val_clean):
        if is_safe_to_highlight_token(val, is_math=True):
            return style + "_math"
        return None

    if re.match(r'^\\(section|subsection|subsubsection)\{.*\}$', val_clean):
        if is_safe_to_highlight_token(val):
            return style + "_format"
        return None

    if re.match(r'^\\(parencite|cite|textcite|citeauthor|citeyear)\*?(?:\[[^\]]*\])*\{.*\}$', val_clean):
        if is_safe_to_highlight_token(val, is_box=True):
            # Citation expansion is unsafe inside soul's text reconstruction.
            return style + "_box"
        return None

    # These macros resolve references or print their own escaped URL text;
    # soul must never reconstruct the target argument as ordinary words.
    if re.match(r'^\\(?:ref|pageref|eqref|autoref|nameref|cref|Cref|url|nolinkurl)\*?\{.*\}$', val_clean, re.S):
        return style + "_box"

    if text_atoms(val_strip):
        return style + "_text"
    # Inline text that mixes in other commands is boxed as a whole.
    if is_safe_to_highlight_token(val, is_box=True):
        return style + "_box"
    return None


def highlight_prose(text, command):
    """Paint words and their connecting glue inside the source formatting."""
    color = next(name for name, cmd in HIGHLIGHT_COMMANDS.items() if cmd == command)
    items = decompose(text)
    return paint(items, [True] * sum(item[0] == "word" for item in items), command, color)


def apply_highlight(style, text):
    if not style or style == "mixed":
        return text + " "

    color = style.split("_")[0]
    if style.endswith("_display"):
        return f"\\begin{{diffmath}}{{{color}}}\n{text}\n\\end{{diffmath}}\n"
    if style.endswith("_container"):
        return render_container(text, [True] * len(token_atoms(("W", text))), color) + " "
    if style.endswith("_compound"):
        return render_inline_parts(text, [True] * len(token_atoms(("W", text))), color) + " "
    if style.endswith("_object"):
        # An opaque image hides a zero-inset background. A small colored
        # frame remains visible without touching the filename or options.
        return (f"{{\\setlength{{\\fboxsep}}{{1pt}}\\setlength{{\\fboxrule}}{{1pt}}"
                f"\\fcolorbox{{{color}}}{{{color}}}{{{text}}}}} ")
    if style.endswith("_text"):
        hl_cmd = HIGHLIGHT_COMMANDS[color]
        # Parentheses and punctuation belong to the changed text as well.
        return highlight_prose(text.strip(), hl_cmd) + " "
    val_strip = text.strip()
    punc_start = ""
    if val_strip.startswith("("):
        punc_start = "("
        val_strip = val_strip[1:]
    punc_end = ""
    punc_match = re.search(r'[\.,;:\?!\)]+$', val_strip)
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


# A prose token splits into words, spaces, and markup: formatting groups,
# font switches, and line breaks. Words are compared one by one, keyed with
# their enclosing formatting, so `\textit{a b}` -> `\textit{a c}` marks only
# b and c, and italicizing a word still counts as a change.
FONT_SWITCHES = ("mdseries", "bfseries", "itshape", "upshape", "slshape", "scshape", "normalfont",
                 "rmfamily", "sffamily", "ttfamily", "tiny", "scriptsize", "footnotesize", "small",
                 "normalsize", "large", "Large", "LARGE", "huge", "Huge", "selectfont")
PROSE_PIECE = re.compile(
    r'(?P<space>\s+)'
    r'|(?P<open>\\(?:textit|textbf|emph|underline|texttt|textsc|textsf|textrm|textup|textmd|textnormal'
    r'|uline|centerline|mbox)\{|\{)'
    r'|(?P<close>\})'
    r'|(?P<switch>\\fontsize\{[^{}]*\}\{[^{}]*\}|\\(?:' + "|".join(FONT_SWITCHES) + r')(?![A-Za-z]))'
    r'|(?P<break>\\\\\*?(?:\[[^\]]*\])?|\\par(?![A-Za-z])|~)'
    r'|(?P<word>(?:[^\s\\{}$%&~^_#]|\\[&%$#_{}])+)')
CITATION_TOKEN = re.compile(r'^\\(parencite|cite|textcite|citeauthor|citeyear)\{.*\}$')


# Formatting commands and the visible style each sets (+) or clears (-).
STYLES = {"textbf": "+bold", "bfseries": "+bold", "textmd": "-bold", "mdseries": "-bold",
          "textit": "+italic", "emph": "+italic", "itshape": "+italic", "slshape": "+italic",
          "textup": "-italic", "upshape": "-italic", "underline": "+underline", "uline": "+underline",
          "texttt": "family:mono", "ttfamily": "family:mono", "textsf": "family:sans", "sffamily": "family:sans",
          "textrm": "family:serif", "rmfamily": "family:serif", "textsc": "+smallcaps", "scshape": "+smallcaps",
          "textnormal": "-all", "normalfont": "-all"}
STYLES.update({name: "size:" + name for name in FONT_SWITCHES
               if name in {"tiny", "scriptsize", "footnotesize", "small", "normalsize",
                           "large", "Large", "LARGE", "huge", "Huge"}})


def visible_style(names):
    """The styles a reader sees after nested formatting, e.g. bold and underlined."""
    style = set()
    for name in names:
        effect = STYLES.get(name, "")
        if effect == "-all":
            # \normalfont resets the family, series, and shape, not its size.
            style = {value for value in style if value.startswith("size:")}
        elif effect.startswith("family:"):
            style -= {"mono", "family:sans"}
            if effect != "family:serif":
                style.add("mono" if effect == "family:mono" else effect)
        elif effect.startswith("size:"):
            style = {value for value in style if not value.startswith("size:")}
            if effect != "size:normalsize":
                style.add(effect)
        elif effect.startswith("+"):
            style.add(effect[1:])
        elif effect.startswith("-"):
            style.discard(effect[1:])
    return tuple(sorted(style))


def decompose(text):
    """Words, spaces, and markup of a prose token, or None when it holds other commands."""
    items, frames, pos = [], [[]], 0
    while pos < len(text):
        match = PROSE_PIECE.match(text, pos)
        if not match:
            return None
        kind, piece = match.lastgroup, match.group(0)
        if kind == "open":
            frames.append([piece.strip("\\{")])
        elif kind == "close":
            if len(frames) == 1:
                return None
            frames.pop()
        elif kind == "switch":
            frames[-1].append(re.match(r'\\([A-Za-z]+)', piece).group(1))
        items.append((kind, piece, tuple(name for frame in frames for name in frame)))
        pos = match.end()
    return items if len(frames) == 1 else None


def text_atoms(text):
    """Words of a prose token in reading order, each with the style it is printed in."""
    return [(visible_style(context), piece) for kind, piece, context in decompose(text) or [] if kind == "word"]


def paint(items, flags, command, color):
    """Re-render decomposed prose, wrapping the words flagged as changed."""
    flags = iter(flags)
    marks = [next(flags) if item[0] == "word" else None for item in items]

    def neighbor_changed(index, step):
        # Glue joins two changed words, through formatting groups but not
        # across a line break, where it would paint the next line's start.
        k = index + step
        while 0 <= k < len(items):
            if items[k][0] == "word":
                return marks[k]
            if items[k][0] not in ("open", "close"):
                return False
            k += step
        return False

    out = []
    for index, (kind, piece, _) in enumerate(items):
        if kind == "word":
            out.append(f"\\{command}{{{piece}}}" if marks[index] else piece)
        # ulem underlines word by word and rejects leaders between them.
        elif (kind == "space" and not {"uline", "underline"} & set(items[index][2])
              and neighbor_changed(index, -1) and neighbor_changed(index, 1)):
            out.append(f"\\diffspace{{{color}}}")
        else:
            out.append(piece)
    return "".join(out)


def token_atoms(token):
    """Comparison units of a token: its words for prose, else the whole token."""
    kind, value = token
    if kind == "NL":
        return [("NL",)]
    parts = inline_parts(value.strip())
    if parts:
        return [atom for part in parts for atom in token_atoms(("W", part))]
    parts = container_parts(value.strip())
    if parts:
        prefix, content, suffix = parts
        children = [atom for child in tokenize_words(content) for atom in token_atoms(child)]
        return [("container", prefix, suffix), *children]
    if classify_token_style("delhl", value) == "delhl_text":
        return [("W", context, word) for context, word in text_atoms(value.strip())] or [("T", value)]
    return [("T", value)]


def read_optional_argument(text, pos):
    """Skip an optional argument, including nested groups and escaped brackets."""
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != "[":
        return pos
    brackets, braces, cursor = 1, 0, pos + 1
    while cursor < len(text):
        char = text[cursor]
        if char == "\\":
            cursor += 2
            continue
        if char == "{":
            braces += 1
        elif char == "}":
            braces -= 1
        elif not braces and char == "[":
            brackets += 1
        elif not braces and char == "]":
            brackets -= 1
            if brackets == 0:
                return cursor + 1
        cursor += 1
    raise ValueError("Unclosed optional LaTeX argument")


def unfinished_optional_argument(text):
    """Whether a buffered command still has an open optional argument."""
    for match in OPTIONAL_ARGUMENT.finditer(text):
        pos = match.end() - 1
        try:
            while pos < len(text) and text[pos] == "[":
                pos = read_optional_argument(text, pos)
        except ValueError:
            return True
    return False


def graphic_end(text, start=0):
    """End of one complete graphic command, never an adjacent caption or macro."""
    command = GRAPHIC_START.match(text, start)
    if not command:
        return None
    try:
        pos = command.end()
        while pos < len(text):
            while pos < len(text) and text[pos].isspace():
                pos += 1
            if pos >= len(text) or text[pos] != "[":
                break
            pos = read_optional_argument(text, pos)
        _, end = read_braced_argument(text, pos)
        return end
    except ValueError:
        return None


def isolate_graphics(text):
    """Separate adjacent graphic/caption commands without splitting image syntax."""
    pieces, cursor = [], 0
    for match in GRAPHIC_START.finditer(text):
        if match.start() < cursor:
            continue
        end = graphic_end(text, match.start())
        if end is None:
            continue
        pieces.extend((text[cursor:match.start()], " ", text[match.start():end]))
        if end < len(text) and text[end] == "\\":
            pieces.append(" ")
        cursor = end
    pieces.append(text[cursor:])
    return "".join(pieces)


def container_parts(text):
    """Return a visible argument's exact wrapper, content, and trailing source.

    Caption and footnote counters remain native. Hyperlink targets and short
    caption titles participate as metadata, so a changed target also marks
    the displayed wording even when that wording itself stayed the same.
    """
    command = CONTAINER_COMMAND.match(text)
    if not command:
        return None
    try:
        pos = command.end()
        if command.group(1) == "captionof":
            _, pos = read_braced_argument(text, pos)
        pos = read_optional_argument(text, pos)
        if command.group(1) == "href":
            _, pos = read_braced_argument(text, pos)
        while pos < len(text) and text[pos].isspace():
            pos += 1
        content, end = read_braced_argument(text, pos)
        return text[:pos + 1], content, text[end - 1:]
    except ValueError:
        return None


def inline_parts(text):
    """Split attached visible commands while retaining their original adjacency.

    A footnote superscript in ``word\\footnote{...}`` has no intervening
    space. These pieces compare independently and join without adding one.
    Groups remain balanced; commands nested inside a visible argument are
    handled when that argument is rendered recursively.
    """
    pieces, last, pos, braces = [], 0, 0, 0
    while pos < len(text):
        char = text[pos]
        if char == "\\":
            match = INLINE_VISIBLE_COMMAND.match(text, pos) if not braces else None
            if match:
                try:
                    end = read_optional_argument(text, match.end())
                    if match.group(1) == "href":
                        _, end = read_braced_argument(text, end)
                    _, end = read_braced_argument(text, end)
                except ValueError:
                    pos += 2
                    continue
                if pos > last:
                    pieces.append(text[last:pos])
                pieces.append(text[pos:end])
                last = pos = end
                continue
            pos += 2
            continue
        if char == "{":
            braces += 1
        elif char == "}":
            braces -= 1
        pos += 1
    if not pieces:
        return None
    if last < len(text):
        pieces.append(text[last:])
    return pieces if len(pieces) > 1 else None


def render_inline_parts(text, flags, color):
    """Render attached pieces without introducing spaces before a footnote."""
    rendered, offset = [], 0
    for part in inline_parts(text.strip()):
        atoms = token_atoms(("W", part))
        part_flags = flags[offset:offset + len(atoms)]
        offset += len(atoms)
        if not any(part_flags):
            rendered.append(part)
            continue
        actions = token_actions([("W", part)], [atoms], part_flags, color)
        rendered.append(_render_runs(actions).removesuffix(" "))
    return "".join(rendered)


def render_container(text, flags, color):
    """Paint a caption/footnote/link argument without boxing its command."""
    prefix, content, suffix = container_parts(text.strip())
    children = tokenize_words(content)
    child_atoms = [token_atoms(child) for child in children]
    child_flags = flags[1:]
    if flags[0]:
        child_flags = [True] * sum(len(atoms) for atoms in child_atoms)
    rendered = _render_runs(_merge_runs(token_actions(children, child_atoms, child_flags, color)))
    return prefix + rendered.rstrip(" ") + suffix


def changed_flags(old, new):
    """Mark the items of each sequence that are not part of their longest common subsequence."""
    common = compute_lcs(old, new)
    old_changed, new_changed = [True] * len(old), [True] * len(new)
    i = j = k = 0
    while i < len(old) or j < len(new):
        if k < len(common) and i < len(old) and j < len(new) and old[i] == common[k] == new[j]:
            old_changed[i] = new_changed[j] = False
            i, j, k = i + 1, j + 1, k + 1
        elif i < len(old) and (k >= len(common) or old[i] != common[k]):
            i += 1
        elif j < len(new) and (k >= len(common) or new[j] != common[k]):
            j += 1
        else:
            i, j = i + 1, j + 1
    return old_changed, new_changed


def token_actions(tokens, atoms, changed, color):
    """(style, text) per token: unchanged, wholly changed, or partly changed ("mixed")."""
    actions, position = [], 0
    for (kind, value), token_atoms_ in zip(tokens, atoms):
        flags = changed[position:position + len(token_atoms_)]
        position += len(token_atoms_)
        if kind == "NL":
            actions.append((None, "\n"))
        elif not any(flags):
            actions.append((None, value))
        elif all(flags):
            style = classify_token_style(color, value)
            if style == f"{color}_text" and CITATION_TOKEN.match(re.sub(r'[\.,;\?!\)]+$', '', value.strip()).strip()):
                value = f"\\mbox{{{value}}}"
            actions.append((style, value))
        else:
            if inline_parts(value.strip()):
                rendered = render_inline_parts(value, flags, color)
            elif container_parts(value.strip()):
                rendered = render_container(value, flags, color)
            else:
                rendered = paint(decompose(value.strip()), flags, HIGHLIGHT_COMMANDS[color], color)
            actions.append(("mixed", rendered))
    return actions


def word_level_render(old_text, new_text, tone="strong"):
    """
    Run word-level LCS between old_text and new_text. Return
    (old_rendered, new_rendered) where only the differing words are
    wrapped in highlight commands (when safe to do so)
    -- everything matching stays plain text on BOTH sides, exactly like
    VSCode's inline word diff. The pale tone marks text without a counterpart.
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
        left_title, right_title = word_level_render(old_title, new_title, tone)
        left_body, right_body = word_level_render(old_text[old_end:], new_text[new_end:], tone)
        return (
            old_heading.group(1) + "{" + left_title.rstrip() + "}" + left_body,
            new_heading.group(1) + "{" + right_title.rstrip() + "}" + right_body,
        )

    old_rendered, new_rendered = render_group([old_text], [new_text], tone)
    return old_rendered[0], new_rendered[0]


def render_group(old_texts, new_texts, tone="strong"):
    """
    Compare the concatenated words of several old texts with several new
    texts, then render each text separately with its own highlights. A
    sentence split in two, or two lines merged into one, keeps its shared words.
    """
    old_color, new_color = tone_colors(tone)
    # Keep paths, table rules, and code intact and give a changed object a
    # block background. Whitespace-only edits do not change its rendering.
    if any(ATOMIC_BLOCK.search(text) for text in (*old_texts, *new_texts)):
        old_source, new_source = "".join(old_texts), "".join(new_texts)
        verbatim = VERBATIM_BLOCK.search(old_source) or VERBATIM_BLOCK.search(new_source)
        unchanged = old_source == new_source if verbatim else old_source.split() == new_source.split()
        if unchanged:
            return list(old_texts), list(new_texts)

        def block(color, text):
            return f"\\begin{{diffmath}}{{{color}}}\n{text}\n\\end{{diffmath}}\n" if text else ""
        return [block(old_color, text) for text in old_texts], [block(new_color, text) for text in new_texts]

    def atomize(texts):
        tokens = [tokenize_words(text) for text in texts]
        return tokens, [[token_atoms(token) for token in text_tokens] for text_tokens in tokens]

    old_tokens, old_atoms = atomize(old_texts)
    new_tokens, new_atoms = atomize(new_texts)
    old_changed, new_changed = changed_flags(
        [atom for text_atoms in old_atoms for atoms in text_atoms for atom in atoms],
        [atom for text_atoms in new_atoms for atoms in text_atoms for atom in atoms])

    def render(texts, tokens, atoms, changed, color):
        rendered, position = [], 0
        for text, text_tokens, text_atoms in zip(texts, tokens, atoms):
            count = sum(len(token) for token in text_atoms)
            flags = changed[position:position + count]
            position += count
            # Unchanged text keeps its exact source spacing.
            if not any(flags):
                rendered.append(text)
                continue
            actions = token_actions(text_tokens, text_atoms, flags, color)
            rendered.append(_render_runs(_merge_runs(actions)))
        return rendered

    return (render(old_texts, old_tokens, old_atoms, old_changed, old_color),
            render(new_texts, new_tokens, new_atoms, new_changed, new_color))


def _merge_runs(actions):
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


def _render_runs(runs):
    parts = []
    joined_newlines = set()

    def inline_color(style):
        if style and style.endswith(("_text", "_math", "_box")):
            return style.split("_")[0]
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
