"""Visible object changes and reference values, beyond paragraph wording."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from diff_layout import Comparison, parse_blocks, split_fragments  # noqa: E402
from sidebydiff import strip_comments  # noqa: E402


def manuscript(*parts):
    return r'\section{Discussion}' + '\n\n' + '\n\n'.join(parts)


class ObjectRegressionTests(unittest.TestCase):
    def test_moved_section_children_remain_unchanged(self):
        first = r'\section{First}' + '\nUnique starting paragraph.'
        moved = r'\section{Moved}' + '\nUnique moved paragraph remains unchanged.'
        last = r'\section{Last}' + '\nUnique closing paragraph remains unchanged.'
        comparison = Comparison(first + '\n' + moved + '\n' + last, first + '\n' + last + '\n' + moved)
        self.assertTrue(comparison.moved)
        self.assertNotRegex(comparison.render(), r'\\begin\{diffmath\}|\\(?:delpale|inspale)')
        self.assertTrue(all(e[2] in ('sama', 'dipindahkan, sama') for e in comparison.change_map()))

    def test_equation_insertion_flags_stable_references(self):
        equation = r'\begin{equation}a=b\label{eq:x}\end{equation}'
        reference = r'Lihat Persamaan~\eqref{eq:x}.'
        comparison = Comparison(manuscript(equation, reference),
                                manuscript(r'\begin{equation}x=y\end{equation}', equation, reference))
        self.assertEqual(comparison.reference_numbers['old']['eq:x'], ('equation', 1))
        self.assertEqual(comparison.reference_numbers['new']['eq:x'], ('equation', 2))
        for color in ('delhl', 'inshl'):
            self.assertIn(rf'\diffinline{{{color}}}{{\eqref{{eq:x}}}}', comparison.render())
            self.assertIn(rf'\diffequationlabel{{{color}}}', comparison.render())

    def test_pure_word_insertion_keeps_the_old_paragraph_plain(self):
        old = 'Alpha paragraph about output.'
        comparison = Comparison(manuscript(old), manuscript('Alpha paragraph about generated output.'))
        index = next(i for i, b in enumerate(comparison.old) if b.kind == 'chunk')
        self.assertEqual(comparison.render_block('old', index), old)
        self.assertIn(r'\inhighlight{generated}', comparison.render())

    def test_align_ignores_nested_matrix_rows_and_notag(self):
        source = manuscript(r'''\begin{align}
a&=\begin{matrix}1&2\\3&4\end{matrix}\label{eq:a}\\
b&=2\notag\\
c&=3\label{eq:c}
\end{align}''')
        comparison = Comparison(source, source)
        self.assertEqual(comparison.reference_numbers['old']['eq:a'], ('equation', 1))
        self.assertEqual(comparison.reference_numbers['old']['eq:c'], ('equation', 2))

    def test_changed_heading_title_flags_stable_nameref(self):
        old = r'\section{Old Title}\label{sec:x}' + '\n' + r'Lihat \nameref{sec:x}.'
        body = Comparison(old, old.replace('Old Title', 'New Title')).render()
        for color in ('delhl', 'inshl'):
            self.assertIn(rf'\diffinline{{{color}}}{{\nameref{{sec:x}}}}', body)

    def test_display_math_and_line_graphics_split_without_blank_lines(self):
        for obj in (r'\[1+2=3\]', r'\includegraphics{image.png}'):
            with self.subTest(obj=obj):
                new = r'\section{Discussion}' + '\nBefore paragraph.\n' + obj + '\nAfter paragraph.'
                comparison = Comparison(manuscript('Before paragraph.', 'After paragraph.'), new)
                row = next(r for r in comparison.rows if any(comparison.new[i].text == obj for i in r.new))
                self.assertFalse(row.old)
                self.assertEqual([comparison.new[i].text for i in row.new], [obj])

    def test_literal_braces_and_commands_preserve_scope_and_comments(self):
        for env in ('verbatim', 'lstlisting', 'minted'):
            with self.subTest(env=env):
                block = rf'\begin{{{env}}}' + '\n{ literal 50% \\section{example}\n' + rf'\end{{{env}}}'
                self.assertEqual(strip_comments(block), block)
                chunks = [b.text for b in parse_blocks(manuscript(block, 'After paragraph.', 'Later paragraph.'))
                          if b.kind == 'chunk']
                self.assertEqual(chunks, [block, 'After paragraph.', 'Later paragraph.'])
                self.assertEqual(''.join(f.core + f.tail for f in split_fragments(block)), block)
        self.assertEqual(strip_comments(r'\verb|50%| % removed' + '\nmore'), r'\verb|50%| more')

    def test_rule_without_words_is_flagged(self):
        body = Comparison(manuscript('Paragraph.'), manuscript('Paragraph.', r'\rule{1cm}{1cm}')).render()
        self.assertIn(r'\begin{diffmath}{inspl}', body)

    def test_map_lists_new_and_renumbered_figures(self):
        figure = r'\begin{figure}\includegraphics{x.png}\caption{Existing}\label{fig:x}\end{figure}'
        added = r'\begin{figure}\includegraphics{y.png}\caption{Added}\label{fig:y}\end{figure}'
        entries = Comparison(manuscript(figure), manuscript(added, figure)).change_map()
        self.assertIn(('', 'Gambar 1: Added', 'baru', None), entries)
        entry = next(e for e in entries if e[0] == 'Gambar 1: Existing')
        self.assertEqual(entry[1], 'Gambar 2: Existing')
        self.assertNotEqual(entry[2], 'sama')


if __name__ == '__main__':
    unittest.main()
