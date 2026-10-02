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

    def test_changed_citations_use_boxes_separate_from_text_highlights(self):
        old, new = diff.word_level_render("Old text.", r"New \parencite{source} text.")
        self.assertIn(r"\diffinline{inshl}{\parencite{source}}", new)
        self.assertNotIn(r"\inhighlight{\parencite", new)

    def test_tex_space_escape_stays_outside_highlights(self):
        old, new = diff.word_level_render("Old text.", "Fang et al.\\ \\parencite{source} text.")
        self.assertIn("al.\\ ", new)
        self.assertNotIn("al.\\}", new)

    def test_changed_tikz_picture_is_highlighted_as_one_block(self):
        picture = "\\begin{tikzpicture}\n\\node (%s) [process] {Step};\n\\end{tikzpicture}"
        old, new = diff.word_level_render(picture % "start", picture % "dev")
        self.assertEqual(old, "\\begin{diffmath}{delhl}\n" + picture % "start" + "\n\\end{diffmath}\n")
        self.assertEqual(new, "\\begin{diffmath}{inshl}\n" + picture % "dev" + "\n\\end{diffmath}\n")
        old, new = diff.word_level_render(picture % "start", "")
        self.assertEqual(new, "")


class SectionRenderingTests(unittest.TestCase):
    def test_heading_format_change_highlights_only_the_formatted_phrase(self):
        old = r"\subsection{Evaluasi Otomatis dalam Music Information Retrieval (MIR)}"
        new = r"\subsection{Evaluasi Otomatis dalam \textit{Music Information Retrieval} (MIR)}"
        left, right = diff.word_level_render(old, new)
        self.assertEqual(left, r"\subsection{Evaluasi Otomatis dalam \delhighlight{Music}\diffspace{delhl}\delhighlight{Information}\diffspace{delhl}\delhighlight{Retrieval} (MIR)}")
        self.assertEqual(right, r"\subsection{Evaluasi Otomatis dalam \textit{\inhighlight{Music}\diffspace{inshl}\inhighlight{Information}\diffspace{inshl}\inhighlight{Retrieval}} (MIR)}")
        for rendered in (left, right):
            self.assertNotIn(r"\renewcommand{\thesubsection}", rendered)
            self.assertNotIn(r"\colorbox", rendered)

    def test_heading_text_change_retains_unchanged_words_and_diffs_body_separately(self):
        old = "\\section{Existing old title}\n\nOld body."
        new = "\\section{Existing new title}\n\nNew body."
        left, right = diff.render_section_text(old, new)
        self.assertIn(r"\section{Existing \delhighlight{old} title}", left)
        self.assertIn(r"\section{Existing \inhighlight{new} title}", right)
        self.assertIn(r"\delhighlight{Old} body.", left)
        self.assertIn(r"\inhighlight{New} body.", right)
        self.assertNotIn(r"\renewcommand", left + right)

    def test_heading_levels_starred_forms_and_optional_titles_keep_their_wrappers(self):
        for command in ("section", "subsection", "subsubsection"):
            for suffix in ("", "*", "[Short title]"):
                with self.subTest(command=command, suffix=suffix):
                    prefix = "\\" + command + suffix
                    old = prefix + "{Same plain wording}"
                    new = prefix + r"{Same \textit{plain} wording}"
                    left, right = diff.word_level_render(old, new)
                    self.assertEqual(left, prefix + r"{Same \delhighlight{plain} wording}")
                    self.assertEqual(right, prefix + r"{Same \textit{\inhighlight{plain}} wording}")

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
        self.assertIn(r"\newpage", cleaned)
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
        self.assertIn(r"\inhighlight{Additional}\diffspace{inshl}\inhighlight{paragraph.}", rendered)
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


class FrontmatterAlignmentTests(unittest.TestCase):
    def abstract(self, language, body, header=True, heading_style="textbf"):
        title, keywords = ("ABSTRAK", "Kata Kunci:") if language == "id" else ("ABSTRACT", "Keywords:")
        heading = rf"\begin{{center}}\{heading_style}{{{title}}}\end{{center}}" if header else ""
        return "\n".join((r"\begin{spacing}{1.15}", heading, "", body, "",
                          rf"\textbf{{{keywords}}} Music, Harmony", r"\end{spacing}"))

    def source(self, indo, english):
        return ("\n" + r"\newpage" + "\n").join((
            r"\begin{titlepage}\bfseries PROPOSAL SKRIPSI\end{titlepage}",
            r"\begin{spacing}{1.15}HALAMAN PENGESAHAN\end{spacing}",
            indo, english, r"\section{Latar Belakang}" + "\nBody text.",
        ))

    def test_each_abstract_pairs_by_language_with_its_header_and_body(self):
        old = diff.clean_latex_for_diff(self.source(
            self.abstract("id", "Indonesia old."), self.abstract("en", "English old.")))
        new = diff.clean_latex_for_diff(self.source(
            self.abstract("id", "Indonesia new. " * 50), self.abstract("en", "English new.")))
        pairs = diff.align_sections(diff.split_sections(old), diff.split_sections(new))
        self.assertEqual([key for key, _ in diff.split_sections(old)][:4], [
            ("frontmatter", "cover"), ("frontmatter", "approval"),
            ("frontmatter", "abstract-id"), ("frontmatter", "abstract-en"),
        ])
        for side in pairs[2]:
            self.assertIn("ABSTRAK", side)
            self.assertIn("Indonesia", side)
            self.assertNotIn("English", side)
        for side in pairs[3]:
            self.assertIn("ABSTRACT", side)
            self.assertIn("English", side)
            self.assertNotIn("Indonesia", side)
        # Container boundaries remain local to each compared unit.
        for pair in pairs:
            for text in pair:
                self.assertEqual(text.count(r"\begin{spacing}"), text.count(r"\end{spacing}"))

    def test_missing_heading_does_not_create_text_or_shift_language_alignment(self):
        old = diff.clean_latex_for_diff(self.source(
            self.abstract("id", "Same Indonesian body.", header=False),
            self.abstract("en", "Same English body.", header=False)))
        new = diff.clean_latex_for_diff(self.source(
            self.abstract("id", "Same Indonesian body."), self.abstract("en", "Same English body.")))
        pairs = diff.align_sections(diff.split_sections(old), diff.split_sections(new))
        self.assertEqual(len(pairs), 5)
        self.assertNotIn("ABSTRAK", pairs[2][0])
        self.assertIn("Same Indonesian body.", pairs[2][0])
        self.assertIn("ABSTRAK", pairs[2][1])
        self.assertNotIn("ABSTRACT", pairs[3][0])
        rendered_old, rendered_new = diff.render_section_text(*pairs[2])
        self.assertNotIn("ABSTRAK", rendered_old)
        self.assertIn(r"\textbf{\inhighlight{ABSTRAK}}", rendered_new)
        self.assertIn("Same Indonesian body.", rendered_old)
        self.assertIn("Same Indonesian body.", rendered_new)

    def test_heading_style_changes_do_not_change_abstract_identity(self):
        old = self.abstract("id", "Old body.", heading_style="textbf")
        new = self.abstract("id", "New body.", heading_style="textsc")
        pairs = diff.align_sections(diff.split_sections(old), diff.split_sections(new))
        self.assertEqual(len(pairs), 1)
        self.assertIn("Old body.", pairs[0][0])
        self.assertIn("New body.", pairs[0][1])

    def test_deleted_indonesian_abstract_does_not_pair_with_english(self):
        old = diff.clean_latex_for_diff(self.source(self.abstract("id", "Indonesian."),
                                                  self.abstract("en", "English.")))
        new = diff.clean_latex_for_diff(self.source("", self.abstract("en", "English.")))
        pairs = diff.align_sections(diff.split_sections(old), diff.split_sections(new))
        self.assertIn("Indonesian.", pairs[2][0])
        self.assertEqual(pairs[2][1], "")
        self.assertIn("English.", pairs[3][0])
        self.assertIn("English.", pairs[3][1])

    def test_source_page_breaks_apply_between_pairs_without_blank_duplicates(self):
        source = diff.clean_latex_for_diff(self.source(self.abstract("id", "Indonesian."),
                                                     self.abstract("en", "English.")))
        source = source.replace(r"\newpage", "\\newpage\n\\clearpage")
        rendered = diff.render_sections(source, source)
        self.assertEqual(rendered.count("\\end{paracol}\n\\newpage\n\\begin{paracol}{2}"), 4)
        self.assertNotIn(r"\clearpage", rendered)
        for column in ("leftside", "rightside"):
            import re
            for text in re.findall(rf"\\begin\{{{column}\}}(.*?)\\end\{{{column}\}}", rendered, re.DOTALL):
                self.assertNotIn(r"\newpage", text)

    def test_break_on_only_one_side_still_starts_both_sections_on_same_page(self):
        old = "\\section{A}\nFirst.\n\\section{B}\nSecond."
        new = old.replace(r"\section{B}", "\\newpage\n\\section{B}")
        rendered = diff.render_sections(old, new)
        self.assertEqual(rendered.count(r"\newpage"), 1)
        self.assertEqual(rendered.count(r"\section{B}"), 2)


class MathAndSourceLayoutTests(unittest.TestCase):
    LEADING_FORMULA = r"""{\small
\begin{multline}
\text{Violation}_{\text{leading}}(t) = \mathds{1}\left(p_{i,t} \equiv L_{\text{pc}} \pmod{12}\right) \times \mathds{1}\left(p_{i,t+1} > p_{i,t}\right) \\
\times \mathds{1}\left(p_{i,t+1} \not\equiv K_{\text{tonic}} \pmod{12}\right) \\
\times \mathds{1}\left(\text{mode} \neq \text{natural minor} \lor L_{\text{pc}} \equiv (K_{\text{tonic}} - 1) \pmod{12}\right)
\end{multline}
}"""

    def test_added_multline_gets_a_block_background_and_preserves_the_formula(self):
        old, new = diff.word_level_render("", self.LEADING_FORMULA)
        self.assertEqual(old, "")
        self.assertIn(r"\begin{diffmath}{inshl}", new)
        self.assertEqual(new.count(r"\begin{multline}"), 1)
        self.assertEqual(new.count(r"\end{multline}"), 1)
        self.assertIn(r"{\small", new)
        self.assertIn(r"\not\equiv K_{\text{tonic}}", new)
        self.assertEqual(new.count(r"\\"), self.LEADING_FORMULA.count(r"\\"))
        import re
        content = re.search(r'\\begin\{diffmath\}\{inshl\}\n(.*?)\n\\end\{diffmath\}', new, re.DOTALL).group(1)
        self.assertEqual(re.sub(r'\s+', ' ', content).strip(),
                         re.sub(r'\s+', ' ', self.LEADING_FORMULA).strip())
        self.assertNotIn(r"\inhighlight{", new)

    def test_deleted_multline_gets_red_and_leaves_the_other_side_empty(self):
        old, new = diff.word_level_render(self.LEADING_FORMULA, "")
        self.assertIn(r"\begin{diffmath}{delhl}", old)
        self.assertEqual(new, "")

    def test_changed_formula_highlights_both_versions_and_unchanged_formula_does_not(self):
        revised = self.LEADING_FORMULA.replace(" > ", " < ")
        old, new = diff.word_level_render(self.LEADING_FORMULA, revised)
        self.assertIn(r"\begin{diffmath}{delhl}", old)
        self.assertIn(r"\begin{diffmath}{inshl}", new)
        self.assertIn(" > ", old)
        self.assertIn(" < ", new)
        same_old, same_new = diff.word_level_render(self.LEADING_FORMULA, self.LEADING_FORMULA)
        self.assertNotIn("diffmath", same_old)
        self.assertNotIn("diffmath", same_new)

    def test_display_environment_variants_and_alignment_tabs_remain_intact(self):
        for env, body in (("equation", "x = 1"), ("equation*", "x = 1"),
                          ("align", r"x &= 1 \\ y &= 2"), ("align*", r"x &= 1 \\ y &= 2"),
                          ("gather", r"x = 1 \\ y = 2"), ("multline*", r"x = 1 \\ + 2"),
                          ("alignat", r"{2} x &= 1 & y &= 2")):
            with self.subTest(env=env):
                source = rf"\begin{{{env}}}{body}\end{{{env}}}"
                _, rendered = diff.word_level_render("", source)
                self.assertIn(r"\begin{diffmath}{inshl}", rendered)
                self.assertIn(body, rendered)
                self.assertIn(rf"\begin{{{env}}}", rendered)
                self.assertIn(rf"\end{{{env}}}", rendered)

    def test_bracket_display_math_is_highlighted_as_a_block(self):
        _, new = diff.word_level_render("", r"\[x = 1\]")
        self.assertIn(r"\begin{diffmath}{inshl}", new)
        self.assertIn(r"\[x = 1\]", new)

    def test_highlighted_prose_leaves_spaces_breakable_including_inside_formatting(self):
        _, new = diff.word_level_render("", r"Plain words \textit{Music \textbf{Information Retrieval}}.")
        self.assertIn(r"\inhighlight{Plain}\diffspace{inshl}\inhighlight{words}", new)
        self.assertIn(r"\textit{\inhighlight{Music}\diffspace{inshl}\textbf{\inhighlight{Information}\diffspace{inshl}\inhighlight{Retrieval}}}\inhighlight{.}", new)
        self.assertNotIn(r"\inhighlight{Plain words}", new)
        self.assertNotIn(r"\inhighlight{\textit", new)
        _, grouped = diff.word_level_render("", "{Grouped words}")
        self.assertEqual(grouped.strip(), r"{\inhighlight{Grouped}\diffspace{inshl}\inhighlight{words}}")

    def test_adjacent_changes_connect_without_coloring_unchanged_neighbors(self):
        old, new = diff.word_level_render("Stable old phrase stays.", "Stable new words stays.")
        self.assertEqual(old, r"Stable \delhighlight{old}\diffspace{delhl}\delhighlight{phrase} stays. ")
        self.assertEqual(new, r"Stable \inhighlight{new}\diffspace{inshl}\inhighlight{words} stays. ")
        _, single = diff.word_level_render("Stable old stays.", "Stable new stays.")
        self.assertNotIn(r"\diffspace", single)

    def test_soft_source_lines_connect_but_paragraph_boundaries_do_not(self):
        _, new = diff.word_level_render("", "First line\nsecond line.\n\nNext paragraph.")
        self.assertIn("\\inhighlight{line}\\diffspace{inshl}%\n\\inhighlight{second}", new)
        self.assertIn("\\inhighlight{line.} \n\n\\inhighlight{Next}", new)

    def test_parentheses_and_punctuation_are_inside_highlights_including_math_and_citations(self):
        phrase = r"(\textit{orderless NADE})"
        old, new = diff.word_level_render(phrase, "")
        self.assertEqual(new, "")
        self.assertEqual(old.strip(), r"\delhighlight{(}\textit{\delhighlight{orderless}\diffspace{delhl}\delhighlight{NADE}}\delhighlight{)}")
        _, new = diff.word_level_render("", phrase + ",")
        self.assertIn(r"\inhighlight{(}", new)
        self.assertTrue(new.endswith(r"\inhighlight{),} "))
        _, math = diff.word_level_render("", "($x = 1$).")
        self.assertIn(r"\diffinline{inshl}{(\ensuremath{x = 1}).}", math)
        _, compact_math = diff.word_level_render("", "($x$),")
        self.assertEqual(compact_math.strip(), r"\diffinline{inshl}{(\ensuremath{x}),}")
        same, _ = diff.word_level_render("($x$),", "($x$),")
        self.assertEqual(same.strip(), "($x$),")
        _, cite = diff.word_level_render("", r"(\parencite{source}),")
        self.assertIn(r"\diffinline{inshl}{(\parencite{source}),}", cite)

    def test_adjacent_inline_formulas_keep_separate_math_boxes(self):
        _, new = diff.word_level_render("", "$x = 1$ $y = 2$")
        self.assertEqual(new.count(r"\diffinline{inshl}"), 2)
        self.assertIn(r"\ensuremath{x = 1}", new)
        self.assertIn(r"\ensuremath{y = 2}", new)

    def test_source_paragraph_settings_are_preserved_without_forced_ragged_alignment(self):
        template = r"""\tolerance=1
\emergencystretch=\maxdimen
\hyphenpenalty=10000
\exhyphenpenalty=10000
\begin{document}
\doublespacing
\end{document}"""
        with patch.object(diff, "find_git_path", return_value="main.tex.template"), \
             patch.object(diff, "get_git_content", return_value=template):
            formatting = diff.extract_section_formatting("ref")
        for line in template.splitlines():
            if not line.startswith((r"\begin", r"\end")):
                self.assertIn(line, formatting)
        rendered = diff.render_sections(r"\section{A}" + "\nJustified paragraph.",
                                        r"\section{A}" + "\nJustified paragraph.")
        self.assertNotIn(r"\raggedright", rendered)
        # Alignment explicitly chosen in the source is still kept.
        signature = r"\begin{minipage}{0.48\textwidth}\raggedright Original signature.\end{minipage}"
        self.assertIn(signature, diff.render_sections(signature, signature))


class ProposalToThesisTests(unittest.TestCase):
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

    def test_citation_page_arguments_stay_whole_and_outside_soul(self):
        tokens = [value for kind, value in diff.tokenize_words(r"kuint \parencite[9, 12]{strube1928}: lalu")
                  if kind == "W"]
        self.assertIn(r"\parencite[9, 12]{strube1928}:", tokens)
        _, new = diff.word_level_render("", r"kuint \parencite[35]{strube1928}: lalu")
        self.assertIn(r"\diffinline{inshl}{\parencite[35]{strube1928}:}", new)
        self.assertNotIn(r"\inhighlight{\parencite", new)
        self.assertEqual(diff.extract_citation_keys(r"\parencite[9]{strube1928} \cite{a, b}"),
                         ["a", "b", "strube1928"])

    def test_changed_bibliography_names_and_dates_remain_parseable(self):
        old = "@book{k,\n  author = {Le, A and Bigo, B},\n  title = {Old},\n  year = {2024}\n}"
        new = "@book{k,\n  author = {Le, A and Keller, C},\n  title = {New},\n  year = {2025}\n}"
        left, right = diff.diff_bib_files(old, new, ["k"], ["k"])
        self.assertIn("author = {Le, A and Bigo, B}", left)
        self.assertIn("year = {2025}", right)
        self.assertIn(r"title = {{\bibdelcolor Old}}", left)
        self.assertIn(r"title = {{\bibinscolor New}}", right)
        self.assertNotIn(r"\textcolor", left + right)


if __name__ == "__main__":
    unittest.main()
