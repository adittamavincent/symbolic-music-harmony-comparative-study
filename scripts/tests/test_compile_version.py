"""Phase-aware ref resolution and source staging for historical builds."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compile_version as cv

PROPOSAL = "docs/proposal-phase/proposal"
THESIS = "docs/final-thesis/thesis"
ASSETS = "docs/proposal-phase/assets"


class CompileVersionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        cwd = os.getcwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, cwd)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write(f"{ASSETS}/isi-proposal.cls", "\\ProvidesClass{isi-proposal}\n")
        self.write(f"{ASSETS}/references.bib", "@book{a, title={A}}\n")
        self.write(f"{ASSETS}/logo-isi.png", "png")
        self.write(f"{PROPOSAL}/main.tex.template",
                   "\\documentclass{isi-proposal}\n\\addbibresource{../assets/references.bib}\n"
                   "\\begin{document}\n\\input{chapters/01-pendahuluan}\n\\end{document}\n")
        self.write(f"{PROPOSAL}/chapters/01-pendahuluan.tex", "Proposal text\n")
        self.commit("proposal")
        self.git("tag", "proposal/v2")
        self.proposal_commit = self.rev("HEAD")
        self.write(f"{THESIS}/main.tex.template",
                   "\\documentclass{isi-proposal}\n"
                   "\\addbibresource{../../proposal-phase/assets/references.bib}\n"
                   "\\newcommand{\\t}{${THESIS_TITLE}}\n\\begin{document}\n"
                   "\\input{chapters/00-frontmatter}\n% \\input{chapters/04-hasil}\n"
                   "\\input{chapters/01-pendahuluan}\n\\end{document}\n")
        self.write(f"{THESIS}/chapters/00-frontmatter.tex", "\\input{chapters/00-titlepage}\n")
        self.write(f"{THESIS}/chapters/00-titlepage.tex", "Cover % trailing comment")
        self.write(f"{THESIS}/chapters/01-pendahuluan.tex", "Thesis text\n")
        self.commit("thesis")
        self.thesis_commit = self.rev("HEAD")

    def git(self, *args):
        subprocess.run(["git", *args], check=True, capture_output=True)

    def rev(self, ref):
        return subprocess.run(["git", "rev-parse", ref], check=True,
                              capture_output=True, text=True).stdout.strip()

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def test_bare_and_prefixed_proposal_versions_resolve_to_tag(self):
        for ref in ("v2", "2", "proposal/v2"):
            self.assertEqual(cv.resolve("proposal", ref), (self.proposal_commit, "v2", "proposal/v2"))

    def test_versions_are_rejected_in_the_wrong_phase(self):
        for phase, ref, hint in (("proposal", "v3", "make thesis v3"),
                                 ("proposal", "proposal/v3", "make thesis v3"),
                                 ("thesis", "v2", "make proposal v2"),
                                 ("thesis", "thesis/v1", "make proposal v1"),
                                 ("thesis", "proposal/v2", "make proposal v2")):
            with self.subTest(phase=phase, ref=ref):
                with self.assertRaisesRegex(cv.VersionError, hint):
                    cv.resolve(phase, ref)

    def test_missing_thesis_tag_names_the_alternatives(self):
        with self.assertRaisesRegex(cv.VersionError, "thesis/v3 does not exist yet.*make thesis head"):
            cv.resolve("thesis", "v3")

    def test_created_thesis_tag_resolves(self):
        self.git("tag", "thesis/v3")
        self.assertEqual(cv.resolve("thesis", "v3"), (self.thesis_commit, "v3", "thesis/v3"))

    def test_head_is_labelled_by_commit_and_its_phase_is_inferred(self):
        commit, label, tag = cv.resolve("thesis", "head")
        self.assertEqual((commit, label, tag), (self.thesis_commit, self.thesis_commit, None))
        self.assertEqual(cv.find_template(commit, "thesis")[0], f"{THESIS}/main.tex.template")
        with self.assertRaisesRegex(cv.VersionError, "thesis phase.*make thesis <ref>"):
            cv.find_template(commit, "proposal")

    def test_untagged_proposal_commit_builds_only_as_proposal(self):
        commit, _, tag = cv.resolve("proposal", self.proposal_commit[:8])
        self.assertEqual(cv.find_template(commit, "proposal", tag)[0], f"{PROPOSAL}/main.tex.template")
        with self.assertRaisesRegex(cv.VersionError, "No thesis manuscript.*make proposal"):
            cv.find_template(commit, "thesis", tag)

    def test_staging_uses_committed_sources_not_the_working_tree(self):
        self.write(f"{THESIS}/chapters/01-pendahuluan.tex", "Uncommitted text\n")
        template, paths = cv.find_template(self.thesis_commit, "thesis")
        out = self.repo / "out"
        out.mkdir()
        tex = Path(cv.stage_sources(self.thesis_commit, template, paths, out, "thesis_x")).read_text()
        self.assertIn("Cover % trailing comment\n", tex)
        self.assertIn("Thesis text", tex)
        self.assertNotIn("Uncommitted", tex)
        self.assertIn("% \\input{chapters/04-hasil}", tex)
        self.assertIn("\\addbibresource{references.bib}", tex)
        self.assertNotIn("${THESIS_TITLE}", tex)
        self.assertEqual({p.name for p in out.iterdir()},
                         {"thesis_x.tex", "references.bib", "isi-proposal.cls", "logo-isi.png"})

    def test_unknown_ref_fails_clearly(self):
        with self.assertRaisesRegex(cv.VersionError, "Unknown Git ref: nope"):
            cv.resolve("thesis", "nope")


if __name__ == "__main__":
    unittest.main()
