# Research log

Keep dated entries. Preserve earlier observations when methods change, and record the reason and affected reruns in a later entry.

History moved out of `PROGRESS.md` on 2026-10-03 is filed under the dated entries below, with headings demoted one level. `PROGRESS.md` now holds only the current status. The editorial notices once removed from the old chapter IV and V drafts are no longer copied here; they remain in Git history (`git show 8048818:docs/final-thesis/PROGRESS.md`).

## 2026-09-28 — v3 preparation

Recorded by the assistant from this repository session, not a lecturer-review transcript.

- Did: Inspected proposal/thesis sources and research code; verified selected primary sources; moved computational ownership into `research/`; prepared continuing final-thesis v3 documents.
- Found: Local outputs contained dry-run metadata only. Existing checks pass, but timing, score definition, controls, quality exclusions, and run isolation need resolution. NotaGen C/D prompts are identical. The quantization probe collapsed distinct onsets with `[0.25]`.
- Changed and why: Preserved computational behavior during the move. Replaced unsupported outcome claims with explicit draft evidence/status; corrected verified model/evaluation descriptions; added thesis cover/chapter divisions and planning/reading records.
- Next: Obtain the actual lecturer notes and department guide; settle scope and musical definitions with the researcher/tutor; repair and validate the instrument/pipeline before the pilot.

### Evidence recorded on 2026-09-28 (moved from PROGRESS.md)

- The repository contains three generation adapters, one condition manifest, an evaluator, four executable software checks, and draft BAB I–III following the department's 2026 research-proposal outline.
- The four existing checks passed on 2026-09-28 before the folder move. They exercise specific cases; they do not establish full instrument validity.
- The Bach fixture, forced to tonic C by the test, returned score `0.7568`, 6 fifth flags, 0 octave flags, and 3 leading-tone flags. The deliberately parallel fixture returned score `0.0`, 14 fifth flags, 7 octave flags, and 0 leading-tone flags. These are outputs of the current, unvalidated instrument.
- At the start of this preparation, the local `outputs/` contained dry-run metadata only. No local generated MIDI dataset, master results, or summary CSV was found. These metadata files have been preserved under `research/outputs/`. Data outside this checkout have not been inspected.
- A timing probe with note onsets `0, 0.25, 0.5, 1, 2` showed that `quantize([0.25])` moved all five to zero and made their durations four beats. With `[4]`, this probe preserved the requested quarter-beat offsets/durations. The instrument needs an explicit grid decision and regression checks.

### Earlier decision list (moved from PROGRESS.md)

The earlier list (2026-09-28) asked whether to compare named pipelines or architectures, whether to keep NotaGen, which score to use, how to treat leading-tone contexts, and what the observation unit is. Protocol version 2 answers these: named pipelines only; NotaGen removed; per-measure rates plus a Yan-weighted index; leading-tone rule removed; the melody is the unit.

### Changes made during v3 preparation (moved from PROGRESS.md)

- Recorded v1/v2 proposal history and the continuing v3 final-thesis phase.
- Moved research ownership to `research/` while retaining root CLI/import compatibility entry points.
- Added a researcher guide, feedback record, reading ledger, and protocol worksheet.
- Replaced unsupported chapter 4/5 outcomes with an explicit evidence boundary and completion prompts.
- Corrected the thesis cover's proposal wording and added chapter divisions and a contents page. Department format approval remains open.
- Following the researcher's correction, removed draft/status text from the front matter and restored the previous approval-page and abstract wording. Readiness is tracked in project documentation.
- Adapted the front-matter sequence from a 2026 S-1 Musik ISI Yogyakarta skripsi (`references/ARINII 'ILMAL HAQQI_2026_BAB I.pdf`): submission page, approval-page wording with blank examination date, statement page, lists of figures and tables, and a Sistematika Penulisan section in BAB I. Still open: daftar lampiran once appendices exist, the approval-page signatory roles (the reference uses Pembimbing I/II, Cognate, and Koordinator Prodi), and supervisor confirmation of the format.
- Added motto, halaman persembahan, and kata pengantar pages, placed between the statement page and the abstract as in the 2026 reference skripsi (Intan Rama Wijaya, Arinii 'Ilmal Haqqi, Yazid Fauzan Ath Thaariq), and listed every front-matter page in the table of contents. The text was drafted by Claude at the researcher's request; the motto is unattributed original wording, and the personal details in the dedication and kata pengantar still need the researcher's review.
- Corrected the thesis committee after the researcher's clarification (2026-10-02): Pembimbing I A. Gathut Bintarto Triprasetyo, Pembimbing II Veronica Yoni Kaestri, Koordinator/Ketua Program Studi Musik Kustap, Dekan FSP Dr. I Nyoman Cau Arsana (confirmed by the researcher). Full names and NIPs come from the Prodi Musik staff page (musik.isi.ac.id/education/staff-pengajar/, retrieved 2026-10-02). Thesis metadata (title, researcher, institution, dates, committee) now lives in the tracked `docs/final-thesis/thesis/metadata.tex` instead of `.env.local`, so each thesis commit rebuilds with its own metadata; proposal builds still read `.env.local`. The approval page now follows the Prodi Musik reference layout: Pembimbing I/Ketua, Pembimbing II/Anggota, Cognate/Anggota stacked in one offset column, then Dekan Fakultas Seni Pertunjukan and Koordinator Program Studi S-1 Musik side by side under "Mengetahui,", with Kode Prodi 91221 (matching the 2026 Prodi Musik approval pages in `references/`). The researcher supplied NUPTKs for the dean (3439749650131083) and Kustap (5033745646137003), and the approval page prints those two as NUPTK, as the 2026 reference pages do. Pembimbing I, Pembimbing II, and Cognate still print NIPs because their NUPTKs are not yet known. Unconfirmed: Adityo Legowo as Cognate (carried over from the former Penguji II field) and Eki Satria as Dosen Pembimbing Akademik (from the `ADVISOR_ACADEMIC` field).

No main experiment, statistical finding, lecturer approval, Git milestone tag, or submission has been created by these changes. See the final verification entry in [maintenance.md](../../maintenance.md) for checks actually run after the move.

## 2026-09-30 — BAB I–III outline, review notes, and literature expansion

Recorded by the assistant. The sections below were written in `PROGRESS.md` on 2026-09-30 and moved here on 2026-10-03 without change except heading level and links. They describe the design before the 2026-10-02 method reset (three models, conditioning levels A–D, clipped Strube Score).

### Outline change to BAB I–III (2026-09-30)

The researcher asked for the v3 manuscript to follow the 2026 research-proposal template (*Riset – Template Proposal TA Penelitian 2026*, supplied locally under the Git-ignored `references/` folder; the "prodi lain" copy has identical text). The template defines BAB I Pendahuluan, BAB II Tinjauan Pustaka dan Landasan Teori, and BAB III Metode Penelitian. Results (BAB IV) and conclusions (BAB V) need main data, so they are not part of v3. The finished-thesis example in `references/Research Proposal Structure.txt` shows how a later five-chapter thesis can continue from this structure.

Section mapping from the earlier five-chapter draft:

| Template section | Content source |
| --- | --- |
| I.A Latar Belakang | Earlier I Latar Belakang, reordered into model facts, evaluation literature, interface differences, rule basis, and relevance |
| I.B.1 Rumusan Masalah | New gap summary, bounded to sources reviewed in BAB II; scope limits placed here because the template has no *batasan* section |
| I.B.2 / I.C | Earlier questions and objectives; objectives now map one-to-one to the questions, and the question and objective that implied architectural causation were reworded |
| II.A Tinjauan Pustaka | Earlier II Tinjauan Pustaka, grouped as models, evaluation, and research position |
| II.B.1 / II.B.2 | Earlier symbolic-music and representation subsections (object); Strube rules (analytical focus) |
| II.C Asumsi dan Hipotesis | New: two stated assumptions; non-directional H0/H1 for the model and conditioning comparisons; the first question is descriptive |
| III.A–E | Earlier III subsections regrouped into approach, population/sample, data collection (generation, instrument, validity/reliability, quality control), analysis, and research flow; validation by annotation, reliability by repeat measurement, and a pilot step added from `research/protocol.md` |
| Removed | Earlier IV Hasil/Pembahasan and V Kesimpulan/Saran; preserved in Git history |

Claims checked against full paper text during this change:

- Huang et al. (Coconet, ISMIR 2017 PDF) evaluates with log-likelihood and human evaluation; the text contains no music21 or parallel-fifth/octave analysis. The earlier claim that Coconet measured parallel fifths/octaves with music21 was removed.
- Fang et al. (arXiv 2006.13329v3) builds its grading function with music21 and includes a parallel-errors feature (parallel unisons, fifths, octaves).
- Wang et al. (NotaGen, arXiv 2502.18008v5) reports CLaMP 2 scores and subjective A/B tests; the text contains no voice-leading or parallel-motion analysis.

Removed or reduced because the cited sources were not shown to support them: the claim that evaluation relies "almost entirely" on two approaches, the DeBerardinis2022 "urgency" clause, the Le et al. "shift" claim, the Chen2020 and uncited LLM sentences, the Ji/Zhou "urgent" conclusion, the "standard increasingly recognized" MIR claim with sturm2020, choi2020, the "stagnant harmony" wording, the benefit claiming to prove Strube's operational relevance, and the institutional-positioning benefit.

Still unverified (a citation audit had no web access and worked from memory; check before submission): dong2020 author list (possibly Berg-Kirkpatrick, not Dubnov), fang2020 workshop name (possibly Machine Learning for Media Discovery), le2025 author "Mathieu Keller" (possibly Mikaela Keller), Retkowski2024 arXiv ID, Ji2023 year/article number, harrison2020 and schoenberg1954 page support, strube1928 edition and rule pages. The shared bibliography is a proposal-phase asset and was not edited.

Decisions for the researcher and supervisor:

1. The template's LAMPIRAN items (survey permit, photos, questionnaire) do not fit this study. Candidates: condition manifest, rule-definition sheets, annotation form. No appendix was added.
2. Scope limits sit at the end of I.B.1. A separate *Batasan Penelitian* section would depart from the template.
3. Cover, approval page, and abstracts were preserved unchanged by instruction. They still say *Skripsi* and describe an architectural-paradigm comparison, which the revised BAB I–III no longer claim. Confirm the wording required for a thesis-phase proposal.
4. The template lists only a contents page; the finished-thesis example also lists figures and tables. No lists were added.

### Revision after the researcher's review notes (2026-09-30)

The researcher supplied notes from the v2 tutoring review; they are recorded verbatim with our interpretation in [feedback.md](../supervision/feedback.md) (F01–F08). Changes made:

- Research questions now start with *Bagaimana* (5W1H) and all name Strube's rules. Question 3 asks about the effect of conditioning level on rule adherence; objectives map one-to-one.
- III.A states a quantitative comparative approach, cites the department template's methodology source, and drops the R&D label that mixed research types.
- III.C.1 *Variabel Penelitian* defines X1 (model), X2 (conditioning level), and Y (rule adherence, with per-rule indicators and the composite Strube Score).
- II.C.2 hypotheses match questions 2 and 3; question 1 is answered descriptively.
- II.B.2 names functional harmony as the grand theory, Strube's voice-leading rules as the derived theory, and the operational definitions as their application.
- Verified from the DeepBach paper (arXiv 1612.01010): evaluation by an online "Bach or Computer" discrimination test, and the authors' example analysis notes compositional errors such as parallel octaves. Added to I.A, I.B.1, and II.A.1.
- Added `leedy2018` and `rangkuti2016` to the shared bibliography, using the metadata and paraphrases in the department template's reference list. The books were not opened; confirm edition and pages. The Schoenberg citation for tonic, dominant, and subdominant functions also needs a page.

Title (F01), resolved 2026-09-30: the researcher chose to revise it along the reviewer's "evaluasi musik hasil x" pattern and a clearly quantitative form. The v3 title now lives in `thesis/main.tex.template`, so rebuilding proposals v1/v2 keeps their metadata title. The abstracts still describe the earlier architecture framing and were not edited. Earlier options considered: The current title names LSTM, CNN, and Transformer. Options for the researcher and lecturer:

1. EVALUASI MUSIK SIMBOLIK HASIL GENERASI DEEPBACH, COCONET, DAN NOTAGEN BERDASARKAN KAIDAH HARMONI FUNGSIONAL GUSTAV STRUBE
2. PENGARUH CONDITIONING LEVEL TERHADAP KEPATUHAN KAIDAH HARMONI GUSTAV STRUBE PADA MUSIK SIMBOLIK HASIL GENERASI DEEPBACH, COCONET, DAN NOTAGEN

### Latar belakang structure (2026-09-30)

At the researcher's request, I.A now covers the template's four elements in prose, without headings:

1. Social facts and developments: the Bach Doodle deployment of Coconet (over 55 million harmonization requests in three days) and the DeepBach MuseScore plugin.
2. Model facts, then literature facts: evaluation methods reported for each model, distributional metrics, Fang et al., and the Bach Doodle music21 analysis of parallel fifths and octaves.
3. Field facts: user complaints about parallel motion in the Bach Doodle, the DeepBach authors' note on parallel octaves, and the interface differences between models.
4. Argument: the Strube rule basis, the adherence definition, and the teaching relevance.

All Bach Doodle figures come from the full arXiv text (`huang2019`, reading ledger). The old v2 claim that the 2017 Coconet paper used music21 to count parallel motion mixed up the two Huang et al. papers: the counting is in the 2019 Bach Doodle paper.

### Positionality, formulas, approach, and grand theory (2026-09-30)

The researcher supplied a second set of review points (feedback F09–F12). Changes:

- III.A now states a quantitative approach with Creswell and Creswell (2018) and classifies the questions with Sugiyono's descriptive, comparative, and causal-associative types. It explains why the score-excerpt review does not make the study mixed methods. The model comparison is described as comparative; the conditioning-level question follows experimental logic within each model.
- III.A has a new *Posisi Peneliti* subsection: insider to the Western harmony tradition, outsider to the models, reflexivity in quantitative research, and five bias controls. Blind labelling of model-output validation examples was added to `research/protocol.md` as a planned control.
- III.C *Instrumen Pengukuran* now says the formulas are the researcher's operationalisation of Strube's rules and defines $p_{i,t}$, $K_{\text{tonic}}$, and $L_{\text{pc}}$, which the formulas used without definition.
- II.B.2 names grand, middle, and applied theory levels, the supporting computational theory, and the deductive use of theory.

New bibliography entries: `creswell2018`, `sugiyono2019`, `jamieson2023`, `holmes2020`, `dwyer2009`. The three journal articles were checked against Crossref metadata and abstracts on 2026-09-30. The two books were not opened. Confirm the Creswell definition page and which Sugiyono edition the researcher uses; Sugiyono's classification of question types and definition of experimental method need page numbers from that copy. A web search for common citation practice in Indonesian music theses could not be run in this session, so the choice of Creswell and Sugiyono follows the researcher's suggestion, not a survey.

Pending decision: a pseudocode appendix for the evaluator. Recommended after the instrument decisions in `research/protocol.md` (quantization, fourths in the fifth check, sounding sonorities, score denominator) are settled, so the appendix does not document behaviour that will change.

### Plain-language revision and title length (2026-09-30)

The researcher reports that readers from the art school find the study hard to follow because of unexplained technical terms. Changes at the researcher's request:

- I.A *Latar Belakang* rewritten for readers without a computing background. Each technical term is explained when it first appears (model generatif musik, musik simbolik, MIDI, music21, definisi operasional, tingkat kendali, the score). Architecture and sampling names (LSTM, pseudo-Gibbs and blocked Gibbs sampling, CLaMP-DPO) and "log-likelihood" were moved out of I.A; BAB II still describes them. Facts, figures, and citations are unchanged.
- *Conditioning level* is now *tingkat kendali* throughout BAB I–III; the English term is given once in I.A and in the variable definition. The III.C synonym *tingkat keterbatasan (constraint level)* was replaced by the same term.
- Title shortened from 18 to 15 words: *Evaluasi Musik Hasil AI DeepBach, Coconet, dan NotaGen: Pengaruh Tingkat Kendali terhadap Kepatuhan Kaidah Strube*. "Simbolik", "Generasi", "Harmoni", and "Gustav" were dropped; "AI" was added so readers know what the three names are. Confirm with the lecturer.
- The *Posisi Peneliti* subsection became one paragraph at the end of III.A, without a heading.

The rumusan masalah (I.B.1) still uses some technical terms (log-likelihood, CLaMP 2, checkpoint) and was not rewritten in this pass.

### Literature expansion from OpenAlex (2026-09-30)

At the researcher's request, BAB I–III were expanded with sources screened from the OpenAlex batch `20260930T015029093933Z`. Criteria, inclusions, and exclusions are in `research/literature/screening-2026-09-30.md`.

- 24 new bibliography entries, all 2018–2026 and peer-reviewed. The chapters now cite 49 distinct keys, and all resolve in the build (48-page PDF).
- I.A keeps the plain-language style and adds field growth, how musicians use generative models, evaluation practice, and annotation subjectivity.
- BAB II has new subsections: *Perkembangan Model Generatif Musik Simbolik*, *Evaluasi Penggunaan Model oleh Musisi*, and *Analisis Harmoni Komputasional dan Anotasi*. The theory section adds tonal-harmony corpus evidence, a current functional-harmony theory, cultural familiarity in consonance, and suspensions as rule exceptions.
- BAB III adds interdisciplinarity and Western-data dominance to the positionality paragraph, annotator disagreement to validation, voice separation to quality control, a rule against reading non-significant results as equivalence, and the rationale for measuring all models with one instrument.
- Fixed bibliography errors: `le2025` fourth author is Mikaela Keller; the `Retkowski2024` arXiv ID is 2412.07948. Protected proper nouns in several existing titles.

All new claims were checked against OpenAlex abstracts only. Record page or section support in the reading ledger before submission.

## 2026-10-02 — method reset to a machine-only design

Recorded by the assistant at the researcher's request.

- Did: Re-read Yan et al. (2018) §4 and Huang et al. (2019) §6.3 in the original PDFs; checked DeepBach's dataset split code, Magenta.js Coconet pitch range, music21 9.3.0 voice-leading methods, the When in Rome folder list, and Open Library metadata for Strube (1928). Computed the sample-size rationale with statsmodels.
- Found: Huang et al. define out-of-distribution input as soprano pitches outside MIDI 60–81 or a leap larger than one octave, and used Kruskal–Wallis and Mann–Whitney tests. Yan et al. used sixteenth-note quantization and noted that 4-bar exercises differ in length from training pieces. DeepBach splits its training tensors contiguously (85/10/5) in corpus order without shuffling. The Coconet checkpoint's training split is undocumented. music21 9.3.0 provides `VoiceLeadingQuartet.parallelFifth`, `parallelOctave`, `voiceCrossing`, `voiceOverlap`; the old `theoryAnalyzer` module is absent. Strube's book is not on archive.org.
- Changed and why: The researcher asked for a design traceable to one prior study and for no human evaluation. Rewrote BAB I–III around Huang et al. as the main prior study, with Yan et al. for categories and Strube for rule wording and melodies; changed the title; wrote protocol version 2; added Strube data templates and a defense Q&A file. Research code and the v1 manifest were not changed.
- Next: Read Strube and fill the rule-page template; inventory exercises; type printed examples; get supervisor agreement; implement instrument v2 and run the four validation checks; pilot.

### Method reset decision (moved from PROGRESS.md)

The researcher reported not understanding parts of their own method because several choices had no source: the four conditioning levels A–D, the choice of three rules, the clipped Strube Score, and Strube citations without pages. They asked to base the study on one prior study and, on the same day, ruled out any human evaluation (graders, students, listeners) as too costly for an undergraduate thesis. Manual data gathering, such as inventorying Strube's exercises, remains acceptable.

Decision executed at the researcher's request (2026-10-02):

- Main prior study: Huang et al. (2019), Bach Doodle §6.3. Kept: per-measure P5/P8 counts with music21, the out-of-distribution hypothesis, Mann–Whitney comparisons, Bach rates as reference.
- Extensions: DeepBach added to Coconet; the same melodies given to both models; melody origin (Bach chorale sopranos vs Strube melody exercises) as X2; three more rules from the Yan et al. (2018) rubric that need no chord analysis (upper-voice spacing, crossing, overlap); Bach's own harmonizations as a reference on the same melodies.
- Roles of the sources: Huang = design and measure; Yan = error categories and weights; Strube = rule wording, exceptions, and the textbook melodies.
- Removed: NotaGen (cannot preserve a given melody), conditioning levels A–D, soprano leading-tone rule (the soprano is given, and the rule depended on automatic key detection), the clipped Strube Score (replaced by per-measure rates and a Yan-weighted index).
- Validation without humans: Strube's printed examples as test fixtures, cross-check against music21 `VoiceLeadingQuartet`, comparison with Huang's Bach rates, deterministic reruns.
- Sample: at least 30 melodies per origin group from a power analysis (d = 0.8, α = 0.05, power 0.8, rank-test efficiency ≥ 0.864); five generations per melody per model, averaged.

Files changed in this reset: `thesis/chapters/01-pendahuluan.tex`, `02-tinjauan-pustaka.tex`, `03-metodologi.tex` (rewritten); `thesis/metadata.tex` (title); two sentences of the kata pengantar in `00-frontmatter.tex` (NotaGen and "ketiga model" removed); `research/protocol.md` (version 2); shared bibliography (`yan2018`, `cohen1988`, `hodges1956`); reading ledger; new templates `research/literature/strube-exercise-inventory.csv`, `strube-rule-pages.csv`, `strube-example-fixtures.csv`; new defense preparation file [defense-qa.md](../study/defense-qa.md). Lecturer-feedback impact is recorded in [feedback.md](../supervision/feedback.md).

Abstracts (Indonesian and English) were rewritten for the v2 design at the researcher's request on 2026-10-02 ("benerin semua"). The v1 code, tests, and condition manifest stay unchanged as the historical instrument.

## 2026-10-02 (later) — Strube reading, inventory, instrument v2

Recorded by the assistant at the researcher's request ("benerin semua sampai ready tag v3").

- Did: OCR-ed the supplied 1928 Strube scan (147 pages) and read the rule and exercise pages as images; filled the rule-page, exercise-inventory, and fixture-list CSVs; implemented `research/voice_leading_v2.py` and 20 software checks; ran validation checks 3–5 on the 371 music21 chorales twice; rewrote both abstracts; aligned BAB I–III, protocol, and defense notes with the Strube pages.
- Found: All five rules are stated by Strube, but crossing is allowed "not over the soprano" (p. 174) and overlap is allowed with stepwise motion (pp. 12–13); fifths by contrary motion are "not objectionable" (p. 9). music21's parallel-fifth function also flags contrary-motion fifths (all 69 extra flags on Bach were of that kind). 69 given-soprano exercises in pp. 11–80; p. 48 missing from the scan. Bach rates under Strube definitions: 0.0078 P5, 0.0030 P8 per measure.
- Changed and why: Narrowed crossing to crossing above the soprano and added the stepwise exception to overlap, so that the measured rules follow the cited source. Limited the Strube melody group to exercises before the non-chord-tone chapters, because the instrument cannot apply non-chord-tone exceptions. This is instrument version 2.0; no study data existed under the earlier draft definitions.
- Next: Researcher confirms pages in print, checks p. 48, types melodies and figures; supervisor consultation; adapters and pilot.

### Strube check and instrument v2 (moved from PROGRESS.md)

The researcher supplied a scan of the original edition (`references/The Theory and Use of Chords.pdf`, Oliver Ditson 1928, matching `strube1928`). The assistant OCR-ed it with tesseract and read the rule pages as images.

- All five rules are in Strube: parallel fifths, octaves, and unisons forbidden in strict writing, contrary motion not objectionable (p. 9; Fig. 30 p. 12); spacing S–A up to an octave, occasionally farther, A–T only transiently (p. 20); occasional crossing allowed, "not over the soprano" (p. 174); overlap defined and allowed when one voice moves stepwise (pp. 12–13). Crossing was narrowed to crossing above the soprano and overlap given the stepwise exception, in the manuscript, protocol, and code. Details: `research/literature/strube-rule-pages.csv`.
- Strube has given-bass and given-melody exercises (p. 8). Exercises 1–118 (pp. 8–81) were inventoried: 69 given-soprano candidates, 47 given basses; exercises 67–68 are on p. 48, which is missing from the scan. Later chapters (suspensions onward) were excluded by a stated criterion (non-chord-tone exercises), and the chorale chapter because its melodies are Bach's. `research/literature/strube-exercise-inventory.csv`.
- Instrument v2 implemented in `research/voice_leading_v2.py` with 20 software checks; `make test` runs them. Validation checks 3–5 were run on the music21 Bach chorales; results are in `research/protocol.md` ("Results of checks 3–5"). In brief: no disagreement with music21 on crossing and overlap predicates; music21's extra parallel flags are all contrary-motion cases that Strube allows; Strube-definition Bach rates 0.0078 P5 and 0.0030 P8 per measure (music21 definition 0.0176 and 0.0059, Huang et al. 0.023 and 0.009); identical hashes on repeat runs.
- Citations now print Indonesian page labels ("hlm.") via `\DefineBibliographyStrings` in `thesis/main.tex.template`.

Remaining before the main experiment (none blocks a `thesis/v3` tag for supervisor consultation, because v3 is the research-proposal manuscript):

1. Researcher: confirm the rule pages against the printed book; check p. 48 (exercises 67–68); type the 69 candidate melodies and the nine textbook figures listed in `strube-example-fixtures.csv` into MusicXML.
2. Supervisor agreement on the machine-only design, the title, and the questions.
3. Generation adapters for arbitrary fixed-soprano melodies, plus the pipeline defects in `docs/maintenance.md` (Coconet offsets, run isolation, completion checks); the v1 adapters still hard-code BWV 66.6 and the A–D conditions.
4. Validation check 2 (textbook fixtures) after typing; then the pilot.

### v2 to v3 change record (moved from PROGRESS.md)

The researcher identified the v2 reviewers as Bu Suryati and Pak Galih, lecturers of Seminar Musikologi 2. [perubahan-v2-ke-v3.md](../supervision/perubahan-v2-ke-v3.md) lists every change from `proposal/v2` to v3 and labels its basis: a lecturer note (F01–F12) or a researcher decision made to satisfy those notes. The lecturers did not ask for NotaGen's removal, the A–D replacement, the five-rule set, or the machine-only design; do not attribute those to them.

## 2026-10-02 — BAB I structure

Recorded by the assistant at the researcher's request. Moved from `PROGRESS.md` on 2026-10-03.

### BAB I compared with 2026 reference theses (2026-10-02)

The researcher asked whether BAB I follows the structure used in the approved 2026 theses under the Git-ignored `references/` folder. Compared sources: six S-1 Musik skripsi (Arinii 'Ilmal Haqqi, Cinta Angelica Paradise, Intan Rama Wijaya, Nourmalita Alya Putri, Stanislaus Anata Warnabinarja Sihombing, Yazid Fauzan Ath Thaariq), one S-2 tesis (Benadito Anicheto Manek), and the department's 2026 proposal template. All reference theses are complete five-chapter documents, not proposals.

| Item | References | v3 before this change |
| --- | --- | --- |
| BAB I sections | All: Latar Belakang, Rumusan Masalah, Tujuan, Manfaat. Intan, Nourmalita, and Benadito also have a separate *Pertanyaan Penelitian* after a prose *Rumusan Masalah*. | Template form: B. Rumusan Masalah dan Pertanyaan Penelitian, C. Tujuan dan Manfaat; prose rumusan then a question list (F03). Kept. |
| Sistematika Penulisan | 4 of 6 S-1 skripsi (Arinii, Cinta, Stanislaus, Yazid); absent in the two music-education skripsi and the S-2 tesis; absent in the template. Three of four write it as prose; Arinii uses a numbered list. | Present since `e67901b` (numbered list, BAB I–III). |
| Heading and contents numbering | Template and every reference contents page: A. → 1.; contents lines with dot leaders; "BAB I PENDAHULUAN". | Subsections printed as B.1, C.1; contents showed "A" without a period, "BAB I: PENDAHULUAN", leaders only on subsections. |
| Manfaat | Numbered or lettered sub-items: 1. Manfaat Teoretis / 2. Manfaat Praktis, with a., b. items. | Unnumbered "Manfaat Teoretis:" labels; the label could fall alone at a page end. |
| Latar Belakang length | About 1,570–2,410 words in the S-1 skripsi; template asks for 2–3 pages. | About 1,530 words (6 pages at double spacing). No change. |

Changes made:

- `main.tex.template`: subsections numbered 1., 2. (subsubsections a.), cross-references keep the parent letter (B.1); contents entries use dot leaders and a period after each label (`titletoc`).
- `layout.tex`: contents entry "BAB I PENDAHULUAN" without a colon.
- I.C.2 *Manfaat Penelitian*: a. Manfaat Teoretis / b. Manfaat Praktis with 1), 2) items, wording unchanged.
- I.D *Sistematika Penulisan*: prose, one paragraph per chapter (the Stanislaus form), now matching the actual BAB II and BAB III headings (adds *Evaluasi Penggunaan Model oleh Musisi*, *Posisi Penelitian*, the symbolic-music theory subsection, reliability, and sample quality control).

Open decision for the researcher: the reference Sistematika sections describe all five chapters, because those theses are complete. The v3 Sistematika describes only BAB I–III, which are the chapters present. Add BAB IV and BAB V when those chapters are written, or earlier if the supervisor expects the planned chapters to be described.

Follow-up at the researcher's request (2026-10-02): combined "X dan Y" sections that only held X and Y as subsections were split into separate lettered sections, as in the reference theses (Intan, Nourmalita, Benadito). This departs from the template's combined headings.

- BAB I: A. Latar Belakang, B. Rumusan Masalah, C. Pertanyaan Penelitian, D. Tujuan Penelitian, E. Manfaat Penelitian (1. Manfaat Teoretis, 2. Manfaat Praktis, items a., b.), F. Sistematika Penulisan.
- BAB II: C. Asumsi and D. Hipotesis replace C. Asumsi dan Hipotesis.
- Not changed: III.B *Objek dan Subjek Penelitian* (its subsections are Populasi and Sampel, not the two title terms) and III.C.5 *Validitas dan Reliabilitas Instrumen* (no subsections).
- Section references such as "I.B.1" earlier in this file use the old numbering.

## 2026-10-02 — Indonesian translation of Strube

Recorded by the assistant. Moved from `PROGRESS.md` on 2026-10-03.


The researcher supplied a scan of the Indonesian translation (`references/teori dan penggunaan akor - terjemahan pak gathut.pdf`, 91 pages, no text layer). Its title page reads *Teori dan Penggunaan Akor: Buku Pelajaran Ilmu Harmoni (I)*, translated by A. Gathut Bintarto T., S.Sos., S.Sn., M.A., UPT Perpustakaan ISI Yogyakarta, 2015. The translator's name and degrees match Pembimbing I. The assistant OCR-ed the scan and checked the rule pages as images.

- Coverage: volume I ends near Fig. 147; the 1928 Minor Modes chapter (p. 74 onward), the suspension chapter, and the chorale chapter (p. 174, crossing rule) are not in it.
- Rule pages in the translation: parallels pp. 12–13 and 16, overlap pp. 17–18, spacing p. 27, positions p. 10, fifth exceptions pp. 43–44.
- Three wording differences from the 1928 text: spacing "occasionally even farther" appears as "biasanya dapat lebih jauh" (p. 27); the overlap sentence omits "stepwise" (p. 17); p. 10 adds that the bass should not be higher than the tenor, which the 1928 p. 7 sentence does not say. These are discussion points for the supervisor, not corrections.
- Exercises 67–68 (1928 p. 48, missing from the 1928 scan) appear on translation p. 58 in treble clef. The inventory now lists both as melody candidates (71 in total), with the source noted.

Study guide for the supervisor meeting: [persiapan-pembimbing-1.md](../study/persiapan-pembimbing-1.md). Updated: `defense-qa.md` (Q12, Q28, gap table), `bimbingan-v3.md` (sample count, question 2), the exercise inventory. The manuscript still cites only the 1928 edition; whether to cite the translation is a supervisor question.

## 2026-10-03 — Shared MusicXML input and output

Recorded by the assistant at the researcher's request.

- Did: wrote `research/harmonization_io.py` (IO version 1.0) and `research/tests/test_harmonization_io.py`; added the tests to `make test`. The researcher chose MusicXML as the shared format after comparing it with MIDI, because MIDI loses pitch spelling, fermatas, and reliable key, meter, and voice information.
- Found in the model sources (DeepBach master `6d75cb9`; magenta-js master, read 2026-10-03): Coconet `infill` fills every silent step unless a mask is given, so soprano rests need an explicit mask; it returns one-step notes, so repeated notes in generated voices cannot be recovered; its defaults are 96 iterations and temperature 0.99, not the 20 iterations of the version-1 runner. DeepBach's vocabulary is keyed by spelled names, and an unknown name is silently added with a warning, so the adapter checks the vocabulary first; its output can contain START/END/OOR symbols that its own score writer prints as rests.
- Found in the corpus: music21 pads short measures with rests on MusicXML export. Before the fix, 6 of 345 Bach sopranos changed length (5 final measures, 1 encoded rest measure in *Christ lag in Todesbanden*). The writer now declares the missing time and reads every file back.
- Checked: 27 software checks pass; Bach's own harmonizations of all 345 eligible chorales, rebuilt through the writer, give the same five rule counts and measure counts as the originals. Existing instrument checks still pass. No model was loaded.
- Next: write the protocol-version-2 generation runners on top of the adapters (run directories, attempt log, effective settings), move the Coconet runner into a tracked JavaScript file, and run the pilot.

## Entry fields for your next session

Record the date and author, then what you did, what you found, what you changed and why, and what to resolve next. Include exact source pages, score/example IDs, run/artifact paths, commands, and any supervisor decision. Distinguish an observation from an interpretation or proposed action.
