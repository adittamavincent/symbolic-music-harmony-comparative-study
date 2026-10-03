#!/usr/bin/env python3
r"""
Generate a side-by-side PDF comparison of two committed manuscript versions.

Read each version's chapters, nested inputs, cover wording, and preamble
macros from Git. diff_layout pairs front-matter pages by role and headings by
ID (\label, else the title slug), aligns the text under them sentence by
sentence, and renders rows that keep paired parts side by side. A change map
on the first page lists every pair with its status and shared-word share.
diff_bibliography lines up the reference lists entry by entry.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

from build_pdf import compile_pdf, export_submission_pdf
from diff_bibliography import (bibliography_rows, diff_bib_files, extract_citation_keys,
                               render_bibliography_rows)
from diff_layout import Comparison, render_change_map
from diff_tokens import read_braced_argument

CLASS_PATH = "docs/proposal-phase/assets/isi-proposal.cls"
# Macros a version defines itself; \renewcommand changes LaTeX's own (\thesection, \contentsname).
TEXT_MACRO = re.compile(r'\\(?:newcommand|providecommand)\*?\s*(?:\{\\([A-Za-z]+)\}|\\([A-Za-z]+))'
                        r'\s*(?:\[(\d)\])?\s*(\[[^\]]*\])?\s*\{')
DEFINITION = re.compile(r'\\(?:newcommand|renewcommand|providecommand)(\*?)\s*(\{\\[A-Za-z@]+\}|\\[A-Za-z@]+)')
CHAPTER_DEFINITION = re.compile(r'\\newcommand\{\\thesischapter\}\[2\]')
# Labels from the sources get a side prefix; the diff's own labels start with "diff".
SOURCE_LABEL = re.compile(r'\\(label|ref|pageref|eqref|autoref)\{(?!diff)([^{}]*)\}')
CITATION = re.compile(r'\\(parencite|cite|textcite|nocite|citeauthor|citeyear)(\*?(?:\[[^\]]*\])*)\{([^}]+)\}')


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
    # Accept the convenient lowercase spelling without requiring a tag.
    if ref.lower() in ("head", "thesis"):
        # `thesis` names the working thesis, not a reviewed tag.
        ref = "HEAD"
    elif ref.lower() == "proposal":
        tags = subprocess.run(
            ["git", "tag", "--list", "proposal/v*", "--sort=-version:refname"],
            capture_output=True, text=True,
        ).stdout.split()
        if not tags:
            raise ValueError("No proposal/v* tag found")
        ref = tags[0]
    candidates = [ref]
    for prefix in ["thesis/", "proposal/"]:
        if not ref.startswith(prefix):
            candidates.append(f"{prefix}{ref}")
    for candidate in candidates:
        res = subprocess.run(
            ["git", "rev-parse", "--verify", "--end-of-options", f"{candidate}^{{commit}}"],
            capture_output=True, text=True,
        )
        if res.returncode == 0:
            tag = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/tags/{candidate}"],
                capture_output=True,
            )
            return candidate if tag.returncode == 0 else res.stdout.strip()
    raise ValueError(f"Unknown Git ref: {ref}")


def strip_comments(text):
    """Remove comments as TeX does: the rest of the line, its end, and the next indent."""
    return re.sub(r'(?<!\\)%[^\n]*(?:\n[ \t]*)?', '', text)


def clean_latex_for_diff(text, class_source=None):
    """Preserve source page boundaries, wording, and local formatting."""
    text = replace_title_page(text, class_source)
    text = strip_comments(text)
    # The renderer handles page boundaries outside the comparison columns.
    text = text.replace(r"\begin{titlepage}", r"\begingroup")
    text = text.replace(r"\end{titlepage}", "\\endgroup\n\\newpage")
    text = re.sub(r'\\vfill\b|\\vspace\*\{\\fill\}', '', text)
    # A source page number must not reset the comparison's page counter.
    text = re.sub(r'\\setcounter\{page\}\{[^{}]*\}', '', text)
    return text


def find_git_path(ref, filename):
    """Find the path of filename in a given git ref dynamically."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    paths = result.stdout.splitlines()
    if filename == "main.tex.template":
        proposal_templates = [
            "docs/proposal-phase/proposal/main.tex.template",
            "thesis/proposal/main.tex.template",
        ]
        thesis_templates = ["docs/final-thesis/thesis/main.tex.template"]
        candidates = (proposal_templates + thesis_templates
                      if ref.startswith("proposal/")
                      else thesis_templates + proposal_templates)
        for path in candidates:
            if path in paths:
                return path
        raise ValueError(f"No manuscript template found at {ref}")
    for line in paths:
        if os.path.basename(line) == filename:
            return line
    return None


def expand_inputs(ref, text, root, stack=()):
    """Inline \\input files relative to the template directory, without comments."""
    def expand(match):
        name = match.group(1).strip()
        if not name.endswith(".tex"):
            name += ".tex"
        path = os.path.normpath(os.path.join(root, name))
        if path in stack:
            raise ValueError(f"Recursive LaTeX input at {ref}:{path}")
        content = get_git_content(ref, path)
        if not content:
            raise ValueError(f"Missing or empty LaTeX input at {ref}:{path}")
        return expand_inputs(ref, content, root, (*stack, path))

    return re.sub(r'\\input\{([^}]+)\}', expand, strip_comments(text))


def template_preamble(ref):
    """The template preamble with its inputs (metadata, layout) inlined."""
    path = find_git_path(ref, "main.tex.template")
    if not path:
        return ""
    preamble = get_git_content(ref, path).split(r"\begin{document}", 1)[0]
    return expand_inputs(ref, preamble, os.path.dirname(path))


def chapter_definition(preamble):
    match = CHAPTER_DEFINITION.search(preamble)
    return read_braced_argument(preamble, match.end())[0] if match else ""


def extract_section_formatting(ref):
    """
    Collect a version's heading numbering and format, paragraph settings,
    caption names, and its chapter heading without page or contents effects.
    Line spacing such as \\doublespacing may sit in the document body.
    """
    path = find_git_path(ref, "main.tex.template")
    body = strip_comments(get_git_content(ref, path)).split(r"\begin{document}", 1)[-1] if path else ""
    content = template_preamble(ref) + "\n" + body
    commands = []
    for line in content.splitlines():
        line_strip = line.strip()
        if any(pat in line_strip for pat in ["\\thesection", "\\titleformat{\\section}", "\\titleformat{\\subsection}", "\\titleformat{\\subsubsection}", "\\renewcommand{\\figurename}", "\\renewcommand{\\tablename}"]):
            commands.append(line_strip)
        elif re.match(r'\\(?:tolerance|emergencystretch|hyphenpenalty|exhyphenpenalty)\s*=', line_strip):
            commands.append(line_strip)
        elif line_strip in (r"\doublespacing", r"\onehalfspacing", r"\singlespacing"):
            commands.append(line_strip)
    body = chapter_definition(content)
    if body:
        body = re.sub(r'\\(?:clearpage|phantomsection)\b', '', body)
        body = re.sub(r'\\addcontentsline\{[^{}]*\}\{[^{}]*\}\{[^{}]*\}', '', body)
        commands.append(r"\def\thesischapter#1#2{" + body + "}")
    return "\n  ".join(commands)


def extract_template_packages(ref):
    """Return the template's package lines; the diff preamble loads hyperref."""
    preamble = template_preamble(ref)
    lines = []
    for match in re.finditer(r'\\(?:usepackage|usetikzlibrary)(?:\[[^\]]*\])?\{([^}]*)\}', preamble):
        if match.group(1).strip() not in ("hyperref", "bookmark"):
            lines.append(re.sub(r'\s+', ' ', match.group(0)))
    return lines


def find_definitions(text):
    """Return text without its macro definitions, and the definitions in order."""
    definitions = []
    pattern = re.compile(r'\\(?:newcommand|renewcommand|providecommand)\*?\s*(?:\{\\[A-Za-z@]+\}|\\[A-Za-z@]+)(?:\s*\[[^\]]*\])*')
    pos = 0
    while match := pattern.search(text, pos):
        try:
            _, end = read_braced_argument(text, match.end())
        except ValueError:
            pos = match.end()
            continue
        definitions.append(text[match.start():end])
        text = text[:match.start()] + text[end:]
        pos = match.start()
    return text, definitions


def extract_source_definitions(text):
    r"""
    Move macro definitions out of the manuscript text. Each comparison block
    is a TeX group, so a \newcommand left in place would vanish before a
    later block used it. The returned definitions run at the start of every
    block on that side instead.
    """
    text, definitions = find_definitions(text)
    return text, "\n".join(definitions)


def build_full_proposal(ref):
    """
    Concatenate all chapter files for a given git ref, in the exact order
    main.tex.template \\input's them, into one continuous LaTeX string --
    this is the "whole proposal compiled as one file" the diff runs against,
    not a per-file diff with separate sections per chapter.
    """
    parts = []
    template_path = find_git_path(ref, "main.tex.template")
    template = strip_comments(get_git_content(ref, template_path))
    document_root = os.path.dirname(template_path)

    # Keep chapter headings from the template in their original input order.
    template_body = template.split(r"\begin{document}", 1)[-1]
    for match in re.finditer(r'\\input\{([^}]+)\}|\\thesischapter\{([^}]+)\}\{([^}]+)\}|\\(?:newpage|clearpage)\b', template_body):
        if match.group(1):
            parts.append(expand_inputs(ref, match.group(0), document_root).strip())
        else:
            parts.append(match.group(0))
    full_text = "\n\n".join(parts)
    # A chapter heading opens a page, whether the template or a chapter file holds it.
    if re.search(r'\\(?:newpage|clearpage)\b', chapter_definition(template_preamble(ref))):
        full_text = re.sub(r'(?m)^[ \t]*(?=\\thesischapter\{)', "\\\\clearpage\n", full_text)
    class_path = find_git_path(ref, "isi-proposal.cls")
    class_source = get_git_content(ref, class_path) if class_path else ""
    return clean_latex_for_diff(full_text, class_source)


ENV_DEFAULTS = {
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
    "THESIS_ADVISOR_1": "[Pembimbing I]",
    "THESIS_ADVISOR_1_NIP": "[NIP]",
    "THESIS_ADVISOR_2": "[Pembimbing II]",
    "THESIS_ADVISOR_2_NIP": "[NIP]",
    "COGNATE": "[Cognate]",
    "COGNATE_NIP": "[NIP]",
    "PROGRAM_COORDINATOR": "[Koordinator Program Studi]",
    "PROGRAM_COORDINATOR_NIP": "[NIP]",
    "DEAN": "[Dekan]",
}
# Metadata macro names and the .env.local keys that fill them.
ENV_MACROS = {
    "thesistitle": "THESIS_TITLE", "researchername": "RESEARCHER_NAME", "researchernim": "RESEARCHER_NIM",
    "institutionname": "INSTITUTION_NAME", "facultyname": "FACULTY_NAME",
    "departmentname": "DEPARTMENT_NAME", "programstudy": "PROGRAM_STUDY", "cityname": "CITY_NAME",
    "submissiondate": "SUBMISSION_DATE", "academicyear": "ACADEMIC_YEAR",
    "graduationyear": "GRADUATION_YEAR", "advisoracademic": "ADVISOR_ACADEMIC",
    "advisoracademicnip": "ADVISOR_ACADEMIC_NIP", "advisorthesis": "ADVISOR_THESIS",
    "advisorthesisnip": "ADVISOR_THESIS_NIP", "examinerone": "EXAMINER_1",
    "examineronenip": "EXAMINER_1_NIP", "examinertwo": "EXAMINER_2", "examinertwonip": "EXAMINER_2_NIP",
    "advisorone": "THESIS_ADVISOR_1", "advisoronenip": "THESIS_ADVISOR_1_NIP",
    "advisortwo": "THESIS_ADVISOR_2", "advisortwonip": "THESIS_ADVISOR_2_NIP", "cognate": "COGNATE",
    "cognatenip": "COGNATE_NIP", "programcoordinator": "PROGRAM_COORDINATOR",
    "programcoordinatornip": "PROGRAM_COORDINATOR_NIP", "deanname": "DEAN",
}


def env_values():
    """Proposal metadata: .env.local, else .env.example, over placeholder defaults."""
    values = dict(ENV_DEFAULTS)
    env_path = ".env.local" if os.path.exists(".env.local") else ".env.example"
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


def load_env_macros():
    """Fallback definitions for metadata macros that a version may not define."""
    values = env_values()
    return "\n".join(rf"\providecommand{{\{name}}}{{{values[key]}}}" for name, key in ENV_MACROS.items())


def overriding(definition):
    r"""Rewrite a definition so it applies whether or not the macro exists yet."""
    match = DEFINITION.match(definition)
    name = match.group(2).strip("{}")
    return rf"\providecommand{{{name}}}{{}}\renewcommand{match.group(1)}{{{name}}}" + definition[match.end():]


def version_definitions(ref, body_definitions=""):
    """Macro definitions of one version: its preamble (metadata, layouts) and text."""
    values = env_values()
    preamble = re.sub(r'\$\{([A-Z0-9_]+)\}', lambda m: values.get(m.group(1), m.group(0)),
                      template_preamble(ref))
    return [definition for definition in find_definitions(preamble)[1] + find_definitions(body_definitions)[1]
            if DEFINITION.match(definition).group(2).strip("{}") != r"\thesischapter"]


def side_setup(ref, body_definitions=""):
    r"""
    Code that opens every column block of one version: its heading format,
    paragraph settings, and macros (metadata, page layouts). The chapter
    heading comes from extract_section_formatting without its page break.
    Definitions nested inside \newenvironment need doubled parameter markers.
    """
    macros = [overriding(definition) for definition in version_definitions(ref, body_definitions)]
    setup = "\n  ".join([extract_section_formatting(ref), *macros])
    return re.sub(r'(?<!\\)#', "##", setup)


def text_macros(definitions):
    """
    Macros a version defines for its own text: metadata values, a cover
    heading, signature blocks. Return {name: (argument count, body)}; a macro
    with an optional argument stays unexpanded.
    """
    macros = {}
    for definition in definitions:
        match = TEXT_MACRO.match(definition)
        if match and not match.group(4):
            name = match.group(1) or match.group(2)
            body, _ = read_braced_argument(definition, match.end() - 1)
            macros[name] = (int(match.group(3) or 0), body)
    return macros


def expand_text_macros(text, macros):
    r"""
    Replace a version's own macros by what they print, so the comparison sees
    what readers see: a renamed macro with the same value is unchanged, a
    changed title is a change, and names inside a signature block compare
    word by word. A control word eats the spaces after it unless an empty
    group ends it, e.g. \researchername{}.
    """
    if macros:
        pattern = re.compile(r'\\(' + "|".join(sorted(map(re.escape, macros), key=len, reverse=True))
                             + r')(?![A-Za-z])')

        def expand_once(text):
            out, pos = [], 0
            while match := pattern.search(text, pos):
                count, body = macros[match.group(1)]
                end = match.end()
                if count:
                    try:
                        arguments = []
                        for _ in range(count):
                            argument, end = read_braced_argument(text, end)
                            arguments.append(argument)
                    except ValueError:
                        out.append(text[pos:match.end()])
                        pos = match.end()
                        continue
                    body = re.sub(r'#([1-9])', lambda m, args=arguments: args[int(m.group(1)) - 1], body)
                else:
                    empty = re.compile(r'\{\}|[ \t]*(?:\n[ \t]*)?').match(text, end)
                    end = empty.end()
                # Text right after a control word, e.g. \selectfont, needs a separating space.
                joined = re.search(r'\\[A-Za-z]+$', text[:match.start()]) and re.match(r'[^\W\d_]', body)
                out.append(text[pos:match.start()] + (" " if joined else "") + body)
                pos = end
            return "".join(out) + text[pos:]

        for _ in range(5):
            expanded = expand_once(text)
            if expanded == text:
                break
            text = expanded
    # \expandafter\uline\expandafter{name} only expands a name macro for ulem.
    text = re.sub(r'\\expandafter\\uline\\expandafter\{', r'\\uline{', text)
    # TeX prints \MakeUppercase{plain text} in capitals; compare what it prints.
    # A space keeps a preceding control word, e.g. \selectfont, from absorbing the text.
    text = re.sub(r'\\MakeUppercase\{([^{}\\]*)\}',
                  lambda m: (" " if re.search(r'\\[A-Za-z]+$', m.string[:m.start()]) else "") + m.group(1).upper(),
                  text)
    return re.sub(r'\\vfill\b|\\vspace\*\{\\fill\}', '', text)


def label_sides(body):
    """Give source labels a side prefix and left citations the left bibliography keys."""
    def left(match):
        content = SOURCE_LABEL.sub(lambda m: rf"\{m.group(1)}{{L-{m.group(2)}}}", match.group(1))
        content = CITATION.sub(lambda m: rf"\{m.group(1)}{m.group(2)}{{" + ", ".join(
            key.strip() + "_v1" for key in m.group(3).split(",") if key.strip()) + "}", content)
        return f"\\begin{{leftside}}{content}\\end{{leftside}}"

    def right(match):
        content = SOURCE_LABEL.sub(lambda m: rf"\{m.group(1)}{{R-{m.group(2)}}}", match.group(1))
        return f"\\begin{{rightside}}{content}\\end{{rightside}}"

    body = re.sub(r'\\begin\{leftside\}(.*?)\\end\{leftside\}', left, body, flags=re.DOTALL)
    return re.sub(r'\\begin\{rightside\}(.*?)\\end\{rightside\}', right, body, flags=re.DOTALL)


def replace_title_page(text, class_source=None):
    """Expand the cover from its version's class; never invent cover labels."""
    if r"\makeisititle" not in text:
        return text
    if class_source is None:
        with open(CLASS_PATH) as source:
            class_source = source.read()
    definition = re.search(r'\\newcommand\{\\makeisititle\}\[5\]', class_source)
    if not definition:
        raise ValueError("Source class has no five-argument makeisititle definition")
    body, _ = read_braced_argument(class_source, definition.end())
    idx = 0
    while (match := re.search(r'\\makeisititle\b', text[idx:])):
        start = idx + match.start()
        pos = start + len(r"\makeisititle")
        args = []
        for _ in range(5):
            arg, pos = read_braced_argument(text, pos)
            args.append(arg)
        replacement = re.sub(r'#([1-5])', lambda m: args[int(m.group(1)) - 1], body)
        text = text[:start] + replacement + text[pos:]
        idx = start + len(replacement)
    return text


def diff_output_stem(ref1, ref2):
    """Keep resolved ref labels in filenames without creating tag subfolders."""
    names = [re.sub(r'[^A-Za-z0-9._-]', '_', ref) for ref in (ref1, ref2)]
    return f"proposal_diff_{names[0]}_{names[1]}"


SIDE_COUNTERS = ("section", "subsection", "subsubsection", "table", "figure", "equation")


def side_environment(name, setup):
    """A column environment that resumes its version's counters and macros."""
    return "\n".join([
        rf"\newenvironment{{{name}side}}{{%",
        r"  \setlength{\textwidth}{\linewidth}%",
        *(rf"  \setcounter{{{counter}}}{{\value{{{name}{counter}}}}}%" for counter in SIDE_COUNTERS),
        f"  {setup}%",
        r"}{%",
        *(rf"  \setcounter{{{name}{counter}}}{{\value{{{counter}}}}}%" for counter in SIDE_COUNTERS),
        r"}",
    ])


def generate_diff_latex(tag1, tag2, outdir):
    os.makedirs(outdir, exist_ok=True)
    stem = diff_output_stem(tag1, tag2)
    bib_filename1 = f"{stem}_references_v1.bib"
    bib_filename2 = f"{stem}_references_v2.bib"
    # Clean old temp files to ensure biber runs correctly
    for ext in ["aux", "log", "bcf", "bbl", "blg", "run.xml", "pdf", "tex", "fdb_latexmk", "fls"]:
        path = os.path.join(outdir, f"{stem}.{ext}")
        if os.path.exists(path):
            os.remove(path)

    old_full, old_definitions = extract_source_definitions(build_full_proposal(tag1))
    new_full, new_definitions = extract_source_definitions(build_full_proposal(tag2))
    old_full = expand_text_macros(old_full, text_macros(version_definitions(tag1, old_definitions)))
    new_full = expand_text_macros(new_full, text_macros(version_definitions(tag2, new_definitions)))
    left_setup = side_setup(tag1, old_definitions)
    right_setup = side_setup(tag2, new_definitions)
    template_packages = list(dict.fromkeys(extract_template_packages(tag1) + extract_template_packages(tag2)))

    # Extract citations
    pure_v1_keys = extract_citation_keys(old_full)
    v1_keys = extract_citation_keys(old_full, suffix="_v1")
    v2_keys = extract_citation_keys(new_full)

    comparison = Comparison(old_full, new_full)
    change_map = render_change_map(comparison, tag1, tag2)
    body = label_sides(comparison.render())

    # Pull class/bib/logo assets so the diff compiles with the real
    # proposal styling instead of a bare article class.
    local_cls = os.path.join("docs", "proposal-phase", "assets", "isi-proposal.cls")
    if os.path.exists(local_cls):
        shutil.copy(local_cls, os.path.join(outdir, "isi-proposal.cls"))
    else:
        cls_path2 = find_git_path(tag2, "isi-proposal.cls")
        cls_path1 = find_git_path(tag1, "isi-proposal.cls")
        cls_content = get_git_content(tag2, cls_path2) if cls_path2 else ""
        if not cls_content and cls_path1:
            cls_content = get_git_content(tag1, cls_path1)
        with open(os.path.join(outdir, "isi-proposal.cls"), "w") as f:
            f.write(cls_content)

    # Write references_v1.bib (from tag1)
    bib_path1 = find_git_path(tag1, "references.bib")
    bib_content_v1 = get_git_content(tag1, bib_path1) if bib_path1 else ""

    # Write references_v2.bib (from tag2 git state; fallback to local if not in git)
    bib_path2 = find_git_path(tag2, "references.bib")
    bib_content_v2 = get_git_content(tag2, bib_path2) if bib_path2 else ""
    if not bib_content_v2:
        local_bib = os.path.join("docs", "proposal-phase", "assets", "references.bib")
        if os.path.exists(local_bib):
            with open(local_bib, "r") as f:
                bib_content_v2 = f.read()

    bib_rows = bibliography_rows(bib_content_v1, bib_content_v2, pure_v1_keys, v2_keys)
    bib_content_v1, bib_content_v2 = diff_bib_files(bib_content_v1, bib_content_v2, pure_v1_keys, v2_keys)
    if bib_rows:
        body += "\n" + render_bibliography_rows(bib_rows, v1_keys, v2_keys)

    bib_content_v1 = re.sub(r'(@[a-zA-Z]+\s*\{)\s*([^,]+)\s*(,)', lambda m: f"{m.group(1)}{m.group(2).strip()}_v1{m.group(3)}", bib_content_v1)

    with open(os.path.join(outdir, bib_filename1), "w") as f:
        f.write(bib_content_v1)

    with open(os.path.join(outdir, bib_filename2), "w") as f:
        f.write(bib_content_v2)

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
        r"\geometry{a3paper,landscape}", # Two A4 page areas; inherit the source class margins
        *template_packages,
        r"\usepackage{paracol}",
        r"\usepackage{xurl}",
        r"\usepackage{etoolbox}",
        r"\usepackage{longtable}",
        r"\usepackage[most]{tcolorbox}",
        # Strong colors mark changed words inside corresponding sentences;
        # pale colors mark text without a counterpart.
        r"\definecolor{delhl}{RGB}{255,183,183}",
        r"\definecolor{inshl}{RGB}{166,229,171}",
        r"\definecolor{delpl}{RGB}{255,232,232}",
        r"\definecolor{inspl}{RGB}{226,245,227}",
        r"\definecolor{deltext}{RGB}{180,0,0}",
        r"\definecolor{instext}{RGB}{0,120,0}",
        # Robust switches: biblatex case changing alters a color argument.
        r"\DeclareRobustCommand{\bibdelcolor}{\color{deltext}}",
        r"\DeclareRobustCommand{\bibinscolor}{\color{instext}}",
        r"\newcommand{\diffmoved}[1]{\par\noindent{\footnotesize\itshape\color{gray}[#1]}\par}",
        r"\newcommand{\diffinline}[2]{{\setlength{\fboxsep}{0pt}\colorbox{#1}{\strut #2}}}",
        r"\newcommand{\diffkey}[3]{{\setlength{\fboxsep}{1.5pt}\colorbox{#1}{\strut kiri}\,\colorbox{#2}{\strut kanan}}~#3}",
        # No inset or added caption: retain the source equation's usable width.
        r"\newtcolorbox{diffmath}[1]{enhanced,breakable,colback=#1,colframe=#1,boxrule=0pt,arc=0pt,boxsep=0pt,left=0pt,right=0pt,top=0pt,bottom=0pt,before skip=0pt,after skip=0pt}",
        rf"\addbibresource{{{bib_filename1}}}",
        rf"\addbibresource{{{bib_filename2}}}",
        r"\AtEveryBibitem{\clearfield{extradate}\clearfield{extrayear}\clearfield{extraalpha}}",
        r"\AtEveryCitekey{\clearfield{extradate}\clearfield{extrayear}\clearfield{extraalpha}}",
        # Custom bibliography environment: tcolorbox wraps del/ins entries for background highlight
        r"\newcommand{\bibdelbegin}{\begin{tcolorbox}[enhanced,breakable,colback=delpl,colframe=delpl,boxrule=0pt,arc=1pt,boxsep=0pt,left=3pt,right=3pt,top=0pt,bottom=0pt,before=\noindent,after=\par,grow to left by=\bibhang]\color{deltext}\noindent\hangindent=\bibhang\hangafter=1}",
        r"\newcommand{\bibinsbegin}{\begin{tcolorbox}[enhanced,breakable,colback=inspl,colframe=inspl,boxrule=0pt,arc=1pt,boxsep=0pt,left=3pt,right=3pt,top=0pt,bottom=0pt,before=\noindent,after=\par,grow to left by=\bibhang]\color{instext}\noindent\hangindent=\bibhang\hangafter=1}",
        r"\newcommand{\bibtcbend}{\end{tcolorbox}}",
        # One entry per synchronized row: the row gap replaces the item gap.
        r"\defbibenvironment{bibliography}{\list{}{\setlength{\leftmargin}{\bibhang}\setlength{\itemindent}{-\leftmargin}\setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}\setlength{\topsep}{0pt}\setlength{\partopsep}{0pt}}}{\endlist}{\item}",
        r"\renewbibmacro*{begentry}{%",
        r"  \iffieldequalstr{userc}{del}{\bibdelbegin}{}%",
        r"  \iffieldequalstr{userc}{ins}{\bibinsbegin}{}%",
        r"}",
        r"\renewbibmacro*{finentry}{%",
        r"  \finentry",
        r"  \iffieldequalstr{userc}{del}{\bibtcbend}{}%",
        r"  \iffieldequalstr{userc}{ins}{\bibtcbend}{}%",
        r"}",
        # Fallback metadata; each side redefines the macros its version defines.
        load_env_macros(),
        # Counters for side-by-side sync
        *(rf"\newcounter{{{side}{counter}}}" for side in ("left", "right") for counter in SIDE_COUNTERS),
        # Version macros may use internal names such as \@currentlabel.
        r"\makeatletter",
        side_environment("left", left_setup),
        side_environment("right", right_setup),
        r"\makeatother",
        # Retain native caption wording/numbering without floating out of columns.
        r"\makeatletter",
        r"\renewenvironment{table}[1][]{\def\@captype{table}}{}",
        r"\renewenvironment{figure}[1][]{\def\@captype{figure}}{}",
        r"\makeatother",
        # Use soul for line-wrapping highlights
        r"\usepackage{soul}",
        r"\soulregister{\parencite}{1}",
        r"\soulregister{\cite}{1}",
        r"\soulregister{\textcite}{1}",
        r"\soulregister{\citeauthor}{1}",
        r"\soulregister{\citeyear}{1}",
        r"\soulregister{\texttt}{1}",
        # Words and connecting spaces share the current font's strut bounds.
        # An explicit legal break before the leaders retains normal wrapping
        # even with the source's extremely large emergency stretch.
        r"\makeatletter",
        r"\def\SOUL@hlpreamble{\SOUL@uldp=\dp\strutbox\SOUL@ulht=\ht\strutbox\let\SOUL@ulcolor\SOUL@hlcolor\spaceskip\SOUL@spaceskip}",
        r"\newcommand{\diffspace}[1]{{\color{#1}\penalty0\leaders\hrule height\ht\strutbox depth\dp\strutbox\hskip\fontdimen2\font plus\fontdimen3\font minus\fontdimen4\font}}",
        r"\makeatother",
        r"\sethlcolor{delhl}",
        r"\newcommand{\delhighlight}[1]{{\sethlcolor{delhl}\hl{#1}}}",
        r"\newcommand{\inhighlight}[1]{{\sethlcolor{inshl}\hl{#1}}}",
        r"\newcommand{\delpale}[1]{{\sethlcolor{delpl}\hl{#1}}}",
        r"\newcommand{\inspale}[1]{{\sethlcolor{inspl}\hl{#1}}}",
        r"\begin{document}",
        r"\thispagestyle{empty}",
        change_map,
        r"\setlength{\columnsep}{\dimexpr\paperwidth-\textwidth\relax}",
        r"\setlength{\columnseprule}{0.3pt}",
        r"\begin{paracol}{2}",
        rf"\noindent\texttt{{{tag1}}}",
        r"\switchcolumn",
        rf"\noindent\texttt{{{tag2}}}",
        r"\end{paracol}",
        body,
        r"\end{document}",
    ]

    tex_path = os.path.join(outdir, f"{stem}.tex")
    with open(tex_path, "w") as f:
        f.write("\n".join(latex))
    return tex_path


def latex_to_pdf(tex_path, outdir):
    """Compile with the same temporary-output workflow as proposal builds."""
    pdf_path = os.path.join(outdir, os.path.splitext(os.path.basename(tex_path))[0] + ".pdf")
    return compile_pdf(tex_path, pdf_path)


def main():
    tag1 = sys.argv[1] if len(sys.argv) > 1 else "proposal/v1"
    tag2 = sys.argv[2] if len(sys.argv) > 2 else "proposal/v2"
    tag1 = resolve_git_ref(tag1)
    tag2 = resolve_git_ref(tag2)
    outdir = sys.argv[3] if len(sys.argv) > 3 else "scratch"

    print(f"=== Building side-by-side diff: {tag1} -> {tag2} ===")
    os.makedirs(outdir, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="diff-", dir=outdir) as temporary:
        tex_path = generate_diff_latex(tag1, tag2, temporary)
        print("=== Compiling PDF ===")
        pdf_path = latex_to_pdf(tex_path, outdir)

    if pdf_path:
        size = os.path.getsize(pdf_path)
        print(f"=== Done: {pdf_path} ({size} bytes) ===")
        export_submission_pdf(pdf_path, "diff", tag1, tag2)
    else:
        print(f"PDF not generated -- check {outdir}/{diff_output_stem(tag1, tag2)}.log")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
