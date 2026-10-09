# v5: final-thesis progress

Updated: 2026-10-09. Active manuscript: `thesis/`, the v5 text, drafted on 2026-10-08 and trimmed on 2026-10-09 to stay close to v4, in the working tree at the researcher's request; not tagged and **not yet agreed by the supervisors** (v4 is tagged `thesis/v4`, v3 `thesis/v3`). v5 is v4 with four changes, after the first meeting with Pembimbing I (G01–G15 in [supervision/feedback.md](supervision/feedback.md)) and the researcher's decisions of 2026-10-08: the Strube exercise group is dropped and all melodies are Bach chorale sopranos from the music21 corpus (40, nothing typed); research question 3 asks where violations fall (near fermatas or inside phrases) instead of melody origin; Strube's role is restated with the chorale chapter (p. 174); title, abstract, and limits follow. Both models, the five rules, the Bach reference, and questions 1–2 stay. Changes and their basis: [supervision/perubahan-v4-ke-v5.md](supervision/perubahan-v4-ke-v5.md). Proposal and agreement sheet for the next meetings (Pembimbing II, then Pembimbing I): [supervision/rancangan-kesepakatan-v5.md](supervision/rancangan-kesepakatan-v5.md) and [supervision/bimbingan-arah-v5.md](supervision/bimbingan-arah-v5.md) (printable copy `scratch/bimbingan-arah-v5.pdf`). Status: BAB I–III v5 written for protocol 3.0; the pipeline is implemented for protocol 3.0 and checked with fake backends; no model has been run; no pilot or main data; not ready for submission as a complete thesis.

This file holds the current status only. Dated history is in [records/research-log.md](records/research-log.md). The design and analysis plan are in [research/protocol.md](../../research/protocol.md). Changes since v4 are in [supervision/perubahan-v4-ke-v5.md](supervision/perubahan-v4-ke-v5.md); since v3 in [supervision/perubahan-v3-ke-v4.md](supervision/perubahan-v3-ke-v4.md); since proposal v2 in [supervision/perubahan-v2-ke-v3.md](supervision/perubahan-v2-ke-v3.md). The options weighed before the decision are in [supervision/rencana-v5.md](supervision/rencana-v5.md).

## Continuity

| Revision | Academic phase | Evidence/status |
| --- | --- | --- |
| v1 | Proposal | `proposal/v1` tag |
| v2 | Proposal | `proposal/v2` tag; reviewed in Seminar Musikologi 2 (F01–F12) |
| v3 | Final thesis | `thesis/v3` tag (2026-10-03); BAB I–III, audit, defense materials |
| v4 | Final thesis | `thesis/v4` tag (2026-10-04): revision after a peer review (P01–P17) and the open audit findings; pipeline ready to run |
| v5 | Final thesis | Drafted 2026-10-08 in the working tree, not tagged: revision after the first Pembimbing I meeting (G01–G15) and the researcher's decisions; protocol 3.0; awaiting supervisor agreement |

Lecturer notes from the v2 review are F01–F12 in [supervision/feedback.md](supervision/feedback.md). The peer review of v3 by a fellow student is in [supervision/review-teman-2026-10-04.md](supervision/review-teman-2026-10-04.md); it is not lecturer feedback. Pembimbing I's notes on v4 are G01–G15 in the same file (transcript supplied 2026-10-06; meeting date not yet recorded). Pembimbing II has not commented; the researcher reports that Bu Yoni asked that Pembimbing I see the work first.

The version map with every reviewer, feedback type, and chapter status per version is built with `make map` (`scratch/peta-versi.pdf`; source [supervision/peta-versi.tex](supervision/peta-versi.tex)). Update it when a version is tagged or a new reviewer appears.

## Current design (v5, protocol 3.0)

Not yet agreed by the supervisors. The one departure from Pembimbing I's advice is keeping two models (G07); it needs his explicit agreement. Details in `research/protocol.md`, Version 3.0.

- Main prior study: Huang et al. (2019), Bach Doodle §6.3 (p. 798). The same soprano melodies go to DeepBach and Coconet: 40 Bach chorale sopranos from the music21 corpus, drawn with seed 20261004 among melodies both models accept. Strube states that his chorale exercises are Bach melodies (1928, p. 174), so no exercise is typed. Five rules from the Yan et al. (2018) rubric worded after Strube; Bach's own harmonizations as the practice reference; machine-only measurement.
- Title (15 words; the researcher's limit is 15): *Evaluasi Musik Hasil AI DeepBach dan Coconet: Kepatuhan Kaidah Gerak Suara Strube pada Harmonisasi Chorale*.
- Questions: 1, each model's adherence compared with Bach (descriptive, with `copy_share`); 2, DeepBach vs Coconet (Wilcoxon, H1, unchanged); 3, violation rate in the fermata zone vs inside the phrase per model (Wilcoxon, H2, two-sided), with Bach's pattern descriptive.
- Landasan teori (v5): Briot, Hadjeres, and Pachet (2020) for the models, including which model receives fermatas; Pearce, Meredith, and Wiggins (2002) for evaluating music made by AI; Strube (1928) for the rules, their stages (p. 45), the chorale chapter (p. 174), and functional harmony; Huron (2001) for why the rules exist; Kerangka Berpikir figure. Storkey (2008) is no longer used.
- Sample: 40 melodies (paired power: d_z = 0.5 needs 38.6 after the 0.864 ARE adjustment); five generations per melody per model, averaged per melody (400 harmonizations).
- Optional, only if the supervisors ask for a manipulated variable: DeepBach with its fermata information removed on the same melodies.

## What is evidenced now

- Manuscript: front matter and BAB I–III, v5. `make thesis` builds `scratch/thesis.pdf` and `scratch/Skripsi_v5_23104810131_Vincent.pdf` (67 pages after the 2026-10-09 trim) without LaTeX warnings, overfull boxes, or undefined references (155 underfull-box messages come from the inherited layout). Against `thesis/v4`, the chapters keep 88–91% of their words; the additions are about 150 words in BAB I, 320 in BAB II, and 470 in BAB III. Cover, figure 1 (Kerangka Berpikir), and equation 5 were checked as page images.
- Study notes (`study/`) were checked against v4 on 2026-10-05; for v5, `researcher-guide.md` sections 1, 2, and 6 and `defense-qa.md` (opening and section N) were updated; the rest of `defense-qa.md` still answers v4 where it mentions melody origin or the Mann–Whitney test.
- Citations: 36 keys cited in v5 (`storkey2008` and `sugiyono2019` are no longer cited); each checked against Crossref or OpenAlex metadata and its full text or abstract (`records/reading-notes.csv`, rows dated 2026-10-04). Full text with page numbers for Hadjeres et al., Huang et al. (2017, 2019), Choi et al., Leemhuis et al., Huron, Pearce et al., Ridhwan and Wisnugraha, Strube; Briot et al. read in the arXiv version of the book. Literature search record: `research/literature/screening-2026-10-04.md`.
- Software checks: `make test` passes (4 checks for instrument v1, 20 for instrument v2, 27 for MusicXML input/output, 32 for the pipeline, covering protocol 3.0 and the 2.1 path). `make dry-run-v2` runs generation, evaluation, phrase zones, analysis, tables, figures, examples, and the completeness check end to end with fake backends.
- Bach frame: 371 iterator entries = 350 distinct files; 23 ineligible, 9 repeat another chorale's soprano; 318 melodies in the sampling frame before the DeepBach vocabulary check; all 318 have at least one fermata and lie within Coconet's range; 8–57 measures (median 15); 1 of 318 lies outside Huang et al.'s limits (`research/outputs/melodies/manifest.csv`, Git-ignored; rebuilt by `make melodies`).
- Exploration on Bach's own harmonizations of the 318 melodies (not study data; `research/experiments/scripts/explore_fermata_zone_bach.py`): the fermata zone holds about 17% of motion opportunities but 55% of Bach's overlaps, 28% of his parallel fifths, and 38% of his parallel octaves, and 2% of his spacing flags (protocol, Version 3.0).
- Instrument v2: validation checks 3–5 were run on 2026-10-02; recomputed on distinct files on 2026-10-04 with negligible differences (protocol, Version 2.1). Check 2 (Strube textbook fixtures) has not been run because the figures are not typed yet.
- Strube: rule pages located in the 1928 edition and the 2015 translation. The 71 exercise candidates and their typing templates stay as history of protocol 2.1.
- No model download, generation, pilot, main data, statistical result, lecturer approval of v3, v4, or v5, or submission exists.

## Completion gates

These are this project's proposed completion criteria. Confirm department requirements with the supervisor.

| Gate | Evidence needed to close it | Current status | Researcher action |
| --- | --- | --- | --- |
| G1. Feedback and scope | Review notes, agreed questions/title, deadline, department guide | F01–F12 answered; peer review P01–P17 answered; Pembimbing I met (G01–G15); v5 drafted 2026-10-08; title, questions, approach, and theory structure not yet agreed | Take `supervision/bimbingan-arah-v5.md` to Pembimbing II, then to Pembimbing I; record both answers with dates in `supervision/feedback.md` |
| G2. Literature | Core sources read; every claim mapped to a source page; search log supports the gap | Assistant verification done for every cited key; researcher's own reading not yet recorded | Read the core sources (list in `study/researcher-guide.md`, section 7) and fill `researcher_read_status` |
| G3. Instrument | Rule pages, v2 definitions, textbook fixtures, music21 cross-check, Huang comparison | Mostly done; textbook fixtures pending | Check the nine figures once the assistant has drafted them from the scan and the 2015 translation |
| G4. Comparative protocol | Melody sets and eligibility, sample seed, model revisions, settings, frozen analysis plan | Protocol 3.0 written 2026-10-08 (2.1 kept as history); settings and seeds fixed; not frozen; awaiting supervisor agreement | Agree protocol 3.0 with the supervisors; freeze after the pilot |
| G5. Pipeline integrity | Isolated runs, attempt log, failure records, completeness checks, reproducible records | Implemented for protocol 3.0 and tested with fake backends | Run `make setup-v2` and `make preflight` when ready |
| G6. Pilot | Both models process the pilot melodies, preserve the soprano, pass QC | Not run | `make select`, `make pilot`, evaluate, record findings |
| G7. Main data and analysis | Frozen protocol, raw artifacts, all attempts, run-specific analysis and figures | Not run | `make generate`, evaluate, analyze, examples, check-run |
| G8. Final manuscript | BAB I–III match executed methods; BAB IV and V from data; abstracts and appendices | BAB I–III v5 for protocol 3.0; BAB IV–V not written | Review the v5 text; write BAB IV–V from `analysis/` outputs |
| G9. Submission and defense | Department checklist, checked PDF, supervisor review, evidence archive, supervision form with at least 12 consultations per supervisor (Jurusan Musik form; handed in at exam registration) | Not ready; form prepared with the v4 title, consultations not yet counted | Fill and sign the form after every meeting; rehearse with `study/defense-qa.md` |

## Open items

### Researcher tasks

1. Record the date of the Pembimbing I meeting in `supervision/feedback.md` and on the supervision form (the form file was created on 6 October at 14:32 and the transcript at 16:18, so the meeting was probably on 6 October; confirm), and move the transcript from `Downloads` to a permanent place outside the repository.
2. Review the v5 text: title, abstract, BAB I–III ([supervision/perubahan-v4-ke-v5.md](supervision/perubahan-v4-ke-v5.md) lists every change).
3. Take [supervision/bimbingan-arah-v5.md](supervision/bimbingan-arah-v5.md) to Bu Yoni, then to Pak Gathut, and record their answers.
4. Read Strube p. 174 (chorale guidance; "the following melodies are taken from J. S. Bach") and p. 45 in the printed book.
5. Check the nine textbook figures for validation check 2 once the assistant has drafted them.
6. Confirm the rule pages against both printed editions of Strube.
7. Read the core sources and record your own reading in `records/reading-notes.csv`, starting with the four theory sources (Briot et al., Pearce et al., Strube, Huron) and the studies in the comparison table of II.A.6.
8. Check the printed page ranges of Briot et al. (2020) in the book itself; the content was read in the arXiv version and cited with the chapter page ranges Crossref lists (Method 11–13; Discussion and Conclusion 243–249).
9. Review the AI-drafted motto, halaman persembahan, and kata pengantar, including their personal details.
10. Confirm Adityo Legowo as Cognate and Eki Satria as Dosen Pembimbing Akademik; NUPTKs for Pembimbing I, II, and Cognate are still unknown.

### Questions for the supervisor

The v4 handout is [supervision/bimbingan-v4.md](supervision/bimbingan-v4.md); its questions were not discussed in the first meeting. Questions for both supervisors about v5 (direction, keeping two models, variables and hypotheses, title change on the form, form and consultation count, exam target, format, AI disclosure, Strube in the harmony course) are in [supervision/bimbingan-arah-v5.md](supervision/bimbingan-arah-v5.md), with the reasoning in [supervision/rancangan-kesepakatan-v5.md](supervision/rancangan-kesepakatan-v5.md). In addition:

- Front matter: the cover and submission page say *Skripsi*; confirm the wording required for this phase, the signatory roles, and the format.
- Appendices: candidates are the rule-definition sheets, the melody list, and a pseudocode appendix for the instrument.
- Sistematika Penulisan was removed in v4 (the template does not require it); confirm the supervisor does not expect it.

### Decisions before main data

0. Design direction for v5: proposed by the researcher on 2026-10-08 and written into v5 (above); to be confirmed by both supervisors, with explicit agreement from Pembimbing I to keep two models.
1. Lapsed under protocol 3.0: the contingency for fewer than 30 eligible Strube melodies.
2. Maximum melody length and time per generation both models can handle (frame 8–57 measures): pilot check.
3. DeepBach training membership: `make membership` marks it verified only when the example count equals the cached tensor dataset (sensitivity analysis b).
4. Whether to report hidden fifths and crossings among alto, tenor, and bass as descriptive extras. The model × origin part lapsed with protocol 3.0.
5. Settled in protocol 2.1 and kept in 3.0, pending supervisor agreement: implementation default sampling settings; Coconet's missing repeated notes handled by sensitivity analysis d.
6. Freeze definitions, settings, seeds, and the analysis plan after the pilot (`"frozen": true` in `protocol_v3.json`).
7. Settled in protocol 2.1: repeated notes are merged in every source only in sensitivity analysis d; the main count is unchanged, so the instrument version stays 2.0.
8. Rate per beat: the evaluation writes `quarters` (melody length in quarter notes) so a per-beat rate can be reported; decide whether it is reported as a sensitivity analysis.
9. Proposed in protocol 3.0: `copy_share` (share of steps where the model sounds Bach's own alto, tenor, and bass pitch) is reported descriptively for question 1 on every melody.
10. Proposed in protocol 3.0: three pilot melodies from outside the main sample (seed 41004). A gap from Huang's Bach rates counts as explained when it is in the range shown in protocol check 4; that range is not written yet.
11. Optional extension, only if the supervisors ask for it: DeepBach with its fermata information removed, on the same melodies (not implemented).

### Citation checks before submission

- Books not opened: `leedy2018`, `rangkuti2016` (both as cited in the department template), `creswell2018`, `cohen1988`. `sugiyono2019` is no longer cited in v5.
- Abstract-level support only: `civit2022`, `mycka2025`, `lerch2025`, `louie2020`, `zacharakis2021`, `huang2020contest`, `koops2019`, `micchi2020`, `harrison2020`, `karystinaios2023`, `mehta2025`, `roberts2025`, `holmes2020`, `dwyer2009`, `jamieson2023`, `wang2025`, `yang2020` (abstract on the publisher page). Their sentences claim only what the abstracts state.
- `fang2020` (ICML workshop paper) has no page numbers.

## Manuscript presentation preference

The researcher requests a final-thesis manuscript with ordinary academic prose. The version number identifies the revision. Do not insert draft labels, readiness notices, writing instructions, or repository-status reports into the cover, front matter, or chapters. Keep outstanding work in this progress record and the protocol worksheet.
