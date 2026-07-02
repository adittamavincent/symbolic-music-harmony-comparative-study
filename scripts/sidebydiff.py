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

# Placeholder identity macros so 00-frontmatter.tex's \makeisititle{...}
# and \advisoracademic etc. compile without needing a real .env.local.
PLACEHOLDER_MACROS = r"""
\newcommand{\researchername}{[Nama Peneliti]}
\newcommand{\researchernim}{[NIM]}
\newcommand{\institutionname}{[Institusi]}
\newcommand{\facultyname}{[Fakultas]}
\newcommand{\departmentname}{[Jurusan]}
\newcommand{\programstudy}{[Program Studi]}
\newcommand{\advisoracademic}{[Dosen Pembimbing Akademik]}
\newcommand{\advisoracademicnip}{[NIP]}
\newcommand{\advisorthesis}{[Dosen Pembimbing Skripsi]}
\newcommand{\advisorthesisnip}{[NIP]}
"""


def get_git_content(ref, path):
    """Get file content from a git tag/commit. Empty string if missing."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def clean_latex_for_diff(text):
    """Strip page-level/environment structures that cross paragraph boundaries or break minipages."""
    text = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', '[Diagram Tikz]', text, flags=re.DOTALL)
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


def build_full_proposal(ref):
    """
    Concatenate all chapter files for a given git ref, in the exact order
    main.tex.template \\input's them, into one continuous LaTeX string --
    this is the "whole proposal compiled as one file" the diff runs against,
    not a per-file diff with separate sections per chapter.
    """
    parts = []
    filenames = [
        "00-frontmatter.tex",
        "01-pendahuluan.tex",
        "02-tinjauan-pustaka.tex",
        "03-metodologi.tex",
        "04-jadwal.tex",
    ]
    for fname in filenames:
        path = find_git_path(ref, fname)
        if path:
            content = get_git_content(ref, path)
            if content:
                parts.append(content.strip())
    full_text = "\n\n".join(parts)
    return clean_latex_for_diff(full_text)


def split_paragraphs(content):
    """Split into paragraph blocks, separated by 1+ blank lines. This is
    the diff unit -- not raw source lines -- so a paragraph written as one
    long .tex line, or a multi-line table/equation block, stays intact."""
    if not content:
        return []
    normalized = content.replace("\r\n", "\n")
    blocks = re.split(r"\n\s*\n+", normalized.strip())
    return [b for b in (blk.strip() for blk in blocks) if b]


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
    Split a paragraph into brace-safe tokens.

    Pass 1: split on whitespace, tracking newlines as boundaries.
    Pass 2: merge consecutive word-tokens whenever the running
            '{' minus '}' count is nonzero, so every emitted token is
            individually brace-balanced. A newline encountered while a
            merge is "open" (balance != 0) is folded into a plain space
            rather than kept as a hard line break, because \\newline
            is itself illegal inside a \\colorbox argument -- losing the
            exact line break there is a fine trade for not crashing.
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
    balance = 0

    def flush():
        if buf:
            merged.append(("W", " ".join(buf)))
            buf.clear()

    for kind, val in stream:
        if kind == "NL":
            if balance != 0:
                # Mid-merge: a hard newline here would need \newline
                # inside a future \colorbox, which is illegal. Fold
                # into a space instead of emitting a real NL token.
                continue
            flush()
            merged.append(("NL", None))
        else:
            buf.append(val)
            balance += val.count("{") - val.count("}")
            if balance <= 0:
                flush()
                balance = 0
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


def word_level_render(old_text, new_text):
    """
    Run word-level LCS between old_text and new_text. Return
    (old_rendered, new_rendered) where only the differing words are
    wrapped in \\colorbox (when safe to do so -- see _is_safe_to_highlight)
    -- everything matching stays plain text on BOTH sides, exactly like
    VSCode's inline word diff.
    """
    old_tokens = tokenize_words(old_text)
    new_tokens = tokenize_words(new_text)
    ops = compute_diff(old_tokens, new_tokens)

    old_parts, new_parts = [], []
    for kind, tok in ops:
        if kind == "equal":
            old_parts.append(render_token(tok))
            new_parts.append(render_token(tok))
        elif kind == "delete":
            old_parts.append(render_token(tok, highlight="delhl"))
        elif kind == "insert":
            new_parts.append(render_token(tok, highlight="inshl"))

    return "".join(old_parts), "".join(new_parts)


def render_pair(old_text, new_text):
    """
    Render one paragraph slot side-by-side.

      - Both old_text and new_text present -> word-level diff: full text
        both sides, only the changed words get a soft highlight box.
      - Only old_text present (pure delete) -> full old text on the left,
        every word highlighted red; right side left blank (there is no
        "B" to show, same as VSCode leaving the opposite gutter empty).
      - Only new_text present (pure insert) -> mirror of the above.
    """
    if old_text and new_text:
        old_rendered, new_rendered = word_level_render(old_text, new_text)
    elif old_text:
        old_rendered = "".join(
            render_token(t, highlight="delhl") for t in tokenize_words(old_text)
        )
        new_rendered = ""
    else:
        old_rendered = ""
        new_rendered = "".join(
            render_token(t, highlight="inshl") for t in tokenize_words(new_text)
        )

    return (
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\setlength{\\textwidth}{\\linewidth}\n"
        f"\\raggedright {old_rendered}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\setlength{\\textwidth}{\\linewidth}\n"
        f"\\raggedright {new_rendered}\n"
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
        f"\\raggedright {rendered}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\setlength{\\textwidth}{\\linewidth}\n"
        f"\\raggedright {rendered}\n"
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


def generate_diff_latex(tag1, tag2, outdir):
    os.makedirs(outdir, exist_ok=True)

    # Clean old temp files to ensure biber runs correctly
    for ext in ["aux", "log", "bcf", "bbl", "blg", "run.xml", "pdf", "tex"]:
        path = os.path.join(outdir, f"proposal_diff.{ext}")
        if os.path.exists(path):
            os.remove(path)

    old_full = build_full_proposal(tag1)
    new_full = build_full_proposal(tag2)

    ops = compute_diff(split_paragraphs(old_full), split_paragraphs(new_full))
    body = render_ops(ops)

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
        r"\usepackage{tikz}",
        r"\usetikzlibrary{shapes.geometric, arrows}",
        r"\addbibresource{references.bib}",
        PLACEHOLDER_MACROS,
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
        r"\begin{document}",
        r"\thispagestyle{empty}",
        r"\begin{center}",
        r"{\Large \textbf{Proposal Diff Report}}\\[0.5em]",
        rf"\texttt{{{tag1} $\rightarrow$ {tag2}}}\\[0.5em]",
        r"\today",
        r"\end{center}",
        r"\newpage",
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
    The -e flag overrides the repo .latexmkrc's $aux_dir=build so all
    aux/pdf output stays inside outdir where isi-proposal.cls lives."""
    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode",
         "-e", f"$aux_dir='{outdir}';$out_dir='{outdir}'",
         tex_path],
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
