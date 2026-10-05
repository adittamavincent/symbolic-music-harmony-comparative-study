"""Reference-list comparison: changed fields, citation keys, and entry rows."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diff_bibliography as bib  # noqa: E402


class BibliographyDiffTests(unittest.TestCase):
    def test_changed_bibliography_names_and_dates_remain_parseable(self):
        old = "@book{k,\n  author = {Le, A and Bigo, B},\n  title = {Old},\n  year = {2024}\n}"
        new = "@book{k,\n  author = {Le, A and Keller, C},\n  title = {New},\n  year = {2025}\n}"
        left, right = bib.diff_bib_files(old, new, ["k"], ["k"])
        self.assertIn("author = {Le, A and Bigo, B}", left)
        self.assertIn("year = {2025}", right)
        self.assertIn(r"title = {{\bibdelcolor Old}}", left)
        self.assertIn(r"title = {{\bibinscolor New}}", right)
        self.assertNotIn(r"\textcolor", left + right)
        self.assertIn("userc = {moddel}", left)
        self.assertIn("userc = {modins}", right)

    def test_unchanged_entry_has_no_change_flag(self):
        original = "@book{k, author = {Strube, Gustav}, title = {Chords}, year = {1928}}"
        left, right = bib.diff_bib_files(original, original, ["k"], ["k"])
        self.assertNotIn("userc", left + right)
        self.assertNotIn(r"\bibdelcolor", left)
        self.assertNotIn(r"\bibinscolor", right)

    def test_parse_sensitive_fields_flag_the_entry_without_coloring_the_value(self):
        for field, old_value, new_value in (
            ("author", "Strube, Gustav", "Strube, G."),
            ("year", "1928", "1929"),
            ("pages", "10--12", "10--13"),
            ("doi", "10.1/old", "10.1/new"),
            ("url", "https://old.example", "https://new.example"),
            ("edition", "1", "2"),
            ("volume", "1", "2"),
            ("publisher", "Old Press", "New Press"),
        ):
            with self.subTest(field=field):
                old = f"@book{{k, title={{Kept}}, {field}={{{old_value}}}}}"
                new = f"@book{{k, title={{Kept}}, {field}={{{new_value}}}}}"
                left, right = bib.diff_bib_files(old, new, ["k"], ["k"])
                self.assertIn("userc = {moddel}", left)
                self.assertIn("userc = {modins}", right)
                self.assertIn(f"{field} = {{{old_value}}}", left)
                self.assertIn(f"{field} = {{{new_value}}}", right)
                self.assertNotIn(r"\bibdelcolor", left)
                self.assertNotIn(r"\bibinscolor", right)

    def test_changed_entry_type_gets_a_change_flag(self):
        left, right = bib.diff_bib_files("@book{k, title={Same}}", "@article{k, title={Same}}", ["k"], ["k"])
        self.assertIn("userc = {moddel}", left)
        self.assertIn("userc = {modins}", right)

    def test_added_and_removed_fields_flag_shared_entry(self):
        left, right = bib.diff_bib_files("@book{k, title={Same}, note={Old}}",
                                       "@book{k, title={Same}, titleaddon={New}}", ["k"], ["k"])
        self.assertIn(r"note = {{\bibdelcolor Old}}", left)
        self.assertIn(r"titleaddon = {{\bibinscolor New}}", right)
        self.assertIn("userc = {moddel}", left)
        self.assertIn("userc = {modins}", right)

    def test_missing_entry_on_one_cited_side_keeps_present_side(self):
        original = "@book{k, title={Same}}"
        left, right = bib.diff_bib_files(original, "", ["k"], ["k"])
        self.assertIn("userc = {del}", left)
        self.assertEqual(right, "")

    def test_source_metadata_is_not_duplicated_in_added_entries(self):
        original = "@book{k, title={Same}, keywords={source}, userc={source}}"
        left, right = bib.diff_bib_files("", original, [], ["k"])
        self.assertEqual(left, "")
        self.assertEqual(right.count("keywords ="), 1)
        self.assertEqual(right.count("userc ="), 1)
        self.assertIn("userc = {ins}", right)

    def test_citation_keys_include_page_arguments_and_lists(self):
        self.assertEqual(bib.extract_citation_keys(r"\parencite[9]{strube1928} \cite{a, b}"),
                         ["a", "b", "strube1928"])
        self.assertEqual(bib.extract_citation_keys(r"\parencite{a}", suffix="_v1"), ["a_v1"])

    def test_author_year_and_starred_citations_are_selected(self):
        self.assertEqual(bib.extract_citation_keys(r"\citeauthor{a} \citeyear{b} \cite*{c}"), ["a", "b", "c"])

    def test_wildcard_selects_each_versions_entries(self):
        old = "@book{kept, title={Same}}\n@book{gone, title={Old}}"
        new = "@book{kept, title={Same}}\n@book{added, title={New}}"
        self.assertEqual(bib.extract_citation_keys(r"\nocite{*}", suffix="_v1"), ["*"])
        left, right = bib.diff_bib_files(old, new, ["*"], ["*"])
        self.assertIn("@book{gone", left)
        self.assertIn("userc = {del}", left)
        self.assertIn("@book{added", right)
        self.assertIn("userc = {ins}", right)
        self.assertNotIn("@book{added", left)
        self.assertNotIn("@book{gone", right)


class BibliographyRowTests(unittest.TestCase):
    OLD = """@book{kept, author = {Strube, Gustav}, title = {Chords}, year = {1928}}
@inproceedings{gone, author = {Ke Chen and Shlomo Dubnov}, title = {Sketch}, year = {2020}}"""
    NEW = """@book{kept, author = {Strube, Gustav}, title = {Chords}, year = {1928}}
@article{added, author = {Huang, Cheng-Zhi Anna}, title = {Doodle}, year = {2019}}"""

    def test_rows_sort_by_family_name_and_leave_missing_sides_blank(self):
        rows = bib.bibliography_rows(self.OLD, self.NEW, ["kept", "gone"], ["kept", "added"])
        self.assertEqual(rows, [("gone", True, False), ("added", False, True), ("kept", True, True)])

    def test_each_row_prints_one_entry_per_side_in_a_synchronized_box(self):
        rows = bib.bibliography_rows(self.OLD, self.NEW, ["kept", "gone"], ["kept", "added"])
        rendered = bib.render_bibliography_rows(rows, ["kept_v1", "gone_v1"], ["kept", "added"])
        self.assertIn(r"\iffieldequalstr{entrykey}{gone_v1}", rendered)
        self.assertIn(r"\iffieldequalstr{entrykey}{added}", rendered)
        self.assertNotIn(r"{entrykey}{added_v1}", rendered)
        self.assertEqual(rendered.count(r"\printbibliography"), 4)
        self.assertEqual(rendered.count(r"\switchcolumn*"), 4)

    def test_wildcard_rows_nocite_only_resolved_side_entries(self):
        rows = bib.bibliography_rows(self.OLD, self.NEW, ["*"], ["*"])
        rendered = bib.render_bibliography_rows(rows, ["*"], ["*"])
        self.assertIn(r"\nocite{gone_v1, kept_v1}", rendered)
        self.assertIn(r"\nocite{added, kept}", rendered)
        self.assertNotIn("*", rendered.split(r"\begin{paracol}", 1)[0])


if __name__ == "__main__":
    unittest.main()
