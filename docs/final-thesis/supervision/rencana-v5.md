# Rencana revisi v5 setelah bimbingan Pembimbing I

Disusun 6 Oktober 2026 dari transkrip bimbingan dengan Pak Gathut. Ini dokumen kerja untuk peneliti, bukan bagian naskah. Catatan resmi masukannya ada di [feedback.md](feedback.md), kode G01–G15. Naskah belum diubah: teks di `thesis/` masih v4 (tag `thesis/v4`), dan protokol 2.1 belum dibekukan.

Pilihan dan rekomendasi di bawah adalah usulan asisten setelah membaca transkrip, naskah v4, dan buku Strube. Keputusan arah ada di tanganmu (G05), lalu dikonfirmasi ke Pak Gathut.

Pembaruan 8 Oktober 2026: atas arahan peneliti, pilihan A–C di bawah tidak dipakai. Usulan v5 sekarang di [rancangan-kesepakatan-v5.md](rancangan-kesepakatan-v5.md): v4 dengan empat perubahan, yaitu tetap dua model, 40 melodi *chorale* Bach dari korpus tanpa pengetikan, dan pertanyaan 3 tentang letak pelanggaran di sekitar fermata atau di dalam frasa. Lembar untuk bimbingan berikutnya ada di [bimbingan-arah-v5.md](bimbingan-arah-v5.md).

## 1. Inti masukan Pak Gathut

1. **Batasi.** Lingkup v4 terlalu lebar untuk waktumu. Pilih yang cepat menghasilkan (G05, G14).
2. **Konteks soal.** Buku Strube bertahap. Setiap soal ditulis untuk bab tertentu, sedangkan model tidak tahu konteks itu. Soal dari depan dan belakang buku diperlakukan sama oleh mesin (G01, G02).
3. **Konteks *chorale* saja.** Ambil konteks yang memang dijelaskan Strube, yaitu *chorale*. Mulai dari soal *chorale* Strube, lalu lacak karya Bach yang menjadi acuannya dan di mana kemiripannya (G06, G12).
4. **Jadikan studi kasus.** Satu sampel dari Strube, dijalankan di mesin, lalu diulas di bagian mana keluarannya keluar dari kaidah. Membandingkan dua AI menurut beliau terlalu banyak untuk sekarang (G07).
5. **Lokasi kesalahan untuk pengajar.** Informasi yang paling berguna adalah di bagian mana kesalahan cenderung terjadi (G08). Paralel dibaca bersama progresi akornya, bukan hanya dihitung (G09).
6. **Sisanya jadi saran.** Pertanyaan yang belum terjawab masuk ke Saran; tidak semua harus diselesaikan (G11).

Usulanmu sendiri di pertemuan itu, yaitu menggabungkan pemeriksa berbasis aturan ("sistem pakar") dengan keluaran AI untuk konteks yang membolehkan paralel, disambut baik (G13).

## 2. Yang belum dibahas

Dari enam pertanyaan di [bimbingan-v4.md](bimbingan-v4.md), transkrip tidak menunjukkan jawaban untuk susunan landasan teori, persetujuan judul dan pertanyaan, pengutipan terjemahan Pak Gathut, Strube sebagai buku ajar mata kuliah, aturan pengungkapan bantuan AI, dan pembekuan protokol. Bawa lagi pertanyaan yang masih relevan setelah arah v5 diputuskan (bagian 8).

## 3. Bukti di buku Strube

Pemeriksaan ini dikerjakan asisten dari pindaian edisi 1928 (`references/The Theory and Use of Chords.pdf`) dengan OCR dan gambar halaman. Cocokkan dengan buku cetak sebelum dikutip.

### Strube memang bertahap

Strube menulis di Preface bahwa ia memandang akor menurut lingkungan musikalnya, bukan sebagai benda yang berdiri sendiri ("in regard to their musical environment"). Dua contoh dari isi bukunya:

- **Hlm. 45 (bab Subordinate Chords, Class I).** Kuint sejajar antara IV dan II disebut tidak berbahaya, tetapi tetap dihindari "for the present" karena belum sesuai gaya ketat. Jadi larangan paralel bergantung pada tahap belajar, sejalan dengan maksud Pak Gathut (G02).
- **Hlm. 55 (latihan 76, bab The Neapolitan Sixth).** Melodi latihan diberi tanda "n. 6th" di tempat sekstan Napoli harus dipakai. Soal itu dibuat untuk melatih satu akor tertentu.

### 71 kandidat melodi v4 berasal dari sepuluh bab

| Bab Strube (1928) | Halaman bab | Halaman soal | Nomor soal | Jumlah |
| --- | --- | --- | --- | --- |
| Triads | sekitar 5–19 | 17, 19 | 12–19, 23–29 | 15 |
| Inversions of the Triad, First Inversion | 20–26 | 26 | 35–39 | 5 |
| Inversions of the Triad, Second Inversion | 27–31 | 31 | 40–45 | 6 |
| Modification of Figures | 38–42 | 42 | 53–59 | 7 |
| Subordinate Chords, Class I | 43–52 | 47, 48, 52 | 65–73 | 9 |
| The Neapolitan Sixth | 53–55 | 54, 55 | 74–76 | 3 |
| Chord of the Dominant-Ninth | 55–60 | 59, 60 | 77–82 | 6 |
| Chord of the Leading-Tone Seventh | 61–64 | 64 | 83–86 | 4 |
| Leading-Tone Triad | 65–66 | 66 | 87–90 | 4 |
| Minor Modes | 74–81 | 78, 79, 80 | 97–108 | 12 |
| **Jumlah** | | | | **71** |

Bab akor dominan septim dan inversinya (hlm. 32–37) tidak menyumbang kandidat melodi di inventaris. Batas bab dibaca dari judul bab di pindaian dan daftar isi; halaman soal dari `research/literature/strube-exercise-inventory.csv`, yang kolom `chapter`-nya masih kosong.

Artinya, kelompok "melodi Strube" di v4 mencampur sepuluh konteks. Soal bab Triads ditulis sebelum Strube mengajarkan inversi dan akor septim, sedangkan model bebas memakai inversi, septim, dan nada hias. Pelanggaran pada soal itu tidak bisa dibaca dengan cara yang sama seperti pelanggaran pada soal bab Minor Modes.

### Bab *chorale* Strube

Bab "Harmonization of Chorales" ada di hlm. 174–179, sesudah semua bab akor, modulasi, dan nada hias. Isinya:

- **Pedoman khusus *chorale* (hlm. 174).** Gaya yang khidmat (*dignified*); akor 6/4, termasuk 6/4 kadens, jarang dipakai; akor nona tidak dipakai kecuali bentuk tanpa akar (*leading-tone seventh* dan *diminished seventh*); akor alterasi dihindari kecuali *augmented triad* pada inversi pertama dan akor *augmented sixth*; pada fermata diusahakan trinada posisi dasar berfungsi tonika; setengah kadens pada dominan juga dipakai; *cross-relation* sesudah fermata dibolehkan karena fermata berfungsi sebagai kadens; persilangan suara (tidak di atas sopran) dipakai bila menghasilkan gerak suara yang lebih baik; *chorale* minor sering berakhir pada tonika mayor; modulasinya kebanyakan ke tangga nada dekat. Istilah Indonesianya ikuti terjemahan Pak Gathut bila jilid yang memuat bab ini ada.
- **Melodinya dari Bach.** Strube menulis bahwa melodi-melodi berikutnya diambil dari J. S. Bach (hlm. 174). Judul *chorale*-nya tidak tercantum di halaman yang terpindai.
- **Isi latihan.** Satu contoh harmonisasi empat suara berlabel *Model* (no. 235, hlm. 174–176) dan latihan no. 236 berisi sepuluh melodi bernomor romawi I–X (hlm. 176–179). Siapa penyusun harmonisasi *Model* belum diperiksa.
- **Halaman hilang.** Hlm. 179 tidak ada di pindaian (hlm. 177 terpindai dua kali), jadi melodi X belum lengkap. Terjemahan Pak Gathut jilid I tidak memuat bab ini.

Di v4 bab ini dikeluarkan karena melodinya akan sama dengan kelompok Bach. Usulan Pak Gathut justru menjadikan bab ini pusat penelitian.

## 4. Akibatnya bagi desain v4

| Bagian desain v4 | Masalah setelah bimbingan |
| --- | --- |
| 71 melodi Strube sebagai satu kelompok | Mencampur sepuluh konteks bab (G02) |
| Asal melodi (X2): Bach lawan Strube | Bila hanya konteks *chorale*, melodi soal Strube adalah melodi Bach, jadi kontras asal melodi hilang |
| Dua model dan uji Wilcoxon | Perbandingan dua AI dianggap terlalu luas untuk sekarang (G07) |
| Uji Mann–Whitney, hipotesis, kekuatan uji | Tidak diperlukan bila v5 berupa studi kasus deskriptif; perlu konfirmasi karena F06 dan F07 meminta hipotesis dan variabel untuk desain kuantitatif |
| Mengetik 71 melodi | Pekerjaan terbesar yang belum dikerjakan; sebagian besar tidak terpakai bila konteks dibatasi |

Yang tetap terpakai di pilihan mana pun: instrumen versi 2.0 (lima kaidah), pembaca dan penulis MusicXML, adaptor DeepBach dan Coconet, kontrol kualitas, pencatatan *seed* dan percobaan, metrik `copy_share` (seberapa sering model membunyikan nada Bach sendiri), Huang dkk. (2019) sebagai studi acuan, tinjauan pustaka, dan semua perbaikan gaya bahasa P01–P17.

## 5. Tiga pilihan arah v5

| | A. Studi kasus satu soal *chorale* | B. Tetap komparatif, ditambah konteks bab | C. Seluruh bab *chorale* Strube |
| --- | --- | --- | --- |
| Bahan | Satu melodi dari latihan 236 | 71 melodi, diberi label bab | *Model* 235 dan sepuluh melodi latihan 236 |
| Model | Coconet (DeepBach opsional) | DeepBach dan Coconet | Coconet (DeepBach opsional) |
| Analisis | Frekuensi dan lokasi pelanggaran pada banyak harmonisasi; dibandingkan dengan harmonisasi Bach dan pedoman hlm. 174 | Seperti v4, ditambah analisis per bab | Seperti A untuk setiap melodi; satu atau dua melodi dibahas mendalam |
| Sesuai masukan | Paling dekat dengan G05–G08 | Hanya menjawab G01–G02; bertentangan dengan G05 dan G07 | Dekat dengan G06; lebih lebar dari "satu sampel" |
| Beban kerja | Paling ringan: ketik satu melodi | Paling berat: ketik 71 melodi | Sedang: ketik sekitar sepuluh melodi; butuh hlm. 179 |
| Judul, pertanyaan, hipotesis | Berubah | Hampir tetap | Berubah |

**Rekomendasi asisten: pilihan A, dengan C sebagai perluasan bila waktu cukup dan Pak Gathut setuju.** Alasannya:

- A paling dekat dengan kata-kata Pak Gathut sendiri ("satu sampel", "case aja dulu, kecil aja dulu").
- Keacakan model, yang beliau persoalkan (G03), berubah menjadi bahan analisis. Satu melodi diharmonisasi berkali-kali, lalu dihitung di birama mana pelanggaran paling sering muncul. Itulah "peluang error di bagian mana" (G08).
- Coconet dipilih karena dipakai di Bach Doodle, angka acuan Huang dkk. berasal dari Coconet, dan cerita BAB I sudah dibangun dari sana. DeepBach bisa ditambahkan sebagai kasus kedua bila Pak Gathut setuju, tanpa uji statistik.
- Pipeline v4 sebagian besar terpakai; yang baru hanya pengetikan satu melodi, pencarian sumber Bach-nya, dan analisis per lokasi.

Bayangkan memeriksa satu soal ujian yang dikerjakan seratus kali oleh murid yang sama. Kamu tidak menilai murid itu secara umum. Kamu melihat di birama mana ia paling sering tergelincir, lalu membandingkannya dengan jawaban Bach dan aturan Strube untuk soal itu.

## 6. Sketsa desain pilihan A

Sketsa ini bahan diskusi, belum keputusan.

1. **Pilih satu melodi** dari latihan 236 bersama Pak Gathut. Syarat yang masuk akal: lengkap di pindaian, sumber *chorale* Bach-nya dapat ditemukan, berada dalam wilayah nada kedua model, dan memuat fermata atau modulasi supaya konteksnya kaya.
2. **Lacak sumber Bach-nya** (G06). Ketik melodi Strube, lalu cocokkan urutan nadanya dengan sopran korpus music21. Catat perbedaan versi Strube dan versi Bach (nada dasar, ritme, fermata).
3. **Harmonisasi berulang.** Melodi versi Strube diberikan kepada Coconet sebanyak N kali. Angka N ditetapkan setelah uji coba waktu generasi dan dicatat di protokol. Semua keluaran mentah disimpan.
4. **Pemeriksaan otomatis.** Lima kaidah dihitung dengan instrumen versi 2.0, lalu dicatat lokasinya: birama, ketukan, pasangan suara, dekat fermata atau tidak.
5. **Lapisan konteks *chorale*** (G12, G13). Tentukan pedoman hlm. 174 mana yang bisa dicek program (misalnya persilangan di atas sopran, yang sudah ada) dan mana yang dianalisis peneliti pada partitur (misalnya fungsi tonika di fermata, akor kuart-sekst).
6. **Acuan.** Harmonisasi Bach untuk melodi yang sama diukur dengan instrumen yang sama. Bila Strube memberi *Model* untuk melodi itu, catat juga.
7. **Analisis.** Peta frekuensi pelanggaran per lokasi pada partitur; pembahasan lokasi yang paling sering melanggar menurut progresi akornya dan pedoman Strube (G09); perbandingan dengan Bach; seberapa sering keluaran menyalin Bach (`copy_share`).

Batas yang harus ditulis:

- Satu melodi tidak dapat digeneralisasi ke soal lain atau ke model secara umum.
- Melodi ini berasal dari Bach, jadi kemungkinan besar ada di data latih kedua model. Kemiripan dengan Bach bisa berarti model mengingat, bukan memahami kaidah. Karena itu `copy_share` dilaporkan.
- Analisis partitur dikerjakan peneliti sendiri. Ini analisis musikologis, bukan penilai manusia; desain tanpa penilai dan pendengar tetap berlaku.

### Contoh judul dan pertanyaan (bahan diskusi)

Pola "Evaluasi musik hasil ..." dan nama Strube dipertahankan karena F01.

- *Evaluasi Musik Hasil AI Coconet pada Soal Harmonisasi Chorale Strube: Studi Kasus Kepatuhan Kaidah Gerak Suara*
- *Kepatuhan Kaidah Gerak Suara Strube pada Harmonisasi Chorale oleh Coconet: Studi Kasus Soal Latihan The Theory and Use of Chords*

Pertanyaan, tetap berbentuk "Bagaimana" (F04):

1. Bagaimana kepatuhan harmonisasi Coconet terhadap kaidah gerak suara Strube pada soal harmonisasi *chorale* Strube?
2. Di bagian mana pelanggaran paling sering muncul, dan bagaimana bagian itu dibaca menurut pedoman harmonisasi *chorale* Strube?
3. Bagaimana harmonisasi Coconet dibandingkan dengan harmonisasi Bach untuk melodi yang sama?

## 7. Perubahan per bab bila A atau C dipilih

| Bagian | v4 | Rencana v5 |
| --- | --- | --- |
| Judul dan abstrak | DeepBach dan Coconet; pengaruh asal melodi | Judul baru (bagian 6); abstrak ditulis ulang paling akhir |
| I.A Latar Belakang | Bach Doodle, Huang dkk., soal latihan sebagai sumber melodi | Sebagian besar tetap; ditambah sifat bertahap buku Strube dan bab *chorale*-nya; ditambah kebutuhan pengajar mengetahui letak kesalahan |
| I.B–I.E | Tiga pertanyaan tentang dua model dan asal melodi | Rumusan, pertanyaan, tujuan, dan manfaat baru; manfaat praktis untuk pengajar harmoni |
| II.A Tinjauan Pustaka | Delapan studi dan tabel | Tetap; posisi penelitian ditulis ulang sebagai studi kasus |
| II.B Landasan Teori | Briot, Storkey, Pearce, Strube, Huron | Strube diperluas: susunan bertahap buku, Preface, pedoman *chorale* hlm. 174. Huron untuk kemandirian empat suara (G12). Pearce tetap. Storkey dan Briot dikurangi atau dihapus bila asal melodi dan perbandingan model tidak dipakai |
| II.C–II.D Asumsi, Hipotesis | Tiga hipotesis | Kemungkinan dihapus bila studi kasus deskriptif; tunggu konfirmasi |
| III.A Pendekatan | Kuantitatif, posisionalitas | Studi kasus; data frekuensi ditambah analisis partitur; posisionalitas tetap |
| III.B Objek dan sampel | 71 melodi Strube dan sampel acak Bach | Satu soal latihan 236 (atau sepuluh, pilihan C); sumber Bach-nya |
| III.C Pengumpulan data | Lima generasi per melodi per model | N generasi satu melodi; instrumen tetap; lapisan konteks *chorale* |
| III.D Analisis | Wilcoxon, Mann–Whitney, Holm, empat analisis sensitivitas | Frekuensi per lokasi, perbandingan dengan Bach, analisis partitur |
| Protokol | Versi 2.1, belum dibekukan | Versi baru ditulis; versi 2.1 disimpan sebagai riwayat |

## 8. Yang perlu dibahas di bimbingan berikutnya

Dengan Pak Gathut:

1. Apakah yang Bapak maksud dengan konteks *chorale* adalah bab "Harmonization of Chorales" (hlm. 174–179)? Satu melodi, atau seluruh sepuluh melodi latihan 236?
2. Satu model (Coconet) saja, atau DeepBach tetap ikut sebagai kasus kedua?
3. Apakah studi kasus deskriptif tanpa hipotesis dapat diterima? Dosen Seminar Musikologi 2 dulu meminta variabel dan hipotesis untuk desain kuantitatif (F06, F07).
4. Pedoman *chorale* Strube mana yang wajib dibahas, dan apakah analisis partitur oleh peneliti sendiri cukup?
5. Judul baru: apakah kata *chorale* perlu disebut (G15)?
6. Apakah ada terjemahan jilid II yang memuat bab *chorale*? Bila ada, istilahnya dipakai.
7. Pertanyaan lama yang masih relevan: pengutipan terjemahan Bapak, Strube sebagai buku ajar mata kuliah, aturan pengungkapan bantuan AI.

Dengan Bu Yoni:

1. Lapor bahwa bimbingan dengan Pembimbing I sudah berjalan dan arah v5 sedang disusun.
2. Tanyakan apa yang beliau perlukan sebelum membaca, termasuk lembar atau kartu bimbingan yang perlu ditandatangani.

## 9. Yang perlu kamu kerjakan, berurutan

Sekarang, sebelum arah diputuskan:

1. **Tahan dulu pengetikan 71 melodi.** Bila v5 memilih A atau C, sebagian besar tidak terpakai. Pengetikan sembilan contoh cetak untuk validasi instrumen tetap perlu di semua pilihan.
2. Catat tanggal pertemuan, lalu pindahkan transkrip dari `Downloads` ke tempat yang tetap (misalnya di samping transkrip review Manda). Isi tanggalnya di `feedback.md`.
3. Baca sendiri bab "Harmonization of Chorales" di buku cetak, termasuk hlm. 179 yang hilang di pindaian. Baca juga hlm. 45 dan 55.
4. Putuskan pilihan A, B, atau C. Bila ragu, bawa A dan C ke Pak Gathut dalam satu halaman.
5. Latih jawaban untuk pertanyaan yang muncul di bimbingan: [defense-qa.md](../study/defense-qa.md) bagian M (Q116–Q123).

Sesudah arah dikonfirmasi:

6. Asisten menulis protokol versi baru dan `perubahan-v4-ke-v5.md`, lalu merevisi BAB I–III. Versi naskah dinaikkan ke v5 saat itu.
7. Ketik melodi yang dipilih, cari sumber Bach-nya, dan cocokkan dengan halaman cetak.
8. Uji coba generasi untuk menentukan N, lalu bekukan protokol.
9. Bawa naskah v5 ke Pak Gathut, lalu ke Bu Yoni.

Tugas lama yang tetap berlaku: membaca sumber inti dan mengisi `researcher_read_status`, memeriksa motto, persembahan, dan kata pengantar, serta melengkapi NUPTK pembimbing.

## 10. Yang perlu dibenahi dari cara menjelaskan

Dari transkrip, beberapa penjelasan lisan bisa membuat Pak Gathut salah tangkap. Perbaiki sebelum bimbingan berikutnya:

- **Data latih.** Di bimbingan kamu menyebut model "diberikan soal-soal dan jawaban" dan "dilatih dengan soal yang sama". Pak Gathut bisa mengira model dilatih dengan soal latihan. Bila memakai analogi ini, tegaskan bahwa "soalnya" melodi sopran *chorale* Bach dan "jawabannya" harmonisasi Bach. Tidak ada soal Strube di data latih.
- **Peran Strube dalam satu kalimat.** Contoh: "Strube menjadi sumber kaidah yang diperiksa, sekaligus sumber konteks soal dan pengecualiannya." Jangan memulai dari "melacak kemiripan Bach dan Strube lewat AI", karena itu terdengar seperti tujuan yang lain lagi.
- **Model, bukan aplikasi.** Pak Gathut bertanya apakah ini "aplikasi". Sebut "model AI", dan jelaskan bahwa Bach Doodle adalah aplikasi yang memakai model Coconet.
- **Keacakan.** Jelaskan bahwa model memilih nada dari peluang, sehingga melodi yang sama bisa menghasilkan harmonisasi berbeda. Karena itu setiap melodi dijalankan berulang kali.
- **"Sistem pakar".** Dalam naskah sebut "program pemeriksa berbasis aturan". Instrumen versi 2.0 sudah termasuk jenis ini; yang diusulkan di bimbingan adalah lapisan konteksnya.
