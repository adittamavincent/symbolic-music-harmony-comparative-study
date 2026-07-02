#!/usr/bin/env python3
"""
Generate side-by-side diff PDF (paragraph-level, not raw source line-level).

Kenapa paragraph-level:
  Baris di file .tex sering gak align sama unit makna (1 paragraf biasanya
  1 baris panjang, tapi table/equation itu multi-baris tanpa blank line).
  Diffing per baris literal bikin hasil diff berantakan dan susah dibaca
  reviewer. Di sini, tiap file dipecah jadi "paragraf" (dipisah oleh baris
  kosong), lalu LCS diff dijalankan di level paragraf itu. Tiap paragraf
  yang beda jadi satu "line" diff, ditampilkan berdampingan (2 kolom).
"""

import os
import re
import subprocess
import sys


def get_git_content(tag, path):
    """Get file content from a git tag. Return '' if file doesn't exist at that tag."""
    result = subprocess.run(
        ["git", "show", f"{tag}:{path}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def escape_latex(text):
    """Escape special LaTeX characters for literal display."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    result = []
    i = 0
    while i < len(text):
        c = text[i]
        if c in replacements:
            result.append(replacements[c])
        else:
            result.append(c)
        i += 1
    return "".join(result)


def format_paragraph_for_display(para):
    """
    Convert a paragraph block (bisa multi-baris, misal table/equation)
    jadi teks yang aman ditampilkan di dalam minipage LaTeX.
    Internal line breaks dipertahankan pakai \\newline, bukan digabung
    jadi satu baris panjang, biar struktur table/equation masih kebaca.
    """
    lines = para.split("\n")
    escaped_lines = [escape_latex(line) for line in lines]
    return r" \newline ".join(escaped_lines)


def split_paragraphs(content):
    """
    Split file content jadi list paragraf, dipisah oleh 1+ baris kosong.
    Ini unit atomik untuk diffing, bukan baris source mentah.
    """
    if not content:
        return []
    normalized = content.replace("\r\n", "\n")
    blocks = re.split(r"\n\s*\n+", normalized.strip())
    return [b for b in (blk.strip() for blk in blocks) if b]


def compute_lcs(a, b):
    """Longest Common Subsequence, dijalankan di level paragraf (bukan baris)."""
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
    """
    Compute paragraph-by-paragraph diff.
    Return list of ops: ('equal' | 'delete' | 'insert', text)
    """
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
    Render 1 pasangan paragraf (old | new) sebagai 2 minipage berdampingan.
    Pakai minipage, bukan longtable row, supaya paragraf panjang tetap bisa
    page-break otomatis tanpa bikin LaTeX macet.
    """
    old_display = format_paragraph_for_display(old_text) if old_text else ""
    new_display = format_paragraph_for_display(new_text) if new_text else ""

    old_colored = f"{{\\color{{diffremove}} {old_display}}}" if old_text else ""
    new_colored = f"{{\\color{{diffadd}} {new_display}}}" if new_text else ""

    return (
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\small\\raggedright\n"
        f"{old_colored}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        "\\small\\raggedright\n"
        f"{new_colored}\n"
        "\\end{minipage}\n"
        "\\par\\vspace{0.3cm}\\hrule\\vspace{0.3cm}\n"
    )


def render_equal(text):
    """Render paragraf yang gak berubah, tampil hitam di dua kolom."""
    display = format_paragraph_for_display(text)
    return (
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        f"\\small\\raggedright {display}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth}\n"
        f"\\small\\raggedright {display}\n"
        "\\end{minipage}\n"
        "\\par\\vspace{0.3cm}\\hrule\\vspace{0.3cm}\n"
    )


def render_ops(ops):
    """
    Ubah list ops jadi blok LaTeX. Delete + insert yang berurutan
    dipasangkan berdampingan (dianggap 'paragraf berubah'), sisanya
    delete-only atau insert-only tampil dengan sisi lawan kosong.
    """
    out = []
    pending_delete = []
    pending_insert = []

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


def get_changed_files(tag1, tag2):
    """Ambil daftar file .tex yang berubah antara dua tag/commit."""
    result = subprocess.run(
        ["git", "diff", "--name-status", "-M", tag1, tag2],
        capture_output=True, text=True
    )
    files = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") or status.startswith("C"):
            old_path = parts[1]
            new_path = parts[2]
        elif status.startswith("D"):
            old_path = parts[1]
            new_path = None
        else:
            old_path = parts[1] if status.startswith("M") else None
            new_path = parts[1]

        path = new_path or old_path
        if path and path.endswith(".tex"):
            files.append((old_path, new_path, path))
    return files


def generate_diff_latex(tag1, tag2, outdir):
    """Generate side-by-side paragraph diff sebagai LaTeX, return path .tex-nya."""
    os.makedirs(outdir, exist_ok=True)
    files = get_changed_files(tag1, tag2)

    latex = []
    latex.append(r"\documentclass[11pt,a4paper]{article}")
    latex.append(r"\usepackage[T1]{fontenc}")
    latex.append(r"\usepackage[utf8]{inputenc}")
    latex.append(r"\usepackage{xcolor}")
    latex.append(r"\usepackage{geometry}")
    latex.append(r"\usepackage{fancyhdr}")
    latex.append(r"\geometry{margin=1.5cm}")
    latex.append(r"\pagestyle{fancy}")
    latex.append(r"\fancyhf{}")
    latex.append(rf"\fancyhead[L]{{\textbf{{Proposal Diff: {tag1} -> {tag2}}}}}")
    latex.append(r"\fancyhead[R]{\thepage}")
    latex.append(r"\fancyfoot[L]{Generated by scripts/sidebydiff.py}")
    latex.append(r"\definecolor{diffremove}{RGB}{178,20,20}")
    latex.append(r"\definecolor{diffadd}{RGB}{20,120,20}")
    latex.append(r"\begin{document}")
    latex.append(r"\thispagestyle{empty}")
    latex.append(r"\begin{center}")
    latex.append(r"{\Large \textbf{Proposal Diff Report}}\\[0.5em]")
    latex.append(rf"\texttt{{{tag1} $\rightarrow$ {tag2}}}\\[0.5em]")
    latex.append(r"\today")
    latex.append(r"\end{center}")
    latex.append(r"\newpage")

    for old_path, new_path, path in files:
        old_content = get_git_content(tag1, old_path) if old_path else ""
        new_content = get_git_content(tag2, new_path) if new_path else ""

        old_paragraphs = split_paragraphs(old_content)
        new_paragraphs = split_paragraphs(new_content)

        ops = compute_diff(old_paragraphs, new_paragraphs)

        latex.append(rf"\section*{{\texttt{{{escape_latex(path)}}}}}")
        latex.append(render_ops(ops))
        latex.append(r"\newpage")

    latex.append(r"\end{document}")

    tex_path = os.path.join(outdir, "proposal_diff.tex")
    with open(tex_path, "w") as f:
        f.write("\n".join(latex))

    return tex_path


def latex_to_pdf(tex_path, outdir):
    """Compile LaTeX to PDF (dijalankan 2x untuk cross-reference/TOC kalau ada)."""
    pdf_path = os.path.join(outdir, "proposal_diff.pdf")
    for _ in range(2):
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode",
             "-output-directory", outdir, tex_path],
            capture_output=True, text=True
        )
    return pdf_path if os.path.exists(pdf_path) else None


def main():
    tag1 = sys.argv[1] if len(sys.argv) > 1 else "proposal/v1"
    tag2 = sys.argv[2] if len(sys.argv) > 2 else "proposal/v2"
    outdir = sys.argv[3] if len(sys.argv) > 3 else "scratch"

    print(f"=== Generating paragraph-level diff: {tag1} -> {tag2} ===")
    tex_path = generate_diff_latex(tag1, tag2, outdir)

    print("=== Compiling PDF ===")
    pdf_path = latex_to_pdf(tex_path, outdir)

    if pdf_path:
        size = os.path.getsize(pdf_path)
        print(f"=== Done! Output: {pdf_path} ({size} bytes) ===")
    else:
        print("PDF not generated, cek log di scratch/proposal_diff.log")


if __name__ == "__main__":
    main()