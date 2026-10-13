"""Build the focused v5 learning packet from the current Markdown sources."""
import subprocess
import tempfile
from pathlib import Path

from build_reading import HEADER, LUA_FILTER, ROOT, SCRATCH, prepare, slug

MATERIALS = [
    "docs/final-thesis/study/panduan-belajar-v5.md",
    "docs/final-thesis/study/latihan-bimbingan-v5.md",
]
OUTPUT = SCRATCH / "Panduan_Belajar_v5_23104810131_Vincent.pdf"


def main():
    for path in MATERIALS:
        if not (ROOT / path).is_file():
            raise SystemExit(f"Bahan belajar tidak ditemukan: {path}")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    anchors = {(ROOT / path).resolve(): slug(path) for path in MATERIALS}
    source = "\n".join(prepare(path, anchors) for path in MATERIALS)
    with tempfile.TemporaryDirectory(prefix="learning-v5-", dir=SCRATCH) as temporary:
        work = Path(temporary)
        (work / "belajar.md").write_text(source, encoding="utf-8")
        (work / "header.tex").write_text(HEADER, encoding="utf-8")
        (work / "paths.lua").write_text(LUA_FILTER, encoding="utf-8")
        staged = work / "belajar.pdf"
        command = [
            "pandoc", "belajar.md", "-o", staged.name,
            "--from=markdown-raw_tex-raw_html-citations-subscript-superscript",
            "--pdf-engine=lualatex", "--top-level-division=chapter",
            "--toc", "--toc-depth=2", "--lua-filter=paths.lua",
            "--include-in-header=header.tex",
            f"--resource-path={ROOT / 'docs/final-thesis/study'}",
            "--metadata=title:Belajar Skripsi v5",
            "--metadata=subtitle:Gerak suara Strube, model AI, metode dan latihan bimbingan",
            "--variable=lang:id", "--variable=documentclass:report",
            "--variable=classoption:oneside", "--variable=fontsize:11pt",
            "--variable=geometry:a4paper,margin=2.2cm",
            "--variable=mainfont:Charter", "--variable=sansfont:Helvetica Neue",
            "--variable=monofont:Menlo", "--variable=monofontoptions:Scale=0.84",
            "--variable=mainfontfallback:Apple Symbols:",
            "--variable=mainfontfallback:Arial Unicode MS:",
            "--variable=monofontfallback:Apple Symbols:",
            "--variable=monofontfallback:Arial Unicode MS:",
            "--variable=colorlinks:true", "--variable=linkcolor:blue",
            "--variable=urlcolor:blue", "--variable=toccolor:black",
        ]
        result = subprocess.run(
            command, check=False, cwd=work, capture_output=True, text=True, errors="replace"
        )
        log = OUTPUT.with_suffix(".log")
        if result.returncode != 0 or not staged.is_file():
            log.write_text(result.stderr, encoding="utf-8")
            raise SystemExit(
                f"PDF belajar gagal; keluaran lama dipertahankan. Log: {log}"
            )
        staged.replace(OUTPUT)
        log.unlink(missing_ok=True)
    print(f"PDF belajar v5: {OUTPUT}")


if __name__ == "__main__":
    main()
