# Final thesis v5

v3 continued proposal v2 as the final thesis; v4 followed peer feedback. v5 was drafted on 8 October and rewritten on 13 October 2026 as a Strube chorale case with contextual voice-leading analysis. The researcher requested local amendment of thesis/v5 after source/PDF review. Supervisor agreement and model data remain unrecorded. [The change record](supervision/perubahan-v4-ke-v5.md) separates the current revision from the archived October design. Proposal sources remain in ../proposal-phase/. The active manuscript has BAB I–III; results and conclusions follow actual main data.

Direction reopened 13 October 2026: start with [the revised agreement](supervision/rancangan-kesepakatan-v5.md) and [the Strube rule map](study/peta-kaidah-gerak-suara-strube.md). The seven-page review packet is `scratch/kesepakatan-revisi-v5.pdf`. The 8-9 October agreement and handout are preserved in dated archive files. The manuscript now follows the case plan; the executable pipeline remains the earlier protocol 3.0.

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
│   ├── perubahan-v4-ke-v5.md      Every change from v4 to v5 and its basis
│   ├── bimbingan-v3.md            Handout for the v3 supervisor meeting
│   ├── bimbingan-v4.md            Handout for the v4 meeting with Pembimbing I
│   ├── rencana-v5.md              Plan for v5 after that meeting: options, questions, tasks
│   ├── rancangan-kesepakatan-v5.md Current source-based case proposal, reasons and agreement items
│   └── bimbingan-arah-v5.md       Handout and agreement sheet for Pembimbing II, then Pembimbing I
├── study/                         For the researcher to learn and rehearse
│   ├── persiapan-pembimbing-1.md  Strube translation, argument chain, concepts, checklist
│   ├── defense-qa.md              All practice questions and answers (Q1–Q123, with 16a–c and 41a–b)
│   ├── peta-kaidah-gerak-suara-strube.md  Rule stages, exceptions, notation evidence for the current agreement
│   ├── model-dan-istilah.md       DeepBach, Coconet, and technical terms in plain Indonesian
│   └── researcher-guide.md        Start here: the study and its five theories in plain Indonesian, study order, reading list
└── records/                       Running records
    ├── research-log.md            Dated history of decisions and findings
    └── reading-notes.csv          Source verification and the researcher's own reading
```

Focused learning material for the current v5: [the learning guide](study/panduan-belajar-v5.md) and [24 supervision questions](study/latihan-bimbingan-v5.md). Run make learn-v5 for the combined PDF. The [editorial report](records/editorial-v5-2026-10-13.md) records the seven minimal chapter edits and preserved claims.

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
| Explain what changed in v5 | [supervision/perubahan-v4-ke-v5.md](supervision/perubahan-v4-ke-v5.md) |
| Prepare the v4 supervisor meeting | [supervision/bimbingan-v4.md](supervision/bimbingan-v4.md) |
| Know what Pembimbing I said and what to do for v5 | [supervision/rencana-v5.md](supervision/rencana-v5.md), then G01–G15 in [supervision/feedback.md](supervision/feedback.md) |
| Prepare the next meeting and reach one agreement on v5 | [supervision/rancangan-kesepakatan-v5.md](supervision/rancangan-kesepakatan-v5.md), then print [supervision/bimbingan-arah-v5.md](supervision/bimbingan-arah-v5.md) |
| Check what the lecturers actually asked | [supervision/feedback.md](supervision/feedback.md) |
| Find when and why something was decided | [records/research-log.md](records/research-log.md) |
| Read the supplied Strube scans as searchable text | [Local OCR corpus](../../references/ocr/README.md): English and Indonesian transcripts, source scans, and OCR checks; ignored by Git |
| Edit the manuscript | The table below |

Research code, the protocol worksheet, and literature data live in [research/](../../research/README.md).

## Edit the source

| File under `thesis/` | Purpose |
| --- | --- |
| `main.tex.template` | Version, document order, contents lists, formatting |
| `metadata.tex` | Title, researcher, committee, dates, institution |
| thesis/references.bib | Active thesis bibliography; proposal bibliography preserved |
| `layout.tex` | Chapter heading (`\thesischapter`) and front-matter page layouts: cover heading, signatures |
| `frontmatter/01-halaman-judul.tex` to `09-abstract.tex` | One file per front-matter page, in page order: halaman judul, pengajuan, pengesahan, pernyataan, motto, persembahan, kata pengantar, abstrak, abstract |
| `chapters/01-pendahuluan.tex` | BAB I: latar belakang, rumusan masalah, pertanyaan penelitian, tujuan, manfaat (no sistematika penulisan since v4) |
| `chapters/02-tinjauan-pustaka.tex` | BAB II: tinjauan pustaka (with comparison table), landasan teori (Briot et al., Pearce et al., Strube with the chorale chapter, Huron), kerangka berpikir, asumsi, hipotesis |
| `chapters/03-metode-penelitian.tex` | BAB III: metode pendekatan, objek/pemilihan kasus/pengulangan, pengumpulan data (aspek pengamatan, transkripsi, generasi, kriteria dan keputusan kontekstual, validitas, kontrol kualitas), analisis, alur penelitian |

Each chapter file opens with its own `\thesischapter` heading. Every section and subsection heading carries a `\label{sec:...}` ID. Keep the ID when a heading is renamed or moved; `make diff` pairs revisions by these IDs. Give a new section a new ID.

The class and logos remain shared with ../proposal-phase/assets/. The active thesis bibliography is thesis/references.bib, with inherited entries and separately verified thesis additions. The reused class does not establish compliance with the department's final-thesis guide.

## Build from the repository root

```bash
make thesis
make thesis FORCE=1
make -B thesis
```

The PDF is `scratch/thesis.pdf` from the repository root. Make removes temporary auxiliary files after compiling. Edit the template and chapters; Make can overwrite generated `thesis/main.tex`. `make clean-docs` removes generated entry points, current PDFs, and legacy build files. `make aux-clean` preserves PDFs.

`make final-phase` builds the thesis and the version map (`make map`). Final defense slides are not implemented. `thesis/v3`, `thesis/v4`, and `thesis/v5` exist. A tag identifies its source snapshot; supervisor agreement remains recorded separately. The 13 October manuscript follows the case agreement materials. Written protocol 4.0 is not yet implemented by the older default pipeline 3.0. Preserve a reviewed milestone using the [root version guide](../../README.md#save-a-final-thesis-milestone) once its source and PDF have been checked.

Use [eval.md](eval.md) to check writing. See [maintenance.md](../maintenance.md) for instrument and tooling issues. Do not fill absent findings with expected outcomes.
