# v3: final-thesis progress

Updated: 2026-10-02. Active manuscript: `thesis/`. Status: method reset to a machine-only design (protocol version 2); BAB I–III rewritten; not ready for submission.

## Continuity

| Revision | Academic phase | Evidence/status |
| --- | --- | --- |
| v1 | Proposal | Existing `proposal/v1` tag |
| v2 | Proposal | Existing `proposal/v2` tag; researcher reports lecturer review during in-class, one-to-one tutoring |
| v3 | Final thesis continuing from v2 | Active manuscript and research plan; future milestone name `thesis/v3`; no tag or completed main experiment yet |

The lecturer comments, review date, submission deadline, and current department guide have not been provided. Record comments in [feedback.md](feedback.md) before attributing any methodological revision to a lecturer.

## Method reset, 2026-10-02 (current design)

The researcher reported not understanding parts of their own method because several choices had no source: the four conditioning levels A–D, the choice of three rules, the clipped Strube Score, and Strube citations without pages. They asked to base the study on one prior study and, on the same day, ruled out any human evaluation (graders, students, listeners) as too costly for an undergraduate thesis. Manual data gathering, such as inventorying Strube's exercises, remains acceptable.

Decision executed at the researcher's request (2026-10-02):

- Main prior study: Huang et al. (2019), Bach Doodle §6.3. Kept: per-measure P5/P8 counts with music21, the out-of-distribution hypothesis, Mann–Whitney comparisons, Bach rates as reference.
- Extensions: DeepBach added to Coconet; the same melodies given to both models; melody origin (Bach chorale sopranos vs Strube melody exercises) as X2; three more rules from the Yan et al. (2018) rubric that need no chord analysis (upper-voice spacing, crossing, overlap); Bach's own harmonizations as a reference on the same melodies.
- Roles of the sources: Huang = design and measure; Yan = error categories and weights; Strube = rule wording, exceptions, and the textbook melodies.
- Removed: NotaGen (cannot preserve a given melody), conditioning levels A–D, soprano leading-tone rule (the soprano is given, and the rule depended on automatic key detection), the clipped Strube Score (replaced by per-measure rates and a Yan-weighted index).
- Validation without humans: Strube's printed examples as test fixtures, cross-check against music21 `VoiceLeadingQuartet`, comparison with Huang's Bach rates, deterministic reruns.
- Sample: at least 30 melodies per origin group from a power analysis (d = 0.8, α = 0.05, power 0.8, rank-test efficiency ≥ 0.864); five generations per melody per model, averaged.

Files changed in this reset: `thesis/chapters/01-pendahuluan.tex`, `02-tinjauan-pustaka.tex`, `03-metodologi.tex` (rewritten); `thesis/metadata.tex` (title); two sentences of the kata pengantar in `00-frontmatter.tex` (NotaGen and "ketiga model" removed); `research/protocol.md` (version 2); shared bibliography (`yan2018`, `cohen1988`, `hodges1956`); reading ledger; new templates `research/literature/strube-exercise-inventory.csv`, `strube-rule-pages.csv`, `strube-example-fixtures.csv`; new defense preparation file [defense-qa.md](defense-qa.md). Lecturer-feedback impact is recorded in [feedback.md](feedback.md).

Abstracts (Indonesian and English) were rewritten for the v2 design at the researcher's request on 2026-10-02 ("benerin semua"). The v1 code, tests, and condition manifest stay unchanged as the historical instrument.

### Strube check and instrument v2 (2026-10-02, same day)

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

### v2 to v3 change record (2026-10-02)

The researcher identified the v2 reviewers as Bu Suryati and Pak Galih, lecturers of Seminar Musikologi 2. [perubahan-v2-ke-v3.md](perubahan-v2-ke-v3.md) lists every change from `proposal/v2` to v3 and labels its basis: a lecturer note (F01–F12) or a researcher decision made to satisfy those notes. The lecturers did not ask for NotaGen's removal, the A–D replacement, the five-rule set, or the machine-only design; do not attribute those to them.

## What is evidenced now

- The repository contains three generation adapters, one condition manifest, an evaluator, four executable software checks, and draft BAB I–III following the department's 2026 research-proposal outline.
- The four existing checks passed on 2026-09-28 before the folder move. They exercise specific cases; they do not establish full instrument validity.
- The Bach fixture, forced to tonic C by the test, returned score `0.7568`, 6 fifth flags, 0 octave flags, and 3 leading-tone flags. The deliberately parallel fixture returned score `0.0`, 14 fifth flags, 7 octave flags, and 0 leading-tone flags. These are outputs of the current, unvalidated instrument.
- At the start of this preparation, the local `outputs/` contained dry-run metadata only. No local generated MIDI dataset, master results, or summary CSV was found. These metadata files have been preserved under `research/outputs/`. Data outside this checkout have not been inspected.
- A timing probe with note onsets `0, 0.25, 0.5, 1, 2` showed that `quantize([0.25])` moved all five to zero and made their durations four beats. With `[4]`, this probe preserved the requested quarter-beat offsets/durations. The instrument needs an explicit grid decision and regression checks.

## Completion gates

These are this project's proposed completion criteria. Confirm department requirements with the supervisor.

| Gate | Evidence needed to close it | Current status | Researcher action |
| --- | --- | --- | --- |
| G1. Feedback and scope | Actual review notes, agreed questions/title, deadline, department guide | Waiting for input | Supply notes and confirm scope with supervisor |
| G2. Literature | Read core sources; every retained claim mapped to a source page/section; search log supports the stated gap | Partial source verification only | Complete [reading notes](reading-notes.csv) |
| G3. Instrument | Strube edition/pages for the five rules, exceptions, v2 definitions implemented, Strube example fixtures pass, music21 cross-check, Huang Bach-rate comparison | Mostly done 2026-10-02: pages found, v2 implemented and tested, checks 3–5 run; textbook fixtures pending | Confirm pages in print; type the nine figures |
| G4. Comparative protocol | Melody inventory and eligibility, Bach sample seed, model revisions and checksums, generation settings, frozen analysis plan | Open; protocol version 2 drafted 2026-10-02 | Inventory Strube; confirm with supervisor; freeze before main generation |
| G5. Pipeline integrity | Timing conversion fixed, quality exclusions applied, isolated runs, failed-file/count checks, reproducible records | Open | Work through [maintenance findings](../maintenance.md#research-correctness) before main generation |
| G6. Pilot | Both models process melodies from both groups, preserve the soprano, and pass quality control; pilot kept separate | Not run here | Record failures and limits; do not select favourable outputs |
| G7. Main data and analysis | Frozen protocol, raw artifacts, all attempts, actual eligible counts, run-specific analysis and figures | Not run here | Collect and review the agreed dataset |
| G8. Final manuscript | BAB I–III match executed methods; results and conclusion chapters, added after main data, cite measured artifacts and answer the questions; abstracts and appendices complete | BAB I–III working draft; results/conclusion chapters not yet written | Review interpretations and write conclusions from data |
| G9. Submission and defense | Department checklist, checked PDF, supervisor review, evidence archive, final presentation if required | Not ready | Confirm local requirements and rehearse the defense |

## Decisions that must be made before main data

Current list (protocol version 2):

1. Strube edition and volume, and whether all five rules and enough melody exercises are in it.
2. Contingency if fewer than 30 (or fewer than about 10) eligible Strube melodies exist; see the risk table in `research/protocol.md`.
3. Maximum melody length both models can process, and how the Coconet adapter handles full-length melodies.
4. Confirmation that DeepBach's pretrained resources used the default contiguous split, so training membership of Bach melodies can be recorded.
5. Freeze definitions, generation settings, the Bach sample seed, and the analysis plan before main generation.

The earlier list (2026-09-28) asked whether to compare named pipelines or architectures, whether to keep NotaGen, which score to use, how to treat leading-tone contexts, and what the observation unit is. Protocol version 2 answers these: named pipelines only; NotaGen removed; per-measure rates plus a Yan-weighted index; leading-tone rule removed; the melody is the unit.

## This preparation changed

- Recorded v1/v2 proposal history and the continuing v3 final-thesis phase.
- Moved research ownership to `research/` while retaining root CLI/import compatibility entry points.
- Added a researcher guide, feedback record, reading ledger, and protocol worksheet.
- Replaced unsupported chapter 4/5 outcomes with an explicit evidence boundary and completion prompts.
- Corrected the thesis cover's proposal wording and added chapter divisions and a contents page. Department format approval remains open.
- Following the researcher's correction, removed draft/status text from the front matter and restored the previous approval-page and abstract wording. Readiness is tracked in project documentation.
- Adapted the front-matter sequence from a 2026 S-1 Musik ISI Yogyakarta skripsi (`references/ARINII 'ILMAL HAQQI_2026_BAB I.pdf`): submission page, approval-page wording with blank examination date, statement page, lists of figures and tables, and a Sistematika Penulisan section in BAB I. Still open: daftar lampiran once appendices exist, the approval-page signatory roles (the reference uses Pembimbing I/II, Cognate, and Koordinator Prodi), and supervisor confirmation of the format.
- Added motto, halaman persembahan, and kata pengantar pages, placed between the statement page and the abstract as in the 2026 reference skripsi (Intan Rama Wijaya, Arinii 'Ilmal Haqqi, Yazid Fauzan Ath Thaariq), and listed every front-matter page in the table of contents. The text was drafted by Claude at the researcher's request; the motto is unattributed original wording, and the personal details in the dedication and kata pengantar still need the researcher's review.
- Corrected the thesis committee after the researcher's clarification (2026-10-02): Pembimbing I A. Gathut Bintarto Triprasetyo, Pembimbing II Veronica Yoni Kaestri, Koordinator/Ketua Program Studi Musik Kustap, Dekan FSP Dr. I Nyoman Cau Arsana (confirmed by the researcher). Full names and NIPs come from the Prodi Musik staff page (musik.isi.ac.id/education/staff-pengajar/, retrieved 2026-10-02). Thesis metadata (title, researcher, institution, dates, committee) now lives in the tracked `docs/final-thesis/thesis/metadata.tex` instead of `.env.local`, so each thesis commit rebuilds with its own metadata; proposal builds still read `.env.local`. The approval page now follows the Prodi Musik reference layout: Pembimbing I/Ketua, Pembimbing II/Anggota, Cognate/Anggota stacked in one offset column, then Dekan Fakultas Seni Pertunjukan and Koordinator Program Studi S-1 Musik side by side under "Mengetahui,", with Kode Prodi 91221 (matching the 2026 Prodi Musik approval pages in `references/`). The researcher supplied NUPTKs for the dean (3439749650131083) and Kustap (5033745646137003), and the approval page prints those two as NUPTK, as the 2026 reference pages do. Pembimbing I, Pembimbing II, and Cognate still print NIPs because their NUPTKs are not yet known. Unconfirmed: Adityo Legowo as Cognate (carried over from the former Penguji II field) and Eki Satria as Dosen Pembimbing Akademik (from the `ADVISOR_ACADEMIC` field).

No main experiment, statistical finding, lecturer approval, Git milestone tag, or submission has been created by these changes. See the final verification entry in [maintenance.md](../maintenance.md) for checks actually run after the move.

## Manuscript presentation preference

The researcher requests a final-thesis manuscript with ordinary academic prose. Version v3 identifies the revision. Do not insert draft labels, readiness notices, writing instructions, or repository-status reports into the cover, front matter, or chapters. Keep outstanding work in this progress record and the protocol worksheet.

Editorial work items removed from the manuscript remain recorded here:

### 02-tinjauan-pustaka.tex

```tex
Kontribusi yang direncanakan adalah perbandingan keluaran model menggunakan kaidah gerak suara yang dirumuskan dari Strube. Klaim bahwa belum ada studi dengan kombinasi model dan instrumen yang sama memerlukan penelusuran literatur yang terdokumentasi. Catatan pencarian harus menjelaskan basis data, kata kunci, tanggal pencarian, sumber yang diperiksa, dan batas pencarian sebelum kebaruan dinyatakan dalam naskah final.
```

### 03-metodologi.tex

```tex
Bab ini memuat rancangan yang diwarisi dari proposal v2. Pada draf \thesisversion, rancangan tersebut belum menjadi laporan metode yang telah dilaksanakan. Kesetaraan kondisi antar-model, definisi skor, validasi instrumen, jumlah sampel, dan rencana analisis masih menunggu penetapan. Bagian-bagian berikut harus direkonsiliasi dengan protokol akhir sebelum pengumpulan data utama.
```

### 04-hasil-pembahasan.tex

```tex
Bab ini merupakan draf skripsi \thesisversion. Dataset utama dan analisis komparatif belum tersedia dalam repositori yang diperiksa pada 28 September 2026. Target 120 berkas MIDI pada proposal merupakan rencana pengumpulan data, bukan jumlah sampel yang telah dievaluasi. Hasil pengujian perangkat lunak berikut dicantumkan untuk mendokumentasikan keadaan instrumen awal.
```

### 04-hasil-pembahasan.tex

```tex
Bagian ini belum dapat dilaporkan. Setelah protokol ditetapkan dan pengumpulan data selesai, cantumkan identitas setiap model dan checkpoint, kondisi yang benar-benar dijalankan, jumlah percobaan, keluaran yang berhasil dibuat, kegagalan konversi, sampel yang memenuhi kriteria, dan alasan eksklusi. Jumlah aktual harus dapat ditelusuri ke log dan berkas mentah setiap run.
```

### 04-hasil-pembahasan.tex

```tex
Tabel dan grafik komparatif belum dibuat karena data utama belum tersedia. Penyajian hasil harus mencakup jumlah sampel yang layak dianalisis, jumlah serta laju penandaan setiap kaidah dengan penyebutnya, distribusi skor per kondisi yang didukung, dan ketidakpastian pengukuran. Uji statistik hanya dilaporkan apabila sesuai dengan unit analisis dan ketergantungan antar-sampel pada protokol akhir.
```

### 04-hasil-pembahasan.tex

```tex
Pembahasan menunggu hasil utama dan pemeriksaan contoh partitur. Kaitkan setiap interpretasi dengan tabel, run, dan lokasi musikal yang dapat diperiksa. Bedakan penandaan algoritmis dari penilaian kontekstual atas gerak suara. Perbandingan ketiga model harus mempertimbangkan perbedaan data latih, checkpoint, antarmuka kendali, prosedur generasi, dan keberhasilan penguraian MIDI. Desain yang ada belum dapat mengisolasi pengaruh arsitektur dari faktor-faktor tersebut.

```

### 05-kesimpulan-saran.tex

```tex
Kesimpulan empiris belum dapat ditarik karena pengumpulan dan analisis data utama belum selesai. Pengujian perangkat lunak pada Bab IV mendokumentasikan perilaku instrumen awal; hasil tersebut belum menjawab rumusan masalah tentang perbandingan model maupun pengaruh kondisi generasi.
```

### 05-kesimpulan-saran.tex

```tex
Setelah analisis selesai, bagian ini harus menjawab setiap rumusan masalah dengan merujuk hasil yang dilaporkan pada Bab IV. Pernyataan tentang perbedaan statistik, penurunan pelanggaran, atau ketepatan instrumen memerlukan bukti yang sesuai. Jika data tidak mendukung perbedaan atau perbandingan tertentu, laporkan batas tersebut. Perbedaan keluaran model tidak boleh diatribusikan pada arsitektur semata dalam desain yang juga berbeda pada data latih dan antarmuka kendali.
```

### 05-kesimpulan-saran.tex

```tex
Saran akhir akan disusun berdasarkan keterbatasan yang ditemukan selama penelitian. Kemungkinan pengembangan yang perlu ditinjau setelah analisis meliputi pemeriksaan resolusi nada penuntun pada suara lain, validasi konteks musikal, dan perbandingan model dengan tugas serta data latih yang lebih terkendali. Usulan tersebut merupakan arah kerja yang perlu dinilai dari temuan, bukan hasil yang telah dibuktikan oleh penelitian ini.

```

## Outline change to BAB I–III (2026-09-30)

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

## Revision after the researcher's review notes (2026-09-30)

The researcher supplied notes from the v2 tutoring review; they are recorded verbatim with our interpretation in [feedback.md](feedback.md) (F01–F08). Changes made:

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

## Latar belakang structure (2026-09-30)

At the researcher's request, I.A now covers the template's four elements in prose, without headings:

1. Social facts and developments: the Bach Doodle deployment of Coconet (over 55 million harmonization requests in three days) and the DeepBach MuseScore plugin.
2. Model facts, then literature facts: evaluation methods reported for each model, distributional metrics, Fang et al., and the Bach Doodle music21 analysis of parallel fifths and octaves.
3. Field facts: user complaints about parallel motion in the Bach Doodle, the DeepBach authors' note on parallel octaves, and the interface differences between models.
4. Argument: the Strube rule basis, the adherence definition, and the teaching relevance.

All Bach Doodle figures come from the full arXiv text (`huang2019`, reading ledger). The old v2 claim that the 2017 Coconet paper used music21 to count parallel motion mixed up the two Huang et al. papers: the counting is in the 2019 Bach Doodle paper.

## Positionality, formulas, approach, and grand theory (2026-09-30)

The researcher supplied a second set of review points (feedback F09–F12). Changes:

- III.A now states a quantitative approach with Creswell and Creswell (2018) and classifies the questions with Sugiyono's descriptive, comparative, and causal-associative types. It explains why the score-excerpt review does not make the study mixed methods. The model comparison is described as comparative; the conditioning-level question follows experimental logic within each model.
- III.A has a new *Posisi Peneliti* subsection: insider to the Western harmony tradition, outsider to the models, reflexivity in quantitative research, and five bias controls. Blind labelling of model-output validation examples was added to `research/protocol.md` as a planned control.
- III.C *Instrumen Pengukuran* now says the formulas are the researcher's operationalisation of Strube's rules and defines $p_{i,t}$, $K_{\text{tonic}}$, and $L_{\text{pc}}$, which the formulas used without definition.
- II.B.2 names grand, middle, and applied theory levels, the supporting computational theory, and the deductive use of theory.

New bibliography entries: `creswell2018`, `sugiyono2019`, `jamieson2023`, `holmes2020`, `dwyer2009`. The three journal articles were checked against Crossref metadata and abstracts on 2026-09-30. The two books were not opened. Confirm the Creswell definition page and which Sugiyono edition the researcher uses; Sugiyono's classification of question types and definition of experimental method need page numbers from that copy. A web search for common citation practice in Indonesian music theses could not be run in this session, so the choice of Creswell and Sugiyono follows the researcher's suggestion, not a survey.

Pending decision: a pseudocode appendix for the evaluator. Recommended after the instrument decisions in `research/protocol.md` (quantization, fourths in the fifth check, sounding sonorities, score denominator) are settled, so the appendix does not document behaviour that will change.

## Plain-language revision and title length (2026-09-30)

The researcher reports that readers from the art school find the study hard to follow because of unexplained technical terms. Changes at the researcher's request:

- I.A *Latar Belakang* rewritten for readers without a computing background. Each technical term is explained when it first appears (model generatif musik, musik simbolik, MIDI, music21, definisi operasional, tingkat kendali, the score). Architecture and sampling names (LSTM, pseudo-Gibbs and blocked Gibbs sampling, CLaMP-DPO) and "log-likelihood" were moved out of I.A; BAB II still describes them. Facts, figures, and citations are unchanged.
- *Conditioning level* is now *tingkat kendali* throughout BAB I–III; the English term is given once in I.A and in the variable definition. The III.C synonym *tingkat keterbatasan (constraint level)* was replaced by the same term.
- Title shortened from 18 to 15 words: *Evaluasi Musik Hasil AI DeepBach, Coconet, dan NotaGen: Pengaruh Tingkat Kendali terhadap Kepatuhan Kaidah Strube*. "Simbolik", "Generasi", "Harmoni", and "Gustav" were dropped; "AI" was added so readers know what the three names are. Confirm with the lecturer.
- The *Posisi Peneliti* subsection became one paragraph at the end of III.A, without a heading.

The rumusan masalah (I.B.1) still uses some technical terms (log-likelihood, CLaMP 2, checkpoint) and was not rewritten in this pass.

## Literature expansion from OpenAlex (2026-09-30)

At the researcher's request, BAB I–III were expanded with sources screened from the OpenAlex batch `20260930T015029093933Z`. Criteria, inclusions, and exclusions are in `research/literature/screening-2026-09-30.md`.

- 24 new bibliography entries, all 2018–2026 and peer-reviewed. The chapters now cite 49 distinct keys, and all resolve in the build (48-page PDF).
- I.A keeps the plain-language style and adds field growth, how musicians use generative models, evaluation practice, and annotation subjectivity.
- BAB II has new subsections: *Perkembangan Model Generatif Musik Simbolik*, *Evaluasi Penggunaan Model oleh Musisi*, and *Analisis Harmoni Komputasional dan Anotasi*. The theory section adds tonal-harmony corpus evidence, a current functional-harmony theory, cultural familiarity in consonance, and suspensions as rule exceptions.
- BAB III adds interdisciplinarity and Western-data dominance to the positionality paragraph, annotator disagreement to validation, voice separation to quality control, a rule against reading non-significant results as equivalence, and the rationale for measuring all models with one instrument.
- Fixed bibliography errors: `le2025` fourth author is Mikaela Keller; the `Retkowski2024` arXiv ID is 2412.07948. Protected proper nouns in several existing titles.

All new claims were checked against OpenAlex abstracts only. Record page or section support in the reading ledger before submission.
