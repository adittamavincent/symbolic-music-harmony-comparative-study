# v4: final-thesis progress

Updated: 2026-10-06. Active manuscript: `thesis/`, still the v4 text (tagged `thesis/v4`; v3 is tagged `thesis/v3`). v5 is being planned after the first meeting with Pembimbing I, who advised narrowing the study to a case in Strube's chorale context (G01–G15 in [supervision/feedback.md](supervision/feedback.md); plan in [supervision/rencana-v5.md](supervision/rencana-v5.md)); the design decision is open and no manuscript text has changed. Status of the v4 text: BAB I–III revised for protocol version 2.1, with a rebuilt landasan teori and verified citations; the full experiment pipeline is implemented and checked with fake backends; no model has been run; no pilot or main data; not ready for submission as a complete thesis.

This file holds the current status only. Dated history is in [records/research-log.md](records/research-log.md). The design and analysis plan are in [research/protocol.md](../../research/protocol.md). Changes since v3, with their basis, are in [supervision/perubahan-v3-ke-v4.md](supervision/perubahan-v3-ke-v4.md); changes since proposal v2 in [supervision/perubahan-v2-ke-v3.md](supervision/perubahan-v2-ke-v3.md).

## Continuity

| Revision | Academic phase | Evidence/status |
| --- | --- | --- |
| v1 | Proposal | `proposal/v1` tag |
| v2 | Proposal | `proposal/v2` tag; reviewed in Seminar Musikologi 2 (F01–F12) |
| v3 | Final thesis | `thesis/v3` tag (2026-10-03); BAB I–III, audit, defense materials |
| v4 | Final thesis | `thesis/v4` tag (2026-10-04): revision after a peer review (P01–P17) and the open audit findings; pipeline ready to run |
| v5 | Final thesis | Planned (2026-10-06): revision after the first Pembimbing I meeting (G01–G15); direction to be decided, see `supervision/rencana-v5.md` |

Lecturer notes from the v2 review are F01–F12 in [supervision/feedback.md](supervision/feedback.md). The peer review of v3 by a fellow student is in [supervision/review-teman-2026-10-04.md](supervision/review-teman-2026-10-04.md); it is not lecturer feedback. Pembimbing I's notes on v4 are G01–G15 in the same file (transcript supplied 2026-10-06; meeting date not yet recorded). Pembimbing II has not commented; the researcher reports that Bu Yoni asked that Pembimbing I see the work first.

The version map with every reviewer, feedback type, and chapter status per version is built with `make map` (`scratch/peta-versi.pdf`; source [supervision/peta-versi.tex](supervision/peta-versi.tex)). Update it when a version is tagged or a new reviewer appears.

## Current design

Under review since 2026-10-06. Pembimbing I questioned pooling Strube exercises from different chapters (each exercise has its own context), asked for a smaller case study in Strube's chorale context, and found the comparison of two models too broad for now (G02, G06, G07). The v4 design below stays on record until the researcher decides decision 0. Unchanged from v3 in substance (see `research/protocol.md`):

- Main prior study: Huang et al. (2019), Bach Doodle §6.3 (p. 798). Same soprano melodies given to DeepBach and Coconet; melody origin (Bach chorale sopranos vs Strube melody exercises) as X2; five rules from the Yan et al. (2018) rubric worded after Strube (1928); Bach's own harmonizations as reference; machine-only measurement.
- Landasan teori (v4): Briot, Hadjeres, and Pachet (2020) for the models; Storkey (2008) for dataset shift; Pearce, Meredith, and Wiggins (2002) for evaluating music made by AI; Strube (1928) for the rules and functional harmony; Huron (2001) for why the rules exist; Kerangka Berpikir figure.
- Sample: every eligible Strube melody plus an equal Bach sample of at least 30 (seed 20261004); five generations per melody per model, averaged per melody.

## What is evidenced now

- Manuscript: front matter and BAB I–III, v4. `make thesis` built `scratch/thesis.pdf` and `scratch/Skripsi_v4_23104810131_Vincent.pdf` (70 pages) on 2026-10-04 without LaTeX warnings; after the 2026-10-05 register and terminology edit the build is 69 pages.
- Study notes (`study/`) were checked against v4 and protocol 2.1 on 2026-10-05; `researcher-guide.md` is now the plain-Indonesian entry point.
- Citations: 38 keys cited; each checked against Crossref or OpenAlex metadata and its full text or abstract (`records/reading-notes.csv`, rows dated 2026-10-04). Full text with page numbers for Hadjeres et al., Huang et al. (2017, 2019), Choi et al., Leemhuis et al., Huron, Pearce et al., Storkey (author copy), Ridhwan and Wisnugraha, Strube; Briot et al. read in the arXiv version of the book. Literature search record: `research/literature/screening-2026-10-04.md`.
- Software checks: `make test` passes (4 checks for instrument v1, 20 for instrument v2, 27 for MusicXML input/output, 26 for the protocol-2.1 pipeline). `make dry-run-v2` runs generation, evaluation, analysis, tables, figures, examples, and the completeness check end to end with fake backends.
- Bach frame: 371 iterator entries = 350 distinct files; 23 ineligible, 9 repeat another chorale's soprano; 318 melodies in the sampling frame before the DeepBach vocabulary check; 1 of 318 lies outside Huang et al.'s limits (`research/outputs/melodies/manifest.csv`, Git-ignored; rebuilt by `make melodies`).
- Instrument v2: validation checks 3–5 were run on 2026-10-02; recomputed on distinct files on 2026-10-04 with negligible differences (protocol, Version 2.1). Check 2 (Strube textbook fixtures) has not been run because the figures are not typed yet.
- Strube: rule pages located in the 1928 edition and the 2015 translation; 71 melody candidates inventoried; 71 empty typing templates created in `research/literature/strube-melodies/`.
- No model download, generation, pilot, main data, statistical result, lecturer approval of v3/v4, or submission exists.

## Completion gates

These are this project's proposed completion criteria. Confirm department requirements with the supervisor.

| Gate | Evidence needed to close it | Current status | Researcher action |
| --- | --- | --- | --- |
| G1. Feedback and scope | Review notes, agreed questions/title, deadline, department guide | F01–F12 answered; peer review P01–P17 answered; Pembimbing I met (G01–G15): scope to be narrowed; title, questions, approach, and theory structure not yet agreed | Decide decision 0; take the questions in `supervision/rencana-v5.md` §8 to Pembimbing I; report to Pembimbing II |
| G2. Literature | Core sources read; every claim mapped to a source page; search log supports the gap | Assistant verification done for every cited key; researcher's own reading not yet recorded | Read the core sources (list in `study/researcher-guide.md`, section 7) and fill `researcher_read_status` |
| G3. Instrument | Rule pages, v2 definitions, textbook fixtures, music21 cross-check, Huang comparison | Mostly done; textbook fixtures pending | Type the nine figures in `strube-example-fixtures.csv` |
| G4. Comparative protocol | Melody inventory and eligibility, sample seed, model revisions, settings, frozen analysis plan | Protocol 2.1 written; settings and seeds fixed; not frozen; on hold since 2026-10-06 because the sample and analysis plan may change (decision 0) | Pause typing the 71 melodies; write the next protocol version after decision 0; freeze after the pilot |
| G5. Pipeline integrity | Isolated runs, attempt log, failure records, completeness checks, reproducible records | Implemented and tested with fake backends | Run `make setup-v2` and `make preflight` when ready |
| G6. Pilot | Both models process melodies from both groups, preserve the soprano, pass QC | Not run | `make select`, `make pilot`, evaluate, record findings |
| G7. Main data and analysis | Frozen protocol, raw artifacts, all attempts, run-specific analysis and figures | Not run | `make generate`, evaluate, analyze, examples, check-run |
| G8. Final manuscript | BAB I–III match executed methods; BAB IV and V from data; abstracts and appendices | BAB I–III v4; BAB IV–V not written | Write BAB IV–V from `analysis/` outputs |
| G9. Submission and defense | Department checklist, checked PDF, supervisor review, evidence archive | Not ready | Rehearse with `study/defense-qa.md` |

## Open items

### Researcher tasks

1. Record the date of the Pembimbing I meeting in `supervision/feedback.md` and move the transcript from `Downloads` to a permanent place outside the repository.
2. Read Strube's "Harmonization of Chorales" (1928, pp. 174–179) in the printed book, including p. 179, which is missing from the scan; also pp. 45 and 55.
3. Paused on 2026-10-06 until decision 0: type the 71 Strube melodies in `research/literature/strube-melodies/` (format in its README), run `make melodies`, and compare each MusicXML file with the printed page. Confirm exercises 67–68 on 1928 p. 48. If v5 uses Strube's chorale chapter, type only the chosen melody or melodies of exercise 236 instead.
4. Type the nine textbook figures in `strube-example-fixtures.csv` as test cases (validation check 2).
5. Confirm the rule pages against both printed editions of Strube.
6. Read the core sources and record your own reading in `records/reading-notes.csv`, starting with the five theory sources (Briot et al., Storkey, Pearce et al., Strube, Huron) and the studies in the comparison table of II.A.6.
7. Check the printed page ranges of Briot et al. (2020) in the book itself; the content was read in the arXiv version and cited with the chapter page ranges Crossref lists (Method 11–13; Discussion and Conclusion 243–249).
8. Review the AI-drafted motto, halaman persembahan, and kata pengantar, including their personal details.
9. Confirm Adityo Legowo as Cognate and Eki Satria as Dosen Pembimbing Akademik; NUPTKs for Pembimbing I, II, and Cognate are still unknown.

### Questions for the supervisor

The v4 handout is [supervision/bimbingan-v4.md](supervision/bimbingan-v4.md); its questions were not discussed in the first meeting. Questions for the next meeting (case material, number of models, approach without hypotheses, chorale guidance, title, translation volume) are in [supervision/rencana-v5.md](supervision/rencana-v5.md) §8. In addition:

- Front matter: the cover and submission page say *Skripsi*; confirm the wording required for this phase, the signatory roles, and the format.
- Appendices: candidates are the rule-definition sheets, the melody inventory, the typed melodies, and a pseudocode appendix for the instrument.
- Sistematika Penulisan was removed in v4 (the template does not require it); confirm the supervisor does not expect it.

### Decisions before main data

0. Design direction for v5 after Pembimbing I (G05–G07), decided by the researcher and confirmed with Pembimbing I. Options in `supervision/rencana-v5.md` §5: A, a case study of one melody from Strube's chorale exercise 236 harmonized many times by Coconet, with violations located in the score and compared with Bach's harmonization and Strube's chorale guidance (p. 174); B, the v4 comparison with each Strube melody labelled by chapter; C, all ten melodies of exercise 236. The assistant recommends A, extended to C if time allows. Decisions 1–10 below were written for the v4 design; revisit them after decision 0.
1. Contingency if fewer than 30 eligible Strube melodies remain after typing and preflight (protocol risk table; the code uses all of them and reports the minimum detectable effect).
2. Maximum melody length and time per generation both models can handle: pilot check.
3. DeepBach training membership: `make membership` marks it verified only when the example count equals the cached tensor dataset.
4. Whether to test the model × origin interaction (not in the plan); how to treat Strube melodies without fermatas (they simply have no fermata exclusions); whether to report hidden fifths and all voice crossings as descriptive extras.
5. Settled in protocol 2.1, pending supervisor agreement: implementation default sampling settings; Coconet's missing repeated notes handled by sensitivity analysis d.
6. Freeze definitions, settings, seeds, and the analysis plan after the pilot (`"frozen": true` in `protocol_v2.json`).
7. Settled in protocol 2.1: repeated notes are merged in every source only in sensitivity analysis d; the main count is unchanged, so the instrument version stays 2.0.
8. Rate per beat: the evaluation now writes `quarters` (melody length in quarter notes) so a per-beat rate can be reported; decide whether it is reported as a sensitivity analysis.
9. Memorisation: the evaluation now writes `copy_share` (share of steps where the model sounds Bach's own alto, tenor, and bass pitch on Bach melodies); decide how it is reported.
10. Proposed in protocol 2.1: pilot Bach melodies come from outside the main sample; pilot Strube melodies stay in the census. A gap from Huang's Bach rates counts as explained when it is in the range shown in protocol check 4.

### Citation checks before submission

- Books not opened: `leedy2018`, `rangkuti2016` (both as cited in the department template), `creswell2018`, `sugiyono2019`, `cohen1988`.
- Abstract-level support only: `civit2022`, `mycka2025`, `lerch2025`, `louie2020`, `zacharakis2021`, `huang2020contest`, `koops2019`, `micchi2020`, `harrison2020`, `karystinaios2023`, `mehta2025`, `roberts2025`, `holmes2020`, `dwyer2009`, `jamieson2023`, `wang2025`, `yang2020` (abstract on the publisher page). Their sentences claim only what the abstracts state.
- `fang2020` (ICML workshop paper) has no page numbers.

## Manuscript presentation preference

The researcher requests a final-thesis manuscript with ordinary academic prose. The version number identifies the revision. Do not insert draft labels, readiness notices, writing instructions, or repository-status reports into the cover, front matter, or chapters. Keep outstanding work in this progress record and the protocol worksheet.
