#!/usr/bin/env python3
"""
Generate side-by-side diff PDF for the FULL proposal (paragraph-level),
concatenating all chapter files in main.tex.template's include order into
one continuous document per git ref, then diffing paragraph-by-paragraph.

Unlike a raw-text diff, changed/unchanged paragraphs are embedded as LIVE
LaTeX (not escaped to typewriter text), so the diff PDF actually renders
sections, italics, tables, and equations the way the real compiled
proposal would -- just with red/green coloring layered on top.
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


def build_full_proposal(ref):
    """
    Concatenate all chapter files for a given git ref, in the exact order
    main.tex.template \\input's them, into one continuous LaTeX string --
    this is the "whole proposal compiled as one file" the diff runs against,
    not a per-file diff with separate sections per chapter.
    """
    parts = []
    for path in CHAPTER_ORDER:
        content = get_git_content(ref, path)
        if content:
            parts.append(content.strip())
    return "\n\n".join(parts)


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


def render_pair(old_text, new_text):
    """
    Render one changed paragraph pair side-by-side. Content is emitted
    RAW (not escaped) so \\section, \\textit, tables, and equations from
    the actual proposal source compile and render normally -- \\color
    just tints the rendered result red/green instead of flattening it
    into escaped typewriter text.
    """
    old_block = f"{{\\color{{diffremove}}\n{old_text}\n}}" if old_text else ""
    new_block = f"{{\\color{{diffadd}}\n{new_text}\n}}" if new_text else ""
    return (
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        f"{old_block}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        f"{new_block}\n"
        "\\end{minipage}\n"
        "\\par\\vspace{0.4cm}\\hrule\\vspace{0.4cm}\n"
    )

def render_equal(text):
    return (
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        f"{text}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        f"{text}\n"
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

    old_full = build_full_proposal(tag1)
    new_full = build_full_proposal(tag2)

    ops = compute_diff(split_paragraphs(old_full), split_paragraphs(new_full))
    body = render_ops(ops)

    # Pull class/bib/logo assets so the diff compiles with the real
    # proposal styling instead of a bare article class.
    cls_content = get_git_content(tag2, CLASS_PATH) or get_git_content(tag1, CLASS_PATH)
    with open(os.path.join(outdir, "isi-proposal.cls"), "w") as f:
        f.write(cls_content)

    bib_content = get_git_content(tag2, BIB_PATH) or get_git_content(tag1, BIB_PATH)
    with open(os.path.join(outdir, "references.bib"), "w") as f:
        f.write(bib_content)

    if os.path.exists(LOGO_PATH):
        shutil.copy(LOGO_PATH, os.path.join(outdir, "logo-isi.png"))

    latex = [
        r"\documentclass{isi-proposal}",
        r"\usepackage{tikz}",
        r"\usetikzlibrary{shapes.geometric, arrows}",
        r"\addbibresource{references.bib}",
        PLACEHOLDER_MACROS,
        r"\definecolor{diffremove}{RGB}{178,20,20}",
        r"\definecolor{diffadd}{RGB}{20,120,20}",
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
    that \\parencite needs actually run before the final PDF is produced."""
    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode",
         "-outdir=" + outdir, tex_path],
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
