# v3: final-thesis progress

Updated: 2026-09-28. Active manuscript: `thesis/`. Status: preparation and method review; not ready for submission.

## Continuity

| Revision | Academic phase | Evidence/status |
| --- | --- | --- |
| v1 | Proposal | Existing `proposal/v1` tag |
| v2 | Proposal | Existing `proposal/v2` tag; researcher reports lecturer review during in-class, one-to-one tutoring |
| v3 | Final thesis continuing from v2 | Active manuscript and research plan; future milestone name `thesis/v3`; no tag or completed main experiment yet |

The lecturer comments, review date, submission deadline, and current department guide have not been provided. Record comments in [feedback.md](feedback.md) before attributing any methodological revision to a lecturer.

## What is evidenced now

- The repository contains three generation adapters, one condition manifest, an evaluator, four executable software checks, and five draft chapters.
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
| G3. Instrument | Strube edition/pages, rule exceptions, voice/key/time definitions, score denominator, human annotations, focused test evidence | Open; timing and scoring problems found | Read rules and label small score excerpts with a tutor |
| G4. Comparative protocol | Supported condition matrix, exact checkpoint/model revisions, seed policy, analysis unit, sample/exclusion plan | Open; NotaGen C and D are identical | Resolve choices in [the protocol](../../research/protocol.md) |
| G5. Pipeline integrity | Timing conversion fixed, quality exclusions applied, isolated runs, failed-file/count checks, reproducible records | Open | Work through [maintenance findings](../maintenance.md#research-correctness) before main generation |
| G6. Pilot | Each retained model/condition can generate, parse, preserve constraints, and be manually checked; pilot kept separate | Not run here | Inspect scores and listen; record problems without selecting only good outputs |
| G7. Main data and analysis | Frozen protocol, raw artifacts, all attempts, actual eligible counts, run-specific analysis and figures | Not run here | Collect and review the agreed dataset |
| G8. Final manuscript | Chapters 1–3 match executed methods; chapter 4 cites measured artifacts; chapter 5 answers questions; abstracts and appendices complete | Working draft | Review interpretations and write conclusions from data |
| G9. Submission and defense | Department checklist, checked PDF, supervisor review, evidence archive, final presentation if required | Not ready | Confirm local requirements and rehearse the defense |

## Decisions that must be made before main data

1. Compare named model/checkpoint pipelines or claim a general architecture effect? The available setup supports the former; it cannot isolate architecture from training data and other differences.
2. Keep a separate NotaGen comparison with its native controls, or restrict the main experiment to a task that all models demonstrably support? Text metadata alone does not establish fixed soprano/bass conditioning.
3. Retain the current clipped penalty index with a correct definition, or implement a true eligible-event adherence rate? These produce different measurements. Preserve and label the earlier instrument if it changes.
4. What musical contexts require leading-tone resolution, and how should the evaluator treat rests, held notes, voice crossings, compound intervals, modulation, and ornaments?
5. What is the independent observation: a generated score, a seed chorale, or a repeated generation within a seed? Decide before choosing statistical tests or pooling conditions.

## This preparation changed

- Recorded v1/v2 proposal history and the continuing v3 final-thesis phase.
- Moved research ownership to `research/` while retaining root CLI/import compatibility entry points.
- Added a researcher guide, feedback record, reading ledger, and protocol worksheet.
- Replaced unsupported chapter 4/5 outcomes with an explicit evidence boundary and completion prompts.
- Corrected the thesis cover's proposal wording and added chapter divisions and a contents page. Department format approval remains open.
- Following the researcher's correction, removed draft/status text from the front matter and restored the previous approval-page and abstract wording. Readiness is tracked in project documentation.

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
