# Final thesis v3

v3 continues proposal v2 as the final thesis. Proposal v1/v2 remain in `../proposal-phase/`. The active manuscript follows the department's 2026 research-proposal outline with BAB I–III. Results and conclusions are written after main data exist; main data, analysis, and department format approval remain open.

## What is in this folder

```text
final-thesis/
├── README.md                      This map, source ownership, build commands
├── PROGRESS.md                    Current status, completion gates, open items
├── eval.md                        Writing checks applied before delivery
├── thesis/                        Manuscript source (LaTeX)
├── supervision/                   From and for the lecturers
│   ├── feedback.md                Lecturer notes F01–F12 from the v2 review, with actions
│   ├── perubahan-v2-ke-v3.md      Every change from proposal v2 to v3 and its basis
│   └── bimbingan-v3.md            One-page handout for the supervisor meeting
├── study/                         For the researcher to learn and rehearse
│   ├── persiapan-pembimbing-1.md  Strube translation, argument chain, concepts, checklist
│   ├── defense-qa.md              All practice questions and answers (Q1–Q78, with 16a–c and 41a–b)
│   └── researcher-guide.md        Research fundamentals and reading list
└── records/                       Running records
    ├── research-log.md            Dated history of decisions and findings
    └── reading-notes.csv          Source verification and the researcher's own reading
```

Where to start:

| You want to | Open |
| --- | --- |
| Know what is done and what is open | [PROGRESS.md](PROGRESS.md) |
| Prepare for Pembimbing I | [study/persiapan-pembimbing-1.md](study/persiapan-pembimbing-1.md), then [study/defense-qa.md](study/defense-qa.md) |
| Explain why the design changed after v2 | [supervision/perubahan-v2-ke-v3.md](supervision/perubahan-v2-ke-v3.md) |
| Check what the lecturers actually asked | [supervision/feedback.md](supervision/feedback.md) |
| Find when and why something was decided | [records/research-log.md](records/research-log.md) |
| Edit the manuscript | The table below |

Research code, the protocol worksheet, and literature data live in [research/](../../research/README.md).

## Edit the source

| File under `thesis/` | Purpose |
| --- | --- |
| `main.tex.template` | Version, document order, contents lists, formatting |
| `metadata.tex` | Title, researcher, committee, dates, institution |
| `layout.tex` | Chapter heading (`\thesischapter`) and front-matter page layouts: cover heading, signatures |
| `frontmatter/01-halaman-judul.tex` to `09-abstract.tex` | One file per front-matter page, in page order: halaman judul, pengajuan, pengesahan, pernyataan, motto, persembahan, kata pengantar, abstrak, abstract |
| `chapters/01-pendahuluan.tex` | BAB I: latar belakang, rumusan masalah, pertanyaan penelitian, tujuan, manfaat, sistematika penulisan |
| `chapters/02-tinjauan-pustaka.tex` | BAB II: tinjauan pustaka, landasan teori, asumsi, hipotesis |
| `chapters/03-metode-penelitian.tex` | BAB III: metode pendekatan, objek/populasi/sampel, pengumpulan data (variabel, melodi, generasi, instrumen, validitas, kontrol kualitas), analisis, alur penelitian |

Each chapter file opens with its own `\thesischapter` heading. Every section and subsection heading carries a `\label{sec:...}` ID. Keep the ID when a heading is renamed or moved; `make diff` pairs revisions by these IDs. Give a new section a new ID.

The class, logos, and bibliography remain shared with `../proposal-phase/assets/`. Thesis chapters are independent of proposal chapters. The reused class does not establish compliance with the department's final-thesis guide.

## Build from the repository root

```bash
make thesis
make thesis FORCE=1
make -B thesis
```

The PDF is `scratch/thesis.pdf` from the repository root. Make removes temporary auxiliary files after compiling. Edit the template and chapters; Make can overwrite generated `thesis/main.tex`. `make clean-docs` removes generated entry points, current PDFs, and legacy build files. `make aux-clean` preserves PDFs.

`make final-phase` currently builds only the thesis. Final defense slides are not implemented. No `thesis/v3` tag has been created. Preserve a reviewed milestone using the [root version guide](../../README.md#save-final-thesis-v3) once its source and PDF have been checked.

Use [eval.md](eval.md) to check writing. See [maintenance.md](../maintenance.md) for instrument and tooling issues. Do not fill absent findings with expected outcomes.
