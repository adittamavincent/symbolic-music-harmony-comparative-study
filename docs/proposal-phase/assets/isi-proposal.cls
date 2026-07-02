\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{isi-proposal}[2026/06/12 ISI Proposal]
\LoadClass[a4paper,12pt]{article}
\renewcommand{\rmdefault}{ptm}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{dsfont}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[top=4cm, left=4cm, bottom=3cm, right=3cm]{geometry}
\RequirePackage{setspace}
\RequirePackage{indentfirst}
\setlength{\parindent}{1.5cm}
\RequirePackage[table]{xcolor}
\RequirePackage[style=apa, backend=biber]{biblatex}
\RequirePackage{titlesec}
\RequirePackage{graphicx}
\RequirePackage{tabularx}
\newcommand{\makeisititle}[5]{
  \begin{titlepage}
    \begin{spacing}{1.15}
    \bfseries
    \vspace*{\fill}
    \begin{center}
      {\fontsize{16pt}{19.2pt}\selectfont\MakeUppercase{#1}\par}
      \vfill
      PROPOSAL SKRIPSI\par
      \programstudy\par
      \vspace{1cm}
      \includegraphics[width=4cm]{logo-isi.png}\par
      \vspace{1cm}
      Oleh:\\
      #2\\
      NIM: #3\par
      \vfill
      Diajukan Untuk Mengikuti Proses Seleksi Proposal Tugas Akhir/Skripsi\par
      #4\par
      \vfill
      \MakeUppercase{\programstudy}\\
      JURUSAN \MakeUppercase{\departmentname} \MakeUppercase{\facultyname}\\
      \MakeUppercase{\institutionname}\\
      #5\par
    \end{center}
    \vspace*{\fill}
    \end{spacing}
  \end{titlepage}
}
