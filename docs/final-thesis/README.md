# Final thesis v4

v3 continued proposal v2 as the final thesis and is tagged `thesis/v3`; v4 is tagged `thesis/v4` and is still the text in the working tree. v5 is being planned after the first meeting with Pembimbing I ([supervision/rencana-v5.md](supervision/rencana-v5.md)). Proposal v1/v2 remain in `../proposal-phase/`. The active manuscript follows the department's 2026 research-proposal outline with BAB I–III. Results and conclusions are written after main data exist; main data, analysis, and department format approval remain open.

## What is in this folder

```text
final-thesis/
├── README.md                      This map, source ownership, build commands
├── PROGRESS.md                    Current status, completion gates, open items
├── eval.md                        Writing checks applied before delivery
├── thesis/                        Manuscript source (LaTeX)
├── supervision/                   From and for the lecturers
│   ├── peta-versi.tex             Version map (make map): every revision, who gave feedback, chapter status
│   ├── feedback.md                Lecturer notes F01–F12 (v2 review) and Pembimbing I notes G01–G15 (v4), with actions
│   ├── perubahan-v2-ke-v3.md      Every change from proposal v2 to v3 and its basis
│   ├── review-teman-2026-10-04.md Peer review of v3 by a fellow student (P01–P17; not lecturer feedback)
│   ├── perubahan-v3-ke-v4.md      Every change from v3 to v4 and its basis
│   ├── bimbingan-v3.md            Handout for the v3 supervisor meeting
│   ├── bimbingan-v4.md            Handout for the v4 meeting with Pembimbing I
│   └── rencana-v5.md              Plan for v5 after that meeting: options, questions, tasks
├── study/                         For the researcher to learn and rehearse
│   ├── persiapan-pembimbing-1.md  Strube translation, argument chain, concepts, checklist
│   ├── defense-qa.md              All practice questions and answers (Q1–Q123, with 16a–c and 41a–b)
│   ├── model-dan-istilah.md       DeepBach, Coconet, and technical terms in plain Indonesian
│   └── researcher-guide.md        Start here: the study and its five theories in plain Indonesian, study order, reading list
└── records/                       Running records
    ├── research-log.md            Dated history of decisions and findings
    └── reading-notes.csv          Source verification and the researcher's own reading
```

Where to start:

| You want to | Open |
| --- | --- |
| Understand your own study in plain language | [study/researcher-guide.md](study/researcher-guide.md) |
| Read every note in one file | `make reading`, then `scratch/bahan-bacaan_<version>.pdf` (study, supervision, records, protocol at the latest `thesis/v*` tag; `make reading head` for the latest commit; links between notes work inside the PDF) |
| Know what is done and what is open | [PROGRESS.md](PROGRESS.md) |
| Prepare for Pembimbing I | [study/persiapan-pembimbing-1.md](study/persiapan-pembimbing-1.md), then [study/defense-qa.md](study/defense-qa.md) |
| Understand how DeepBach and Coconet work | [study/model-dan-istilah.md](study/model-dan-istilah.md) |
| See every version, its feedback source, and chapter status | `make map`, then `scratch/peta-versi.pdf` (source: [supervision/peta-versi.tex](supervision/peta-versi.tex)) |
| Explain why the design changed after v2 | [supervision/perubahan-v2-ke-v3.md](supervision/perubahan-v2-ke-v3.md) |
| Explain what changed in v4 | [supervision/perubahan-v3-ke-v4.md](supervision/perubahan-v3-ke-v4.md) |
| Prepare the v4 supervisor meeting | [supervision/bimbingan-v4.md](supervision/bimbingan-v4.md) |
| Know what Pembimbing I said and what to do for v5 | [supervision/rencana-v5.md](supervision/rencana-v5.md), then G01–G15 in [supervision/feedback.md](supervision/feedback.md) |
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
| `chapters/01-pendahuluan.tex` | BAB I: latar belakang, rumusan masalah, pertanyaan penelitian, tujuan, manfaat (no sistematika penulisan since v4) |
| `chapters/02-tinjauan-pustaka.tex` | BAB II: tinjauan pustaka (with comparison table), landasan teori (Briot et al., Storkey, Pearce et al., Strube, Huron), kerangka berpikir, asumsi, hipotesis |
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

`make final-phase` builds the thesis and the version map (`make map`). Final defense slides are not implemented. `thesis/v3` and `thesis/v4` exist; create `thesis/v5` after the v5 sources are committed and checked. Preserve a reviewed milestone using the [root version guide](../../README.md#save-a-final-thesis-milestone) once its source and PDF have been checked.

Use [eval.md](eval.md) to check writing. See [maintenance.md](../maintenance.md) for instrument and tooling issues. Do not fill absent findings with expected outcomes.
