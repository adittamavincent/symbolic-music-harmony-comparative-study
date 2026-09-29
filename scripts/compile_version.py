#!/usr/bin/env python3
"""Rebuild a committed proposal or thesis revision with the current tooling.

Usage: compile_version.py {proposal|thesis} <ref>

Revisions v1 and v2 are proposals (tags proposal/v1, proposal/v2). Revision
v3 and later belong to the thesis phase (tags thesis/v3, ...). A bare version
such as ``v2`` or ``3`` resolves to the tag of its phase. Branches, commit IDs,
and ``head`` resolve to commits; the phase is inferred from the manuscript
sources present at that commit. Sources come from Git, never the working tree.
"""
import os
import re
import subprocess
import sys
import tempfile

from build_pdf import compile_pdf

PHASES = ("proposal", "thesis")
FIRST_THESIS_VERSION = 3
PROPOSAL_TEMPLATES = (
    "docs/proposal-phase/proposal/main.tex.template",
    "thesis/proposal/main.tex.template",  # layout used by proposal/v1
)
THESIS_TEMPLATES = ("docs/final-thesis/thesis/main.tex.template",)
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".pdf")


class VersionError(ValueError):
    """A ref that cannot be built for the requested phase."""


def git(*args, binary=False):
    return subprocess.run(["git", *args], capture_output=True, text=not binary)


def git_blob(commit, path, binary=False):
    result = git("show", f"{commit}:{path}", binary=binary)
    if result.returncode != 0:
        raise VersionError(f"Missing file at {commit[:12]}: {path}")
    return result.stdout


def tag_exists(name):
    return git("show-ref", "--verify", "--quiet", f"refs/tags/{name}").returncode == 0


def version_phase(number):
    return "thesis" if number >= FIRST_THESIS_VERSION else "proposal"


def resolve(phase, ref):
    """Return (commit, output label, tag or None) after checking the phase."""
    if phase not in PHASES:
        raise VersionError(f"Unknown phase: {phase}")
    ref = "HEAD" if ref.lower() == "head" else ref
    prefix, _, version = ref.partition("/")
    # Up to three bare digits: longer digit strings can be abbreviated commit IDs.
    bare = re.fullmatch(r"v(\d+)|(\d{1,3})", ref)
    if bare or (prefix in PHASES and re.fullmatch(r"v\d+", version)):
        number = int(bare.group(bare.lastindex) if bare else version[1:])
        expected = version_phase(number)
        if expected != phase or (not bare and prefix != phase):
            raise VersionError(
                f"v{number} is a {expected} revision (proposal: v1-v2, thesis: "
                f"v{FIRST_THESIS_VERSION} and later). Use `make {expected} v{number}`.")
        tag = f"{phase}/v{number}"
        if not tag_exists(tag):
            raise VersionError(
                f"Tag {tag} does not exist yet. Use `make {phase}` for the working "
                f"tree or `make {phase} head` for the latest commit.")
    elif prefix in PHASES and prefix != phase:
        raise VersionError(f"{ref} is a {prefix} tag. Use `make {prefix} {ref}`.")
    else:
        tag = ref if tag_exists(ref) else None
    result = git("rev-parse", "--verify", "--end-of-options", f"{tag or ref}^{{commit}}")
    if result.returncode != 0:
        raise VersionError(f"Unknown Git ref: {ref}")
    commit = result.stdout.strip()
    label = tag.split("/", 1)[-1] if tag and tag.startswith(f"{phase}/") else (tag or commit)
    return commit, label.replace("/", "_"), tag


def find_template(commit, phase, tag=None):
    """Select the manuscript template; untagged refs must match their phase."""
    paths = git("ls-tree", "-r", "--name-only", commit).stdout.splitlines()
    proposal = next((p for p in PROPOSAL_TEMPLATES if p in paths), None)
    thesis = next((p for p in THESIS_TEMPLATES if p in paths), None)
    if thesis is None:
        # Earlier thesis layouts: any manuscript template outside the proposal.
        thesis = next((p for p in paths if p.endswith("/main.tex.template")
                       and p not in PROPOSAL_TEMPLATES and "presentation" not in p
                       and "slides" not in p), None)
    tagged = tag is not None and tag.startswith(f"{phase}/")
    if phase == "proposal":
        if thesis and not tagged:
            raise VersionError(
                f"{commit[:12]} belongs to the thesis phase (v{FIRST_THESIS_VERSION} and later). "
                "Use `make thesis <ref>`; saved proposals are built with "
                "`make proposal v1` or `make proposal v2`.")
        template = proposal
    else:
        template = thesis
    if template is None:
        other = "thesis" if phase == "proposal" else "proposal"
        raise VersionError(f"No {phase} manuscript at {commit[:12]}. Try `make {other} <ref>`.")
    return template, paths


def load_env_vars():
    env_path = ".env.local" if os.path.exists(".env.local") else ".env.example"
    values = {
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
        "EXAMINER_2_NIP": "[NIP]",
    }
    if os.path.exists(env_path):
        with open(env_path) as handle:
            for line in handle:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    value = value.strip().strip('"').strip("'")
                    if value:
                        values[key.strip()] = value
    return values


def expand_inputs(commit, template_path):
    """Inline every \\input relative to the template, as LaTeX would."""
    root = os.path.dirname(template_path)

    def read(path, stack=()):
        if path in stack:
            raise VersionError(f"Recursive LaTeX input at {commit[:12]}:{path}")

        def expand(match):
            if match.group(1) is None:
                return match.group(0)  # a comment, including any \input it disables
            name = match.group(1).strip()
            name = name if name.endswith(".tex") else f"{name}.tex"
            content = read(os.path.normpath(os.path.join(root, name)), (*stack, path))
            return content.rstrip("\n") + "\n"

        return re.sub(r"(?<!\\)%[^\n]*|\\input\{([^}]+)\}", expand, git_blob(commit, path))

    return read(template_path)


def stage_sources(commit, template_path, paths, outdir, name):
    """Write a self-contained entry point plus the class, bibliography, and images."""
    content = expand_inputs(commit, template_path)
    for key, value in load_env_vars().items():
        content = content.replace(f"${{{key}}}", value)

    root = os.path.dirname(template_path)
    for bib in re.findall(r"\\addbibresource\{([^}]+)\}", content):
        source = os.path.normpath(os.path.join(root, bib))
        with open(os.path.join(outdir, "references.bib"), "w") as handle:
            handle.write(git_blob(commit, source))
    content = re.sub(r"\\addbibresource\{[^}]+\}", lambda _: r"\addbibresource{references.bib}", content)

    document_class = re.search(r"\\documentclass(?:\[[^]]*\])?\{([^}]+)\}", content)
    class_path = document_class and next(
        (p for p in paths if os.path.basename(p) == f"{document_class.group(1)}.cls"), None)
    if class_path:
        with open(os.path.join(outdir, os.path.basename(class_path)), "w") as handle:
            handle.write(git_blob(commit, class_path))
        assets = os.path.dirname(class_path)
        for path in paths:
            if os.path.dirname(path) == assets and path.lower().endswith(IMAGE_EXTENSIONS):
                with open(os.path.join(outdir, os.path.basename(path)), "wb") as handle:
                    handle.write(git_blob(commit, path, binary=True))

    tex_path = os.path.join(outdir, f"{name}.tex")
    with open(tex_path, "w") as handle:
        handle.write(content)
    return tex_path


def build(phase, ref, scratch="scratch"):
    commit, label, tag = resolve(phase, ref)
    template_path, paths = find_template(commit, phase, tag)
    name = f"{phase}_{label}"
    destination = os.path.join(scratch, f"{name}.pdf")
    print(f"=== Compiling {phase} {tag or commit[:12]} from {template_path} ===")
    os.makedirs(scratch, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"{phase}-", dir=scratch) as temporary:
        tex_path = stage_sources(commit, template_path, paths, temporary, name)
        pdf_path = compile_pdf(tex_path, destination)
    if not pdf_path:
        return 1
    print(f"=== Done: {pdf_path} ({os.path.getsize(pdf_path)} bytes) ===")
    return 0


def main(argv):
    if len(argv) != 2 or argv[0] not in PHASES:
        print("Usage: compile_version.py {proposal|thesis} <ref>", file=sys.stderr)
        return 2
    try:
        return build(*argv)
    except VersionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
