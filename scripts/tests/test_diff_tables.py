"""Tables compare as a whole, then by row, then by cell, then by word."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diff_layout as layout  # noqa: E402
import diff_tables as tables  # noqa: E402
import diff_tokens as tokens  # noqa: E402


def table(*rows, spec="|l|l|"):
    return "\n".join((rf"\begin{{tabular}}{{{spec}}}", r"\hline",
                      *(row + r" \\ \hline" for row in rows), r"\end{tabular}"))


class TableHighlightTests(unittest.TestCase):
    def test_changed_cell_highlights_only_its_changed_words(self):
        old = table("Kaidah & Bobot", "Kuint sejajar & satu", "Oktaf sejajar & satu")
        new = table("Kaidah & Bobot", "Kuint sejajar & dua", "Oktaf sejajar & satu")
        left, right = tokens.word_level_render(old, new)
        self.assertIn(r"Kuint sejajar & \delhighlight{satu} \\", left)
        self.assertIn(r"Kuint sejajar & \inhighlight{dua} \\", right)
        self.assertIn(r"Oktaf sejajar & satu \\", left)
        self.assertNotIn("diffmath", left + right)
        self.assertNotIn(r"\diffrow", left + right)
        self.assertNotIn(r"\diffcell", left + right)

    def test_row_without_counterpart_gets_a_pale_row_color(self):
        old = table("Kaidah & Bobot", "Kuint sejajar & 1")
        new = table("Kaidah & Bobot", "Kuint sejajar & 1", "Persilangan & 0,5")
        left, right = tokens.word_level_render(old, new)
        self.assertEqual(left, old)
        self.assertIn(r"\hline\diffrow{inspl}" + "\nPersilangan & 0,5 \\\\", right)
        self.assertEqual(right.count(r"\diffrow"), 1)
        left, right = tokens.word_level_render(new, old)
        self.assertIn(r"\diffrow{delpl}" + "\nPersilangan & 0,5 \\\\", left)
        self.assertEqual(right, old)

    def test_rewritten_row_at_the_same_place_has_no_counterpart(self):
        old = table("Kaidah & Bobot", "Kuint sejajar & 1")
        new = table("Kaidah & Bobot", "Persilangan & 0,5")
        left, right = tokens.word_level_render(old, new)
        self.assertIn(r"\diffrow{delpl}" + "\nKuint sejajar & 1", left)
        self.assertIn(r"\diffrow{inspl}" + "\nPersilangan & 0,5", right)

    def test_changed_rule_colors_only_that_rule(self):
        old = r"\begin{tabular}{ll} A & B \\ \hline \end{tabular}"
        new = r"\begin{tabular}{ll} A & B \\ \cline{1-2} \end{tabular}"
        left, right = tokens.word_level_render(old, new)
        self.assertEqual(left, r"\begin{tabular}{ll} A & B \\\diffrule{deltext}{ \hline} \end{tabular}")
        self.assertEqual(right, r"\begin{tabular}{ll} A & B \\\diffrule{instext}{ \cline{1-2}} \end{tabular}")

    def test_changed_column_layout_marks_the_whole_table(self):
        old, new = table("A & B"), table("A & C", spec="|l|c|")
        left, right = tokens.word_level_render(old, new)
        self.assertEqual(left, "\\begin{diffmath}{delhl}\n" + old + "\n\\end{diffmath}\n")
        self.assertEqual(right, "\\begin{diffmath}{inshl}\n" + new + "\n\\end{diffmath}\n")

    def test_cell_change_without_highlightable_words_colors_the_cell(self):
        old = table(r"A & \makecell{satu\\dua}")
        new = table(r"A & \makecell{satu\\tiga}")
        left, right = tokens.word_level_render(old, new)
        self.assertIn(r"A & \diffcell{delhl}\makecell{satu\\dua} \\", left)
        self.assertIn(r"A & \diffcell{inshl}\makecell{satu\\tiga} \\", right)
        self.assertNotIn(r"\diffrow", left + right)

    def test_row_spacing_change_colors_the_row(self):
        old = r"\begin{tabular}{ll} A & B \\ C & D \\ \end{tabular}"
        new = r"\begin{tabular}{ll} A & B \\[4pt] C & D \\ \end{tabular}"
        left, right = tokens.word_level_render(old, new)
        self.assertEqual(left, r"\begin{tabular}{ll}\diffrow{delhl} A & B \\ C & D \\ \end{tabular}")
        self.assertEqual(right, r"\begin{tabular}{ll}\diffrow{inshl} A & B \\[4pt] C & D \\ \end{tabular}")

    def test_multicolumn_compares_its_content_and_colors_a_changed_span(self):
        old = table(r"\multicolumn{2}{|c|}{Ringkasan lama}", "A & B")
        new = table(r"\multicolumn{2}{|c|}{Ringkasan baru}", "A & B")
        left, right = tokens.word_level_render(old, new)
        self.assertIn(r"\multicolumn{2}{|c|}{Ringkasan \delhighlight{lama}}", left)
        self.assertIn(r"\multicolumn{2}{|c|}{Ringkasan \inhighlight{baru}}", right)
        new = table(r"\multicolumn{1}{|c|}{Ringkasan lama} & B", "A & B")
        left, right = tokens.word_level_render(old, new)
        self.assertIn(r"\multicolumn{2}{|c|}{\diffcell{delhl}Ringkasan lama}", left)
        # The second cell of the narrower span has no counterpart.
        self.assertIn(r"\multicolumn{1}{|c|}{\diffcell{inshl}Ringkasan lama} & \diffcell{inspl}B \\", right)

    def test_rows_and_cells_split_only_at_top_level_separators(self):
        parts = tables.table_parts(r"\begin{tabular}{ll} R\&D & \makecell{a\\b} \\ \hline"
                                   r" \begin{tabular}{c} x \\ y \end{tabular} & z \\[2pt] \end{tabular}")
        self.assertEqual([row.cells for row in parts.rows],
                         [[r" R\&D ", r" \makecell{a\\b} "],
                          [r" \begin{tabular}{c} x \\ y \end{tabular} ", " z "], [" "]])
        self.assertEqual([row.rules for row in parts.rows], ["", r" \hline", ""])
        self.assertEqual([row.end for row in parts.rows], [r"\\", r"\\[2pt]", ""])

    def test_unchanged_table_keeps_its_source(self):
        source = table("A & B")
        self.assertEqual(tokens.word_level_render(source, source.replace("\n", "  \n")),
                         (source, source.replace("\n", "  \n")))

    def test_table_in_a_manuscript_keeps_its_rules_and_marks_one_row(self):
        def manuscript(value):
            return "\n".join((r"\section{T}", "Teks.", "", r"\begin{table}[ht]", r"\centering",
                              r"\begin{tabularx}{\textwidth}{|l|X|}", r"\hline",
                              r"Kaidah & Bobot \\ \hline", rf"Kuint sejajar & {value} \\ \hline",
                              r"\end{tabularx}", r"\caption{Kaidah}", r"\label{tab:kaidah}", r"\end{table}"))
        rendered = layout.Comparison(manuscript("satu"), manuscript("dua")).render()
        self.assertNotIn("diffmath", rendered)
        self.assertIn(r"Kuint sejajar & \delhighlight{satu} \\ \hline", rendered)
        self.assertIn(r"Kuint sejajar & \inhighlight{dua} \\ \hline", rendered)
        self.assertIn(r"Kaidah & Bobot \\ \hline", rendered)
        self.assertEqual(rendered.count(r"\diffcaptionlabel{table}"), 2)
        self.assertIn(r"\penalty0" + "\n" + r"\diffcaptionlabel{table}{delhl}", rendered)


if __name__ == "__main__":
    unittest.main()
