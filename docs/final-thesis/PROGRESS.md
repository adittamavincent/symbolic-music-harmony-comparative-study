# v5: final-thesis progress

Updated: 2026-10-13. BAB I–III, title and bilingual abstracts now follow the Strube chorale case design. The researcher requested local amendment of thesis/v5 after manuscript/PDF review. Versioning does not record supervisor approval: no agreement on the revised scope, pilot, or main model data exists.

## Current manuscript and design

- Title, 15 words: *Evaluasi Musik Hasil AI DeepBach dan Coconet Berdasarkan Kaidah Gerak Suara Strube dalam Harmonisasi Chorale*.
- Two questions: contextual agreement with Strube and descriptive comparison of voice-leading profiles on the same case. Fermata is metadata/cadence context only.
- One chorale case; MODEL 285 is the primary candidate. Its printed harmonization is a reference for choices, not proven Bach authorship or a per-exercise answer key. A clearer copy is required for the occluded opening bass and uncertain final soprano duration.
- DeepBach and Coconet remain the researcher's plan, with 20 attempts per model proposed for score-review workload. Two models and the final count require academic agreement; G07 advised a small case and consideration of one model.
- Seven families organize main/supplementary reading: fifths, octaves, overlap, spacing, crossing, melodic movement and hidden-interval approaches. Seven other mapped families provide harmonic context.
- Program flags are candidate events. Score decisions distinguish confirmed deviations, conditional acceptance and unresolved cases. Horizontal A/T/B profiles, per-criterion denominators, state episodes/durations and repeated locations are included.
- The general music framework is Strube's harmony theory of chord functions and four-part writing. Model description, evaluation purpose and perceptual interpretation have distinct supporting sources.
- Written protocol 4.0 and contextual instrument 3.0 are plans in [research/protocol.md](../../research/protocol.md), not implemented software. Executable defaults still belong to historical protocol 3.0/instrument 2.0. Main collection commands must not be used as if they implemented this revision.

## What the researcher needs to do

1. Read the revised PDF and [learning guide](study/panduan-belajar-v5.md), explain Fig. 33, and answer the [24 supervision questions](study/latihan-bimbingan-v5.md). Use the [researcher guide](study/researcher-guide.md) for next actions and check source pages in the [rule map](study/peta-kaidah-gerak-suara-strube.md).
2. Obtain readable MODEL 285 notation, especially the obscured bass and final soprano duration; verify transcriptions. If not recoverable, select another complete case in the same context before seeing model results.
3. Take [the meeting handout](supervision/bimbingan-arah-v5.md) and manuscript to Bu Yoni then Pak Gathut. Record actual dates and decisions on case, one/two models, criteria, attempts, method/hypotheses and format.
4. Read core sources and fill researcher_read_status in [reading-notes.csv](records/reading-notes.csv). Assistant source checks are not the researcher's own reading.
5. Once scope/source/criteria are settled, request contextual pipeline implementation and a separate pilot. Then freeze the executable protocol and collect main data; add results and conclusion chapters from those data.

## Source and verification evidence

After the researcher liked the revised v5, both writing skills were applied to BAB I–III with seven minimal edits. The [editorial record](records/editorial-v5-2026-10-13.md) gives the original wording, revised wording and reasons. Citation/reference/label tokens, numbers and mathematics are preserved; front matter, bibliography, protocol and evaluator are unchanged from a5129ac. This is editorial review, not evidence of authorship or instrument validation.

The focused learning packet contains five study sessions, the source Fig. 33, three explicitly illustrative calculation exercises and 24 questions with answer anchors. Run make learn-v5 from the repository root to build scratch/Panduan_Belajar_v5_23104810131_Vincent.pdf. Its 14 pages and the edited manuscript's 57 pages were rendered and visually reviewed; page/glyph checks found no replacement/null glyphs or words outside pages. Verification is retained in research/outputs/writing-v5-2026-10-13/.

Both supplied scans have text-OCR coverage for every PDF page: 147 English and 91 Indonesian pages. This is not whole-book proofreading or notation accuracy. All five MODEL systems and the exercise boundary have been viewed. Fourteen relevant rule families have page/stage/exception mapping, detector gaps and annotation needs.

Two Fig. 33 panels have manually entered MusicXML, 16 note events and provenance. Readback preserves the entered pitches/durations; v2 overlap counts are 0 for the first good panel and 1 for avoid. This supports two overlap conditions only; independent researcher confirmation and broader validation remain open. Full MODEL SATB transcription is incomplete and failed/partial OMR remains retained as such.

The manuscript adds the source Fig. 33 illustration. Thesis-only bibliography additions Flyvbjerg (2006) and Lazic (2010) were checked from primary author/publisher sources and the prior reading ledger. Proposal bibliography and all proposal manuscript sources are unchanged.

make thesis passed with 57 pages; all page images and key tables/notation/diagrams were reviewed, 32 citation keys resolve, and the delivery copy is byte-identical. Verification and the local tag request are recorded in [research-log.md](records/research-log.md); the local ref check is kept in research/outputs/manuscript-v5-review/. Main model setup, pilot, training-membership verification, generation, main analysis and research results have not been run.

## Continuity and feedback

| Revision | Academic phase | Status |
| --- | --- | --- |
| v1–v2 | Proposal | proposal/v1 and proposal/v2; v2 review in Seminar Musikologi 2, F01–F12 |
| v3 | Final thesis | thesis/v3; BAB I–III and earlier audit/defense materials |
| v4 | Final thesis | thesis/v4; revision after peer feedback P01–P17 |
| v5 | Final thesis | Rewritten 13 October following source reading and the researcher's direction; academic approval and research data open |

G01–G15 record Pembimbing I's comments on v4; the first meeting date still needs confirmation. F01–F12 are lecturer comments from the seminar course; P01–P17 are peer comments. Keeping two models is a researcher choice, not recorded supervisor approval. No new lecturer feedback is invented.

Older designs and evidence stay in the dated [9 October change record](supervision/perubahan-v4-ke-v5-2026-10-09.md), [old guide](study/researcher-guide-2026-10-09.md), protocol versions 2.1/3.0, historical JSON and research-log. The old 318-melody frame, software tests, corpus probes and fake-model runs do not provide results for the revised case design.

## Completion gates

| Gate | Current evidence | Remaining work |
| --- | --- | --- |
| Scope and department requirements | Revised manuscript/handout and G01–G15 | Agree case, models, criteria, count, approach/hypotheses, title and formatting; record dates |
| Sources and literature | Source map and assistant checks | Read sources independently; obtain clear notation and verify complete input/reference |
| Contextual instrument | Five historical detectors and two source probes | Implement/version episodes, all crossings, contextual records, spelling limits, denominators and missed-event checks; validate beyond two panels |
| Executable protocol | Written plan 4.0; older software preserved | Align implementation with agreed plan; check settings and freeze after requested pilot |
| Pilot | Not run | Technical encoding, fixed soprano, timing, runtime and quality checks, stored separately |
| Main data | Not run | New initialized attempts, raw artifacts, all failures, score decisions and descriptive analysis |
| Results and final thesis | BAB I–III only | Results/conclusion from collected data; abstracts updated from actual findings |
| Submission/defense | Forms and earlier practice material | Confirm department checklist and consultation requirements; update form title and defense answers |

## Other researcher checks

Confirm the first meeting date and keep the supervision transcript in permanent storage. Verify source-page citations in the printed Briot book, since the previous content check used its author version. Confirm committee roles, applicable final-thesis format and current consultation-form requirements with the supervisors. Review personal front-matter details; these were preserved. Record any new requirements rather than attributing them to existing feedback.

The following earlier citation limitations remain useful to check. Rangkuti, Cohen, Mehta, Roberts and Dwyer are no longer cited in the current manuscript.

### Citation checks before submission

- Books not opened: `leedy2018`, `rangkuti2016` (both as cited in the department template), `creswell2018`, `cohen1988`. `sugiyono2019` is no longer cited in v5.
- Abstract-level support only: `civit2022`, `mycka2025`, `lerch2025`, `louie2020`, `zacharakis2021`, `huang2020contest`, `koops2019`, `micchi2020`, `harrison2020`, `karystinaios2023`, `mehta2025`, `roberts2025`, `holmes2020`, `dwyer2009`, `jamieson2023`, `wang2025`, `yang2020` (abstract on the publisher page). Their sentences claim only what the abstracts state.
- `fang2020` (ICML workshop paper) has no page numbers.

## Manuscript presentation preference

The version identifies revision status. The manuscript uses ordinary academic prose without draft labels, readiness reports or writing instructions. Readiness stays in this file and the protocol. No absent research findings are replaced with expected results.
