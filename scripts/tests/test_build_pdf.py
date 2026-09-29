"""Publishing and cleanup checks without depending on a TeX installation."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_pdf


class PdfBuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.source = self.root / "docs/proposal-phase/proposal/main.tex"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("\\documentclass{article}\n\\begin{document}\nsource\n\\end{document}\n")
        self.pdf = self.root / "scratch/proposal.pdf"
        self.patch = patch.object(build_pdf, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def compiler(self, code):
        def run(command, **kwargs):
            output = Path(next(arg.split("=", 1)[1] for arg in command if arg.startswith("-outdir=")))
            (output / "main.pdf").write_bytes(b"new PDF")
            (output / "main.aux").write_text("aux")
            (output / "main.log").write_text("compiler log")
            self.assertEqual(kwargs["cwd"], self.source.parent)
            self.assertIn(str(self.pdf.parent), kwargs["env"]["TEXINPUTS"])
            self.assertIn(str(self.root / "scripts"), kwargs["env"]["TEXINPUTS"])
            staged = Path(command[-1])
            self.assertEqual(staged.parent, output)
            self.assertIn("\\usepackage{pdf-navigation}\n\\begin{document}", staged.read_text())
            self.assertNotIn("pdf-navigation", self.source.read_text())
            return subprocess.CompletedProcess(command, code, "", "")
        return run

    def test_success_publishes_only_pdf_and_removes_legacy_source_pdf(self):
        self.source.with_suffix(".pdf").write_bytes(b"old PDF")
        with patch.object(build_pdf.subprocess, "run", side_effect=self.compiler(0)):
            self.assertEqual(build_pdf.compile_pdf(self.source, self.pdf), str(self.pdf))
        self.assertEqual(self.pdf.read_bytes(), b"new PDF")
        self.assertEqual(list(self.pdf.parent.iterdir()), [self.pdf])
        self.assertFalse(self.source.with_suffix(".pdf").exists())
        self.assertTrue(self.source.exists())

    def test_failure_preserves_previous_pdf_and_only_retains_log(self):
        self.pdf.parent.mkdir()
        self.pdf.write_bytes(b"previous PDF")
        with patch.object(build_pdf.subprocess, "run", side_effect=self.compiler(1)):
            self.assertIsNone(build_pdf.compile_pdf(self.source, self.pdf))
        self.assertEqual(self.pdf.read_bytes(), b"previous PDF")
        self.assertEqual(self.pdf.with_suffix(".log").read_text(), "compiler log")
        self.assertEqual(set(self.pdf.parent.iterdir()), {self.pdf, self.pdf.with_suffix(".log")})

    def test_cleanup_preserves_pdfs_sources_and_unrelated_scratch_files(self):
        names = ["scratch/proposal_v1.aux", "scratch/proposal_diff_x_y_references_v1.bib",
                 "docs/proposal-phase/proposal/build/main.aux"]
        keep = ["scratch/proposal_v1.pdf", "scratch/notes.txt", "scratch/custom.tex"]
        for name in names + keep:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture")
        build_pdf.clean_auxiliary_files()
        self.assertTrue(self.source.exists())
        for name in names:
            self.assertFalse((self.root / name).exists())
        for name in keep:
            self.assertTrue((self.root / name).exists())


if __name__ == "__main__":
    unittest.main()
