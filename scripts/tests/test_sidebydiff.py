"""Regression checks for committed manuscript diffs, independent of TeX."""
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


class RefAndSourceTests(unittest.TestCase):
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

    def test_changed_citations_use_boxes_separate_from_text_highlights(self):
        old, new = diff.word_level_render("Old text.", r"New \parencite{source} text.")
        self.assertIn(r"\colorbox{inshl}{\parencite{source}}", new)
        self.assertNotIn(r"\inhighlight{\parencite", new)

    def test_tex_space_escape_stays_outside_highlights(self):
        old, new = diff.word_level_render("Old text.", "Fang et al.\\ \\parencite{source} text.")
        self.assertIn("al.\\ ", new)
        self.assertNotIn("al.\\}", new)


class SectionRenderingTests(unittest.TestCase):
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

    def test_frontmatter_retains_text_formatting_and_font_scope(self):
        source = r"""\begin{titlepage}
\begin{center}\bfseries SKRIPSI\par Oleh:\\ Name\end{center}
\end{titlepage}
\setcounter{page}{2}\newpage
\begin{spacing}{1.15}\begin{center}HALAMAN PENGESAHAN\end{center}
Original approval.\end{spacing}"""
        cleaned = diff.clean_latex_for_diff(source)
        self.assertIn(r"\begin{center}\bfseries SKRIPSI\par Oleh:\\ Name\end{center}", cleaned)
        self.assertIn("Original approval.", cleaned)
        self.assertNotIn(r"\newpage", cleaned)
        self.assertNotIn(r"\setcounter{page}", cleaned)
        self.assertEqual(diff.render_section_text(cleaned, cleaned), (cleaned, cleaned))

    def test_added_sections_and_subsections_do_not_shift_later_matches(self):
        old = r"""Cover text.
\section{A}
A text.
\subsection{Existing}
Existing text.
\section{B}
B text."""
        new = old.replace(r"\subsection{Existing}", "\\subsection{Added}\nAdded text.\n\\subsection{Existing}")
        new = new.replace(r"\section{B}", "\\section{Inserted}\nInserted text.\n\\section{B}")
        pairs = diff.align_sections(diff.split_sections(old), diff.split_sections(new))
        self.assertEqual(len(pairs), 6)
        self.assertEqual(pairs[2][0], "")
        self.assertIn(r"\subsection{Added}", pairs[2][1])
        self.assertEqual(pairs[3][0], pairs[3][1])
        self.assertEqual(pairs[4][0], "")
        self.assertEqual(pairs[-1][0], pairs[-1][1])

    def test_chapter_additions_keep_existing_section_alignment(self):
        old = "\\section{Background}\nText.\n\\section{Method}\nMethod."
        new = "\\thesischapter{I}{INTRODUCTION}\n" + old
        pairs = diff.align_sections(diff.split_sections(old), diff.split_sections(new))
        self.assertEqual(pairs[0][0], "")
        self.assertIn(r"\thesischapter", pairs[0][1])
        self.assertEqual(pairs[1][0], pairs[1][1])
        self.assertEqual(pairs[2][0], pairs[2][1])

    def test_long_section_flows_without_per_paragraph_boxes_or_padding(self):
        old = "\\section{Long}\n\n" + "\n\n".join(f"Paragraph {i}." for i in range(80))
        new = old + "\n\nAdditional paragraph."
        rendered = diff.render_sections(old, new)
        self.assertEqual(rendered.count(r"\switchcolumn*"), 1)
        self.assertNotIn("minipage", rendered)
        self.assertNotIn(r"\hrule", rendered)
        self.assertNotIn(r"\newpage", rendered)
        self.assertIn(r"\inhighlight{Additional paragraph}", rendered)
        self.assertIn("Paragraph 79.", rendered)

    def test_deleted_section_and_renamed_section_keep_both_sources(self):
        old = "\\section{A}\nFirst.\n\\section{Deleted}\nRemoved.\n\\section{B}\nLast."
        new = "\\section{A}\nFirst.\n\\section{B}\nLast."
        pairs = diff.align_sections(diff.split_sections(old), diff.split_sections(new))
        self.assertEqual(pairs[1], ("\\section{Deleted}\nRemoved.", ""))
        self.assertEqual(pairs[-1][0], pairs[-1][1])
        renamed = diff.align_sections(diff.split_sections(new), diff.split_sections(new.replace("{B}", "{C}")))
        self.assertIn("{B}", renamed[-1][0])
        self.assertIn("{C}", renamed[-1][1])


if __name__ == "__main__":
    unittest.main()
