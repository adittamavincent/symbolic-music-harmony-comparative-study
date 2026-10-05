#!/usr/bin/env python3
"""Compile the researcher's Markdown reading material into one PDF (`make reading`).

Usage: build_reading.py [ref]

Without a ref, the notes come from the latest thesis version tag (thesis/v*);
a ref may be a version (v3, thesis/v4), ``head``, a branch, or a commit ID.
The Markdown is read from Git at that commit, never from the working tree,
and built with the current tooling, like ``make thesis <ref>``. Links between
included files become links inside the PDF; links to other files keep their
text. The result is ``scratch/bahan-bacaan_<label>.pdf``, replaced only when
pandoc and LuaLaTeX succeed.
"""
from datetime import date
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from compile_version import VersionError, git, resolve


ROOT = Path(__file__).resolve().parent.parent
SCRATCH = ROOT / "scratch"
THESIS_DOCS = "docs/final-thesis"

# Reading order: each part becomes \part, each file a chapter.
PARTS = [
    ("Belajar", [
        f"{THESIS_DOCS}/study/researcher-guide.md",
        f"{THESIS_DOCS}/study/model-dan-istilah.md",
        f"{THESIS_DOCS}/study/persiapan-pembimbing-1.md",
        f"{THESIS_DOCS}/study/defense-qa.md",
    ]),
    ("Status dan bimbingan", [
        f"{THESIS_DOCS}/PROGRESS.md",
        f"{THESIS_DOCS}/supervision/bimbingan-v4.md",
        f"{THESIS_DOCS}/supervision/feedback.md",
        f"{THESIS_DOCS}/supervision/review-teman-2026-10-04.md",
        f"{THESIS_DOCS}/supervision/perubahan-v3-ke-v4.md",
        f"{THESIS_DOCS}/supervision/perubahan-v2-ke-v3.md",
        f"{THESIS_DOCS}/supervision/bimbingan-v3.md",
    ]),
    ("Protokol dan catatan riset", [
        "research/protocol.md",
        "research/README.md",
        "research/literature/strube-melodies/README.md",
        f"{THESIS_DOCS}/records/research-log.md",
    ]),
    ("Arsip audit 3 Oktober 2026", [
        f"{THESIS_DOCS}/records/audit-2026-10-03/README.md",
        f"{THESIS_DOCS}/records/audit-2026-10-03/AUDIT.md",
        f"{THESIS_DOCS}/records/audit-2026-10-03/simulasi-sidang.md",
        f"{THESIS_DOCS}/records/audit-2026-10-03/usulan-revisi-bab-1-3.md",
    ]),
    ("Peta folder dan cek tulisan", [
        f"{THESIS_DOCS}/README.md",
        f"{THESIS_DOCS}/eval.md",
    ]),
]

MONTHS = ("Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
          "Agustus", "September", "Oktober", "November", "Desember")

LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)\)")
SEPARATOR = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")

# Inline code made only of these characters can break at / . - _ inside a
# narrow table cell; anything else stays ordinary \texttt. Headings are left
# alone so PDF bookmarks keep plain text.
LUA_FILTER = r"""
local safe = "^[%w%./_%-:=<>+*,@]+$"
return {
  traverse = "topdown",
  Header = function(el) return el, false end,
  Code = function(el)
    if #el.text > 12 and el.text:match(safe) then
      return pandoc.RawInline("latex", "\\PathCode{" .. el.text .. "}")
    end
  end,
}
"""

HEADER = r"""
\usepackage{xurl}
\DeclareUrlCommand\PathCode{\urlstyle{tt}}
\usepackage{fvextra}
\RecustomVerbatimEnvironment{verbatim}{Verbatim}{breaklines,breakanywhere,fontsize=\small}
\setlength{\emergencystretch}{3em}
\renewcommand{\arraystretch}{1.2}
"""


def slug(path):
    return "berkas-" + re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def split_row(line):
    """Cells of one pipe-table row; escaped pipes stay inside a cell."""
    cells, current, escaped = [], "", False
    for char in line.strip().strip("|"):
        if char == "|" and not escaped:
            cells.append(current)
            current = ""
        else:
            current += char
        escaped = char == "\\" and not escaped
    cells.append(current)
    return [cell.strip() for cell in cells]


def widen_separator(rows, separator):
    """Dash counts that follow each column's typical and longest cell, so pandoc sizes columns sensibly.

    Pandoc gives wide pipe tables relative column widths from the dashes under the header.
    """
    old = split_row(separator)
    header = split_row(rows[0])
    body = [split_row(row) for row in rows[1:]] or [header]
    cells = []
    for column, spec in enumerate(old):
        lengths = [len(row[column]) for row in body if column < len(row)] or [0]
        mean = sum(lengths) / len(lengths)
        weight = round(0.6 * mean + 0.4 * min(max(lengths), 90))
        title = header[column] if column < len(header) else ""
        floor = max(8, int(1.6 * max((len(word) for word in title.split()), default=0)) + 2)
        dashes = "-" * max(floor, min(weight, 60))
        cells.append((":" if spec.startswith(":") else "") + dashes + (":" if spec.endswith(":") else ""))
    return "| " + " | ".join(cells) + " |"


def rewrite_link(match, source, anchors):
    text, target = match.group(1), match.group(2)
    if re.match(r"^[a-z]+:", target):
        return match.group(0)
    file_part = target.split("#", 1)[0]
    if not file_part:
        return text
    resolved = (source.parent / file_part).resolve()
    if resolved in anchors:
        return f"[{text}](#{anchors[resolved]})"
    return text


def prepare(path, anchors, root=None):
    """Return one file's Markdown, read from `root`, ready to be joined with the others."""
    source = (root or ROOT) / path
    lines = source.read_text(encoding="utf-8").splitlines()
    output, in_code, titled = [], False, False
    index = 0
    while index < len(lines):
        line = lines[index]
        if FENCE.match(line):
            in_code = not in_code
            output.append(line)
            index += 1
            continue
        if in_code:
            output.append(line)
            index += 1
            continue
        if not titled and line.startswith("# "):
            output.append(f"{line} {{#{anchors[source.resolve()]}}}")
            output.append("")
            output.append(f"*Berkas sumber: `{path}`*")
            titled = True
            index += 1
            continue
        if line.startswith("|") and index + 1 < len(lines) and SEPARATOR.match(lines[index + 1]):
            block_end = index + 2
            while block_end < len(lines) and lines[block_end].startswith("|"):
                block_end += 1
            rows = [lines[index]] + lines[index + 2:block_end]
            table = [lines[index], widen_separator(rows, lines[index + 1])] + lines[index + 2:block_end]
            output.extend(LINK.sub(lambda m: rewrite_link(m, source, anchors), row) for row in table)
            index = block_end
            continue
        output.append(LINK.sub(lambda m: rewrite_link(m, source, anchors), line))
        index += 1
    return "\n".join(output) + "\n"


def latest_version_tag():
    """Highest thesis/vN tag; the reading notes belong to the thesis phase."""
    tags = git("tag", "-l", "thesis/v*").stdout.split()
    numbered = [(int(tag.split("/v", 1)[1]), tag) for tag in tags if re.fullmatch(r"thesis/v\d+", tag)]
    if not numbered:
        raise VersionError("No thesis/v* tag found. Use `make reading head` for the latest commit.")
    return max(numbered)[1]


def snapshot(commit, root):
    """Write every Markdown file under docs/ and research/ at `commit` into `root`."""
    listing = git("ls-tree", "-r", "--name-only", commit, "--", "docs", "research")
    for path in listing.stdout.splitlines():
        if not path.endswith(".md"):
            continue
        blob = git("show", f"{commit}:{path}", binary=True)
        if blob.returncode != 0:
            raise VersionError(f"Cannot read {path} at {commit[:12]}")
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob.stdout)


def present_parts(root):
    """PARTS limited to files that exist in `root`, and the files that do not."""
    parts, absent = [], []
    for title, files in PARTS:
        here = [f for f in files if (root / f).is_file()]
        absent += [f for f in files if f not in here]
        if here:
            parts.append((title, here))
    return parts, absent


def introduction(parts, version):
    lines = [
        "# Cara memakai PDF ini {.unnumbered}",
        "",
        f"PDF ini menggabungkan bahan bacaan Markdown tentang skripsi pada {version}. "
        "Isinya diambil dari Git pada commit tersebut, bukan dari berkas yang sedang diedit. "
        "Setiap bab mencantumkan berkas sumbernya. Untuk mengubah isi, edit berkas `.md`, commit, "
        "lalu bangun lagi: `make reading` memakai tag versi terbaru, `make reading head` memakai "
        "commit terakhir. Tautan antarberkas menjadi tautan di dalam PDF. Tautan ke berkas lain "
        "(kode, CSV, PDF) hanya ditampilkan sebagai teks.",
        "",
        "Bagian dalam PDF ini:",
        "",
    ]
    for number, (title, files) in enumerate(parts, start=1):
        lines.append(f"{number}. **{title}**: " + ", ".join(f"`{Path(f).name}`" for f in files) + ".")
    lines += ["", "Naskah skripsi sendiri tidak termasuk; bangun dengan `make thesis`.", ""]
    return "\n".join(lines)


def missing_files(root=None):
    """Markdown files under docs/final-thesis that are not in the reading order."""
    root = root or ROOT
    listed = {(root / f).resolve() for _, files in PARTS for f in files}
    found = (root / THESIS_DOCS).rglob("*.md")
    relative = (p.relative_to(root) for p in found if p.resolve() not in listed)
    return sorted(str(p) for p in relative if not str(p).startswith(f"{THESIS_DOCS}/thesis/"))


def build_markdown(root, parts, version):
    files = [f for _, group in parts for f in group]
    anchors = {(root / f).resolve(): slug(f) for f in files}
    chunks = [introduction(parts, version)]
    for title, group in parts:
        chunks.append(f"```{{=latex}}\n\\part{{{title}}}\n```\n")
        chunks.extend(prepare(f, anchors, root) for f in group)
    return "\n".join(chunks)


def describe(commit, tag):
    short = commit[:7]
    if tag and tag.startswith("thesis/v"):
        return f"versi {tag.split('/', 1)[1]} (tag {tag}, commit {short})"
    if tag:
        return f"tag {tag} (commit {short})"
    return f"commit {short} (tanpa tag versi)"


def main(argv):
    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc tidak ditemukan. Pasang dengan: brew install pandoc")
    if len(argv) > 2:
        raise SystemExit("Usage: make reading [ref]")
    ref = argv[1] if len(argv) == 2 else latest_version_tag()
    try:
        commit, label, tag = resolve("thesis", ref)
    except VersionError as error:
        raise SystemExit(f"Error: {error}")
    version = describe(commit, tag)
    output = SCRATCH / f"bahan-bacaan_{label}.pdf"
    today = date.today()
    built = f"{today.day} {MONTHS[today.month - 1]} {today.year}"
    print(f"=== Bahan bacaan dari {version} ===")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="reading-", dir=SCRATCH) as temporary:
        work = Path(temporary)
        source = work / "sumber"
        snapshot(commit, source)
        parts, absent = present_parts(source)
        if not parts:
            raise SystemExit(f"Tidak ada bahan bacaan pada {version}.")
        (work / "bahan-bacaan.md").write_text(build_markdown(source, parts, version), encoding="utf-8")
        (work / "header.tex").write_text(HEADER, encoding="utf-8")
        (work / "paths.lua").write_text(LUA_FILTER, encoding="utf-8")
        staged = work / "bahan-bacaan.pdf"
        command = [
            "pandoc", "bahan-bacaan.md", "-o", staged.name,
            "--from=markdown-raw_tex-raw_html-citations-subscript-superscript",
            "--pdf-engine=lualatex", "--top-level-division=chapter",
            "--toc", "--toc-depth=1", "--lua-filter=paths.lua", "--include-in-header=header.tex",
            "--metadata=title:Bahan Bacaan Skripsi",
            f"--metadata=subtitle:{version[0].upper() + version[1:]}",
            f"--metadata=date:Dibangun {built} dari berkas Markdown di Git",
            "--variable=lang:id", "--variable=documentclass:report",
            "--variable=classoption:oneside", "--variable=fontsize:11pt",
            "--variable=geometry:a4paper,margin=2.2cm",
            "--variable=mainfont:Charter", "--variable=sansfont:Helvetica Neue",
            "--variable=monofont:Menlo", "--variable=monofontoptions:Scale=0.84",
            "--variable=mainfontfallback:Apple Symbols:", "--variable=mainfontfallback:Arial Unicode MS:",
            "--variable=monofontfallback:Apple Symbols:", "--variable=monofontfallback:Arial Unicode MS:",
            "--variable=colorlinks:true", "--variable=linkcolor:blue",
            "--variable=urlcolor:blue", "--variable=toccolor:black",
        ]
        result = subprocess.run(command, cwd=work, capture_output=True, text=True, errors="replace")
        if result.returncode != 0 or not staged.is_file():
            log = output.with_suffix(".log")
            log.write_text(result.stderr, encoding="utf-8")
            sys.stderr.write(result.stderr[-4000:])
            raise SystemExit(f"Gagal membangun {output.relative_to(ROOT)}; PDF lama tidak diubah. Log: {log.relative_to(ROOT)}")
        staged.replace(output)
        unlisted = missing_files(source)
    print(f"PDF bacaan: {output}")
    for path in absent:
        print(f"Tidak ada pada {version}, dilewati: {path}")
    for path in unlisted:
        print(f"Belum dimasukkan (tambahkan ke PARTS di scripts/build_reading.py bila perlu): {path}")


if __name__ == "__main__":
    main(sys.argv)
