"""Graphics use versioned binary blobs and fail unresolved source names."""

import hashlib
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from diff_assets import stage_graphics  # noqa: E402


class GraphicSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        self.repo.mkdir()
        self.previous = Path.cwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, self.previous)
        self.addCleanup(self.temporary.cleanup)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Diff Tests")
        self.git("config", "user.email", "diff-tests@example.invalid")
        self.output = Path(self.temporary.name) / "output"

    def git(self, *args):
        return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()

    def write(self, name, data):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Fixture revision")
        return self.git("rev-parse", "HEAD")

    @staticmethod
    def staged_path(text):
        return re.search(r"\{(diff-assets/[^{}]+)\}", text).group(1)

    def test_same_filename_changed_bytes_get_distinct_paths_and_real_binary_snapshots(self):
        old_bytes, new_bytes = b"\x89PNG\r\n\x1a\nold\x00\xff", b"\x89PNG\r\n\x1a\nnew\x00\xfe"
        self.write("thesis/figures/diagram.png", old_bytes)
        old = self.commit()
        self.write("thesis/figures/diagram.png", new_bytes)
        new = self.commit()
        # Dirty local bytes must never enter either compared revision.
        self.write("thesis/figures/diagram.png", b"dirty local image")
        source = r"\includegraphics[width=0.8\textwidth]{figures/diagram.png}"
        left = stage_graphics(old, source, self.output, "thesis/main.tex.template")
        right = stage_graphics(new, source, self.output, "thesis")
        self.assertNotEqual(left, right)
        for rendered, expected in ((left, old_bytes), (right, new_bytes)):
            staged = self.staged_path(rendered)
            self.assertEqual((self.output / staged).read_bytes(), expected)
            self.assertIn(hashlib.sha256(expected).hexdigest(), staged)
            self.assertTrue(rendered.startswith(r"\includegraphics[width=0.8\textwidth]"))

    def test_different_names_same_bytes_share_rendered_path_even_with_extension_change(self):
        data = b"\x89PNG\r\n\x1a\nidentical bytes"
        self.write("thesis/old.png", data)
        old = self.commit()
        self.git("rm", "thesis/old.png")
        self.write("thesis/new.pdf", data)
        new = self.commit()
        left = stage_graphics(old, r"\includegraphics{old.png}", self.output, "thesis")
        right = stage_graphics(new, r"\includegraphics{new.pdf}", self.output, "thesis")
        self.assertEqual(left, right)
        self.assertTrue(self.staged_path(right).endswith(".png"))

    def test_missing_extension_resolves_common_graphics_extension(self):
        self.write("thesis/diagram.pdf", b"%PDF-1.7\nfixture")
        ref = self.commit()
        rendered = stage_graphics(ref, r"\includegraphics* [height={2cm},clip]{diagram}", self.output, "thesis")
        self.assertTrue(rendered.startswith(r"\includegraphics* [height={2cm},clip]"))
        self.assertTrue(self.staged_path(rendered).endswith(".pdf"))

    def test_class_asset_directory_resolves_logo_before_basename_fallback(self):
        self.write("proposal/assets/isi-proposal.cls", b"Class fixture")
        self.write("proposal/assets/logo.png", b"class image")
        self.write("unrelated/logo.png", b"unrelated image")
        ref = self.commit()
        rendered = stage_graphics(ref, r"\includegraphics{logo.png}", self.output, "thesis")
        self.assertEqual((self.output / self.staged_path(rendered)).read_bytes(), b"class image")

    def test_manuscript_relative_name_wins_over_class_asset_and_basename_matches(self):
        self.write("thesis/logo.png", b"manuscript image")
        self.write("assets/class.cls", b"Class fixture")
        self.write("assets/logo.png", b"class image")
        ref = self.commit()
        rendered = stage_graphics(ref, r"\includegraphics{logo.png}", self.output, "thesis")
        self.assertEqual((self.output / self.staged_path(rendered)).read_bytes(), b"manuscript image")

    def test_explicit_repo_path_and_unique_basename_fallback_resolve(self):
        self.write("assets/figures/diagram.png", b"image")
        ref = self.commit()
        explicit = stage_graphics(ref, r"\includegraphics{assets/figures/diagram.png}", self.output, "thesis")
        fallback = stage_graphics(ref, r"\includegraphics{diagram.png}", self.output, "thesis")
        self.assertEqual(explicit, fallback)

    def test_graphicspath_and_nested_option_values_preserve_native_source(self):
        self.write("thesis/figures/diagram.png", b"image")
        self.write("unrelated/diagram.png", b"other image")
        ref = self.commit()
        source = r"\graphicspath{{figures/}} Before \includegraphics[width={\dimexpr[2pt]+3pt\relax}]{diagram.png} After"
        rendered = stage_graphics(ref, source, self.output, "thesis")
        self.assertTrue(rendered.startswith(r"\graphicspath{{figures/}} Before \includegraphics[width={\dimexpr[2pt]+3pt\relax}]"))
        self.assertTrue(rendered.endswith(" After"))
        self.assertEqual((self.output / self.staged_path(rendered)).read_bytes(), b"image")

    def test_ambiguous_basename_and_extension_candidates_fail(self):
        self.write("one/logo.png", b"first image")
        self.write("two/logo.png", b"second image")
        self.write("thesis/diagram.png", b"png")
        self.write("thesis/diagram.pdf", b"pdf")
        ref = self.commit()
        for source in (r"\includegraphics{logo.png}", r"\includegraphics{diagram}"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(ValueError, "Ambiguous graphic"):
                    stage_graphics(ref, source, self.output, "thesis")

    def test_missing_historical_asset_never_uses_current_untracked_file(self):
        self.write("tracked.txt", b"fixture")
        ref = self.commit()
        self.write("thesis/local.png", b"untracked image")
        with self.assertRaisesRegex(ValueError, "Missing graphic 'local.png'"):
            stage_graphics(ref, r"\includegraphics{local.png}", self.output, "thesis")

    def test_escaped_and_detokenized_literal_paths_are_supported(self):
        self.write("thesis/a_b #c.png", b"image")
        ref = self.commit()
        escaped = stage_graphics(ref, r"\includegraphics{a\_b \#c.png}", self.output, "thesis")
        detokenized = stage_graphics(ref, r"\includegraphics{\detokenize{a_b #c.png}}", self.output, "thesis")
        self.assertEqual(escaped, detokenized)

    def test_comments_stay_unchanged_and_dynamic_paths_fail_explicitly(self):
        self.write("thesis/a.png", b"image")
        ref = self.commit()
        source = "% \\includegraphics{missing.png}\n" + r"\includegraphics{a.png}"
        rendered = stage_graphics(ref, source, self.output, "thesis")
        self.assertTrue(rendered.startswith("% \\includegraphics{missing.png}\n"))
        with self.assertRaisesRegex(ValueError, "Unsupported dynamic graphic filename"):
            stage_graphics(ref, r"\includegraphics{\unknown/a.png}", self.output, "thesis")

    def test_text_without_graphics_needs_no_git_revision(self):
        self.assertEqual(stage_graphics("missing-ref", "Ordinary paragraph.", self.output, "thesis"), "Ordinary paragraph.")

    def test_literal_graphic_examples_are_preserved_without_loading_fake_assets(self):
        for environment in ("verbatim", "verbatim*", "Verbatim", "lstlisting", "minted"):
            with self.subTest(environment=environment):
                source = (rf"\begin{{{environment}}}" + "\n"
                          + r"\graphicspath{{missing/}} \includegraphics{missing.png}" + "\n"
                          + rf"\end{{{environment}}}")
                self.assertEqual(stage_graphics("missing-ref", source, self.output, "thesis"), source)
        for source in (r"\verb|\includegraphics{missing.png}|", r"\verb*+\graphicspath{{missing/}}+",
                       r"\verb|% \includegraphics{missing.png}|"):
            with self.subTest(source=source):
                self.assertEqual(stage_graphics("missing-ref", source, self.output, "thesis"), source)

    def test_real_graphic_after_literal_example_is_still_staged(self):
        self.write("thesis/real.png", b"image")
        ref = self.commit()
        literal = r"\verb|\includegraphics{missing.png}|"
        source = literal + "\n" + r"\includegraphics{real.png}"
        rendered = stage_graphics(ref, source, self.output, "thesis")
        self.assertTrue(rendered.startswith(literal + "\n"))
        self.assertEqual((self.output / self.staged_path(rendered)).read_bytes(), b"image")

    def test_literal_percent_does_not_hide_real_graphic_on_same_line(self):
        self.write("thesis/real.png", b"image")
        ref = self.commit()
        literal = r"\verb|% fake \includegraphics{missing.png}|"
        source = literal + " " + r"\includegraphics{real.png}"
        rendered = stage_graphics(ref, source, self.output, "thesis")
        self.assertTrue(rendered.startswith(literal + " "))
        self.assertEqual((self.output / self.staged_path(rendered)).read_bytes(), b"image")


if __name__ == "__main__":
    unittest.main()
