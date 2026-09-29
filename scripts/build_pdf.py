#!/usr/bin/env python3
"""Compile a PDF in temporary storage and publish only a successful output."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
AUX_EXTENSIONS = ("aux", "log", "bcf", "bbl", "blg", "run.xml", "fdb_latexmk",
                  "fls", "out", "toc", "nav", "snm", "vrb", "synctex.gz")


def clean_auxiliary_files():
    """Remove known generated files without removing any PDF or manuscript."""
    directories = [ROOT / "docs/proposal-phase/proposal",
                   ROOT / "docs/proposal-phase/presentation",
                   ROOT / "docs/final-thesis/thesis"]
    for directory in directories:
        shutil.rmtree(directory / "build", ignore_errors=True)
        for ext in AUX_EXTENSIONS:
            for path in directory.glob(f"*.{ext}"):
                path.unlink()
    scratch = ROOT / "scratch"
    for prefix in ("proposal_",):
        for ext in (*AUX_EXTENSIONS, "tex", "bib", "bcf-SAVE-ERROR", "bbl-SAVE-ERROR"):
            for path in scratch.glob(f"{prefix}*.{ext}"):
                path.unlink()
    for name in ("isi-proposal.cls", "logo-isi.png", "references.bib", "references_v1.bib", "references_v2.bib"):
        (scratch / name).unlink(missing_ok=True)


def compile_pdf(tex_path, pdf_path, force=False):
    source = Path(tex_path).resolve()
    destination = Path(pdf_path).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    failure_log = destination.with_suffix(".log")
    env = os.environ.copy()
    search_paths = [source.parent, ROOT / "scripts", ROOT / "docs/proposal-phase/assets", destination.parent]
    env["TEXINPUTS"] = os.pathsep.join(map(str, search_paths)) + os.pathsep + env.get("TEXINPUTS", "")
    with tempfile.TemporaryDirectory(prefix="latex-", dir=destination.parent) as temporary:
        work = Path(temporary)
        # Stage the source so old Git snapshots also receive current navigation
        # support without changing archived manuscripts or relative input paths.
        staged_source = work / source.name
        content = source.read_text()
        content, count = re.subn(r'(?m)^([ \t]*)\\begin\{document\}',
                                lambda match: r'\usepackage{pdf-navigation}' + '\n' + match.group(0),
                                content, count=1)
        if count != 1:
            raise ValueError(f"No document environment found in {source}")
        staged_source.write_text(content)
        command = ["latexmk", "-pdf", "-interaction=nonstopmode",
                   f"-auxdir={work}", f"-outdir={work}"]
        if force:
            command.append("-g")
        result = subprocess.run(command + [str(staged_source)], cwd=source.parent,
                                env=env, capture_output=True, text=True)
        built_pdf = work / f"{source.stem}.pdf"
        if result.returncode != 0 or not built_pdf.is_file():
            log = work / f"{source.stem}.log"
            if log.is_file():
                shutil.copyfile(log, failure_log)
            else:
                failure_log.write_text(result.stdout + result.stderr)
            print(result.stdout[-3000:])
            print(result.stderr[-3000:])
            print(f"PDF compilation failed; log: {failure_log}", file=sys.stderr)
            return None
        # Preserve the previous successful PDF until the new build is complete.
        built_pdf.replace(destination)
        failure_log.unlink(missing_ok=True)
        if source.is_relative_to(ROOT / "docs"):
            source.with_suffix(".pdf").unlink(missing_ok=True)
    return str(destination)


if __name__ == "__main__":
    if sys.argv[1:] == ["--clean-aux"]:
        clean_auxiliary_files()
        sys.exit(0)
    result = compile_pdf(sys.argv[1], sys.argv[2], force="--force" in sys.argv[3:])
    if result:
        print(f"PDF: {result}")
    sys.exit(0 if result else 1)
