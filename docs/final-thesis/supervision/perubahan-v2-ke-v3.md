# Perubahan dari proposal v2 ke naskah v3

Disusun 2 Oktober 2026. Dokumen ini menjelaskan apa yang berubah dari proposal v2 (tag `proposal/v2`) ke naskah v3, mengapa berubah, dan dasar setiap perubahan.

## Asal revisi

Proposal v2 dibahas dalam kelas mata kuliah **Seminar Musikologi 2** oleh dosen pengampu **Bu Suryati** dan **Pak Galih**, dalam sesi bimbingan tatap muka di kelas. Masukan dari sesi itu menjadi acuan revisi v3. Catatan masukan ditulis oleh peneliti dengan kata-katanya sendiri, bukan transkrip ucapan dosen. Catatan asli dan tafsirannya tersimpan di [feedback.md](feedback.md) dengan kode F01–F12.

Dokumen ini membedakan dua jenis dasar perubahan:

- **Masukan dosen:** perubahan yang langsung menjawab catatan F01–F12.
- **Tindak lanjut peneliti:** perubahan yang diputuskan peneliti agar masukan tersebut dapat dipenuhi secara konsisten. Contohnya, setelah variabel dan hipotesis wajib ada, rancangan kondisi lama ternyata tidak dapat dipertahankan. Dosen tidak meminta perubahan ini secara khusus. Dasarnya adalah evaluasi peneliti atas metode dan sumber yang dibaca.

Pembedaan ini penting saat sidang. Jika ditanya "apakah dosen meminta NotaGen dihapus?", jawaban yang benar adalah bahwa penghapusan itu keputusan peneliti untuk memenuhi tuntutan variabel dan hipotesis yang jelas, bukan permintaan langsung.

## Ringkasan perubahan

| Aspek | Proposal v2 | Naskah v3 | Dasar |
| --- | --- | --- | --- |
| Judul | *Evaluasi Akurasi Kaidah Harmoni Fungsional pada Musik Simbolik Hasil Generasi LSTM, CNN, dan Transformer* | *Evaluasi Musik Hasil AI DeepBach dan Coconet: Pengaruh Asal Melodi terhadap Kepatuhan Kaidah Gerak Suara Strube* | Masukan dosen F01 ("evaluasi musik hasil x", "hasil Gustav"); bentuk "pengaruh X terhadap Y" dari F06 |
| Jenis penelitian | Kuantitatif komparatif dengan paradigma R&D | Kuantitatif. Pertanyaan 1 deskriptif, 2 komparatif, 3 asosiatif kausal (Creswell; Sugiyono). Tidak memakai metode campuran | Masukan dosen F02 dan F11 |
| Bentuk rumusan | Pertanyaan "Sejauh mana", "Apakah", "manakah" | Paragraf masalah diikuti tiga pertanyaan "Bagaimana", semuanya menyebut kaidah Strube | Masukan dosen F03, F04, F05 |
| Variabel | Variabel independen empat kondisi instruksi; variabel dependen *Strube Score* | X1 model, X2 asal melodi, Y laju pelanggaran per birama untuk lima kaidah | Masukan dosen F06, F07; perubahan isi variabel adalah tindak lanjut peneliti |
| Hipotesis | Tidak dirumuskan sebagai H0/H1 | H0/H1 untuk pertanyaan 2 dan 3; arah untuk kuint dan oktaf mengikuti temuan Huang dkk. (2019) | Masukan dosen F07 |
| Landasan teori | Teori harmoni fungsional Strube dan formalisasi matematis arsitektur model | Grand theory harmoni fungsional, middle theory kaidah gerak suara Strube, applied theory definisi operasional, teori pendukung model generatif dan distribusi data latih | Masukan dosen F08, F12 |
| Rujukan Strube | Dikutip tanpa halaman | Setiap kaidah dikutip dengan halaman edisi 1928: hlm. 9, 12–13, 20, 174 | Masukan dosen F05 ("perlu Strube"); halaman dibaca peneliti dari buku |
| Rumus | Rumus tanpa penjelasan asal | Rumus dinyatakan sebagai definisi operasional susunan peneliti, simbolnya didefinisikan, dan setiap syarat dirujuk ke halaman Strube | Masukan dosen F10 |
| Posisi peneliti | Tidak dibahas | Paragraf posisionalitas: insider terhadap tradisi teori, outsider terhadap model, refleksivitas, dan langkah pengendalian bias | Masukan dosen F09 |
| Model | DeepBach, Coconet, NotaGen | DeepBach dan Coconet | Tindak lanjut peneliti: NotaGen tidak dapat diberi melodi yang harus dipertahankan |
| Variabel bebas kedua | Empat tingkat kendali A–D | Asal melodi: sopran chorale Bach vs latihan melodi Strube | Tindak lanjut peneliti (lihat bagian berikut) |
| Kaidah | Kuint sejajar, oktaf sejajar, resolusi nada penuntun | Kuint sejajar, oktaf/unisono sejajar, jarak suara atas, persilangan di atas sopran, tumpang tindih suara | Tindak lanjut peneliti: kategori dari rubrik Yan dkk. (2018), rumusan dan pengecualian dari Strube |
| Ukuran | *Strube Score*, disebut proporsi momen bebas pelanggaran | Laju pelanggaran per birama (satuan Huang dkk. 2019) dan indeks berbobot rubrik Yan | Tindak lanjut F10: rumus lama tidak punya sumber dan salah dideskripsikan |
| Penelitian terdahulu utama | Tidak ada satu acuan desain | Melanjutkan analisis Bach Doodle (Huang dkk., 2019) | Tindak lanjut peneliti agar setiap pilihan metode punya sumber |
| Sampel | 120 berkas (3 model × 4 kondisi × 10) | Minimal 30 melodi per kelompok dari analisis daya; unit analisis melodi; lima harmonisasi per melodi dirata-rata | Tindak lanjut peneliti; mendukung hipotesis F07 |
| Analisis | Kruskal–Wallis | Wilcoxon (model, berpasangan) dan Mann–Whitney (asal melodi), koreksi Holm, ukuran efek | Tindak lanjut peneliti mengikuti desain baru |
| Validasi instrumen | Uji positif BWV 66.6 dan uji negatif | Uji contoh cetak Strube, pemeriksaan silang dengan music21, perbandingan dengan angka Huang dkk., pengulangan pengukuran | Tindak lanjut peneliti |
| Penilai manusia | Tidak ada | Tidak ada (ditegaskan sebagai batas lingkup) | Keputusan peneliti: seluruh pengujian komputasional |
| Manfaat | Termasuk "data empiris pertama", "membuktikan" relevansi Strube, dan posisi institusi | Klaim dibatasi pada yang dapat didukung data | Tindak lanjut peneliti: klaim tanpa bukti dihapus |
| Struktur | BAB I–III dan jadwal penelitian, format proposal lama | BAB I–III sesuai *Template Proposal TA Penelitian 2026*; bab hasil ditambahkan setelah data utama | Template departemen 2026 |

## Masukan dosen dan tindak lanjutnya

| Kode | Catatan peneliti dari kelas | Perubahan di v3 | Lokasi |
| --- | --- | --- | --- |
| F01 | "my judul", "evaluasi musik hasil x", "hasil Gustav" | Judul menyebut objek (musik hasil AI DeepBach dan Coconet), variabel, dan Strube | `thesis/metadata.tex`; sampul |
| F02 | "kualitatif … kuantitatif", "material: objek" | Pendekatan kuantitatif dinyatakan tegas; objek material adalah harmonisasi simbolik hasil model | BAB III Metode Pendekatan; Objek |
| F03 | "Rumusan: Paragraf, List" | Rumusan masalah berbentuk paragraf, lalu daftar pertanyaan | BAB I Rumusan Masalah |
| F04 | "Pakai: 5W 1H" | Semua pertanyaan diawali "Bagaimana" | BAB I Pertanyaan Penelitian |
| F05 | "Q3 tidak boleh naratif, perlu Strube" | Pertanyaan 3 berbentuk pertanyaan langsung; semua pertanyaan menyebut kaidah Strube; kaidah dikutip dengan halaman | BAB I; BAB II Landasan Teori |
| F06 | "efektivitas / peningkatan … terhadap … var terikat" | Pertanyaan 3: pengaruh asal melodi terhadap tingkat kepatuhan | BAB I; BAB III Variabel |
| F07 | "Quant: harus ada hipotesis dan variabel" | Variabel X1, X2, Y; hipotesis H0/H1 per kaidah | BAB II Asumsi dan Hipotesis; BAB III Variabel |
| F08 | Grand theory | Harmoni fungsional sebagai grand theory | BAB II Landasan Teori |
| F09 | Posisionalitas, insider/outsider, refleksivitas | Paragraf posisi peneliti dan pengendalian bias | BAB III akhir Metode Pendekatan |
| F10 | Rumus matematis: ada sumbernya? | Rumus diatribusikan sebagai definisi operasional peneliti, simbol didefinisikan, syarat dirujuk ke Strube; rumus skor tanpa sumber diganti | BAB III Instrumen Pengukuran |
| F11 | Kualitatif atau kuantitatif, rujuk Creswell atau Sugiyono | Creswell (2018) dan Sugiyono (2019) dikutip | BAB III Metode Pendekatan |
| F12 | Grand theory (diulang) | Tingkatan grand, middle, applied, dan teori pendukung dinyatakan | BAB II Landasan Teori |

## Mengapa rancangan inti ikut berubah

Masukan F06, F07, dan F10 menuntut variabel yang jelas, hipotesis yang dapat diuji, dan rumus yang punya sumber. Ketika rancangan v2 disusun ulang untuk memenuhi tuntutan itu, empat masalah muncul:

1. **Tingkat kendali A–D tidak setara antar-model.** Pada NotaGen, kondisi C dan D memakai metadata yang identik, dan kondisi B tidak meminta tangga nada C mayor. Variabel bebas yang tidak benar-benar berubah tidak dapat diuji dengan hipotesis.
2. **NotaGen tidak dapat diberi melodi.** Antarmukanya hanya menerima periode, komponis, dan instrumentasi, sehingga tidak dapat mengerjakan soal yang sama dengan model lain.
3. **Pemilihan tiga kaidah dan rumus *Strube Score* tidak bersumber.** Rumus itu juga dideskripsikan sebagai proporsi momen bebas pelanggaran, padahal yang dihitung adalah jumlah penandaan per nada sopran yang dipotong pada nol.
4. **Resolusi nada penuntun bergantung pada deteksi tonalitas otomatis**, yang bisa jatuh diam-diam ke C mayor.

Peneliti kemudian mengikatkan setiap pilihan pada sumber tertulis:

- **Desain dan ukuran:** analisis Bach Doodle (Huang dkk., 2019, §6.3). Kuint dan oktaf sejajar dihitung per birama dengan music21, dan pelanggaran meningkat ketika melodi tidak menyerupai data latih. Gagasan ini menjadi variabel asal melodi.
- **Kategori kesalahan:** rubrik Yan dkk. (2018), dibatasi pada kategori yang dapat diukur tanpa analisis akor.
- **Rumusan dan pengecualian kaidah:** Strube (1928). Persilangan dibolehkan Strube kecuali melewati sopran (hlm. 174), dan tumpang tindih dibolehkan bila satu suara melangkah (hlm. 12–13), sehingga kedua kaidah dirumuskan mengikuti batas itu.
- **Melodi soal:** latihan melodi Strube hlm. 11–80 (69 latihan). Latihan bab nada non-akor dan melodi chorale Bach dikeluarkan dengan alasan tertulis.

Seluruh pengukuran dilakukan secara komputasional. Penilai manusia tidak digunakan karena berada di luar cakupan dan sumber daya penelitian sarjana ini; keterbatasan ini dinyatakan sebagai batas klaim.

## Yang tidak berubah

- Topik: evaluasi keluaran model AI musik simbolik terhadap kaidah harmoni Strube.
- Pendekatan kuantitatif dan penggunaan music21.
- DeepBach dan Coconet sebagai model yang diuji.
- Batas penafsiran: perbedaan antar-model tidak diatribusikan pada arsitektur semata.
- Sumber proposal v1 dan v2 disimpan tanpa perubahan di `docs/proposal-phase/`. Instrumen versi 1 dan konfigurasi kondisi A–D tetap ada di repositori sebagai versi historis.

## Bukti dan berkas pendukung

| Hal | Berkas |
| --- | --- |
| Catatan masukan kelas | [feedback.md](feedback.md) |
| Protokol versi 2 dan alasan penggantian versi 1 | [research/protocol.md](../../../research/protocol.md) |
| Halaman kaidah Strube | [strube-rule-pages.csv](../../../research/literature/strube-rule-pages.csv) |
| Inventaris latihan Strube | [strube-exercise-inventory.csv](../../../research/literature/strube-exercise-inventory.csv) |
| Instrumen versi 2 dan hasil validasinya | [research/voice_leading_v2.py](../../../research/voice_leading_v2.py); protokol bagian "Results of checks 3–5" |
| Catatan kronologis | [research-log.md](../records/research-log.md), [PROGRESS.md](../PROGRESS.md) |
| Perbandingan teks berdampingan | `make diff proposal/v2 head` (setelah perubahan di-commit) |

## Kalimat untuk menjelaskan revisi

> Proposal v2 dibahas di kelas Seminar Musikologi 2 oleh Bu Suryati dan Pak Galih. Masukannya meminta judul berpola "evaluasi musik hasil", pendekatan kuantitatif yang tegas, pertanyaan 5W1H yang menyebut Strube, variabel dan hipotesis, grand theory, posisionalitas, dan sumber rumus. Untuk memenuhi masukan itu, saya menyusun ulang rancangan: kondisi A–D dan NotaGen tidak bisa menghasilkan variabel yang setara, jadi saya melanjutkan analisis Huang dkk. (2019) dengan asal melodi sebagai variabel, dan merumuskan setiap kaidah dari halaman buku Strube.
