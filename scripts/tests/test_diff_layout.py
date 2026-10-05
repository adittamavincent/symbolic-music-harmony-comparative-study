"""Keep paragraph/object alignment and change flags independent of TeX compilation."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diff_layout as layout  # noqa: E402


def anchor_pairs(comparison):
    """(old title, new title) for every page and heading, in reading order."""
    pairs = []
    for op in comparison.operations():
        if op[0] != "pair":
            continue
        _, i, j = op
        block = comparison.old[i] if i is not None else comparison.new[j]
        if block.kind in ("page", "heading"):
            pairs.append((comparison.old[i].text if i is not None else None,
                          comparison.new[j].text if j is not None else None))
    return pairs


def rows_text(comparison):
    """Rendered (left, right) column text of every row."""
    body = comparison.render()
    left = re.findall(r'\\begin\{leftside\}\n(.*?)\n\\par\\end\{leftside\}', body, re.DOTALL)
    right = re.findall(r'\\begin\{rightside\}\n(.*?)\n\\par\\end\{rightside\}', body, re.DOTALL)
    return list(zip(left, right))


def page(title, body):
    return r"\phantomsection" + "\n" + rf"\addcontentsline{{toc}}{{matter}}{{{title}}}" + "\n" + body


def manuscript(*paragraphs):
    """A body section with real paragraph breaks, rather than literal slash-n."""
    return r"\section{Pembahasan}" + "\n\n" + "\n\n".join(paragraphs)


def chunk_pairs(comparison):
    """Paragraph/object source pairs, including the blank side of an insertion."""
    return [(comparison.old[i].text if i is not None else None,
             comparison.new[j].text if j is not None else None)
            for i, j in comparison.pairs
            if (comparison.old[i] if i is not None else comparison.new[j]).kind == "chunk"]


class BlockTests(unittest.TestCase):
    def test_blocks_keep_headings_paragraphs_breaks_and_heading_ids(self):
        blocks = layout.parse_blocks("\n".join((
            r"\section{Latar Belakang}\label{sec:latar-belakang}", "",
            "First paragraph.", "", "Second paragraph.",
            r"\newpage",
            r"\subsection{Rumusan Masalah}", "Body.",
        )))
        self.assertEqual([block.kind for block in blocks],
                         ["heading", "chunk", "chunk", "break", "heading", "chunk"])
        self.assertEqual(blocks[0].key, "latar-belakang")
        self.assertEqual(blocks[4].key, "rumusan-masalah")  # title slug when there is no label
        self.assertEqual((blocks[0].level, blocks[4].level), (1, 2))
        self.assertEqual(blocks[1].owner, 0)
        self.assertEqual(blocks[5].owner, 4)

    def test_explicit_paragraph_commands_split_body_paragraphs(self):
        source = r"\section{Pembahasan}" + "\n" + r"Alpha paragraph.\par Beta paragraph.\par Gamma paragraph."
        blocks = layout.parse_blocks(source)
        self.assertEqual([block.text for block in blocks if block.kind == "chunk"],
                         ["Alpha paragraph.", "Beta paragraph.", "Gamma paragraph."])

    def test_standalone_objects_without_blank_lines_are_separate_body_rows(self):
        objects = {
            "figure": r"\begin{figure}\includegraphics{flow.pdf}\caption{Rancangan Alur Penelitian}\end{figure}",
            "list": r"\begin{enumerate}\item Pertama.\item Kedua.\end{enumerate}",
            "equation": r"\begin{equation}1+2=3\end{equation}",
            "table": r"\begin{table}\begin{tabular}{ll}A & B\\\end{tabular}\end{table}",
        }
        for kind, object_source in objects.items():
            with self.subTest(kind=kind):
                source = r"\section{Pembahasan}" + "\nBefore paragraph.\n" + object_source + "\nAfter paragraph."
                chunks = [block.text for block in layout.parse_blocks(source) if block.kind == "chunk"]
                self.assertEqual(chunks, ["Before paragraph.", object_source, "After paragraph."])
                comparison = layout.Comparison(source, source)
                self.assertEqual(len(comparison.rows), 4)
                self.assertTrue(all(len(row.old) == len(row.new) == 1 for row in comparison.rows))

    def test_chapter_headings_and_environments_stay_whole(self):
        blocks = layout.parse_blocks("\n".join((
            r"\thesischapter{II}{TINJAUAN PUSTAKA}",
            r"\section*{Pengantar}",
            r"\begin{enumerate}", r"\item One.", "", r"\item Two.", r"\end{enumerate}",
        )))
        self.assertEqual([block.kind for block in blocks], ["heading", "heading", "chunk"])
        self.assertEqual(blocks[0].prefix, r"\thesischapter{II}")
        self.assertEqual(blocks[0].level, 0)
        self.assertFalse(blocks[1].numbered)
        self.assertEqual(blocks[2].items, 2)

    def test_frontmatter_pages_take_their_role_from_contents_entries_or_wording(self):
        blocks = layout.parse_blocks("\n\\newpage\n".join((
            r"\begingroup PROPOSAL SKRIPSI \endgroup",
            page("HALAMAN PERNYATAAN", "Saya menyatakan."),
            r"\begin{center}HALAMAN PENGESAHAN\end{center}" + "\nApproval.",
            r"\section{Latar Belakang}",
        )))
        pages = [block for block in blocks if block.kind == "page"]
        self.assertEqual([p.key for p in pages], ["cover", "pernyataan", "approval"])
        self.assertEqual(pages[1].text, "HALAMAN PERNYATAAN")
        chunks = [block.text for block in blocks if block.kind == "chunk"]
        self.assertNotIn(r"\addcontentsline", "".join(chunks))
        self.assertNotIn(r"\phantomsection", "".join(chunks))

    def test_sentences_list_items_and_lines_split_without_breaking_markup(self):
        text = (r"Kalimat satu (Strube, 1928). Huang et al.\ (2019) menemukan pola. "
                r"\textit{Kalimat. Dalam} grup.\par Baris\\ dua" + "\n"
                r"\begin{enumerate}" + "\n" + r"\item Satu." + "\n" + r"\item Dua." + "\n" + r"\end{enumerate}")
        fragments = layout.split_fragments(text)
        cores = [fragment.core for fragment in fragments]
        self.assertEqual("".join(fragment.core + fragment.tail for fragment in fragments), text)
        self.assertIn("Kalimat satu (Strube, 1928).", cores)
        self.assertIn(r"Huang et al.\ (2019) menemukan pola.", cores)
        self.assertIn(r"\textit{Kalimat. Dalam} grup.\par", cores)
        self.assertIn(r"Baris\\", cores)
        self.assertIn(r"\item Satu.", cores)
        self.assertIn(r"\begin{enumerate}", cores)


class PairingTests(unittest.TestCase):
    def test_inserted_paragraph_leaves_a_blank_left_row_without_shifting_later_pairs(self):
        a, b, c = "Alpha opening paragraph.", "Beta body paragraph.", "Gamma closing paragraph."
        d = "Delta inserted paragraph."
        comparison = layout.Comparison(manuscript(a, b, c), manuscript(a, d, b, c))
        self.assertEqual(chunk_pairs(comparison), [(a, a), (None, d), (b, b), (c, c)])
        self.assertEqual(len(comparison.rows), 5)
        rows = rows_text(comparison)
        self.assertEqual(rows[2][0], "")
        self.assertIn(r"\inspale{Delta}", rows[2][1])
        self.assertEqual(rows[3], (b, b))
        self.assertEqual(rows[4], (c, c))

    def test_deleted_paragraph_leaves_a_blank_right_row_without_shifting_later_pairs(self):
        a, b, c = "Alpha opening paragraph.", "Beta body paragraph.", "Gamma closing paragraph."
        d = "Delta deleted paragraph."
        comparison = layout.Comparison(manuscript(a, d, b, c), manuscript(a, b, c))
        self.assertEqual(chunk_pairs(comparison), [(a, a), (d, None), (b, b), (c, c)])
        rows = rows_text(comparison)
        self.assertEqual(rows[2][1], "")
        self.assertIn(r"\delpale{Delta}", rows[2][0])
        self.assertEqual(rows[3], (b, b))
        self.assertEqual(rows[4], (c, c))

    def test_similar_edited_paragraphs_share_a_row_and_mark_only_changed_words(self):
        old = "Model menyusun nada dan mengisi suara bawah secara bertahap."
        new = "Model menyusun nada dan mengisi suara bawah secara serentak."
        closing = "Evaluasi mencatat pelanggaran pada setiap keluaran."
        comparison = layout.Comparison(manuscript(old, closing), manuscript(new, closing))
        self.assertEqual(chunk_pairs(comparison), [(old, new), (closing, closing)])
        left, right = rows_text(comparison)[1]
        self.assertIn(r"\delhighlight{bertahap.}", left)
        self.assertIn(r"\inhighlight{serentak.}", right)
        self.assertNotRegex(left + right, r"(?:highlight|pale)\{(?:Model|suara|bawah)\}")

    def test_exact_paragraph_anchors_survive_a_near_identical_insertion(self):
        a = "Tahap pertama mencatat keluaran model dan menghitung pelanggaran."
        b = "Tahap kedua mencatat keluaran model dan menghitung pelanggaran."
        c = "Tahap ketiga mencatat keluaran model dan menghitung pelanggaran."
        inserted = "Tahap tambahan mencatat keluaran model dan menghitung pelanggaran."
        comparison = layout.Comparison(manuscript(a, b, c), manuscript(a, inserted, b, c))
        self.assertEqual(chunk_pairs(comparison), [(a, a), (None, inserted), (b, b), (c, c)])
        self.assertEqual(rows_text(comparison)[2][0], "")

    def test_repeated_paragraphs_keep_the_insertion_between_the_correct_occurrences(self):
        repeated = "Pengukuran dilakukan dengan aturan yang sama."
        middle = "Bagian tengah mencatat hasil pengukuran."
        closing = "Peneliti memeriksa kembali hasil akhir."
        inserted = "Perubahan tambahan diterapkan sesudah bagian tengah."
        comparison = layout.Comparison(manuscript(repeated, middle, repeated, closing),
                                       manuscript(repeated, middle, inserted, repeated, closing))
        self.assertEqual(chunk_pairs(comparison), [
            (repeated, repeated), (middle, middle), (None, inserted),
            (repeated, repeated), (closing, closing),
        ])

    def test_moved_paragraph_has_position_flags_and_keeps_intervening_paragraphs_paired(self):
        first = "Alpha establishes the study background and motivation."
        moved = "Gamma reports measurement validity and researcher decisions."
        middle = "Beta describes sample preparation and input collection."
        last = "Delta concludes the evaluation procedure and output records."
        comparison = layout.Comparison(manuscript(first, middle, moved, last),
                                       manuscript(first, moved, middle, last))
        self.assertEqual(len(comparison.moved), 2)
        old_moved = next(i for side, i in comparison.moved if side == "old")
        new_moved = comparison.counterpart["old", old_moved]
        self.assertEqual(comparison.old[old_moved].text, comparison.new[new_moved].text)
        self.assertIn(comparison.old[old_moved].text, (middle, moved))
        rendered = comparison.render()
        self.assertIn(r"\diffmoved{dipindahkan ke posisi baru}", rendered)
        self.assertIn(r"\diffmoved{dipindahkan dari posisi lama}", rendered)
        self.assertNotIn("highlight", rendered)

    def test_every_source_block_occurs_once_in_each_side_and_keeps_source_order(self):
        figure = r"\begin{figure}\includegraphics{flow.pdf}\caption{Alur penelitian}\end{figure}"
        old = manuscript("Alpha introduction.", "Beta method.", figure, "Gamma discussion.")
        new = manuscript("Alpha introduction.", "Delta inserted text.", figure,
                         "Beta method with revised detail.", "Gamma discussion.")
        comparison = layout.Comparison(old, new)
        for side, blocks in comparison.sides.items():
            with self.subTest(side=side):
                expected = [index for index, block in enumerate(blocks) if block.kind != "break"]
                actual = [index for row in comparison.rows for index in getattr(row, side)]
                self.assertEqual(actual, expected)
                self.assertEqual(len(actual), len(set(actual)))

    def test_added_frontmatter_pages_leave_approval_beside_approval(self):
        old = "\n\\newpage\n".join((
            r"\begingroup PROPOSAL SKRIPSI \endgroup",
            r"\begin{center}HALAMAN PENGESAHAN\end{center} Old approval.",
            r"\begin{center}\textbf{ABSTRAK}\end{center}" + "\nIsi lama.",
        ))
        new = "\n\\newpage\n".join((
            page("HALAMAN JUDUL", r"\begingroup Cover \endgroup"),
            page("HALAMAN PENGAJUAN", "Submission."),
            page("HALAMAN PENGESAHAN", "New approval."),
            page("HALAMAN PERNYATAAN", "Statement."),
            page("KATA PENGANTAR", "Preface."),
            page("ABSTRAK", "Isi baru."),
        ))
        comparison = layout.Comparison(old, new)
        self.assertEqual(anchor_pairs(comparison), [
            ("HALAMAN JUDUL", "HALAMAN JUDUL"), (None, "HALAMAN PENGAJUAN"),
            ("HALAMAN PENGESAHAN", "HALAMAN PENGESAHAN"), (None, "HALAMAN PERNYATAAN"),
            (None, "KATA PENGANTAR"), ("ABSTRAK", "ABSTRAK"),
        ])
        rows = rows_text(comparison)
        approval = next(row for row in rows if "approval" in row[0])
        self.assertIn("approval.", approval[1])

    def test_abstracts_pair_by_language_even_without_or_with_restyled_headings(self):
        def abstract(language, body, heading=True, style="textbf"):
            title, keywords = ("ABSTRAK", "Kata Kunci:") if language == "id" else ("ABSTRACT", "Keywords:")
            head = rf"\begin{{center}}\{style}{{{title}}}\end{{center}}" + "\n\n" if heading else ""
            return head + body + "\n\n" + rf"\textbf{{{keywords}}} Music"

        old = abstract("id", "Isi.", heading=False) + "\n\\newpage\n" + abstract("en", "Body.")
        new = abstract("id", "Isi.", style="textsc") + "\n\\newpage\n" + abstract("en", "Body.")
        comparison = layout.Comparison(old, new)
        self.assertEqual([(a, b) for a, b in anchor_pairs(comparison)],
                         [("ABSTRAK", "ABSTRAK"), ("ABSTRACT", "ABSTRACT")])
        deleted = layout.Comparison(old, abstract("en", "Body."))
        self.assertEqual(anchor_pairs(deleted), [("ABSTRAK", None), ("ABSTRACT", "ABSTRACT")])

    def test_shared_ids_pair_headings_across_levels(self):
        old = "\n".join((r"\section{Rumusan Masalah}", "Pertanyaan.", r"\section{Tujuan Penelitian}", "Tujuan."))
        new = "\n".join((
            r"\section{Rumusan Masalah dan Pertanyaan Penelitian}\label{sec:rumusan-dan-pertanyaan}",
            r"\subsection{Rumusan Masalah}\label{sec:rumusan-masalah}", "Masalah.",
            r"\section{Tujuan dan Manfaat}\label{sec:tujuan-dan-manfaat}",
            r"\subsection{Tujuan Penelitian}\label{sec:tujuan-penelitian}", "Tujuan baru.",
        ))
        self.assertEqual(anchor_pairs(layout.Comparison(old, new)), [
            (None, "Rumusan Masalah dan Pertanyaan Penelitian"),
            ("Rumusan Masalah", "Rumusan Masalah"),
            (None, "Tujuan dan Manfaat"),
            ("Tujuan Penelitian", "Tujuan Penelitian"),
        ])

    def test_a_label_keeps_a_renamed_heading_paired(self):
        old = r"\section{Metode Pendekatan}\label{sec:metode}" + "\nTeks lama sekali."
        new = r"\section{Pendekatan Penelitian}\label{sec:metode}" + "\nUraian yang sama sekali berbeda."
        comparison = layout.Comparison(old, new)
        self.assertEqual(anchor_pairs(comparison), [("Metode Pendekatan", "Pendekatan Penelitian")])
        left, right = rows_text(comparison)[0]
        self.assertIn(r"\delhighlight{Metode}", left)
        self.assertIn(r"\inhighlight{Penelitian}", right)
        self.assertEqual(left.count(r"\label{sec:metode}"), 1)
        self.assertEqual(right.count(r"\label{sec:metode}"), 1)
        self.assertIn(r"\label{diffo0}", left)
        self.assertIn(r"\label{diffn0}", right)

    def test_chapter_title_matches_a_section_with_the_same_words_without_highlights(self):
        old = r"\section{Metode Penelitian}" + "\n" + r"\subsection{Sampel}" + "\nSama."
        new = r"\thesischapter{III}{METODE PENELITIAN}" + "\n" + r"\section{Sampel}" + "\nSama."
        comparison = layout.Comparison(old, new)
        self.assertEqual(anchor_pairs(comparison), [("Metode Penelitian", "METODE PENELITIAN"),
                                                    ("Sampel", "Sampel")])
        self.assertNotIn("highlight", comparison.render())

    def test_added_sections_and_chapters_do_not_shift_later_pairs(self):
        old = "\n".join((r"\section{A}", "A text.", r"\subsection{Existing}", "Existing text.",
                         r"\section{B}", "B text."))
        new = "\n".join((r"\thesischapter{I}{PENDAHULUAN}", r"\section{A}", "A text.",
                         r"\subsection{Added}", "Added text.", r"\subsection{Existing}", "Existing text.",
                         r"\section{Inserted}", "Inserted text.", r"\section{B}", "B text."))
        self.assertEqual(anchor_pairs(layout.Comparison(old, new)), [
            (None, "PENDAHULUAN"), ("A", "A"), (None, "Added"), ("Existing", "Existing"),
            (None, "Inserted"), ("B", "B"),
        ])

    def test_deleted_and_renamed_sections_keep_both_sources(self):
        old = "\n".join((r"\section{A}", "First.", r"\section{Deleted}", "Removed.", r"\section{B}", "Last."))
        new = "\n".join((r"\section{A}", "First.", r"\section{C}", "Last."))
        comparison = layout.Comparison(old, new)
        # B was renamed C: no shared ID or title words, but the same text.
        self.assertEqual(anchor_pairs(comparison), [("A", "A"), ("Deleted", None), ("B", "C")])
        rendered = comparison.render()
        self.assertIn(r"\delpale{Removed.}", rendered)
        self.assertIn("Last.", rendered)

    def test_moved_section_is_compared_with_its_counterpart_at_both_positions(self):
        moved = r"\section{Sistematika Penulisan}" + "\nBab satu memaparkan latar belakang penelitian."
        old = "\n".join((r"\section{Latar Belakang}", "Konteks.", r"\section{Metode}", "Langkah.", moved))
        new = "\n".join((r"\section{Latar Belakang}", "Konteks.",
                         moved.replace("memaparkan", "menjelaskan"), r"\section{Metode}", "Langkah."))
        comparison = layout.Comparison(old, new)
        self.assertEqual(len(comparison.moved), 2)
        rendered = comparison.render()
        self.assertIn(r"\diffmoved{dipindahkan ke posisi baru}", rendered)
        self.assertIn(r"\diffmoved{dipindahkan dari posisi lama}", rendered)
        self.assertIn(r"\delhighlight{memaparkan}", rendered)
        self.assertIn(r"\inhighlight{menjelaskan}", rendered)
        self.assertNotIn(r"highlight{latar}", rendered)

    def test_lists_compare_item_by_item_within_their_section_only(self):
        def section(title, items):
            return "\n".join([rf"\section{{{title}}}", r"\begin{enumerate}"]
                             + [rf"\item {item}" for item in items] + [r"\end{enumerate}"])

        old = "\n".join((section("Manfaat", ["Menguji kaidah lama.", "Memberi data."]),
                         section("Jadwal", ["Tahap satu."])))
        new = "\n".join((section("Manfaat", ["Menguji kaidah baru.", "Memberi panduan."]),
                         section("Sistematika", ["BAB I.", "BAB II."])))
        comparison = layout.Comparison(old, new)
        rows = rows_text(comparison)
        benefits = next(row for row in rows if "Menguji" in row[0])
        self.assertIn("Menguji kaidah", benefits[0].replace(r"\delhighlight{lama.}", ""))
        self.assertIn(r"\inhighlight{baru.}", benefits[1])
        self.assertIn("Memberi", benefits[1])
        # The new Sistematika list is not paired with the old Jadwal list.
        self.assertIn(r"\inspale{BAB}", comparison.render())

    def test_unrelated_sentences_stay_unpaired_and_edited_ones_mark_only_changes(self):
        old = r"\section{A}" + "\n\nFirst paragraph about model output.\n\nClosing words stay mostly the same here."
        new = (r"\section{A}" + "\n\nAn entirely unrelated inserted paragraph.\n\n"
               "First paragraph about generated model output.\n\nClosing words stay mostly the same now.")
        rendered = layout.Comparison(old, new).render()
        self.assertIn(r"\inhighlight{generated}", rendered)
        self.assertNotIn(r"highlight{First}", rendered)
        self.assertIn(r"\inspale{unrelated}", rendered)
        self.assertIn(r"\delhighlight{here.}", rendered)
        self.assertIn(r"\inhighlight{now.}", rendered)

    def test_a_sentence_split_in_two_keeps_its_shared_words(self):
        old = r"\section{A}" + "\nModel menyusun nada dan mengisi suara bawah secara bertahap sampai selesai."
        new = (r"\section{A}" + "\nModel menyusun nada. Model mengisi suara bawah secara bertahap sampai selesai.")
        rendered = layout.Comparison(old, new).render()
        self.assertNotIn("pale", rendered)
        self.assertNotIn(r"highlight{bawah}", rendered)

    def test_structured_pages_compare_words_across_lines(self):
        old = page("HALAMAN PENGESAHAN", "\n".join((
            r"\begin{center}", r"Penguji I\par", r"\textbf{Veronica Yoni}\par", r"NIP 1978\par",
            r"\end{center}")))
        new = page("HALAMAN PENGESAHAN", "\n".join((
            r"\begin{center}", r"Pembimbing II/Anggota\par", r"\textbf{Veronica Yoni}\par", r"NIP 1978\par",
            r"\end{center}")))
        left, right = rows_text(layout.Comparison(old, new))[0]
        self.assertIn(r"\textbf{Veronica Yoni}", left)
        self.assertIn(r"\textbf{Veronica Yoni}", right)
        self.assertIn(r"\delhighlight{Penguji}", left)
        self.assertIn(r"\inhighlight{Pembimbing}", right)

    def test_table_without_counterpart_gets_one_background(self):
        table = "\n".join((r"\begin{tabular}{|l|l|}", r"\hline", r"A & B \\", r"\hline", r"\end{tabular}"))
        rendered = layout.Comparison(r"\section{T}" + "\nTeks.", r"\section{T}" + "\nTeks.\n\n" + table).render()
        self.assertIn("\\begin{diffmath}{inspl}\n" + table, rendered)
        self.assertNotIn(r"\inspale{A}", rendered)


class RenderingTests(unittest.TestCase):
    def test_identical_versions_render_without_highlights(self):
        source = "\n".join((
            r"\begingroup", r"\begin{center}\bfseries SKRIPSI\par Oleh:\\ Name\end{center}", r"\endgroup",
            r"\newpage", r"\section{A}", "Justified paragraph.",
            r"\begin{minipage}{0.48\textwidth}\raggedright Original signature.\end{minipage}",
        ))
        rendered = layout.Comparison(source, source).render()
        self.assertNotRegex(rendered, r"highlight|pale\{|diffmath|diffmoved")
        self.assertIn(r"\begin{center}\bfseries SKRIPSI\par Oleh:\\ Name\end{center}", rendered)
        self.assertIn(r"\begin{minipage}{0.48\textwidth}\raggedright Original signature.\end{minipage}", rendered)
        self.assertNotIn(r"\raggedright" + "\n", rendered.replace("Original", ""))

    def test_long_section_flows_in_paragraph_rows_without_boxes_and_an_addition_is_pale(self):
        old = "\\section{Long}\n\n" + "\n\n".join(f"Paragraph {i} text." for i in range(80))
        new = old + "\n\nAdditional paragraph."
        rendered = layout.Comparison(old, new).render()
        self.assertEqual(rendered.count(r"\switchcolumn*"), 82)
        self.assertNotIn("minipage", rendered)
        self.assertNotIn(r"\newpage", rendered)
        self.assertIn(r"\inspale{Additional}\diffspace{inspl}\inspale{paragraph.}", rendered)
        self.assertIn("Paragraph 79 text.", rendered)

    def test_object_only_fragments_remain_visible_and_insertions_receive_flags(self):
        objects = (
            r"\begin{equation}1+2=3\end{equation}",
            r"\[1+2=3\]",
            r"\includegraphics[width=0.8\linewidth]{flow.pdf}",
            r"\begin{tikzpicture}\draw (0,0) -- (1,1);\end{tikzpicture}",
        )
        for object_source in objects:
            with self.subTest(source=object_source):
                fragments = layout.split_fragments(object_source)
                self.assertTrue(any(fragment.visible for fragment in fragments))
                self.assertEqual("".join(fragment.core + fragment.tail for fragment in fragments), object_source)
                comparison = layout.Comparison(manuscript("Before."), manuscript("Before.", object_source))
                inserted = rows_text(comparison)[-1]
                self.assertEqual(inserted[0], "")
                self.assertRegex(inserted[1], r"diffmath|fcolorbox")
                self.assertIn("inspl", inserted[1])
                self.assertIn(re.sub(r"\s+", "", object_source), re.sub(r"\s+", "", inserted[1]))
                self.assertLessEqual(inserted[1].count(r"\begin{diffmath}"), 1)
                self.assertNotEqual(comparison.change_map()[0][2], "sama")

    def test_inserted_research_flow_figure_flags_caption_and_image(self):
        figure = (r"\begin{figure}" + "\n" + r"\includegraphics{research-flow.pdf}" + "\n"
                  + r"\caption{Rancangan Alur Penelitian}\label{fig:alur}" + "\n" + r"\end{figure}")
        paragraph = "Prosedur penelitian memuat tahap persiapan dan evaluasi."
        comparison = layout.Comparison(manuscript(paragraph), manuscript(paragraph, figure))
        self.assertEqual(chunk_pairs(comparison), [(paragraph, paragraph), (None, figure)])
        inserted = rows_text(comparison)[-1]
        self.assertEqual(inserted[0], "")
        self.assertIn("inspl", inserted[1])
        self.assertIn("research-flow.pdf", inserted[1])
        self.assertIn("Rancangan", inserted[1])
        self.assertIn("Alur", inserted[1])
        self.assertIn("Penelitian", inserted[1])
        self.assertNotEqual(comparison.change_map()[0][2], "sama")

    def test_figure_image_replacement_is_flagged_even_with_an_unchanged_caption(self):
        old_figure = (r"\begin{figure}\includegraphics{flow-v3.pdf}"
                      r"\caption{Rancangan Alur Penelitian}\label{fig:alur}\end{figure}")
        new_figure = old_figure.replace("flow-v3.pdf", "flow-v4.pdf")
        comparison = layout.Comparison(manuscript(old_figure), manuscript(new_figure))
        self.assertEqual(chunk_pairs(comparison), [(old_figure, new_figure)])
        left, right = rows_text(comparison)[1]
        self.assertIn("flow-v3.pdf", left)
        self.assertIn("flow-v4.pdf", right)
        self.assertRegex(left, r"delhl|delpl")
        self.assertRegex(right, r"inshl|inspl")
        self.assertIn(r"\diffcaptionlabel{figure}{delhl}", left)
        self.assertIn(r"\diffcaptionlabel{figure}{inshl}", right)
        self.assertNotEqual(comparison.change_map()[0][2], "sama")

    def test_inserted_figure_flags_later_caption_numbers_and_stable_references(self):
        existing = (r"\begin{figure}\includegraphics{existing.pdf}"
                    r"\caption{Gambar tetap}\label{fig:tetap}\end{figure}")
        inserted = (r"\begin{figure}\includegraphics{inserted.pdf}"
                    r"\caption{Gambar tambahan}\label{fig:tambahan}\end{figure}")
        reference = r"Peneliti menjelaskan hasil pada Gambar \ref{fig:tetap}."
        comparison = layout.Comparison(manuscript(existing, reference),
                                       manuscript(inserted, existing, reference))
        self.assertEqual(chunk_pairs(comparison), [(None, inserted), (existing, existing), (reference, reference)])
        old_index = next(index for index, block in enumerate(comparison.old) if block.text == existing)
        new_index = comparison.counterpart["old", old_index]
        self.assertEqual(comparison.object_numbers["old", old_index], 1)
        self.assertEqual(comparison.object_numbers["new", new_index], 2)
        left, right = rows_text(comparison)[2]
        self.assertIn(r"\diffcaptionlabel{figure}{delhl}", left)
        self.assertIn(r"\diffcaptionlabel{figure}{inshl}", right)
        left, right = rows_text(comparison)[3]
        self.assertIn(r"\diffinline{delhl}{\ref{fig:tetap}}", left)
        self.assertIn(r"\diffinline{inshl}{\ref{fig:tetap}}", right)

    def test_caption_revision_marks_the_caption_without_rewriting_shared_words(self):
        old_figure = (r"\begin{figure}\includegraphics{flow.pdf}"
                      r"\caption{Rancangan Alur Penelitian}\label{fig:alur}\end{figure}")
        new_figure = old_figure.replace("Penelitian}", "Evaluasi}")
        comparison = layout.Comparison(manuscript(old_figure), manuscript(new_figure))
        self.assertEqual(chunk_pairs(comparison), [(old_figure, new_figure)])
        left, right = rows_text(comparison)[1]
        self.assertIn(r"\delhighlight{Penelitian}", left)
        self.assertIn(r"\inhighlight{Evaluasi}", right)
        self.assertNotRegex(left + right, r"highlight\{(?:Rancangan|Alur)\}")

    def test_source_page_breaks_start_both_columns_on_a_new_page_once(self):
        old = "\\section{A}\nFirst.\n\\section{B}\nSecond."
        new = old.replace("\\section{B}", "\\newpage\n\\clearpage\n\\section{B}")
        rendered = layout.Comparison(old, new).render()
        self.assertEqual(rendered.count(r"\newpage"), 1)
        self.assertEqual(rendered.count(r"\section{B}"), 2)
        for column in ("leftside", "rightside"):
            for text in re.findall(rf"\\begin\{{{column}\}}(.*?)\\end\{{{column}\}}", rendered, re.DOTALL):
                self.assertNotIn(r"\newpage", text)
                self.assertNotIn(r"\clearpage", text)

    def test_numbered_headings_get_labels_for_the_change_map(self):
        comparison = layout.Comparison(r"\section{A}" + "\nIsi sama.\n" + r"\section*{Starred}",
                                       r"\thesischapter{I}{BAB}" + "\n" + r"\section{A}" + "\nIsi sama.")
        rendered = comparison.render()
        self.assertIn(r"\section{A}\label{diffo0}", rendered)
        self.assertNotIn(r"\section*{\delpale{Starred}}\label", rendered)
        entries = comparison.change_map()
        self.assertEqual(entries[0], ("", "BAB I BAB", "baru", None))
        self.assertEqual(entries[1][:3], (r"\ref{diffo0} A", r"I.\ref{diffn1} A", "sama"))
        self.assertEqual(entries[1][3], 1.0)
        self.assertEqual(entries[2][2], "dihapus")


class ChangeMapTests(unittest.TestCase):
    def test_tiny_edit_in_a_long_section_is_never_reported_as_unchanged(self):
        paragraphs = [f"Paragraf {i} mencatat pengukuran keluaran model dalam penelitian ini."
                      for i in range(120)]
        updated = paragraphs.copy()
        updated[60] = updated[60].replace("pengukuran", "evaluasi")
        comparison = layout.Comparison(manuscript(*paragraphs), manuscript(*updated))
        self.assertGreater(comparison.change_map()[0][3], 0.98)
        self.assertNotEqual(comparison.change_map()[0][2], "sama")
        rendered = comparison.render()
        self.assertIn(r"\delhighlight{pengukuran}", rendered)
        self.assertIn(r"\inhighlight{evaluasi}", rendered)

    def test_formatting_only_paragraph_and_heading_edits_are_reported(self):
        changes = (
            (manuscript("Isi penelitian."), manuscript(r"\textbf{Isi} penelitian.")),
            (r"\section{Pembahasan}" + "\nIsi sama.",
             r"\section{\textit{Pembahasan}}" + "\nIsi sama."),
            (r"\section{Pembahasan}" + "\nIsi sama.",
             r"\section*{Pembahasan}" + "\nIsi sama."),
            (r"\section{Pembahasan}" + "\nIsi sama.",
             r"\subsection{Pembahasan}" + "\nIsi sama."),
        )
        for old, new in changes:
            with self.subTest(new=new):
                comparison = layout.Comparison(old, new)
                self.assertEqual(len(comparison.change_map()), 1)
                self.assertNotEqual(comparison.change_map()[0][2], "sama")
                self.assertRegex(comparison.render(), r"highlight|pale|diffmoved|diffmath")

    def test_status_reflects_shared_words_and_title_changes(self):
        old = "\n".join((r"\section{Same}", "Alpha beta gamma delta.",
                         r"\section{Rewritten}", "Completely different wording here.",
                         r"\section{Old title}\label{sec:x}", "Kept sentence stays here exactly."))
        new = "\n".join((r"\section{Same}", "Alpha beta gamma delta.",
                         r"\section{Rewritten}", "Nothing in common with before.",
                         r"\section{New title}\label{sec:x}", "Kept sentence stays here exactly."))
        entries = layout.Comparison(old, new).change_map()
        self.assertEqual([entry[2] for entry in entries], ["sama", "ditulis ulang", "sama, judul diubah"])
        table = layout.render_change_map(layout.Comparison(old, new), "proposal/v2", "thesis/v3")
        self.assertIn(r"\begin{longtable}", table)
        self.assertIn("ditulis ulang", table)


if __name__ == "__main__":
    unittest.main()
