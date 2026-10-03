# v3: final-thesis progress

Updated: 2026-10-03. Active manuscript: `thesis/`. Status: BAB I–III drafted for protocol version 2 (machine-only design); instrument version 2 implemented and partly validated; no pilot or main data; not ready for submission.

This file holds the current status only. Dated history is in [records/research-log.md](records/research-log.md). The design and analysis plan are in [research/protocol.md](../../research/protocol.md). Changes since proposal v2, with their basis, are in [supervision/perubahan-v2-ke-v3.md](supervision/perubahan-v2-ke-v3.md).

## Continuity

| Revision | Academic phase | Evidence/status |
| --- | --- | --- |
| v1 | Proposal | Existing `proposal/v1` tag |
| v2 | Proposal | Existing `proposal/v2` tag; researcher reports lecturer review during in-class, one-to-one tutoring |
| v3 | Final thesis continuing from v2 | Active manuscript and research plan; future milestone name `thesis/v3`; no tag or completed main experiment yet |

Lecturer notes from the v2 review are recorded as F01–F12 in [supervision/feedback.md](supervision/feedback.md). The review date and the submission deadline have not been supplied. Record later comments there before attributing any methodological revision to a lecturer.

## Current design

Decided at the researcher's request on 2026-10-02 (details in the research log):

- Main prior study: Huang et al. (2019), Bach Doodle §6.3. Kept: per-measure P5/P8 counts with music21, the out-of-distribution hypothesis, Mann–Whitney comparisons, Bach rates as reference.
- Extensions: DeepBach added to Coconet; the same melodies given to both models; melody origin (Bach chorale sopranos vs Strube melody exercises) as X2; three more rules from the Yan et al. (2018) rubric that need no chord analysis (upper-voice spacing, crossing above the soprano, overlap); Bach's own harmonizations as a reference on the same melodies.
- Roles of the sources: Huang = design and measure; Yan = error categories and weights; Strube = rule wording, exceptions, and the textbook melodies.
- Removed: NotaGen, conditioning levels A–D, the soprano leading-tone rule, and the clipped Strube Score.
- Validation without humans: Strube's printed examples as test fixtures, cross-check against music21 `VoiceLeadingQuartet`, comparison with Huang's Bach rates, deterministic reruns.
- Sample: at least 30 melodies per origin group from a power analysis; five generations per melody per model, averaged.

The lecturers did not ask for NotaGen's removal, the A–D replacement, the five-rule set, or the machine-only design. Do not attribute those to them.

## What is evidenced now

- Manuscript: front matter and BAB I–III. `make thesis` built `scratch/thesis.pdf` (63 pages) on 2026-10-02.
- Instrument v2: `research/voice_leading_v2.py`. Its 20 software checks passed with `make test` on 2026-10-02. Validation checks 3–5 were run on the music21 Bach chorales (results in `research/protocol.md`). Check 2, the Strube textbook fixtures, has not been run because the figures are not typed yet.
- Strube: rule pages located in the 1928 edition and in the 2015 Indonesian translation by Pembimbing I (`research/literature/strube-rule-pages.csv`; translation pages in [study/persiapan-pembimbing-1.md](study/persiapan-pembimbing-1.md)). Exercise inventory: 71 melody candidates and 47 given basses in exercises 1–118 (`research/literature/strube-exercise-inventory.csv`).
- Instrument v1 (historical, kept unchanged): `research/strube_evaluator.py`, four software checks, the A–D condition manifest, and generation adapters that hard-code BWV 66.6. Its known defects are listed in [maintenance.md](../maintenance.md).
- Local outputs contain dry-run metadata, OpenAlex search results, and the instrument v2 validation runs only. No generated MIDI dataset, pilot, main data, statistical result, lecturer approval, Git milestone tag, or submission exists.

## Completion gates

These are this project's proposed completion criteria. Confirm department requirements with the supervisor.

| Gate | Evidence needed to close it | Current status | Researcher action |
| --- | --- | --- | --- |
| G1. Feedback and scope | Review notes, agreed questions/title, deadline, department guide | Notes F01–F12 recorded; department template supplied; title, questions, and machine-only design await supervisor agreement; deadline not supplied | Confirm scope with Pembimbing I |
| G2. Literature | Read core sources; every retained claim mapped to a source page/section; search log supports the stated gap | Assistant verification for core sources; researcher reading not yet recorded; many sources checked from abstracts only | Read the core sources and fill `researcher_read_status` in [records/reading-notes.csv](records/reading-notes.csv) |
| G3. Instrument | Strube pages for the five rules, exceptions, v2 definitions implemented, textbook fixtures pass, music21 cross-check, Huang Bach-rate comparison | Mostly done: pages found in both editions, v2 implemented and tested, checks 3–5 run; textbook fixtures pending | Confirm pages in print; type the nine figures |
| G4. Comparative protocol | Melody inventory and eligibility, Bach sample seed, model revisions and checksums, generation settings, frozen analysis plan | Protocol version 2 drafted; inventory complete, typing and eligibility checks pending | Type melodies; agree the protocol; freeze before main generation |
| G5. Pipeline integrity | Timing conversion fixed, quality exclusions applied, isolated runs, failed-file/count checks, reproducible records | Open | Work through [maintenance findings](../maintenance.md#research-correctness) before main generation |
| G6. Pilot | Both models process melodies from both groups, preserve the soprano, and pass quality control; pilot kept separate | Not run | Record failures and limits; do not select favourable outputs |
| G7. Main data and analysis | Frozen protocol, raw artifacts, all attempts, actual eligible counts, run-specific analysis and figures | Not run | Collect and review the agreed dataset |
| G8. Final manuscript | BAB I–III match executed methods; results and conclusion chapters, added after main data, cite measured artifacts and answer the questions; abstracts and appendices complete | BAB I–III working draft; results and conclusion chapters not written | Review interpretations and write conclusions from data |
| G9. Submission and defense | Department checklist, checked PDF, supervisor review, evidence archive, final presentation if required | Not ready | Confirm local requirements and rehearse with [study/defense-qa.md](study/defense-qa.md) |

## Open items

### Researcher tasks

1. Confirm the rule pages against both printed editions of Strube, and check 1928 p. 48 (exercises 67–68, read from translation p. 58).
2. Type the 71 candidate melodies into MusicXML and fill the key, meter, length, and fermata columns of the inventory. Type the nine textbook figures in `strube-example-fixtures.csv`.
3. Read the core sources and record your own reading in the reading ledger.
4. Review the AI-drafted motto, halaman persembahan, and kata pengantar, including their personal details.
5. Confirm Adityo Legowo as Cognate and Eki Satria as Dosen Pembimbing Akademik. Pembimbing I, Pembimbing II, and Cognate still print NIPs because their NUPTKs are unknown.

### Questions for the supervisor

The handout is [supervision/bimbingan-v3.md](supervision/bimbingan-v3.md). In addition:

- Whether to cite the 2015 translation, and how to read its three wording differences from the 1928 edition (spacing, overlap, bass below the tenor).
- Front matter: the cover and submission page say *Skripsi*; confirm the wording required for this phase, the signatory roles, and the format.
- Appendices: the template's LAMPIRAN items (permits, photos, questionnaire) do not fit this study. Candidates are the rule-definition sheets, the melody inventory, and a pseudocode appendix for the instrument after the definitions are frozen.
- Scope limits sit at the end of BAB I Rumusan Masalah; a separate *Batasan Penelitian* section would depart from the template.
- Sistematika Penulisan describes only BAB I–III. Add BAB IV and V when written, or earlier if the supervisor expects the planned chapters.

### Decisions before main data

1. Contingency if fewer than 30 eligible Strube melodies remain after typing and model checks; see the risk table in `research/protocol.md`.
2. Maximum melody length both models can process, and how the Coconet adapter handles full-length melodies (the current adapter uses 32 sixteenth steps).
3. Confirmation that DeepBach's pretrained resources used the default contiguous split, so training membership of Bach melodies can be recorded.
4. Points raised in `study/persiapan-pembimbing-1.md` on 2026-10-02: how the Wilcoxon test handles zero differences; whether to test the model × origin interaction; how to treat fermatas that the Strube melodies may lack; whether to report hidden fifths and all voice crossings as additional descriptive data.
5. Freeze definitions, generation settings, the Bach sample seed, and the analysis plan before main generation.

### Citation checks before submission

- Not yet verified: `dong2020` author list, `fang2020` workshop name, `Ji2023` year and article number, page support for `harrison2020consonance` and `schoenberg1954`.
- Books not opened: `leedy2018`, `rangkuti2016`, `creswell2018` (definition page), `sugiyono2019` (edition and pages), `cohen1988`; `hodges1956` checked from Crossref metadata only.
- Sources added from OpenAlex on 2026-09-30 were checked against abstracts only. Record page or section support before submission.

## Manuscript presentation preference

The researcher requests a final-thesis manuscript with ordinary academic prose. Version v3 identifies the revision. Do not insert draft labels, readiness notices, writing instructions, or repository-status reports into the cover, front matter, or chapters. Keep outstanding work in this progress record and the protocol worksheet.
