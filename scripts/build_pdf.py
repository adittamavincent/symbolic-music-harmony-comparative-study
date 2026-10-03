#!/usr/bin/env python3
"""Compile a PDF in temporary storage and publish only a successful output."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
# Submission identity and short name supplied by the researcher.
SUBMISSION_ID = "23104810131_Vincent"
AUX_EXTENSIONS = ("aux", "log", "bcf", "bbl", "blg", "run.xml", "fdb_latexmk",
                  "fls", "out", "toc", "nav", "snm", "vrb", "synctex.gz")


def export_submission_pdf(pdf_path, kind, revision, other_revision=None):
    """Publish an identical PDF copy with the researcher's submission naming."""
    prefixes = {"proposal": "Proposal", "thesis": "Skripsi", "diff": "Diff"}

    def label(ref):
        ref = re.sub(r"^(?:proposal|thesis)/(?=v\d+$)", "", ref)
        return re.sub(r"[^A-Za-z0-9._-]", "_", ref)

    versions = label(revision)
    if other_revision is not None:
        versions += "-" + label(other_revision)
    source = Path(pdf_path).resolve()
    destination = source.parent / f"{prefixes[kind]}_{versions}_{SUBMISSION_ID}.pdf"
    with tempfile.TemporaryDirectory(prefix="submission-", dir=source.parent) as temporary:
        staged = Path(temporary) / destination.name
        shutil.copyfile(source, staged)
        staged.replace(destination)
    print(f"PDF untuk dikirim: {destination}")
    return str(destination)


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
    for prefix in ("proposal_", "thesis_"):
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
        # TeX logs are not guaranteed UTF-8: pdfTeX writes 8-bit bytes and
        # line wrapping can split multibyte characters.
        result = subprocess.run(command + [str(staged_source)], cwd=source.parent,
                                env=env, capture_output=True, text=True,
                                errors="replace")
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_path")
    parser.add_argument("pdf_path")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--submission", nargs=2, metavar=("KIND", "REVISION"))
    args = parser.parse_args()
    if args.submission and args.submission[0] not in ("proposal", "thesis"):
        parser.error("--submission KIND must be proposal or thesis")
    result = compile_pdf(args.tex_path, args.pdf_path, force=args.force)
    if result:
        print(f"PDF: {result}")
        if args.submission:
            export_submission_pdf(result, *args.submission)
    sys.exit(0 if result else 1)
