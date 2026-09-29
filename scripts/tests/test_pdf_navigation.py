"""Check actual PDF destinations, including old sources with no PDF packages."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_pdf import compile_pdf

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


@unittest.skipUnless(PdfReader and shutil.which("latexmk"), "Requires pypdf and latexmk")
class PdfNavigationTests(unittest.TestCase):
    def compile(self, content):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        source = Path(temporary.name).resolve() / "document.tex"
        output = source.with_suffix(".pdf")
        source.write_text(content)
        self.assertEqual(compile_pdf(source, output), str(output))
        self.assertEqual(source.read_text(), content)
        self.assertEqual(sorted(p.name for p in source.parent.iterdir()), ["document.pdf", "document.tex"])
        reader = PdfReader(output)
        self.assertEqual(reader.root_object["/PageMode"], "/UseOutlines")
        return reader

    def test_numbering_resets_and_starred_heading_land_on_their_own_pages(self):
        reader = self.compile(r"""\documentclass{article}
\usepackage{titlesec}
\begin{document}
\section{First}
First page.
\newpage
\setcounter{section}{0}
\section{Second}
Second page.
\newpage
\section*{Bibliography}
Third page.
\end{document}
""")
        self.assertEqual([item.title for item in reader.outline], ["1 First", "1 Second", "Bibliography"])
        self.assertEqual([reader.get_destination_page_number(item) for item in reader.outline], [0, 1, 2])

    def test_beamer_existing_hyperref_and_explicit_frame_bookmarks(self):
        reader = self.compile(r"""\documentclass{beamer}
\begin{document}
\begin{frame}{First}
\pdfbookmark[0]{First}{slide.1}
First slide.
\end{frame}
\begin{frame}{Second}
\pdfbookmark[0]{Second}{slide.2}
Second slide.
\end{frame}
\end{document}
""")
        self.assertEqual([item.title for item in reader.outline], ["First", "Second"])
        self.assertEqual([reader.get_destination_page_number(item) for item in reader.outline], [0, 1])

    def test_diff_titles_exclude_highlight_colors_and_spacing_commands(self):
        reader = self.compile(r"""\documentclass{article}
\usepackage{xcolor}
\definecolor{inshl}{rgb}{0,1,0}
\newcommand{\inhighlight}[1]{\colorbox{inshl}{#1}}
\newcommand{\diffspace}[1]{{\color{#1}\penalty0\leaders\hrule height\ht\strutbox depth\dp\strutbox\hskip\fontdimen2\font}}
\begin{document}
\section{\colorbox{inshl}{Music}\diffspace{inshl}\inhighlight{Information} Retrieval}
Body.
\end{document}
""")
        self.assertEqual([item.title for item in reader.outline], ["1 Music Information Retrieval"])
        self.assertEqual(reader.get_destination_page_number(reader.outline[0]), 0)


if __name__ == "__main__":
    unittest.main()
