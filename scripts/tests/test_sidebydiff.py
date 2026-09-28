"""Regression checks for committed manuscript diffs, independent of TeX."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "sidebydiff.py"
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
        Path(f"{name}.pdf").write_bytes(b"compiled PDF")
        with patch.object(diff.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")) as run:
            self.assertEqual(diff.latex_to_pdf(f"{name}.tex", "."), f"./{name}.pdf")
            self.assertEqual(run.call_args.args[0][-1], f"{name}.tex")

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


if __name__ == "__main__":
    unittest.main()
