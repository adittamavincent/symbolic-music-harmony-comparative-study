"""Source assembly for committed manuscript diffs: refs, inputs, macros, and the LaTeX document."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "sidebydiff.py"
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location("sidebydiff", SCRIPT)
diff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diff)


class GitRepoCase(unittest.TestCase):
    """A repository with proposal v1, proposal v2, and thesis v3 tags."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        previous = os.getcwd()
        os.chdir(self.tmp.name)
        self.addCleanup(os.chdir, previous)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Diff Test")
        self.git("config", "user.email", "diff-test@example.invalid")
        self.write("thesis/proposal/main.tex.template", r"\input{chapters/00-frontmatter}")
        self.write("thesis/proposal/chapters/00-frontmatter.tex", "PROPOSAL V1")
        self.git("add", ".")
        self.git("commit", "-qm", "Historical layout")
        self.old_sha = self.git("rev-parse", "HEAD")
        self.git("tag", "-a", "proposal/v1", "-m", "v1")

        self.write("docs/proposal-phase/proposal/main.tex.template", r"\input{chapters/00-frontmatter}")
        self.write("docs/proposal-phase/proposal/chapters/00-frontmatter.tex", "PROPOSAL V2")
        self.write("docs/final-thesis/thesis/main.tex.template", "\n".join(
            rf"\input{{chapters/{name}}}" for name in ["00-frontmatter", "04-results", "05-conclusion"]
        ))
        self.write("docs/final-thesis/thesis/chapters/00-frontmatter.tex",
                   "\\input{chapters/00-titlepage}\n\nTHESIS FRONTMATTER")
        self.write("docs/final-thesis/thesis/chapters/00-titlepage.tex",
                   "\\begin{titlepage}\nCOVER\n\\end{titlepage}")
        self.write("docs/final-thesis/thesis/chapters/04-results.tex", "RESULTS")
        self.write("docs/final-thesis/thesis/chapters/05-conclusion.tex", "CONCLUSION")
        self.git("add", ".")
        self.git("commit", "-qm", "Both phases")
        self.sha = self.git("rev-parse", "HEAD")
        self.git("tag", "proposal/v2")
        self.git("tag", "thesis/v3")

    def git(self, *args):
        return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()

    def write(self, path, content):
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)


class RefAndSourceTests(GitRepoCase):
    def test_untagged_refs_resolve_to_full_commit_id(self):
        for ref in ("head", "HEAD", "Head", "main", self.sha[:8], self.sha):
            with self.subTest(ref=ref):
                self.assertEqual(diff.resolve_git_ref(ref), self.sha)
        self.assertEqual(diff.resolve_git_ref("HEAD~1"), self.old_sha)

    def test_tags_keep_names_and_shortcuts(self):
        for ref in ("proposal/v1", "proposal/v2", "thesis/v3"):
            self.assertEqual(diff.resolve_git_ref(ref), ref)
        self.assertEqual(diff.resolve_git_ref("v1"), "proposal/v1")
        self.assertEqual(diff.resolve_git_ref("v3"), "thesis/v3")

    def test_phase_names_resolve_to_latest_proposal_and_head(self):
        self.git("tag", "proposal/v10", "HEAD~1")
        self.assertEqual(diff.resolve_git_ref("proposal"), "proposal/v10")
        # A thesis tag exists here, yet `thesis` still means the current commit.
        self.assertEqual(diff.resolve_git_ref("thesis"), self.sha)

    def test_invalid_ref_fails(self):
        with self.assertRaisesRegex(ValueError, "Unknown Git ref"):
            diff.resolve_git_ref("missing-ref")

    def test_proposal_tags_select_their_phase_in_both_layouts(self):
        self.assertEqual(diff.build_full_proposal("proposal/v1"), "PROPOSAL V1")
        self.assertEqual(diff.build_full_proposal("proposal/v2"), "PROPOSAL V2")

    def test_latest_commit_includes_nested_inputs_and_final_chapters(self):
        self.write("docs/final-thesis/thesis/chapters/04-results.tex", "UNCOMMITTED")
        text = diff.build_full_proposal(diff.resolve_git_ref("head"))
        self.assertIn("COVER", text)
        self.assertIn("THESIS FRONTMATTER", text)
        self.assertIn("RESULTS", text)
        self.assertIn("CONCLUSION", text)
        self.assertNotIn("PROPOSAL", text)
        self.assertNotIn("UNCOMMITTED", text)
        self.assertNotIn(r"\input", text)
        self.assertNotIn("titlepage", text)

    def test_chapter_definition_preserves_source_wording_inside_column_environments(self):
        self.write("docs/final-thesis/thesis/main.tex.template", r"""\newcommand{\thesischapter}[2]{
\clearpage
\phantomsection
\setcounter{section}{0}
\addcontentsline{toc}{part}{BAB #1: #2}
\begin{center}\bfseries BAB #1\par #2\end{center}
}
\begin{document}
\thesischapter{IV}{HASIL DAN PEMBAHASAN}
\input{chapters/04-results}
\end{document}""")
        self.git("add", ".")
        self.git("commit", "-qm", "Chapter heading")
        ref = diff.resolve_git_ref("head")
        source = diff.build_full_proposal(ref)
        self.assertIn(r"\thesischapter{IV}{HASIL DAN PEMBAHASAN}", source)
        latex = Path(diff.generate_diff_latex("proposal/v1", ref, "scratch")).read_text()
        self.assertIn(r"\def\thesischapter##1##2{", latex)
        self.assertIn(r"BAB ##1\par ##2", latex)
        self.assertNotIn(r"\addcontentsline", latex)
        self.assertNotIn(r"\phantomsection", latex)
        self.assertNotIn(r"\AtBeginEnvironment{leftside}", latex)
        self.assertIn(r"\setlength{\textwidth}{\linewidth}", latex)

    def test_missing_chapter_fails_instead_of_omitting_it(self):
        self.write("docs/final-thesis/thesis/main.tex.template", r"\input{chapters/missing}")
        self.git("add", ".")
        self.git("commit", "-qm", "Missing input")
        with self.assertRaisesRegex(ValueError, "Missing or empty LaTeX input"):
            diff.build_full_proposal(diff.resolve_git_ref("head"))

    def test_failed_compilation_rejects_existing_pdf(self):
        pdf = Path("proposal_diff.pdf")
        pdf.write_bytes(b"incomplete PDF")
        Path("proposal_diff.tex").write_text("\\documentclass{article}\n\\begin{document}\n\\end{document}\n")
        with patch.object(diff.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "")):
            self.assertIsNone(diff.latex_to_pdf("proposal_diff.tex", "."))

    def test_pair_names_use_tags_or_resolved_commit_ids(self):
        head = diff.resolve_git_ref("head")
        self.assertEqual(diff.diff_output_stem("proposal/v1", "proposal/v2"),
                         "proposal_diff_proposal_v1_proposal_v2")
        self.assertEqual(diff.diff_output_stem("proposal/v1", head),
                         f"proposal_diff_proposal_v1_{self.sha}")
        self.assertEqual(diff.diff_output_stem(self.sha, self.old_sha),
                         f"proposal_diff_{self.sha}_{self.old_sha}")

    def test_generating_another_pair_preserves_previous_artifacts(self):
        first = Path(diff.generate_diff_latex("proposal/v1", "proposal/v2", "scratch"))
        first_text = first.read_text()
        first.with_suffix(".pdf").write_bytes(b"previous PDF")
        second = Path(diff.generate_diff_latex("proposal/v1", self.sha, "scratch"))
        self.assertNotEqual(first, second)
        self.assertEqual(first.read_text(), first_text)
        self.assertEqual(first.with_suffix(".pdf").read_bytes(), b"previous PDF")
        for tex in (first, second):
            for side in ("v1", "v2"):
                bib_name = f"{tex.stem}_references_{side}.bib"
                self.assertTrue((tex.parent / bib_name).is_file())
                self.assertIn(rf"\addbibresource{{{bib_name}}}", tex.read_text())

    def test_compiler_returns_the_named_pdf(self):
        name = f"proposal_diff_proposal_v1_{self.sha}"
        with patch.object(diff, "compile_pdf", return_value=f"./{name}.pdf") as run:
            self.assertEqual(diff.latex_to_pdf(f"{name}.tex", "."), f"./{name}.pdf")
            run.assert_called_once_with(f"{name}.tex", f"./{name}.pdf")

    def test_diff_clean_removes_pair_files_and_preserves_unrelated_files(self):
        generated = ["proposal_diff.pdf", "proposal_diff_proposal_v1_proposal_v2.tex",
                     f"proposal_diff_proposal_v1_{self.sha}_references_v1.bib",
                     f"proposal_diff_proposal_v1_{self.sha}.run.xml"]
        preserved = ["notes.txt", "proposal_v1.pdf", "isi-proposal.cls"]
        for name in generated + preserved:
            self.write(f"scratch/{name}", "fixture")
        subprocess.run(["make", "-f", str(SCRIPT.parent.parent / "Makefile"), "diff-clean"],
                       check=True, capture_output=True, text=True)
        for name in generated:
            self.assertFalse(Path(f"scratch/{name}").exists())
        for name in preserved:
            self.assertTrue(Path(f"scratch/{name}").exists())


class CoverAndCleaningTests(unittest.TestCase):
    def test_cover_expands_original_class_wording_and_nested_arguments(self):
        class_source = r"""\newcommand{\makeisititle}[5]{
\begin{titlepage}
\bfseries
\textbf{#1}\par
PROPOSAL SKRIPSI\par
Oleh: #2\par
NIM: #3\par
Diajukan Untuk Mengikuti Proses Seleksi Proposal Tugas Akhir/Skripsi\par
#4\par
JURUSAN \MakeUppercase{\departmentname}\par
#5\par
\end{titlepage}
}"""
        source = r"\makeisititle{A \textit{nested} title}{Name}{123}{Semester 1}{2026}"
        cover = diff.clean_latex_for_diff(source, class_source)
        self.assertIn(r"\textbf{A \textit{nested} title}", cover)
        for original in ("PROPOSAL SKRIPSI", "Oleh: Name", "NIM: 123", "Semester 1", "2026",
                         "Diajukan Untuk Mengikuti Proses Seleksi Proposal Tugas Akhir/Skripsi",
                         r"JURUSAN \MakeUppercase{\departmentname}"):
            self.assertIn(original, cover)
        for invented in ("Judul Proposal", "Peneliti", "Pendaftaran"):
            self.assertNotIn(invented, cover)
        self.assertIn(r"\begingroup", cover)
        self.assertIn(r"\endgroup", cover)
        # A changed source class must change the cover, even with identical arguments.
        revised = diff.clean_latex_for_diff(source, class_source.replace("Oleh:", "Disusun oleh:"))
        self.assertIn("Disusun oleh: Name", revised)
        self.assertNotIn("Oleh: Name", revised)

    def test_missing_cover_definition_fails_without_fabricating_text(self):
        with self.assertRaisesRegex(ValueError, "makeisititle definition"):
            diff.clean_latex_for_diff(r"\makeisititle{T}{N}{1}{Y}{2}", "")

    def test_comments_are_removed_as_tex_reads_them(self):
        self.assertEqual(diff.strip_comments("a % note\n  b"), "a b")
        self.assertEqual(diff.strip_comments("{%\n  \\begin{center}"), "{\\begin{center}")
        # A comment line does not become a paragraph break.
        self.assertEqual(diff.strip_comments("text\n% full line\nmore"), "text\nmore")
        self.assertEqual(diff.strip_comments(r"50\% kept"), r"50\% kept")

    def test_frontmatter_cleaning_keeps_formatting_and_drops_the_page_counter(self):
        source = r"""\begin{titlepage}
\begin{center}\bfseries SKRIPSI\par Oleh:\\ Name\end{center}
\end{titlepage}
\setcounter{page}{2}\newpage
\begin{spacing}{1.15}\begin{center}HALAMAN PENGESAHAN\end{center}
Original approval.\end{spacing}"""
        cleaned = diff.clean_latex_for_diff(source)
        self.assertIn(r"\begin{center}\bfseries SKRIPSI\par Oleh:\\ Name\end{center}", cleaned)
        self.assertIn("Original approval.", cleaned)
        self.assertIn(r"\newpage", cleaned)
        self.assertIn(r"\begingroup", cleaned)
        self.assertNotIn(r"\setcounter{page}", cleaned)


class MacroExpansionTests(unittest.TestCase):
    DEFINITIONS = [
        r"\newcommand{\researchername}{Vincent Nuridzati}",
        r"\newcommand{\thesistitlelines}{EVALUASI\\ MUSIK}",
        r"\newcommand{\coverhead}{{\fontsize{14pt}{16pt}\selectfont\thesistitlelines\par}}",
        r"\newcommand{\signatory}[2]{#1\par\textbf{\expandafter\uline\expandafter{#2}}\par}",
        r"\newcommand{\examinercolumn}[2]{\noindent\signatory{#1}{#2}}",
        r"\newcommand{\optional}[2][x]{#1#2}",
        r"\renewcommand{\thesection}{\Alph{section}}",
    ]

    def expand(self, text):
        return diff.expand_text_macros(text, diff.text_macros(self.DEFINITIONS))

    def test_macro_table_skips_optional_arguments_and_latex_internals(self):
        macros = diff.text_macros(self.DEFINITIONS)
        self.assertEqual(macros["researchername"], (0, "Vincent Nuridzati"))
        self.assertEqual(macros["signatory"][0], 2)
        self.assertNotIn("optional", macros)
        self.assertNotIn("thesection", macros)

    def test_argument_free_macros_print_their_text_with_tex_spacing(self):
        self.assertEqual(self.expand(r"Oleh \researchername{} dan"), "Oleh Vincent Nuridzati dan")
        # A control word eats the following space, as TeX does.
        self.assertEqual(self.expand(r"\researchername dan"), "Vincent Nuridzatidan")
        self.assertEqual(self.expand(r"\coverhead"),
                         r"{\fontsize{14pt}{16pt}\selectfont EVALUASI\\ MUSIK\par}")

    def test_macros_with_arguments_expand_with_nested_macros(self):
        self.assertEqual(self.expand(r"\examinercolumn{Dekan}{\researchername}"),
                         r"\noindent Dekan\par\textbf{\uline{Vincent Nuridzati}}\par")
        self.assertEqual(self.expand(r"\optional{a}"), r"\optional{a}")

    def test_uppercase_plain_text_prints_in_capitals(self):
        self.assertEqual(self.expand(r"JURUSAN \MakeUppercase{Musik}"), "JURUSAN MUSIK")
        self.assertEqual(self.expand(r"\selectfont\MakeUppercase{Judul}"), r"\selectfont JUDUL")
        self.assertEqual(self.expand(r"\MakeUppercase{\textit{a}}"), r"\MakeUppercase{\textit{a}}")


class SourceAssemblyTests(unittest.TestCase):
    def test_source_macro_definitions_leave_the_text_for_every_block(self):
        source = (r"\newcommand{\coverhead}{%" "\n" r"  {\bfseries Title}\par" "\n}\n"
                  r"\newcommand{\signatory}[2]{#1 \textbf{#2}}" "\n"
                  r"\coverhead" "\n" r"\signatory{Dekan}{Name}")
        text, definitions = diff.extract_source_definitions(source)
        self.assertNotIn(r"\newcommand", text)
        self.assertIn(r"\coverhead", text)
        self.assertIn(r"\signatory{Dekan}{Name}", text)
        self.assertIn(r"\newcommand{\coverhead}{%", definitions)
        self.assertIn(r"\newcommand{\signatory}[2]{#1 \textbf{#2}}", definitions)

    def test_template_packages_skip_hyperref_and_keep_options(self):
        template = r"""\documentclass{isi-proposal}
\usepackage[normalem]{ulem}
% \usepackage{commented}
\usepackage[unicode,
  hidelinks]{hyperref}
\usepackage{bookmark}
\usetikzlibrary{shapes.geometric, arrows}
\begin{document}
\usepackage{late}
\end{document}"""
        with patch.object(diff, "find_git_path", return_value="main.tex.template"), \
             patch.object(diff, "get_git_content", return_value=template):
            packages = diff.extract_template_packages("ref")
        self.assertEqual(packages, [r"\usepackage[normalem]{ulem}",
                                    r"\usetikzlibrary{shapes.geometric, arrows}"])

    def test_side_setup_redefines_each_version_macro_and_keeps_its_chapter_heading(self):
        template = r"""\documentclass{isi-proposal}
\newcommand{\researchername}{${RESEARCHER_NAME}}
\newcommand{\signatory}[2]{#1: #2}
\newcommand{\thesischapter}[2]{\clearpage\phantomsection\addcontentsline{toc}{part}{BAB #1}\begin{center}BAB #1\par #2\end{center}}
\begin{document}
\doublespacing
\end{document}"""
        with patch.object(diff, "find_git_path", return_value="main.tex.template"), \
             patch.object(diff, "get_git_content", return_value=template), \
             patch.object(diff, "env_values", return_value={"RESEARCHER_NAME": "Nama"}):
            setup = diff.side_setup("ref")
        self.assertIn(r"\providecommand{\researchername}{}\renewcommand{\researchername}{Nama}", setup)
        self.assertIn(r"\providecommand{\signatory}{}\renewcommand{\signatory}[2]{##1: ##2}", setup)
        self.assertIn(r"\def\thesischapter##1##2{", setup)
        self.assertNotIn(r"\renewcommand{\thesischapter}", setup)
        self.assertNotIn(r"\addcontentsline", setup)
        # Line spacing may sit in the document body of the template.
        self.assertIn(r"\doublespacing", setup)

    def test_source_labels_get_side_prefixes_and_left_citations_left_keys(self):
        body = (r"\begin{leftside}\label{tab:a} Tabel~\ref{tab:a} \parencite[9]{x, y}\end{leftside}"
                r"\begin{rightside}\label{tab:a} \section{A}\label{diffn1} \parencite{x}\end{rightside}")
        labeled = diff.label_sides(body)
        self.assertIn(r"\label{L-tab:a} Tabel~\ref{L-tab:a} \parencite[9]{x_v1, y_v1}", labeled)
        self.assertIn(r"\label{R-tab:a} \section{A}\label{diffn1} \parencite{x}", labeled)

    def test_starred_references_and_wildcard_citations_keep_their_meaning(self):
        body = (r"\begin{leftside}\ref*{sec:a} \autoref*{fig:b} \nameref{sec:a} "
                r"\citeauthor{x} \citeyear[2]{x} \nocite{*}\end{leftside}")
        labeled = diff.label_sides(body)
        for command in (r"\ref*{L-sec:a}", r"\autoref*{L-fig:b}", r"\nameref{L-sec:a}",
                        r"\citeauthor{x_v1}", r"\citeyear[2]{x_v1}", r"\nocite{*}"):
            self.assertIn(command, labeled)

    def test_caption_and_modified_bibliography_handlers_are_in_the_generated_document(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(diff, "build_full_proposal", return_value="Text."), \
                patch.object(diff, "find_git_path", return_value=None), \
                patch.object(diff, "version_definitions", return_value=""), \
                patch.object(diff, "side_setup", return_value=""), \
                patch.object(diff, "extract_template_packages", return_value=[]):
            latex = Path(diff.generate_diff_latex("old", "new", directory)).read_text()
        self.assertIn(r"\newcommand{\diffcaptionlabel}[2]", latex)
        for status, begin in (("moddel", "bibdelbegin"), ("modins", "bibinsbegin")):
            self.assertIn(rf"\iffieldequalstr{{userc}}{{{status}}}{{\{begin}}}", latex)
            self.assertIn(rf"\iffieldequalstr{{userc}}{{{status}}}{{\bibtcbend}}", latex)


class ThesisLayoutTests(GitRepoCase):
    """The v3 layout: chapter files hold their headings, the preamble inputs metadata and layout."""

    def setUp(self):
        super().setUp()
        root = "docs/final-thesis/thesis"
        self.write(f"{root}/main.tex.template", "\n".join((
            r"\documentclass{isi-proposal}", r"\usepackage[normalem]{ulem}",
            r"\input{metadata}", r"\input{layout}", r"\begin{document}",
            r"\input{frontmatter/01-halaman-judul}", r"\setcounter{page}{2}",
            r"\input{frontmatter/02-halaman-pengesahan}", r"\input{chapters/01-pendahuluan}",
            r"\end{document}")))
        self.write(f"{root}/metadata.tex", r"\newcommand{\researchername}{Nama Peneliti}")
        self.write(f"{root}/layout.tex", "\n".join((
            r"% Chapter heading",
            r"\newcommand{\thesischapter}[2]{%",
            r"  \clearpage\phantomsection\addcontentsline{toc}{part}{BAB #1: #2}%",
            r"  \begin{center}\bfseries BAB #1\par #2\end{center}}",
            r"\newcommand{\signatory}[2]{#1\par\textbf{\expandafter\uline\expandafter{#2}}\par}")))
        self.write(f"{root}/frontmatter/01-halaman-judul.tex", "\n".join((
            r"\begin{titlepage}", r"\phantomsection", r"\addcontentsline{toc}{matter}{HALAMAN JUDUL}",
            r"\researchername\par", r"\end{titlepage}")))
        self.write(f"{root}/frontmatter/02-halaman-pengesahan.tex", "\n".join((
            r"\newpage", r"\phantomsection", r"\addcontentsline{toc}{matter}{HALAMAN PENGESAHAN}",
            r"\signatory{Dekan}{\researchername}")))
        self.write(f"{root}/chapters/01-pendahuluan.tex", "\n".join((
            r"\thesischapter{I}{PENDAHULUAN}", "",
            r"\section{Latar Belakang}\label{sec:latar-belakang}", "Isi bab.")))
        self.git("add", ".")
        self.git("commit", "-qm", "Thesis layout")
        self.head = diff.resolve_git_ref("head")

    def test_chapter_heading_inside_a_chapter_file_opens_a_page(self):
        source = diff.build_full_proposal(self.head)
        self.assertIn("\\clearpage\n\\thesischapter{I}{PENDAHULUAN}", source)
        self.assertIn(r"\addcontentsline{toc}{matter}{HALAMAN PENGESAHAN}", source)
        self.assertNotIn("% Chapter heading", diff.template_preamble(self.head))
        self.assertIn(r"\def\thesischapter#1#2{", diff.extract_section_formatting(self.head))

    def test_diff_expands_page_macros_and_lists_parts_in_the_change_map(self):
        latex = Path(diff.generate_diff_latex("thesis/v3", self.head, "scratch")).read_text()
        self.assertIn("PETA PERUBAHAN", latex)
        self.assertIn("HALAMAN PENGESAHAN", latex)
        self.assertIn(r"\textbf{\uline{", latex)
        self.assertIn("Nama Peneliti", latex)
        self.assertIn(r"\providecommand{\signatory}{}\renewcommand{\signatory}[2]", latex)
        self.assertNotIn(r"\label{sec:latar-belakang}", latex)
        self.assertIn(r"\label{R-sec:latar-belakang}", latex)


if __name__ == "__main__":
    unittest.main()
