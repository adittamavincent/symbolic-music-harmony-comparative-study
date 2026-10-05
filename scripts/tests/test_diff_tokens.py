"""Word-level highlighting of one compared pair of LaTeX texts."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diff_tokens as tokens  # noqa: E402


class WordHighlightTests(unittest.TestCase):
    def test_changed_citations_use_boxes_separate_from_text_highlights(self):
        old, new = tokens.word_level_render("Old text.", r"New \parencite{source} text.")
        self.assertIn(r"\diffinline{inshl}{\parencite{source}}", new)
        self.assertNotIn(r"\inhighlight{\parencite", new)

    def test_tex_space_escape_stays_outside_highlights(self):
        old, new = tokens.word_level_render("Old text.", "Fang et al.\\ \\parencite{source} text.")
        self.assertIn("al.\\ ", new)
        self.assertNotIn("al.\\}", new)

    def test_changed_tikz_picture_is_highlighted_as_one_block(self):
        picture = "\\begin{tikzpicture}\n\\node (%s) [process] {Step};\n\\end{tikzpicture}"
        old, new = tokens.word_level_render(picture % "start", picture % "dev")
        self.assertEqual(old, "\\begin{diffmath}{delhl}\n" + picture % "start" + "\n\\end{diffmath}\n")
        self.assertEqual(new, "\\begin{diffmath}{inshl}\n" + picture % "dev" + "\n\\end{diffmath}\n")
        old, new = tokens.word_level_render(picture % "start", "")
        self.assertEqual(new, "")

    def test_heading_format_change_highlights_only_the_formatted_phrase(self):
        old = r"\subsection{Evaluasi Otomatis dalam Music Information Retrieval (MIR)}"
        new = r"\subsection{Evaluasi Otomatis dalam \textit{Music Information Retrieval} (MIR)}"
        left, right = tokens.word_level_render(old, new)
        self.assertEqual(left, r"\subsection{Evaluasi Otomatis dalam \delhighlight{Music}\diffspace{delhl}\delhighlight{Information}\diffspace{delhl}\delhighlight{Retrieval} (MIR)}")
        self.assertEqual(right, r"\subsection{Evaluasi Otomatis dalam \textit{\inhighlight{Music}\diffspace{inshl}\inhighlight{Information}\diffspace{inshl}\inhighlight{Retrieval}} (MIR)}")
        for rendered in (left, right):
            self.assertNotIn(r"\renewcommand{\thesubsection}", rendered)
            self.assertNotIn(r"\colorbox", rendered)

    def test_heading_levels_starred_forms_and_optional_titles_keep_their_wrappers(self):
        for command in ("section", "subsection", "subsubsection"):
            for suffix in ("", "*", "[Short title]"):
                with self.subTest(command=command, suffix=suffix):
                    prefix = "\\" + command + suffix
                    old = prefix + "{Same plain wording}"
                    new = prefix + r"{Same \textit{plain} wording}"
                    left, right = tokens.word_level_render(old, new)
                    self.assertEqual(left, prefix + r"{Same \delhighlight{plain} wording}")
                    self.assertEqual(right, prefix + r"{Same \textit{\inhighlight{plain}} wording}")


class MathAndFormulaTests(unittest.TestCase):
    LEADING_FORMULA = r"""{\small
\begin{multline}
\text{Violation}_{\text{leading}}(t) = \mathds{1}\left(p_{i,t} \equiv L_{\text{pc}} \pmod{12}\right) \times \mathds{1}\left(p_{i,t+1} > p_{i,t}\right) \\
\times \mathds{1}\left(p_{i,t+1} \not\equiv K_{\text{tonic}} \pmod{12}\right) \\
\times \mathds{1}\left(\text{mode} \neq \text{natural minor} \lor L_{\text{pc}} \equiv (K_{\text{tonic}} - 1) \pmod{12}\right)
\end{multline}
}"""


    def test_added_multline_gets_a_block_background_and_preserves_the_formula(self):
        old, new = tokens.word_level_render("", self.LEADING_FORMULA)
        self.assertEqual(old, "")
        self.assertIn(r"\begin{diffmath}{inshl}", new)
        self.assertEqual(new.count(r"\begin{multline}"), 1)
        self.assertEqual(new.count(r"\end{multline}"), 1)
        self.assertIn(r"{\small", new)
        self.assertIn(r"\not\equiv K_{\text{tonic}}", new)
        self.assertEqual(new.count(r"\\"), self.LEADING_FORMULA.count(r"\\"))
        content = re.search(r'\\begin\{diffmath\}\{inshl\}\n(.*?)\n\\end\{diffmath\}', new, re.DOTALL).group(1)
        self.assertEqual(re.sub(r'\s+', ' ', content).strip(),
                         re.sub(r'\s+', ' ', self.LEADING_FORMULA).strip())
        self.assertNotIn(r"\inhighlight{", new)

    def test_deleted_multline_gets_red_and_leaves_the_other_side_empty(self):
        old, new = tokens.word_level_render(self.LEADING_FORMULA, "")
        self.assertIn(r"\begin{diffmath}{delhl}", old)
        self.assertEqual(new, "")

    def test_changed_formula_highlights_both_versions_and_unchanged_formula_does_not(self):
        revised = self.LEADING_FORMULA.replace(" > ", " < ")
        old, new = tokens.word_level_render(self.LEADING_FORMULA, revised)
        self.assertIn(r"\begin{diffmath}{delhl}", old)
        self.assertIn(r"\begin{diffmath}{inshl}", new)
        self.assertIn(" > ", old)
        self.assertIn(" < ", new)
        same_old, same_new = tokens.word_level_render(self.LEADING_FORMULA, self.LEADING_FORMULA)
        self.assertNotIn("diffmath", same_old)
        self.assertNotIn("diffmath", same_new)

    def test_display_environment_variants_and_alignment_tabs_remain_intact(self):
        for env, body in (("equation", "x = 1"), ("equation*", "x = 1"),
                          ("align", r"x &= 1 \\ y &= 2"), ("align*", r"x &= 1 \\ y &= 2"),
                          ("gather", r"x = 1 \\ y = 2"), ("multline*", r"x = 1 \\ + 2"),
                          ("alignat", r"{2} x &= 1 & y &= 2")):
            with self.subTest(env=env):
                source = rf"\begin{{{env}}}{body}\end{{{env}}}"
                _, rendered = tokens.word_level_render("", source)
                self.assertIn(r"\begin{diffmath}{inshl}", rendered)
                self.assertIn(body, rendered)
                self.assertIn(rf"\begin{{{env}}}", rendered)
                self.assertIn(rf"\end{{{env}}}", rendered)

    def test_bracket_display_math_is_highlighted_as_a_block(self):
        _, new = tokens.word_level_render("", r"\[x = 1\]")
        self.assertIn(r"\begin{diffmath}{inshl}", new)
        self.assertIn(r"\[x = 1\]", new)

    def test_highlighted_prose_leaves_spaces_breakable_including_inside_formatting(self):
        _, new = tokens.word_level_render("", r"Plain words \textit{Music \textbf{Information Retrieval}}.")
        self.assertIn(r"\inhighlight{Plain}\diffspace{inshl}\inhighlight{words}", new)
        self.assertIn(r"\textit{\inhighlight{Music}\diffspace{inshl}\textbf{\inhighlight{Information}\diffspace{inshl}\inhighlight{Retrieval}}}\inhighlight{.}", new)
        self.assertNotIn(r"\inhighlight{Plain words}", new)
        self.assertNotIn(r"\inhighlight{\textit", new)
        _, grouped = tokens.word_level_render("", "{Grouped words}")
        self.assertEqual(grouped.strip(), r"{\inhighlight{Grouped}\diffspace{inshl}\inhighlight{words}}")

    def test_adjacent_changes_connect_without_coloring_unchanged_neighbors(self):
        old, new = tokens.word_level_render("Stable old phrase stays.", "Stable new words stays.")
        self.assertEqual(old, r"Stable \delhighlight{old}\diffspace{delhl}\delhighlight{phrase} stays. ")
        self.assertEqual(new, r"Stable \inhighlight{new}\diffspace{inshl}\inhighlight{words} stays. ")
        _, single = tokens.word_level_render("Stable old stays.", "Stable new stays.")
        self.assertNotIn(r"\diffspace", single)

    def test_soft_source_lines_connect_but_paragraph_boundaries_do_not(self):
        _, new = tokens.word_level_render("", "First line\nsecond line.\n\nNext paragraph.")
        self.assertIn("\\inhighlight{line}\\diffspace{inshl}%\n\\inhighlight{second}", new)
        self.assertIn("\\inhighlight{line.} \n\n\\inhighlight{Next}", new)

    def test_parentheses_and_punctuation_are_inside_highlights_including_math_and_citations(self):
        phrase = r"(\textit{orderless NADE})"
        old, new = tokens.word_level_render(phrase, "")
        self.assertEqual(new, "")
        self.assertEqual(old.strip(), r"\delhighlight{(}\textit{\delhighlight{orderless}\diffspace{delhl}\delhighlight{NADE}}\delhighlight{)}")
        _, new = tokens.word_level_render("", phrase + ",")
        self.assertIn(r"\inhighlight{(}", new)
        self.assertTrue(new.endswith(r"\inhighlight{),} "))
        _, math = tokens.word_level_render("", "($x = 1$).")
        self.assertIn(r"\diffinline{inshl}{(\ensuremath{x = 1}).}", math)
        _, compact_math = tokens.word_level_render("", "($x$),")
        self.assertEqual(compact_math.strip(), r"\diffinline{inshl}{(\ensuremath{x}),}")
        same, _ = tokens.word_level_render("($x$),", "($x$),")
        self.assertEqual(same.strip(), "($x$),")
        _, cite = tokens.word_level_render("", r"(\parencite{source}),")
        self.assertIn(r"\diffinline{inshl}{(\parencite{source}),}", cite)

    def test_adjacent_inline_formulas_keep_separate_math_boxes(self):
        _, new = tokens.word_level_render("", "$x = 1$ $y = 2$")
        self.assertEqual(new.count(r"\diffinline{inshl}"), 2)
        self.assertIn(r"\ensuremath{x = 1}", new)
        self.assertIn(r"\ensuremath{y = 2}", new)


class ProseTokenTests(unittest.TestCase):
    def test_changed_font_size_and_family_are_visible_changes(self):
        for old, new in ((r"{\small ukuran}", r"{\large ukuran}"),
                         (r"\textsf{huruf}", r"\textrm{huruf}"),
                         (r"{\sffamily huruf}", r"{\rmfamily huruf}")):
            with self.subTest(old=old, new=new):
                left, right = tokens.word_level_render(old, new)
                self.assertIn(r"\delhighlight", left)
                self.assertIn(r"\inhighlight", right)
                self.assertNotIn("highlight{\\", left + right)
        left, right = tokens.word_level_render(r"{\normalsize\textrm{Same}}", "Same")
        self.assertNotIn("highlight", left + right)

    def test_words_inside_formatting_compare_one_by_one(self):
        old, new = tokens.word_level_render(r"Mengukur \textit{constraint adherence} ketiga",
                                            r"Mengukur \textit{constraint compliance} kedua")
        self.assertIn(r"\textit{constraint \delhighlight{adherence}}", old)
        self.assertIn(r"\textit{constraint \inhighlight{compliance}}", new)
        self.assertTrue(old.startswith("Mengukur "))

    def test_same_visible_style_is_not_a_change(self):
        old, new = tokens.word_level_render(r"\underline{\textbf{Veronica Yoni}}\par",
                                            r"\textbf{\uline{Veronica Yoni}}\par")
        self.assertNotIn("highlight", old + new)

    def test_font_switch_groups_and_line_breaks_compare_word_by_word(self):
        old, new = tokens.word_level_render(r"{\fontsize{16pt}{19.2pt}\selectfont EVALUASI AKURASI\\ HARMONI\par}",
                                            r"{\fontsize{14pt}{16pt}\selectfont EVALUASI MUSIK\\ HARMONI\par}")
        self.assertIn(r"\selectfont EVALUASI \delhighlight{AKURASI}", old)
        self.assertIn(r"\selectfont EVALUASI \inhighlight{MUSIK}", new)
        for rendered in (old, new):
            self.assertIn("HARMONI", rendered)
            self.assertNotIn(r"highlight{HARMONI}", rendered)
            self.assertNotIn(r"highlight{\\", rendered)
            # Leaders never reach across a line break.
            self.assertNotRegex(rendered, r"diffspace\{[a-z]+\}\\\\")

    def test_ulem_underlines_get_no_leaders(self):
        old, new = tokens.word_level_render(r"\textbf{\uline{Old Name}}", r"\textbf{\uline{New Title}}")
        self.assertIn(r"\uline{\delhighlight{Old} \delhighlight{Name}}", old)
        self.assertNotIn(r"\diffspace", old + new)

    def test_pale_tone_marks_text_without_counterpart(self):
        old, new = tokens.word_level_render("Removed words", "", "pale")
        self.assertEqual(old, r"\delpale{Removed}\diffspace{delpl}\delpale{words} ")
        self.assertEqual(new, "")

    def test_line_breaks_do_not_hide_the_word_before_them(self):
        old, new = tokens.word_level_render("Old line\\\\", "New line\\par")
        self.assertIn(r"\delhighlight{Old}", old)
        self.assertIn(r"\inhighlight{New}", new)
        self.assertNotIn(r"highlight{line", old + new)

    def test_render_group_keeps_shared_words_when_a_line_is_split(self):
        old, new = tokens.render_group(["JURUSAN MUSIK FAKULTAS SENI\\\\"],
                                       ["JURUSAN MUSIK\\par", "FAKULTAS SENI\\par"])
        self.assertEqual(len(old), 1)
        self.assertEqual(len(new), 2)
        self.assertNotIn("highlight", "".join(old + new))

    def test_citation_page_arguments_stay_whole_and_outside_soul(self):
        words = [value for kind, value in tokens.tokenize_words(r"kuint \parencite[9, 12]{strube1928}: lalu")
                 if kind == "W"]
        self.assertIn(r"\parencite[9, 12]{strube1928}:", words)
        _, new = tokens.word_level_render("", r"kuint \parencite[35]{strube1928}: lalu")
        self.assertIn(r"\diffinline{inshl}{\parencite[35]{strube1928}:}", new)
        self.assertNotIn(r"\inhighlight{\parencite", new)


class ObjectHighlightTests(unittest.TestCase):
    def test_added_research_flow_caption_is_flagged_without_changing_its_counter(self):
        source = r"\caption{Rancangan Alur Penelitian}"
        left, right = tokens.word_level_render("", source, "pale")
        self.assertEqual(left, "")
        self.assertEqual(right.strip(), r"\caption{\inspale{Rancangan}\diffspace{inspl}\inspale{Alur}\diffspace{inspl}\inspale{Penelitian}}")
        self.assertEqual(right.count(r"\caption{"), 1)
        self.assertNotIn("renewcommand", right)
        self.assertNotIn("fcolorbox", right)

    def test_caption_content_compares_nested_words_math_and_citations(self):
        old = r"\caption[Short title]{Rancangan \textit{Alur Penelitian} $x$ \parencite[9, 12]{source}}"
        new = old.replace("Penelitian", "Analisis").replace("$x$", "$y$").replace("source}", "revised}")
        left, right = tokens.word_level_render(old, new)
        self.assertIn(r"\caption[Short title]{Rancangan \textit{Alur \delhighlight{Penelitian}}", left)
        self.assertIn(r"\caption[Short title]{Rancangan \textit{Alur \inhighlight{Analisis}}", right)
        self.assertIn(r"\diffinline{inshl}{\ensuremath{y}}", right)
        self.assertIn(r"\diffinline{inshl}{\parencite[9, 12]{revised}}", right)
        self.assertNotIn(r"highlight{Rancangan}", left + right)
        self.assertNotIn(r"highlight{Alur}", left + right)
        self.assertNotIn(r"highlight{\parencite", left + right)

    def test_starred_and_captionof_wrappers_keep_their_native_arguments(self):
        for prefix in (r"\caption*", r"\caption*[Short {nested title}]",
                       r"\captionof{figure}", r"\captionof{table}[Short title]"):
            with self.subTest(prefix=prefix):
                left, right = tokens.word_level_render(prefix + "{Same old label}", prefix + "{Same new label}")
                self.assertEqual(left.strip(), prefix + r"{Same \delhighlight{old} label}")
                self.assertEqual(right.strip(), prefix + r"{Same \inhighlight{new} label}")

    def test_changed_short_caption_and_hyperlink_target_also_flag_the_displayed_text(self):
        for old, new in ((r"\caption[Old title]{Same caption}", r"\caption[New title]{Same caption}"),
                         (r"\href{https://old.example/a_b}{Same label}", r"\href{https://new.example/a_b}{Same label}"),
                         (r"\hyperref[old]{Same label}", r"\hyperref[new]{Same label}")):
            with self.subTest(old=old):
                left, right = tokens.word_level_render(old, new)
                self.assertIn(r"\delhighlight{Same}", left)
                self.assertIn(r"\inhighlight{Same}", right)
                self.assertNotIn(r"\diffinline", left + right)

    def test_reference_targets_and_urls_are_highlighted_as_safe_whole_commands(self):
        for command in ("ref", "ref*", "pageref", "eqref", "autoref", "nameref", "cref", "Cref", "url", "nolinkurl"):
            with self.subTest(command=command):
                old = "\\" + command + "{old_target}"
                new = "\\" + command + "{new_target}"
                left, right = tokens.word_level_render(old, new)
                self.assertEqual(left.strip(), r"\diffinline{delhl}{" + old + "}")
                self.assertEqual(right.strip(), r"\diffinline{inshl}{" + new + "}")

    def test_footnote_body_is_highlighted_inside_its_command(self):
        left, right = tokens.word_level_render(r"\footnote[2]{An old \textit{note text}.}",
                                               r"\footnote[2]{An new \textit{note text}.}")
        self.assertEqual(left.strip(), r"\footnote[2]{An \delhighlight{old} \textit{note text}.}")
        self.assertEqual(right.strip(), r"\footnote[2]{An \inhighlight{new} \textit{note text}.}")
        self.assertNotIn("diffinline", left + right)

    def test_attached_footnote_and_nested_link_compare_without_a_space_before_the_superscript(self):
        old = r"Old prose note\footnote{Footnote with \href{https://example.com}{old link}.}"
        new = r"New prose note\footnote{Footnote with \href{https://example.com}{new link}.}"
        left, right = tokens.word_level_render(old, new)
        self.assertIn(r"\delhighlight{Old}", left)
        self.assertIn(r"\inhighlight{New}", right)
        self.assertIn(r"note\footnote{Footnote with \href{https://example.com}{\delhighlight{old} link}.}", left)
        self.assertIn(r"note\footnote{Footnote with \href{https://example.com}{\inhighlight{new} link}.}", right)
        self.assertNotIn(r"note \footnote", left + right)
        self.assertNotIn("fcolorbox", left + right)

    def test_attached_link_and_reference_commands_keep_their_adjacent_text(self):
        left, right = tokens.word_level_render(r"See\href{https://example.com}{old label},Figure\ref{old}.",
                                               r"See\href{https://example.com}{new label},Figure\ref{new}.")
        self.assertIn(r"See\href{https://example.com}{\delhighlight{old} label},Figure\diffinline{delhl}{\ref{old}}.", left)
        self.assertIn(r"See\href{https://example.com}{\inhighlight{new} label},Figure\diffinline{inshl}{\ref{new}}.", right)

    def test_changed_graphic_path_and_options_get_a_visible_frame_without_touching_the_syntax(self):
        graphic = r"\includegraphics[width=\textwidth, trim={1pt 2pt 3pt 4pt},clip]{figures/my_image.pdf}"
        revised = graphic.replace("my_image.pdf", "new_image.pdf")
        left, right = tokens.word_level_render(graphic, revised)
        self.assertIn(r"\fcolorbox{delhl}{delhl}{" + graphic + "}", left)
        self.assertIn(r"\fcolorbox{inshl}{inshl}{" + revised + "}", right)
        self.assertNotIn(r"highlight{my_image", left)
        unchanged = tokens.word_level_render(graphic, graphic)
        self.assertEqual(unchanged, (graphic, graphic))
        _, added = tokens.word_level_render("", graphic + ".", "pale")
        self.assertIn(r"\fcolorbox{inspl}{inspl}{" + graphic + ".}", added)

    def test_caption_after_same_line_graphic_compares_without_flagging_the_unchanged_image(self):
        graphic = r"\includegraphics[width=\linewidth]{same_image.pdf}"
        old = graphic + r"\caption{Same old caption}"
        new = graphic + r"\caption{Same new caption}"
        left, right = tokens.word_level_render(old, new)
        self.assertIn(graphic, left)
        self.assertIn(graphic, right)
        self.assertIn(r"\caption{Same \delhighlight{old} caption}", left)
        self.assertIn(r"\caption{Same \inhighlight{new} caption}", right)
        self.assertNotIn("fcolorbox", left + right)

    def test_changed_table_commands_and_verbatim_text_keep_whole_source_blocks(self):
        for old, new in ((r"\begin{tabular}{ll} A & B \\ \hline \end{tabular}",
                         r"\begin{tabular}{ll} A & B \\ \cline{1-2} \end{tabular}"),
                        ("\\begin{verbatim}\npath old_image\n\\end{verbatim}",
                         "\\begin{verbatim}\npath new_image\n\\end{verbatim}"),
                        ("\\begin{verbatim}\n  indentation\n\\end{verbatim}",
                         "\\begin{verbatim}\n    indentation\n\\end{verbatim}")):
            with self.subTest(old=old):
                left, right = tokens.word_level_render(old, new)
                self.assertEqual(left, "\\begin{diffmath}{delhl}\n" + old + "\n\\end{diffmath}\n")
                self.assertEqual(right, "\\begin{diffmath}{inshl}\n" + new + "\n\\end{diffmath}\n")
                self.assertNotIn("highlight", left + right)


if __name__ == "__main__":
    unittest.main()
