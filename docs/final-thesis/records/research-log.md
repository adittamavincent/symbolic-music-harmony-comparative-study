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

## 2026-10-03 — Records, study, and supervision files aligned

Recorded by the assistant at the researcher's request.

- Did: compared every file in `supervision/`, `study/`, and `records/` with the manuscript, `research/protocol.md`, and the code; rebuilt the thesis (63 pages) and ran `make test`.
- Found: `feedback.md` described the 2026-09-30 answers (NotaGen, conditioning levels, blind annotation) in its main table and the 2026-10-02 design in a second table. Several files still gave 69 Strube melody candidates instead of 71, 371 chorales where 345 were evaluated, the 32-step Coconet adapter, and old section names (*Asumsi dan Hipotesis*). Defense question 37 said all outputs lack spelling; DeepBach output is spelled, Coconet output is not.
- Changed and why: merged the two `feedback.md` tables into one table of current answers, leaving the original notes unchanged; corrected the counts, section names, and adapter status in `perubahan-v2-ke-v3.md`, `bimbingan-v3.md`, `defense-qa.md`, `persiapan-pembimbing-1.md`, `PROGRESS.md`, `README.md`, and `research/protocol.md`; removed two closed rows from the defense gap table; added defense questions 41a (MusicXML) and 41b (Coconet repeated notes); added two source rows for the model code read on 2026-10-03 to `reading-notes.csv`. Earlier log entries were left as written.
- Next: unchanged from the previous entry.

## 2026-10-03 — Audit of BAB I–III and examiner simulation

Recorded by the assistant at the researcher's request ("audit skripsiku ... simulasikan semua kemungkinan dari dosen penguji ... benahin bab 1 sampai 3").

- Did: read BAB I–III, the department template and the 2026 reference theses in `references/`, `research/protocol.md`, `research/voice_leading_v2.py`, and the study and supervision files; compared the manuscript with the template, the code, and the protocol; rebuilt the thesis.
- Found in the manuscript: I.A ran to six pages and repeated BAB II material (Le, Ji, Yin, Araneda, Fang, Herremans, AI Song Contest, the architecture caveat already in the scope paragraph). I.B repeated the developer-evaluation paragraph of I.A. Question 3 and objective 3 used *terhadap* twice. *Checkpoint* was used without definition or italics. III.B defined the population as harmonizations while the unit of analysis and the sample are melodies. III.B stated that the eligible Strube melodies exceed the 30-melody minimum, although only the 71 candidates are known and eligibility is checked after typing; the same paragraph also gave a contingency for fewer than 30. The Strube group is a census, which the text did not say. The power calculation applied the Hodges–Lehmann bound, which assumes continuous data, without noting zero-heavy rates or the Holm correction. III.C.4 referred to an attached rule-definition sheet, but the manuscript has no appendix. III.C.3 did not mention the Coconet repeated-note limitation. II.B.2 said MIDI output lacks spelling; since IO version 1.0 only Coconet output lacks it. II.B.2 did not explain why functional harmony is the grand theory when the five rules were chosen to avoid functional analysis (defense Q64 already raised this). II.C assumption 3 claimed rules are decidable without chord interpretation although Strube's exceptions need it. III.B called NotaGen text-only while II.A describes period, composer, and instrumentation prompts. Prefixes *antar-*, *non-*, and *multi-* were hyphenated against Indonesian spelling rules.
- Found in the instrument: `evaluate_grids` counts spacing and crossing at every pair event, so a repeated note adds a count and a held note does not. Coconet output cannot contain repeated notes in the lower voices, so its spacing and crossing counts are lower by construction. Parallel and overlap counts are unaffected. Recorded as decision 7 in `PROGRESS.md`; the instrument was not changed.
- Changed and why (manuscript): shortened I.A from 1,527 to 1,116 words by removing material that BAB II covers, merging the two-sentence user-complaint paragraph into the Bach Doodle paragraph, and condensing the annotation-disagreement sentences; facts and figures kept are unchanged. Rewrote the first paragraph of I.B as a gap summary and defined *checkpoint* in the scope paragraph. Reworded question 3 and objective 3 to match the title. II.A: explained *orderless NADE*. II.B.2: added three sentences linking functional harmony to the exceptions the instrument cannot apply; stated that diminished-to-perfect fifths are not counted even when not passing; corrected the augmented-second reason to Coconet's unspelled output. II.C: restated the assumptions so that tests check the operationalisation, not the assumptions. II.D: labelled the three hypotheses as first, second, third. III.A: replaced the paragraph that repeated II.A.6 with one sentence; split the positionality paragraph into interdisciplinarity, positionality and controls, and the Western-norm paragraph. III.B: population as two melody populations with harmonizations as repeated observations; inventory count stated as found; census and limited generalisation stated; power caveats added; NotaGen description aligned with II.A. III.C: named the data-collection steps (document study, generation, automatic measurement); stated that the five indicators are analysed separately; replaced the appendix reference with a table reference; added the shared MusicXML output and the Coconet repeated-note limitation. Joined *antar-*, *non-*, *multi-* prefixes (except *non-Barat*).
- Reverted during the session: a merge of II.C *Asumsi* and II.D *Hipotesis* into one section following the template. The researcher had split them on 2026-10-02 to follow the reference theses (entry above), so the split stands.
- Not changed: abstracts, front matter, title, and the BAB IV and V paragraphs of the Sistematika that appeared in the working tree during the session; `references.bib` edits made outside this session.
- Added: defense questions 79–101 in `study/defense-qa.md` (format, theory, method and statistics, consistency, and questions that will follow BAB IV); decisions 7–10 and a reading-ledger gap in `PROGRESS.md`. Power figures for α = 0.01 (d = 0.8, power 0.8): 38.2 per group two-sided and 32.8 one-sided before the 0.864 adjustment; minimum detectable d ≈ 0.98 with 30 per group (statsmodels, 2026-10-03).
- Checked: `make thesis` builds (63 pages); no undefined references.
- Next: decide the repeated-note treatment before the pilot; search Indonesian sources; record reading for the 29 cited keys without a ledger row.

## 2026-10-04 — Thesis v4: peer review, landasan teori, citations, pipeline

Recorded by the assistant at the researcher's request ("v3 udah locked … bikin v4 … revisi semua yang dimaksud, research beneran, rethink yang di-address di bab 2 … bab 1–3 ready … research experiment ready, don't run yet").

- Did: read the transcript of a peer review call with Manda (`whatsapp-conversation/v3-manda`, outside the repository) and recorded it as P01–P17 in `supervision/review-teman-2026-10-04.md`; checked all 61 bibliography entries against Crossref and OpenAlex; ran the OpenAlex batch with six new queries (q22–q27; 679 records); searched Google Scholar, Garuda, and the ISI repository; read full texts of Hadjeres et al. (2017), Huang et al. (2017, 2019), Choi et al. (2023), Leemhuis et al. (2020), Huron (2001), Pearce et al. (2002), Storkey (2008), Ridhwan and Wisnugraha (2026), and the arXiv version of Briot et al. (2020); OCR-ed the Strube scan again for the preface and p. 6; rewrote BAB I–III; implemented the protocol-2.1 pipeline and its tests; built the v4 PDF.
- Found: two author errors (`choi2023`, `koops2019`) and one wrong DOI (`DeBerardinis2022`); twenty v3 citations supported only by abstracts and not needed. The music21 Riemenschneider iterator lists 371 entries for 350 distinct files, so the 2026-10-02 validation run counted 18 files twice among its 345 entries; rates on distinct files differ only in the fourth decimal. Of the 350 files, 23 are ineligible and 9 repeat another chorale's soprano, leaving 318 melodies; 1 of them lies outside Huang et al.'s limits, so melody origin will mostly not coincide with Huang's out-of-range criterion (already anticipated in the protocol). SciPy 1.15.3 for Python 3.10 no longer loads on this macOS (dyld rejects `_spropack`), so the environment moved to Python 3.12. The protocol's minimum detectable effect for n = 30 is 0.79, not 0.78.
- Changed and why: BAB I (plain explanation of the model task, rules named directly, one-paragraph rumusan masalah, Indonesian source), BAB II (studies discussed with title, method, finding, and relation; comparison table; landasan teori by named experts — Briot et al., Storkey, Pearce et al., Strube, Huron — with a kerangka berpikir figure), BAB III (classification sentence removed, settings and seeds stated, QC and sensitivity analyses aligned with the code), abstract italics and keywords; prose colons removed; 38 cited keys, all verified. Protocol 2.1: settings pinned, duplicate handling, QC additions, sensitivity analysis d, membership verification rule, pilot rule. Pipeline: `melody_text.py`, `melody_sets.py`, `generation_v2.py`, `coconet/run_coconet_v2.js`, `evaluate_v2.py`, `analysis_v2.py`, `run_checks_v2.py`, `deepbach_membership.py`, `scripts/bootstrap_v2.py`, `experiments/scripts/v2.py`, Make targets, 26 tests; 71 typing templates. No model was installed or run.
- Checked: `make test` passes (4 + 20 + 27 + 26); `make dry-run-v2` completes with fake backends; `make thesis` builds 70 pages without LaTeX warnings; lint for prose colons, unitalicized terms, em dashes, and cross-chapter references.
- Next: researcher types the 71 Strube melodies and nine textbook figures; bring `supervision/bimbingan-v4.md` to Pembimbing I; then `make setup-v2`, `make preflight`, `make select`, `make pilot`.

- Follow-up the same day, at the researcher's request: removed I.F *Sistematika Penulisan* (the researcher reported that Manda thought it unnecessary; the template does not require it, and P14 objects to chapter-by-chapter cross-references), removed the remaining within-text references ("dibahas pada subbab berikut", "diuraikan di bawah", "pada akhir subbab ini"), and set the abstract keyword lines without indentation. References to Strube's own book chapters and to tables and figures stay.

## 2026-10-05 — Register edit for P06

Recorded by the assistant at the researcher's request ("yang Bahasa terlalu formal itu aku juga setuju, ayo kita ubah ... in some places, add shuffling for SPOK ... scarce is okay").

- Did: listed P01–P17 against the v4 sources; read BAB I–III in full; loosened about 50 stiff sentences.
- Changed and why: moved mid-sentence "karena itu" and "dengan demikian" (English "therefore" calques, 13 cases) to the front or merged it into "sehingga", varying the connective; replaced several "merupakan" and nominal phrases with plain verbs; rewrote the count-first "dua hal. Pertama ... Kedua ..." in II.A.3; reordered a few sentences to start with the adverbial or a clefted predicate (for example "Yang dievaluasi dalam penelitian ini adalah ...", "Meskipun repertoarnya berbeda, ..."). One meaning fix: Coconet raw outputs are stored "agar pengukurannya dapat diulang" instead of claiming that this guarantees reproducible generation.
- Not changed: terms (including "laju pelanggaran"), citations, numbers, hypotheses, formulas, Strube rule list, abstract and front matter.
- Open from the P01–P17 check: "dataset" is still upright in four places (P02); ask Manda about P03 and have her reread v4 (P17); confirm "sintesis" (P09) and the theory structure (P12) with the supervisor.
- Second pass the same day ("istilah dari terjemahan pak gathut, boleh lah ... yang indo ga lazim itu ... no ai slop harus di gas ... abstrak perlu diubah ... laju pelanggaran pakai opsi satu"):
  - Terms: "laju pelanggaran" became "pelanggaran per birama" in BAB I–III, the figure, the hypotheses, and both abstracts ("violations per measure"); the symbol $L_r$ is unchanged. Unusual Indonesian coinages replaced: *seed*, *temperature*, *loss function*, *pre-training* (English, italic, glossed at first use); "analisis sensitivitas", "anotator", "satuan not seperenam belas", "kejadian yang ditandai", "alat untuk mengarahkan model", "harmoni apa saja yang dianggap sah". *dataset* italicized (closes the P02 leftover).
  - Pak Gathut's translation (OCR of the 2015 scan, pp. 12–18 and 43–44): it uses "Paralel Kuint / Kuint Sejajar", "Paralel Oktaf atau Unison", "tumpang tindih", "sifat sebagai nada lewat", "tidak … murni". The manuscript terms already match; "kuint lewat" became "kuint yang bersifat lewat". "Unisono" kept (KBBI form) although the translation writes "unison".
  - No-AI-slop: the three Landasan Teori closers that repeated "Kerangka ini dipakai untuk menafsirkan hasil pertanyaan penelitian …" now differ; dropped a redundant "bukan hukum mutlak" (II.B) and "bukan sumber data" (III.A); split five "…, sehingga …" sentences in BAB III; "bukan kesalahan yang pasti" became "belum tentu kesalahan".
  - Not changed: study notes (`study/defense-qa.md`, `study/persiapan-pembimbing-1.md`) and `research/protocol.md` still say "laju"; code and CSV names unchanged.
- Checked: `make thesis` builds (69 pages).

## 2026-10-05 — Study notes aligned with v4

Recorded by the assistant at the researcher's request ("setelah v4 jadi, mari kita benerin docs skripsi yang terkait pengembangan diriku ... fact check ... easy language").

- Did: read BAB I–III v4, the four `study/` files, `PROGRESS.md`, `research/protocol.md`, the v3→v4 change record, the peer review, the v4 handout, `feedback.md`, and the reading ledger; checked study-note claims against them and against the code and local outputs.
- Checked: `make thesis` builds 69 pages; `make test` passes (4 + 20 + 27 + 26). Recomputed from `research/outputs/validation_v2/20261002T065120Z/` with each file once (327 files, 5,096 measures): spacing flags 112 S–A and 260 A–T (0.022 and 0.051 per measure; the 345-entry run gave 117 and 283), matching the protocol-2.1 rates. Power figures in defense Q25 and Q94 recomputed with SciPy (25.5/29.5; 38.2/44.2 and 32.8/37.9 at α = 0.01; 63.8/73.8 for d = 0.5; minimum detectable d 0.79 and 0.98 for n = 30). The two hand-count examples (BWV 153.1 m. 6 tenor–bass; BWV 86.6 mm. 9–10 soprano–tenor) re-read with music21: pitches and the B4 fermata as stated.
- Found stale in the study notes: v3 titles and handout (`bimbingan-v3.md`); "laju pelanggaran", "analisis kepekaan", "bilangan acak", "kisi" after the 2026-10-05 term change; Yin et al., MuseGAN, and Anticipation-RNN described as in BAB II although v4 dropped them; Huron described as "not in the manuscript"; Wilcoxon zero handling, the Coconet repeated-note decision, pilot-melody reuse, memorisation (`copy_share`), and per-beat rates (`quarters`) described as undecided or unimplemented although protocol 2.1 settled or implemented them; validation figures from the run that counted 18 files twice; Garuda and the ISI repository described as not searched; "runner generasi belum" in the gap table.
- Changed and why: `study/researcher-guide.md` rewritten in plain Indonesian as the entry point (study in five minutes, the five BAB II theories with analogies and the question each serves, research chain, terms, chapter tasks, status, reading list with the v4 theory sources); `persiapan-pembimbing-1.md` retargeted to v4 and `bimbingan-v4.md` (argument chain with Storkey, Pearce, Huron, Briot; numbers on distinct files; seeds and settings; theory sources to read; checklist); `model-dan-istilah.md` (training data, seed, and implementation rows; Briot's dimensions mapped to the comparison table; theory glossary; v4 terms; M9 and M12); `defense-qa.md` (source roles, gap table, and about thirty answers, keeping Q numbers). Also `README.md` (entry point), `PROGRESS.md` (69 pages), `bimbingan-v4.md` (one term), `feedback.md` (v4 section locations), `peta-versi.tex` (v4 tag commit `48d72e2`, 69 pages).
- Not changed: manuscript, abstract, front matter, `research/protocol.md`, earlier log entries, audit records.
- Next: unchanged from the 2026-10-04 entry. Open wording to settle: the numeric range that makes a Huang gap "explained" (PROGRESS decision 10) is not written anywhere yet.

## 2026-10-06 — First meeting with Pembimbing I; planning v5

Recorded by the assistant at the researcher's request ("setelah bertemu pembimbing 1 pak gathut ... menambahkan konteks untuk draft kita revisi v5 ... apa aja yang perlu kita bahas, perlu pembenahan ... aku perlu ngapain").

- Did: read the machine transcript of the meeting with Pak Gathut (`~/Downloads/transcript.txt`, two speaker labels, about 24 KB; not copied into the repository); read `PROGRESS.md`, `feedback.md`, `bimbingan-v4.md`, the v3→v4 change record, the peer review, BAB I, the study notes, and the protocol; OCR-ed the 1928 Strube scan (PDF pages 7–147, tesseract) and checked page images for the contents, chapter openings, pp. 45, 55, and 174–178.
- Found in the meeting: Pembimbing I asked how strict Strube's staged guide is and whether the models detect the context of an exercise; noted that every Strube exercise has its own purpose in context while the machine treats them alike; asked what Strube is used for and what a random output is for; advised limiting the scope, taking Strube's chorale context only, and making it a case (one sample, run through the machine, then review where it leaves the rules); found comparing two AIs too much for now; said that the useful information for teachers is where errors are likely; gave Mozart's *Musical Joke* as an example of parallels judged in context; said remaining questions belong in the suggestions; welcomed the researcher's idea of combining a rule-based checker with the AI output; left the choice to the researcher. Recorded as G01–G15 in `supervision/feedback.md`. The meeting date is not in the transcript. The researcher also told him that the Seminar Musikologi 2 review had commented on substance only through the title; added to the F review record as the researcher's recollection.
- Found in Strube (1928 scan): the 71 v4 candidate melodies come from ten chapters (Triads 15, First Inversion 5, Second Inversion 6, Modification of Figures 7, Subordinate Chords I 9, Neapolitan Sixth 3, Dominant-Ninth 6, Leading-Tone Seventh 4, Leading-Tone Triad 4, Minor Modes 12), mapped from the inventory pages and the chapter headings; the inventory's `chapter` column is still empty. Rules are stage-dependent in Strube's own text: parallel fifths between IV and II are "perfectly harmless" but avoided "for the present" (p. 45); exercise 76 marks where the Neapolitan sixth is used (p. 55); the Preface considers chords "in regard to their musical environment". "Harmonization of Chorales" (pp. 174–179) gives chorale-specific guidance, a four-voice Model (no. 235), and exercise 236 with ten melodies I–X taken from J. S. Bach; p. 179 is missing from the scan (p. 177 scanned twice), and p. 60 is scanned twice.
- Changed and why: `supervision/feedback.md` (retitled for lecturer and supervisor feedback; G01–G15 with interpretation and consequences; open handout questions listed); new `supervision/rencana-v5.md` (summary, Strube evidence, effect on the v4 design, options A–C with a recommendation for A, a design sketch, chapter-by-chapter changes, questions for both supervisors, ordered tasks, and corrections to the oral explanation); `PROGRESS.md` (status, v5 row, gates G1 and G4, tasks reordered with typing paused, decision 0); `study/defense-qa.md` section M (Q116–Q123); pointers in `bimbingan-v4.md`, `persiapan-pembimbing-1.md`, `researcher-guide.md` §6, `README.md`, `peta-versi.tex`, `research/protocol.md`, and `AGENTS.md`.
- Not changed: manuscript chapters, front matter, abstracts, title, `research/protocol.md` content and `protocol_v2.json`, the Strube inventory, code, and the `thesis/v4` tag. The version number stays v4 until v5 text changes begin.
- Next: researcher decides decision 0 (options A–C) and confirms it with Pembimbing I; records the meeting date; reads Strube pp. 174–179 in print. After the decision: a new protocol version, `perubahan-v4-ke-v5.md`, and the BAB I–III revision.

## 2026-10-08 — Proposed agreement for v5; preparing the Pembimbing II meeting

Recorded by the assistant at the researcher's request ("untuk bimbingan selanjutnya, bener dengan bu yoni ... best effort menjawab semua, celah, dan lain-lain, supaya dapat 1 kesepakatan supaya kita ready v5 ... i need all you recommendations").

- Did: reread the Pembimbing I transcript (`~/Downloads/transcript.txt`); read the Jurusan Musik supervision form (`~/Downloads/FORM BIMBINGAN SKRIPSI vincent.pdf`), the department proposal template (`references/Riset - Template Proposal TA Penelitian 2026 (1).docx`), BAB I–III v4, the protocol, `evaluate_v2.py` outputs, and the study notes; rendered the 1928 scan, PDF pages 136–139 (book pp. 174–178), at 400 dpi.
- Found: the scan of the chorale chapter is embedded at 96 ppi (1122 × 791 px per two-page spread), too coarse to read pitches reliably, so no Bach source was identified from it. Model 235 (pp. 174–176) is complete in the scan: one sharp, a pickup, about 14 measures, seven fermatas, eighth notes in the inner voices; it is the chapter's only melody printed with a four-part harmonization. Exercise 236 melodies I–IX are complete in the scan; X starts on p. 178 and continues on the missing p. 179. The supervision form requires at least 12 consultations with each supervisor before the TA/skripsi exam and is handed in at registration; it carries the v4 title. The template lists "Asumsi (biasanya untuk penelitian kualitatif) / Hipotesis (biasanya untuk penelitian kuantitatif)" and names purposive sampling. `flags.csv` already records measure, beat, and voice pair for every flag, so a location map needs no change to instrument 2.0. One transcript passage not in G01–G15: asked whether the researcher could decide whose rules to use, the reply was roughly "Bisa", e.g. if chorale is treated in another book (attribution uncertain). The form file was created on 6 October at 14:32 and the transcript at 16:18, so the meeting was probably on 6 October; not confirmed.
- Changed and why: new `supervision/rancangan-kesepakatan-v5.md` (one proposed design K1–K14: case study of Model 235 harmonized 100 times by Coconet, instrument 2.0 unchanged plus a chorale context layer mapped to every p. 174 guideline, location map and hot-spot analysis, comparison with Strube's model and Bach, one non-directional location hypothesis, new title and questions; answers to every open question from `rencana-v5.md` §8, `bimbingan-v4.md`, and PROGRESS decisions 1–10; gaps; chapter changes; form and schedule; meeting script; work order); new `supervision/bimbingan-arah-v5.md` (handout and agreement sheet for Pembimbing II, then Pembimbing I; printable copy `scratch/bimbingan-arah-v5.pdf`, 2 pages, built with pandoc and LuaLaTeX from a copy with wider table columns); `study/defense-qa.md` section N (Q124–Q130); `feedback.md` (the unrecorded transcript remark, and that an oral remark is not a written source); pointers in `PROGRESS.md` (status, gates G1 and G9, task 1, decision 0), `README.md`, `rencana-v5.md`, `researcher-guide.md` §6, and `AGENTS.md`; `scripts/build_reading.py` now includes `rencana-v5.md` and both new files in `make reading`.
- Not changed: manuscript, front matter, title in `metadata.tex`, `research/protocol.md` and `protocol_v2.json`, instrument and pipeline code, the Strube inventory, `thesis/v4`. No model was installed or run.
- Next: the researcher reviews K1–K14, marks any disagreement, and takes the handout to Bu Yoni, then to Pak Gathut; records both answers with dates in `feedback.md`. Optional before the meeting: type the Model 235 soprano from the printed book so its Bach source can be matched in the music21 corpus. After agreement: protocol version 3.0, `perubahan-v4-ke-v5.md`, BAB I–III revision.

## 2026-10-08 — Researcher's direction: low-effort v5 design

Recorded by the assistant. Researcher decision, not supervisor feedback: "mending kita pakai punya kita sendiri, masukkan dari pak gathut, kayaknya tidak perlu kita ambil / implementasi semua, mari kita bikin yang lowest effort (no need to parse / write manual many things, fewer is better) so we just go and state our reason so clearly, no celah, still has temuan baru penelitian".

- Did: replaced the Model 235 case design (K1–K14, entry above) with a design that needs no typing and no per-event manual analysis; ran an exploration of instrument v2.0 on Bach's own harmonizations by phrase zone (`research/experiments/scripts/explore_fermata_zone_bach.py`, new; output `research/outputs/exploration/20261008T113017Z/fermata_zone_bach.csv`, Git-ignored); recomputed the paired sample size with SciPy.
- Found: all 318 eligible Bach melodies in the frame have at least one fermata and lie within Coconet's range (MIDI 36–81); 8–57 measures, median 15; fermatas 1–22, median 6. Exploration on Bach (not study data; 318 chorales, main count; fermata zone = motions starting or arriving inside a soprano fermata note, events inside it for vertical rules): overlap 257 of 469 flags (54.8%) in the zone, which holds 17.1% of overlap opportunities (rate ratio 5.88); parallel fifths 11 of 40 (27.5%) vs 17.2% (1.83); parallel octaves 5 of 13 (38.5%) vs 17.2% (3.01); spacing 7 of 360 (1.9%) vs 9.7% (0.18); crossing above the soprano 5 of 50 (10.0%) vs 9.8% (1.02). Bach's violations depend on phrase position. The paired t-test needs 33.4 pairs for d_z = 0.5 (α = 0.05 two-sided, power 0.8); divided by 0.864, 38.6, so 40 melodies; minimum detectable d_z with 40 melodies about 0.49 (ARE-adjusted). Huang et al. (2019, §6.3) state that the Bach Doodle chorale data lacked fermatas (reading notes).
- Changed and why: rewrote `supervision/rancangan-kesepakatan-v5.md` (D1–D10: Coconet only; 40 Bach chorale sopranos from the corpus, seed 20261004, justified by Strube p. 174; five harmonizations each; instrument 2.0 unchanged; Bach's harmonization as paired reference; H1 Coconet vs Bach, H2 fermata zone vs inside the phrase; a G01–G15 table of what is used and what is not, with three stated departures; questions it must answer; remaining manual work; chapter changes; meeting script) and `supervision/bimbingan-arah-v5.md` (rebuilt `scratch/bimbingan-arah-v5.pdf`, 2 pages); `study/defense-qa.md` section N rewritten (Q124–Q130); pointers in `PROGRESS.md` (status, gate G1, tasks 2–4, decision 0 and the fate of decisions 1–10), `README.md`, `rencana-v5.md`, `feedback.md`, and `AGENTS.md`.
- Not changed: manuscript, title in `metadata.tex`, protocol files, instrument and pipeline code. No model installed or run.
- Next: the researcher takes the handout to Bu Yoni, then to Pak Gathut, who must agree explicitly to the three departures from his advice. After agreement: protocol version 3.0, Coconet-only pipeline with 40 melodies, fermata-zone counting in the evaluation with software tests, H1 and H2 analysis, a drafted set of the nine textbook fixtures for the researcher to check, and the BAB I–III revision.

## 2026-10-08 — Researcher's direction: stay close to v4

Recorded by the assistant. Researcher decisions, not supervisor feedback, in three messages: keep two models ("aku tadi tuh kepikiran supaya tetep 2 model ... reduksi yang dimaksud pak gathut di v5 ini tuh tetep pakai 2 model, tapi bukan all"); a framing in which Bach's practice and the models' output are both read with Strube's rules ("kita mau menemukan apakah dari melodi bach sendiri ada kaidah, terus hasil dari ai ... kita menilai keduanya"); and finally "kayaknya ga perlu banyak jauh dari v4 kemarin, masukkan dari gathut ambil beberapa aja yang masuk akal".

- Did: rewrote `supervision/rancangan-kesepakatan-v5.md` as v4 with four changes, rewrote `supervision/bimbingan-arah-v5.md` and rebuilt `scratch/bimbingan-arah-v5.pdf` (2 pages), rewrote `study/defense-qa.md` section N (Q124–Q130), and updated the pointers in `PROGRESS.md`, `README.md`, `rencana-v5.md`, and `AGENTS.md`. Ideas offered in chat but not adopted: Bach's own rule profile as a separate research question, inherited vs new violations, a chance baseline for parallels, Coconet temperature, a given bass, and DeepBach with and without fermata information (kept in the proposal as an optional addition if a manipulated variable is requested).
- Proposal: DeepBach and Coconet with the v4 settings; 40 Bach chorale sopranos from the music21 corpus drawn with seed 20261004 among melodies both models accept, nothing typed (Strube states that his chorale exercises are Bach melodies, p. 174); five harmonizations per melody per model (400); questions 1–2 and H1 as in v4; question 3 and H2 on violation rates in the fermata zone vs inside the phrase per model, with Bach's pattern described from the same melodies; Storkey and the Mann–Whitney origin tests dropped; sensitivity analyses a–d kept; title *Evaluasi Musik Hasil AI DeepBach dan Coconet: Kepatuhan dan Letak Pelanggaran Kaidah Gerak Suara Strube pada Harmonisasi Chorale*. From G01–G15, all are used except G07 (one model, one sample), with G09 and G12 in part. The sample size of 40 follows the paired calculation already in protocol 2.1 for question 2 (about 39 pairs for d_z = 0.5).
- Not changed: manuscript, title in `metadata.tex`, protocol files, instrument and pipeline code. No model installed or run.
- Next: the researcher takes the handout to Bu Yoni, then to Pak Gathut, who must agree explicitly to keeping two models; records both answers with dates in `feedback.md`. After agreement: protocol version 3.0, pipeline without the Strube group and with a 40-melody Bach sample, fermata-zone counting in the evaluation with software tests, the H2 analysis, the nine textbook fixtures drafted for the researcher to check, and the BAB I–III revision with `perubahan-v4-ke-v5.md`.

## 2026-10-08 to 2026-10-09 — Thesis v5 drafted (protocol 3.0)

Recorded by the assistant. Researcher request: "oke, gas! aku mau final v5 let's go! nanti aku pertimbangkna lagi". The v5 text follows the direction of the previous entry and was written before the supervisors agreed to it; the app was closed once during the work and the work resumed on 2026-10-09 from the saved files.

- Did: wrote protocol 3.0 (`research/protocol.md`, Version 3.0; `research/experiments/protocol_v3.json`, now the pipeline default; `protocol_v2.json` unchanged); added `research/phrase_zones.py` and fermata-zone columns in `evaluate_v2.py` (per generation, per melody as sums, Bach reference, zone of every flag); added the question-3 zone test, Bach zone pattern, LaTeX tables, and zone figure to `analysis_v2.py`, keeping the 2.1 origin test for runs made under 2.1; changed sample selection in `experiments/scripts/v2.py` (40 Bach melodies, 3 pilot melodies outside the sample; 2.1 behaviour kept) and the dry run (origins from the protocol); refactored the exploration script to use `phrase_zones.py` (same numbers as before); revised the manuscript (title in `metadata.tex`, version v5 in `main.tex.template`, BAB I–III, the design sentences and keywords of both abstracts); wrote `supervision/perubahan-v4-ke-v5.md`; updated `PROGRESS.md`, `README.md`, `feedback.md` (a v5 note under the F table), `peta-versi.tex`, `study/researcher-guide.md` (sections 1, 2, 6), `study/defense-qa.md` (opening, source roles, gap table), `study/model-dan-istilah.md` (one sentence), `research/README.md`, the Makefile help and submission name, `scripts/build_reading.py`, and `AGENTS.md`.
- Checked: `make test` passes (4 + 20 + 27 + 32; the pipeline suite gained checks for phrase zones adding up to the instrument totals, zone sorting on a constructed score, zone rates, Bach-only selection with a disjoint pilot, the 2.1 path, and the 40-pair minimum detectable effect of 0.49); `make dry-run-v2` completes with fake backends (q2 6 rows, q3 zone 10 rows, no origin rows); `make thesis` builds 68 pages, and a manual build of the same source shows no LaTeX warnings, no overfull boxes, and no undefined references (163 underfull-box messages from the inherited layout); the cover, the Kerangka Berpikir figure, and equation 5 were checked as page images; `make map` builds 5 pages with the v5 box readable. The v5 chapters cite 36 keys; `storkey2008` and `sugiyono2019` are no longer cited.
- Found: a `git stash` used to compare Ruff counts staged three new untracked files on `git stash pop`; they were unstaged again with `git restore --staged`, contents unchanged. Ruff reports 47 findings in `research/` both before and after the changes; the files changed here are clean.
- Not changed: instrument 2.0 (`voice_leading_v2.py`), IO 1.0, the Strube inventory and typing templates, cover wording other than the title, the approval page layout, kata pengantar, and the `thesis/v3` and `thesis/v4` tags. No model installed or run; no `thesis/v5` tag.
- Next: the researcher reviews the v5 text and takes `supervision/bimbingan-arah-v5.md` to Bu Yoni, then to Pak Gathut; supervisor answers go to `feedback.md` with dates; adjust v5 if they ask; then commit, review, and tag `thesis/v5`. Still open: the nine textbook fixtures (validation check 2), the Huang-gap range for protocol check 4, and the parts of `defense-qa.md` A–L that still answer v4.

## 2026-10-09 — v5 text trimmed toward v4

Recorded by the assistant. Researcher instruction: "no need change so much from v4". Design unchanged (v4 with four changes); only the added wording was reduced.

- Changed: BAB I, the context paragraph cut to two sentences (Strube p. 174), and the sentences on DeepBach and Coconet fermata input and the extra benefit clause removed; BAB II, the Briot addition reduced to one sentence in the existing paragraph, the Yan et al. sentence on Bach as practice reference removed, the stage and chorale paragraph cut from seven sentences to four, the Kerangka Berpikir text and the second hypothesis paragraph shortened, and one figure node simplified; BAB III, the zone paragraph's closing sentences cut to one, the `copy_share` sentence in the analysis removed, and the sentence on figures and discussion examples restored to the v4 wording. `perubahan-v4-ke-v5.md`, `PROGRESS.md`, and `study/researcher-guide.md` follow.
- Measured against `thesis/v4` (word-level diff): words kept 93% (BAB I), 90% (BAB II), 88% (BAB III); new words 129, 290, and 458 (before the trim 225, 473, and 536). Most removed v4 words belong to the Strube exercise group, Storkey, the origin hypotheses, and the two-group power analysis.
- Checked: `make thesis` 67 pages; a manual build of the same source shows no LaTeX warnings, overfull boxes, or undefined references (155 underfull-box messages); `make test` passes (4 + 20 + 27 + 32); `make dry-run-v2` complete. No model run.
- Next: unchanged from the entry above.

## 2026-10-09 — v5 title limited to 15 words; flow check

Recorded by the assistant. Researcher instruction: "ingat di memori, judul max 15 kata! ubah semua v5! harus bener. semua perubahan harus make sense in a way yang juga memudahkan alur skripsi".

- Found: the v5 title had 18 words and the v4 title 16 (every token counted, including "AI", "dan", and the model names).
- Changed: title (`metadata.tex`, printed on the cover, submission, and approval pages) to *Evaluasi Musik Hasil AI DeepBach dan Coconet: Kepatuhan Kaidah Gerak Suara Strube pada Harmonisasi Chorale* (15 words). "Kepatuhan kaidah gerak suara" covers all three questions; "Harmonisasi Chorale" is also the name of Strube's chapter that sets the context. Flow fixes: BAB I, the design paragraph introduces the chorale melodies through Strube's chapter, and the fermata-as-cadence sentence moved to the paragraph on where violations fall; the rumusan masalah no longer asks whether Huang et al.'s out-of-distribution pattern recurs (v5 does not test it) and now states the gap in the terms of the three questions; the opening sentence of both abstracts changed for the same reason; BAB II links the stage-dependent rules to the single context with "Karena itu", defines "zona fermata" at its first use, and explains "pelanggaran per kesempatan" before the hypotheses; BAB III uses "pelanggaran per kesempatan" instead of "laju pelanggaran" (the v4 term decision) and lists it among the data. Title also updated in `rancangan-kesepakatan-v5.md`, `bimbingan-arah-v5.md` (PDF rebuilt, 2 pages), `perubahan-v4-ke-v5.md`, `feedback.md`, and `PROGRESS.md`; practice question Q131 added. Two memory notes saved (title limit; revisions keep the thesis chain aligned).
- Checked: `make thesis` 67 pages; manual build without LaTeX warnings, overfull boxes, or undefined references. Against `thesis/v4`: words kept 91%, 90%, 88%; new words 151, 323, 467.
- Next: unchanged.

## Entry fields for your next session

Record the date and author, then what you did, what you found, what you changed and why, and what to resolve next. Include exact source pages, score/example IDs, run/artifact paths, commands, and any supervisor decision. Distinguish an observation from an interpretation or proposed action.
