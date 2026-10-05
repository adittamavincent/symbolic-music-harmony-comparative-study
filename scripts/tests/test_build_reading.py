"""Markdown preparation checks for the reading PDF, without pandoc or TeX."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_reading


class ReadingPreparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        patcher = patch.object(build_reading, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.write("docs/final-thesis/study/a.md", "# Judul A\n\nLihat [B](../supervision/b.md#bagian), "
                   "[kode](../../../research/x.py), [web](https://example.org), dan [atas](#judul-a).\n\n"
                   "```text\n[tetap](b.md)\n```\n")
        self.write("docs/final-thesis/supervision/b.md", "# Judul B\n")
        self.anchors = {self.root / f: build_reading.slug(f) for f in
                        ("docs/final-thesis/study/a.md", "docs/final-thesis/supervision/b.md")}

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_links_point_inside_the_pdf_or_keep_their_text(self):
        text = build_reading.prepare("docs/final-thesis/study/a.md", self.anchors)
        self.assertIn("[B](#berkas-docs-final-thesis-supervision-b-md)", text)
        self.assertIn("Lihat [B]", text)
        self.assertIn(", kode, [web](https://example.org), dan atas.", text)
        self.assertIn("```text\n[tetap](b.md)\n```", text)

    def test_first_heading_gets_anchor_and_source_line(self):
        text = build_reading.prepare("docs/final-thesis/study/a.md", self.anchors)
        self.assertTrue(text.startswith("# Judul A {#berkas-docs-final-thesis-study-a-md}\n\n"
                                        "*Berkas sumber: `docs/final-thesis/study/a.md`*\n"))

    def test_table_separator_follows_cell_lengths(self):
        rows = ["| Halaman | Isi |", "| 9 | " + "x" * 80 + " |"]
        separator = build_reading.widen_separator(rows, "| --- | :---: |")
        first, second = build_reading.split_row(separator)
        self.assertGreaterEqual(len(first), 13)
        self.assertEqual(len(second), 60 + 2)
        self.assertTrue(second.startswith(":") and second.endswith(":"))

    def test_escaped_pipe_stays_in_its_cell(self):
        self.assertEqual(build_reading.split_row(r"| a \| b | c |"), [r"a \| b", "c"])

    def test_latest_tag_is_the_highest_thesis_version(self):
        listing = type("Result", (), {"stdout": "thesis/v10\nthesis/v3\nthesis/v4\nthesis/v4-draft\n"})
        with patch.object(build_reading, "git", return_value=listing):
            self.assertEqual(build_reading.latest_version_tag(), "thesis/v10")

    def test_files_missing_at_a_revision_are_skipped(self):
        parts = [("Belajar", ["docs/final-thesis/study/a.md", "docs/final-thesis/study/baru.md"]),
                 ("Kosong", ["docs/final-thesis/tidak-ada.md"])]
        with patch.object(build_reading, "PARTS", parts):
            present, absent = build_reading.present_parts(self.root)
        self.assertEqual(present, [("Belajar", ["docs/final-thesis/study/a.md"])])
        self.assertEqual(absent, ["docs/final-thesis/study/baru.md", "docs/final-thesis/tidak-ada.md"])

    def test_version_label_names_tag_and_commit(self):
        commit = "48d72e2e94ddaec332618c01e2a90345d92c7518"
        self.assertEqual(build_reading.describe(commit, "thesis/v4"), "versi v4 (tag thesis/v4, commit 48d72e2)")
        self.assertEqual(build_reading.describe(commit, None), "commit 48d72e2 (tanpa tag versi)")

    def test_unlisted_notes_are_reported(self):
        self.write("docs/final-thesis/records/baru.md", "# Baru\n")
        self.write("docs/final-thesis/thesis/README.md", "# Naskah\n")
        with patch.object(build_reading, "PARTS", [("Belajar", ["docs/final-thesis/study/a.md"])]):
            missing = build_reading.missing_files()
        self.assertEqual(missing, ["docs/final-thesis/records/baru.md", "docs/final-thesis/supervision/b.md"])


if __name__ == "__main__":
    unittest.main()
