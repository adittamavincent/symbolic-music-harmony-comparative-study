# Panduan peneliti: memahami penelitianmu sendiri

Diperbarui 5 Oktober 2026 untuk naskah v4 (protokol 2.1). Bagian 1, 2, dan 6 diperbarui 9 Oktober 2026 untuk naskah v5 (protokol 3.0); bagian lain berlaku untuk keduanya. Berkas ini bahan belajar, bukan bagian naskah. Urutan dan saran di sini adalah rekomendasi asisten setelah membaca naskah dan kode, bukan aturan prodi. Versi sebelumnya (berbahasa Inggris, untuk v3) ada di riwayat Git.

## Isi folder `study/`

| Berkas | Isinya | Buka saat |
| --- | --- | --- |
| researcher-guide.md (berkas ini) | Penelitianmu dalam bahasa sederhana, empat teori BAB II, dasar-dasar penelitian, daftar bacaan | Pertama kali, atau saat gambaran besarnya mulai kabur |
| [model-dan-istilah.md](model-dan-istilah.md) | Cara kerja DeepBach dan Coconet, kamus istilah | Ada istilah teknis yang membingungkan |
| [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md) | Strube dan terjemahan Pak Gathut, rantai argumen, angka penting, latihan hitung, daftar periksa | Sebelum bimbingan dengan Pembimbing I |
| [defense-qa.md](defense-qa.md) | Q1–Q131, latihan menjawab (bagian N untuk v5) | Setelah paham, untuk latihan lisan |

Urutan belajar yang disarankan:

1. Bagian 1 dan 2 berkas ini, sampai kamu bisa menceritakan penelitianmu dalam dua menit tanpa catatan.
2. [model-dan-istilah.md](model-dan-istilah.md) bagian 1–6.
3. [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md) bagian 1–4. Pembimbing I menerjemahkan buku Strube, jadi bagian 1 paling mungkin ditanyakan.
4. [defense-qa.md](defense-qa.md): kalimat pegangan dan bagian N (v5), lalu bagian A–F, J, dan L. Jawaban lama tentang asal melodi dan uji Mann–Whitney berlaku untuk v4.
5. Daftar periksa di [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md) bagian 7.

## 1. Penelitianmu dalam lima menit

### Masalahnya

Ada program AI yang bisa mengharmonisasi melodi. Kamu memberi melodi sopran, lalu program mengisi alto, tenor, dan bas. Dua program yang dibahas di sini adalah DeepBach dan Coconet. Coconet dipakai di Bach Doodle Google tahun 2019 dan menerima lebih dari 55 juta permintaan dalam tiga hari (Huang dkk. 2019, hlm. 793). Banyak pemakainya bukan musisi terlatih, jadi mereka belum tentu bisa memeriksa sendiri gerak suaranya.

Pengembang kedua model menilai modelnya lewat pendengar dan ukuran statistik. Mereka tidak menghitung pelanggaran kaidah gerak suara.

### Yang sudah diketahui

Tim Bach Doodle menghitung kuint dan oktaf sejajar pada 21,8 juta harmonisasi Coconet dengan music21. Hasilnya 0,365 kuint dan 0,391 oktaf sejajar per birama, sedangkan pada chorale Bach hanya 0,023 dan 0,009. Paralel lebih sering muncul ketika melodi pengguna tidak mirip melodi yang dipelajari model (Huang dkk. 2019, hlm. 798).

Kelemahannya, data itu tidak dikendalikan. Melodinya ditulis bebas oleh pengguna, modelnya hanya satu, dan kaidahnya hanya dua.

### Yang kamu lakukan

Kamu melanjutkan analisis Huang dkk. dalam kondisi yang dikendalikan:

- melodi yang sama diberikan kepada DeepBach dan Coconet;
- melodinya 40 sopran *chorale* Bach dari korpus music21. Strube sendiri mengambil soal *chorale*-nya dari Bach (hlm. 174), jadi tidak ada soal yang diketik dari buku;
- pelanggaran dihitung untuk lima kaidah Strube, yaitu kuint sejajar, oktaf sejajar, jarak suara atas, persilangan di atas sopran, dan tumpang tindih suara;
- harmonisasi asli Bach untuk melodi yang sama diukur dengan cara yang sama sebagai acuan;
- setiap pelanggaran dicatat letaknya: di sekitar fermata, yang oleh Strube disebut kadens, atau di dalam frasa.

Semua pengukuran dikerjakan program. Tidak ada penilai, pendengar, atau partisipan manusia.

Bayangkan dua murid yang belajar harmoni hanya dengan menyalin ratusan chorale Bach, tanpa pernah membaca buku aturan. Kamu memberi mereka soal chorale yang sama, lalu memeriksa jawaban mereka dengan lima aturan Strube. Jawaban Bach sendiri ikut diperiksa, karena Bach pun kadang melanggar aturan buku ajar, terutama di dekat akhir frasa. Kamu juga melihat di mana mereka salah: di kadens atau di tengah frasa. Murid pertama (DeepBach) diberi tahu letak fermata; murid kedua (Coconet) tidak.

### Tiga pertanyaan

| Pertanyaan | Dalam bahasa sehari-hari | Cara menjawab |
| --- | --- | --- |
| 1 | Seberapa patuh setiap model, dibandingkan dengan Bach pada melodi yang sama? | Statistik deskriptif, tanpa hipotesis; juga seberapa sering model membunyikan nada Bach (`copy_share`) |
| 2 | Pada melodi yang sama, apakah DeepBach dan Coconet berbeda? | Uji Wilcoxon, karena datanya berpasangan |
| 3 | Di bagian frasa mana model lebih sering melanggar, di sekitar fermata atau di dalam frasa? | Uji Wilcoxon per model, berpasangan per melodi; pola Bach sebagai pembanding |

### Variabel dan sampel

- X1, model: DeepBach atau Coconet.
- X2, letak dalam frasa: zona fermata atau di dalam frasa. Letak bukan perlakuan dari peneliti, jadi hasilnya dibaca sebagai hubungan, bukan sebab.
- Y, tingkat kepatuhan: pelanggaran per birama (pertanyaan 1 dan 2) dan pelanggaran per kesempatan di setiap zona (pertanyaan 3). Makin kecil angkanya, makin patuh. Kelima kaidah dianalisis terpisah.
- Unit analisis adalah melodi. Setiap model mengharmonisasi setiap melodi lima kali, lalu nilainya digabung menjadi satu angka per melodi per model.
- Sampelnya 40 melodi, diambil acak dengan *seed* 20261004 dari 318 melodi layak. Angka 40 berasal dari analisis daya untuk uji berpasangan. Jumlah harmonisasi: 40 × 2 model × 5 = 400.

### Yang boleh dan tidak boleh kamu klaim

- Boleh: "*checkpoint* DeepBach yang diuji lebih (atau kurang) patuh daripada *checkpoint* Coconet yang diuji, pada melodi ini."
- Jangan: "LSTM lebih baik daripada CNN." Kedua model berbeda data latih, representasi, jaringan, dan cara mengisi nada sekaligus.
- Boleh: "pada Coconet, tumpang tindih lebih sering muncul di zona fermata." Jangan: "Coconet salah di kadens karena tidak diberi fermata." Informasi fermata hanya salah satu perbedaan kedua model.
- Boleh: "pelanggaran menurut definisi operasional." Jangan menyebut setiap kejadian sebagai kesalahan musikal, karena pengecualian yang memerlukan analisis akor tidak diterapkan.
- Kepatuhan pada kaidah Strube adalah kesesuaian dengan norma satu tradisi, yaitu harmoni tonal Barat. Angka ini tidak mengukur mutu musik secara umum.

## 2. Empat teori di BAB II dengan bahasa sederhana

BAB II memisahkan dua hal. Tinjauan pustaka membahas penelitian terdahulu. Landasan teori berisi teori para ahli yang dipakai untuk membaca data. Landasan teori dibagi lagi menjadi teori tentang objek (model dan cara menilainya) dan teori tentang fokus (kaidah gerak suara), mengikuti template departemen. Setiap teori punya tugas sendiri.

### Briot, Hadjeres, dan Pachet (2020): lima dimensi model

Sistem pembuat musik berbasis *deep learning* dapat digambarkan dengan lima dimensi, yaitu tujuan, representasi, arsitektur, tantangan, dan strategi (hlm. 11–13). Kelima dimensi itu saling memengaruhi.

Bayangkan dua dapur yang memasak menu yang sama. Bahan, alat, dan resepnya berbeda. Kalau rasanya berbeda, kamu tidak bisa bilang penyebabnya alatnya saja.

Dipakai untuk pertanyaan 2. DeepBach dan Coconet punya tujuan yang sama di penelitian ini, tetapi berbeda representasi, arsitektur, strategi, dan data latih. Karena itu perbedaan hasilnya tidak boleh disebut akibat arsitektur. Rinciannya ada di [model-dan-istilah.md](model-dan-istilah.md) bagian 4.

Dipakai juga untuk pertanyaan 3. Dimensi representasi menunjukkan informasi apa yang diterima model: DeepBach menerima letak fermata, Coconet tidak, dan data chorale yang dipakai tim Bach Doodle juga tanpa fermata (Huang dkk. 2019, hlm. 798).

Catatan: Hadjeres dan Pachet juga pengembang DeepBach. Teori mereka dipakai di sini hanya sebagai kerangka untuk menggambarkan model, bukan untuk menilai DeepBach lebih baik.

Storkey (2008), teori pergeseran *dataset*, dipakai di v4 untuk pertanyaan asal melodi. Di v5 pertanyaan itu diganti, jadi Storkey tidak dipakai lagi.

### Pearce, Meredith, dan Wiggins (2002): cara menilai musik buatan program

Program penyusun musik dibuat dengan motivasi yang berbeda-beda, dan setiap motivasi menuntut cara evaluasi yang berbeda. Mereka membedakan empat kegiatan, yaitu komposisi algoritmik, alat bantu komposisi, pemodelan gaya musik, dan pemodelan kognisi musik. Model gaya dapat gagal dengan dua cara, yaitu tidak mampu menghasilkan karya yang sesuai gaya, atau menghasilkan karya yang tidak sesuai gaya. Kegagalan kedua diuji dengan membuat karya baru lalu memeriksanya dengan prosedur yang eksplisit.

Bayangkan menilai murid yang meniru gaya Bach. Kesan "kedengarannya seperti Bach" tidak cukup. Kamu perlu daftar pemeriksaan tertulis yang bisa diulang orang lain.

Dipakai untuk pertanyaan 1 dan untuk membatasi kesimpulan. DeepBach dan Coconet adalah model gaya chorale Bach. Lima kaidah Strube adalah satu prosedur eksplisit yang sempit. Model yang lolos kelima kaidah belum tentu sesuai gaya Bach secara keseluruhan.

### Strube (1928): kaidah gerak suara dan harmoni fungsional

Dalam Preface, Strube menyatakan bahwa bukunya menekankan fungsi harmonis akor. Di hlm. 6 ia menyebut trinada I, IV, dan V sebagai tonika, subdominan, dan dominan. Dari situ disusun tiga tingkat teori:

- teori paling umum (*grand theory*): harmoni tonal fungsional;
- tingkat tengah: kaidah gerak suara Strube;
- tingkat terapan: definisi operasional yang kamu susun untuk program pemeriksa.

Pembagian tiga tingkat ini susunanmu sendiri, dan BAB II menyatakannya. Strube juga menulis bahwa harmoni mengikuti kebiasaan dan cita rasa, bukan hukum yang tidak dapat diubah (Preface). Karena itu kaidahnya dipandang sebagai norma penulisan, yaitu rangkuman praktik. Kaidah buku ajar dipengaruhi chorale Bach, tetapi tidak diikuti Bach secara ketat (Yan dkk. 2018), jadi harmonisasi Bach menjadi acuan praktik, bukan contoh tanpa pelanggaran.

Di v5 ada dua tambahan. Pertama, kaidah Strube bergantung pada tahap: kuint sejajar antara akor IV dan II disebut tidak berbahaya, tetapi tetap dihindari untuk sementara (hlm. 45). Inilah yang dimaksud Pak Gathut dengan konteks soal. Kedua, bab harmonisasi chorale (hlm. 174) memberi pedoman khusus, menyebut fermata sebagai kadens, dan menyatakan bahwa melodi latihannya diambil dari Bach. Dua pedoman bab itu dipakai, yaitu persilangan tidak boleh melewati sopran dan fermata sebagai batas frasa. Pedoman lain, seperti akor kuart-sekst dan fungsi tonika di fermata, memerlukan penentuan akor, jadi tidak diukur.

Dipakai untuk merumuskan lima kaidah dan pengecualiannya, serta untuk menentukan konteks dan zona fermata. Teori fungsional juga membatasi tafsiran hasil, karena beberapa pengecualian Strube bergantung pada fungsi akor dan tidak dapat diperiksa program. Contohnya kuint yang bersifat lewat dan kuint pada pengulangan akor (hlm. 34–35).

### Huron (2001): alasan perseptual di balik kaidah

Strube menyatakan kaidah, tetapi tidak menjelaskan rinci mengapa kaidah itu perlu. Huron menurunkan kaidah gerak suara dari prinsip persepsi pendengaran. Tujuan gerak suara menurut sejumlah ahli teori adalah alur suara yang terdengar mandiri (hlm. 2).

| Kaidah | Prinsip Huron | Artinya bagi pendengar | Halaman |
| --- | --- | --- | --- |
| Kuint dan oktaf sejajar | Fusi nada dan ko-modulasi nada | Unisono, oktaf, dan kuint cenderung terdengar menyatu, apalagi bila bergerak searah. Dua suara terdengar seperti satu | 19, 31, 37 |
| Persilangan dan tumpang tindih | Kedekatan nada | Telinga mengikuti satu suara lewat nada yang berdekatan. Bila suara saling melewati, alurnya sulit diikuti | 24, 35 |
| Jarak suara atas | Penyamaran minimum | Nada yang berbunyi bersama paling sedikit saling menutupi bila jarak suara bawah lebih lebar daripada jarak suara atas | 18, 33 |

Bayangkan paduan suara empat orang. Kalau dua penyanyi terus bergerak dalam oktaf yang sama, pendengar seolah hanya mendengar tiga suara.

Dipakai untuk menafsirkan arti setiap jenis pelanggaran. Penelitianmu tidak mengukur pendengar, jadi tafsiran ini bersandar pada teori. Huron sendiri menegaskan bahwa uraiannya tidak dimaksudkan untuk membenarkan kaidah harmoni Barat (hlm. 4). Ia juga mencatat bahwa ahli teori masa kini cenderung memandang kaidah gerak suara sebagai konvensi dari satu masa sejarah, bukan aturan universal (hlm. 2).

### Kerangka berpikir dalam satu gambar

```text
Model (X1) ────────> harmonisasi model ──┐
                                          ├──> instrumen lima kaidah ──> pelanggaran (Y)
Harmonisasi Bach (acuan praktik) ────────┘                                    ^
                                                  Letak dalam frasa (X2): zona fermata | dalam frasa

Briot dkk.     : kenapa dua model bisa berbeda; siapa yang menerima fermata   (X1)
Strube; Huang  : fermata sebagai kadens; paralel di batas frasa              (X2)
Strube         : kaidah dan pengecualian                                     (instrumen)
Huron          : arti setiap jenis pelanggaran                               (Y)
Pearce dkk.    : batas kesimpulan                                            (Y)
```

Ini Gambar Kerangka Berpikir di BAB II, ditulis ulang tanpa kotak.

## 3. Rantai penelitian

Skripsimu harus memungkinkan pembaca mengikuti satu pertanyaan sampai jawabannya, memeriksa buktinya, dan menilai jawabanmu. Kamu juga perlu menjelaskan alasan memilih metode dan apa yang tidak dapat dibuktikan oleh bukti itu.

```text
Pertanyaan penelitian
  → kaidah musik yang terbit, beserta pengecualiannya (Strube)
  → definisi operasional dan program pemeriksa yang sudah divalidasi
  → tugas yang memang bisa dikerjakan model, dengan pengaturan generasi yang dicatat
  → keluaran mentah, kegagalan, dan eksklusi yang disimpan
  → pengukuran dan analisis yang bisa diulang
  → tafsiran musikal dan kesimpulan yang dibatasi
```

Kode hanya mengisi sebagian rantai ini. Pilihan yang dibuat kode tetap harus kamu jelaskan.

Contohnya kuint sejajar. Sebelum menghitung, kamu harus menentukan dua suara mana yang dibandingkan, peristiwa bunyi mana yang diperiksa, apa yang disebut kuint, dan situasi musik mana yang dihitung. Setelah itu program dibandingkan dengan contoh yang labelnya sudah diketahui. Sebelum langkah itu selesai, angka `parallel_fifths` hanyalah keluaran program yang arti musikalnya belum diperiksa.

## 4. Istilah dasar penelitian

| Istilah | Artinya dalam proyek ini |
| --- | --- |
| Masalah penelitian | Pertanyaan khusus yang belum terjawab tentang cara menilai musik simbolik buatan model |
| Celah penelitian | Apa yang tidak ditemukan dalam penelusuran yang tercatat, dalam lingkup penelusuran itu |
| Pertanyaan penelitian | Pertanyaan yang bisa dijawab dengan keluaran model dan instrumen yang tersedia |
| Teori | Uraian musik yang dipakai untuk merumuskan kaidah dan konteksnya, dan uraian ahli yang dipakai membaca hasil |
| Definisi operasional | Peristiwa musik, syarat, dan cara menghitung yang dipakai untuk mengukur satu kaidah |
| Instrumen | Pembaca partitur, pemetaan suara, pemeriksa kaidah, dan perhitungan per birama, sebagai satu kesatuan |
| Uji perangkat lunak | Masukan yang hasilnya sudah diketahui, untuk memeriksa perilaku kode |
| Validasi instrumen | Bukti bahwa keluaran program memang mengukur sifat musik yang dimaksud |
| Uji coba (*pilot*) | Percobaan kecil untuk menemukan masalah sebelum prosedur utama dibekukan |
| Data utama | Sampel yang dikumpulkan dengan prosedur yang disepakati, untuk menjawab pertanyaan skripsi |
| Unit analisis | Apa yang dihitung sebagai satu pengamatan. Di sini melodi, bukan harmonisasi |
| Hasil | Apa yang diukur, beserta sumber, jumlah, dan ketidakpastiannya |
| Pembahasan | Tafsiranmu yang didukung bukti, penjelasan lain yang mungkin, dan contoh partitur |
| Keterbatasan | Batas yang mempersempit jawaban atau generalisasinya |

## 5. Tugas setiap bab

Naskah v4 mengikuti template Proposal TA Penelitian 2026 dengan BAB I–III. Bab hasil dan bab kesimpulan ditambahkan setelah data utama ada. Nama bab sesudah BAB III ikuti pedoman prodi; skripsi acuan Prodi Musik 2026 terdiri atas lima bab.

| Bab | Pertanyaan pembaca | Yang perlu kamu sediakan |
| --- | --- | --- |
| I. Pendahuluan | Apa pertanyaannya dan kenapa diteliti? | Masalah yang spesifik, celah yang didukung sumber, pertanyaan, tujuan, manfaat |
| II. Tinjauan Pustaka dan Landasan Teori | Penelitian dan teori apa yang mendasari pilihanmu? | Ringkasan studi yang akurat beserta halaman, tabel posisi penelitian, lima teori, kerangka berpikir, asumsi, hipotesis |
| III. Metode Penelitian | Bagaimana orang lain mengulang dan memeriksa pekerjaanmu? | Pendekatan, objek dan sampel, variabel, instrumen dan rumusnya, validitas, kontrol kualitas, rencana analisis, alur |
| Bab hasil dan pembahasan | Apa yang terjadi, dan bagaimana kamu membacanya? | Jumlah sebenarnya, kegagalan generasi dan kontrol kualitas, hasil per kaidah, uji statistik, contoh partitur, penjelasan lain |
| Bab kesimpulan dan saran | Jawaban apa yang didukung bukti? | Jawaban setiap pertanyaan dari bab hasil, batasnya, dan saran lanjutan yang spesifik |

Abstrak diperbarui terakhir, setelah hasil dan kesimpulan pasti. Abstrak harus menyebut metode dan temuan yang sebenarnya.

Alur kerja yang praktis: bekukan BAB III dulu, tulis bab hasil dan kesimpulan dari data, cocokkan lagi BAB I dan II dengan lingkup akhirnya, lalu selesaikan abstrak. Ini saran, bukan urutan wajib.

## 6. Sudah sampai mana

Status lengkap selalu ada di [PROGRESS.md](../PROGRESS.md). Ringkasannya per 9 Oktober 2026:

| Sudah ada | Belum ada |
| --- | --- |
| Naskah v5, BAB I–III (PDF 67 halaman), disusun 8 Oktober atas permintaanmu dan dipangkas 9 Oktober agar tetap dekat dengan v4; perubahannya di [perubahan-v4-ke-v5.md](../supervision/perubahan-v4-ke-v5.md) | Persetujuan Bu Yoni dan Pak Gathut atas arah v5 |
| Protokol 3.0; pipeline untuk 40 melodi Bach dan analisis zona fermata, diuji dengan model palsu; `make test` lulus | Model belum dipasang dan belum dijalankan |
| Instrumen versi 2.0; validasi langkah 3–5 sudah dijalankan pada chorale Bach | Validasi langkah 2: contoh cetak Strube |
| Kerangka sampel Bach: 318 melodi; eksplorasi letak pelanggaran pada harmonisasi Bach | Bacaanmu sendiri atas sumber inti (kolom `researcher_read_status` masih kosong) |
| Bimbingan pertama dengan Pak Gathut, catatan G01–G15 | Uji coba, data utama, bab hasil dan kesimpulan |

Langkah berikutnya:

1. Baca naskah v5 dan [perubahan-v4-ke-v5.md](../supervision/perubahan-v4-ke-v5.md).
2. Bawa [bimbingan-arah-v5.md](../supervision/bimbingan-arah-v5.md) ke Bu Yoni, lalu ke Pak Gathut. Butir dua model perlu persetujuan Pak Gathut secara eksplisit. Alasan setiap butir ada di [rancangan-kesepakatan-v5.md](../supervision/rancangan-kesepakatan-v5.md).
3. Baca hlm. 174 dan 45 buku Strube di buku cetak.
4. Cocokkan sembilan contoh cetak untuk validasi langkah 2 setelah asisten menyiapkannya.
5. Baca sumber inti (bagian 7) dan isi `researcher_read_status` di [reading-notes.csv](../records/reading-notes.csv).
6. Model baru dipasang dan dijalankan setelah protokol 3.0 disepakati, atas permintaanmu.

Keputusan desain dicatat di [research/protocol.md](../../../research/protocol.md). Cacat teknis dan perbaikannya dicatat di [maintenance.md](../../maintenance.md).

Setelah setiap sesi kerja, tulis empat baris pendek di [research-log.md](../records/research-log.md): apa yang kukerjakan, apa yang kutemukan, apa yang kuubah dan kenapa, apa yang harus kuselesaikan berikutnya. Sertakan halaman sumber atau lokasi berkas. Jangan mengubah catatan lama agar cocok dengan penjelasan yang datang belakangan.

## 7. Bacaan, berurutan

Pinjam lewat perpustakaan atau akses kampus bila bisa. Mulailah dari bagian yang disebut dan satu tugas tertulis; kamu tidak perlu membaca setiap buku dari awal sampai akhir.

| Urutan | Bacaan | Yang dikerjakan |
| --- | --- | --- |
| 1 | Booth dkk., [The Craft of Research, edisi 5](https://press.uchicago.edu/ucp/books/book/chicago/C/bo215874008) | Baca bagian tentang pertanyaan dan masalah penelitian, sumber, klaim, dan bukti. Tulis pertanyaanmu, batas klaimmu, dan bukti yang dibutuhkan untuk menjawabnya |
| 2 | Evans, Gruba, dan Zobel, [How to Write a Better Thesis, edisi 3](https://link.springer.com/book/10.1007/978-3-319-04286-2) | Mulai dari "What Is a Thesis?", "Thesis Structure", dan "Establishing Your Contribution". Pakai "Outcomes and Results", "The Discussion or Interpretation", dan "Before You Submit" saat menulis bab hasil |
| 3 | Strube, *The Theory and Use of Chords* (1928), dan terjemahan *Teori dan Penggunaan Akor (I)* oleh A. Gathut Bintarto T. (2015), Pembimbing I ([katalog perpustakaan ISI](https://opac.isi.ac.id/index.php?id=29353&p=show_detail)) | Baca bunyi kaidah, pengecualian, dan contoh cetak di kedua edisi. Peta halaman dan tiga perbedaan teks ada di [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md) bagian 1 |
| 4 | Huang dkk. (2019) §6.3, hlm. 798; Yan dkk. (2018) §4 dan rubrik suplemennya | Desain, ukuran, dan kategori kaidah berasal dari dua makalah ini. Bagian yang dibaca ada di [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md) bagian 5 |
| 5 | Hadjeres dkk., [DeepBach](https://proceedings.mlr.press/v70/hadjeres17a.html); Huang dkk., [Counterpoint by Convolution](https://archives.ismir.net/ismir2017/paper/000187.pdf) | Catat representasi, data latih, kendali yang tersedia, dan cara mengambil sampel. DeepBach memakai *pseudo-Gibbs sampling*; menyebutnya LSTM biasa yang menulis dari kiri ke kanan itu keliru |
| 6 | Sumber landasan teori: Briot dkk. ([DOI buku](https://doi.org/10.1007/978-3-319-70163-9), hlm. 11–13 dan 243–249); [Pearce dkk. (2002)](https://doi.org/10.1177/102986490200600203); [Huron (2001)](https://doi.org/10.1525/mp.2001.19.1.1), hlm. 2–5 dan 18–37 | Untuk setiap teori, tulis satu kalimat intinya dan pertanyaan penelitian yang dibantunya. Cocokkan dengan bagian 2 berkas ini. Halaman cetak Briot dkk. belum dicek di buku (PROGRESS, tugas 7) |
| 7 | Leemhuis dkk. (2020); Choi dkk. (2023); Fang dkk., [Bach or Mock?](https://arxiv.org/html/2006.13329v3); Wang dkk., [NotaGen](https://arxiv.org/html/2502.18008v5) | Jelaskan kenapa uji dengar tidak sama dengan patuh kaidah (Leemhuis), kenapa menekan paralel bisa merusak ciri lain (Choi), kenapa skor Fang mengukur kedekatan gaya, bukan pelanggaran, dan kenapa NotaGen tidak dipakai |
| 8 | [NeurIPS reproducibility checklist](https://neurips.cc/public/guides/PaperChecklist) dan laporan [Pineau dkk.](https://www.jmlr.org/papers/v22/20-303.html) | Pakai daftar pertanyaannya untuk memeriksa paket buktimu: metode, lingkungan, data, ketidakpastian, perintah yang bisa diulang. Ini panduan riset, bukan aturan kampusmu |

Untuk urusan kode, lihat dokumentasi resmi [music21 voice leading](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html), [stream dan kuantisasi](https://music21.org/music21docs/moduleReference/moduleStreamBase.html), serta SciPy untuk [uji Wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html). Pustaka program menjalankan keputusanmu. Pustaka itu tidak menentukan tafsiran musik mana yang kamu pakai.

## 8. Baca, catat, baru tulis

[reading-notes.csv](../records/reading-notes.csv) memisahkan pemeriksaan sumber oleh asisten dari bacaanmu sendiri. Untuk setiap sumber inti, catat halaman atau bagiannya, klaim yang didukungnya, apa yang tidak dibuktikannya, dan pengaruhnya pada desainmu.

Untuk penelusuran literatur, catat tanggal, situs atau basis data, kata kunci persis, jumlah hasil yang disaring, dan alasan menyimpan sumber. Rencana kueri OpenAlex ada di `research/literature/openalex_queries.json`, dan catatan penyaringan v4 di `research/literature/screening-2026-10-04.md`. Google Scholar, arsip ISMIR, Garuda, dan repositori ISI berguna untuk menemukan sumber; setelah itu baca publikasi aslinya. Minta bantuan pustakawan untuk sumber yang sulit diakses.

Rumusan celah yang aman menyebut perbandingan yang tidak ditemukan dalam sumber yang kamu tinjau. Kalimat "belum pernah ada yang meneliti ini" memerlukan bukti yang jauh lebih luas. Jangan mengutip sumber hanya karena sumber itu menyebut musik AI; cari bagian yang mendukung kalimatmu.

## 9. Tanggung jawabmu dan bantuan yang tersedia

Kamu harus memahami dan bisa mempertahankan sendiri:

- pertanyaan penelitian;
- kaidah musik dan halaman Strube-nya;
- definisi operasional dan cara kerja setiap rumus;
- keputusan memilih dan mengeluarkan melodi;
- alasan setiap uji statistik;
- tafsiran hasil dan contoh partitur yang dibahas.

Baca sendiri sumber yang kamu kutip dan periksa partitur di balik hasil penting. Sepakati dengan pembimbing bentuk pengungkapan bantuan AI yang dipakai prodi.

Asisten AI dapat membantu memperbaiki pipeline, menerjemahkan definisi yang disepakati menjadi uji dan kode, membuat tabel dan grafik yang bisa diulang, memeriksa sitasi, menyunting naskah, dan menyiapkan pertanyaan sidang. Pengamatanmu, penilaianmu sebagai musisi, dan keputusan pembimbing tidak dapat ditebak oleh kode atau tulisan buatan AI.

## Bacaan tambahan dari forum

Diskusi berikut membahas riset pascasarjana secara umum. Sesuaikan sarannya dengan lingkup S-1 dan permintaan pembimbingmu.

- [Academia Stack Exchange: seberapa rinci implementasi ditulis dalam tesis?](https://academia.stackexchange.com/questions/40820/how-detailed-should-i-be-about-my-implemented-system-while-writing-a-ph-d-thesi) Bandingkan jawabannya dengan BAB III: bisakah pembaca lain menyusun ulang pengukuranmu? Pakai untuk menemukan penjelasan yang kurang, bukan untuk menetapkan jumlah halaman.
- [Academia Stack Exchange: menyimpan informasi selama riset](https://academia.stackexchange.com/questions/108625/how-to-store-incidental-information-gleaned-in-the-course-of-conducting-research) Di proyek ini, pakai reading-notes.csv dan research-log.md.
- [Ulasan How to Write a Better Thesis, University of Victoria Graduate Writers Community](https://onlineacademiccommunity.uvic.ca/gradwriters/2019/03/01/seeing-the-big-picture-a-review-of-how-to-write-a-better-thesis/) Baca bersama bukunya bila perlu gambaran sebelum memilih bab.
