# Rancangan kesepakatan v5

Disusun 8 Oktober 2026 untuk bimbingan berikutnya dengan Bu Yoni (Pembimbing II), lalu untuk konfirmasi ke Pak Gathut (Pembimbing I). Arahan terakhir peneliti hari itu: v5 tidak perlu jauh dari v4, dan dari masukan Pak Gathut diambil yang masuk akal saja. **Belum ada yang disepakati pembimbing.** Atas permintaan peneliti, naskah v5 sudah disusun mengikuti usulan ini sebelum bimbingan (8 Oktober 2026); perubahannya tercatat di [perubahan-v4-ke-v5.md](perubahan-v4-ke-v5.md).

Sumber yang dibaca: transkrip bimbingan dengan Pak Gathut (`~/Downloads/transcript.txt`), form bimbingan skripsi (`~/Downloads/FORM BIMBINGAN SKRIPSI vincent.pdf`), template proposal prodi, naskah v4, protokol 2.1, catatan bacaan Huang dkk. (2019), dan pindaian Strube hlm. 174–179. Lembar yang dibawa ke bimbingan ada di [bimbingan-arah-v5.md](bimbingan-arah-v5.md).

## 1. Ringkasnya

v5 adalah v4 dengan empat perubahan:

1. **Kelompok soal Strube dihapus.** Semua melodi diambil dari satu konteks, yaitu sopran *chorale* Bach di korpus music21. Tidak ada melodi yang diketik.
2. **Pertanyaan 3 diganti.** Pengaruh asal melodi diganti letak pelanggaran: di sekitar fermata atau di dalam frasa.
3. **Peran Strube dipertegas.** Buku Strube diposisikan sebagai panduan yang merangkum praktik, dan pedoman bab *chorale* (hlm. 174) masuk BAB II.
4. **Judul, batas penelitian, dan saran disesuaikan.**

Selebihnya tetap: dua model, pengaturan generasi, lima kaidah dan instrumen 2.0, harmonisasi Bach sebagai pembanding, pertanyaan 1 dan 2, uji Wilcoxon untuk perbedaan model, dan pengukuran tanpa penilai manusia.

## 2. Yang berubah dan yang tetap

| Bagian | v4 | v5 |
| --- | --- | --- |
| Judul | *Evaluasi Musik Hasil AI DeepBach dan Coconet: Pengaruh Asal Melodi terhadap Kepatuhan Kaidah Gerak Suara Strube* (16 kata) | *Evaluasi Musik Hasil AI DeepBach dan Coconet: Kepatuhan Kaidah Gerak Suara Strube pada Harmonisasi Chorale* (15 kata, batas maksimal 15) |
| Model | DeepBach dan Coconet, pengaturan bawaan | Tetap |
| Melodi | 71 soal Strube (diketik) + sampel acak Bach sebanyak itu, minimal 30 | 40 sopran *chorale* Bach dari korpus, acak dengan *seed* 20261004, dari melodi yang lolos pemeriksaan masukan kedua model |
| Generasi | 5 per melodi per model, sedikitnya 600 harmonisasi | 5 per melodi per model, 400 harmonisasi |
| Pertanyaan 1 | Tingkat kepatuhan tiap model per asal melodi, dibanding Bach | Tingkat kepatuhan tiap model, dibanding Bach pada melodi yang sama |
| Pertanyaan 2 | Beda DeepBach dan Coconet | Tetap |
| Pertanyaan 3 | Pengaruh asal melodi | Letak pelanggaran: di sekitar fermata atau di dalam frasa, per model, dibanding Bach |
| Variabel | X1 model, X2 asal melodi, Y pelanggaran per birama | X1 model, X2 letak dalam frasa, Y pelanggaran per birama dan per kesempatan |
| Hipotesis | H1 beda model; H2–H3 Strube lawan Bach (Mann–Whitney) | H1 tetap; H2 di sekitar fermata lawan di dalam frasa (Wilcoxon berpasangan per melodi) |
| Ukuran sampel | Analisis daya dua kelompok (30 per kelompok) | Analisis daya berpasangan: 40 melodi untuk *d_z* sekitar 0,5. Angka ini sudah ada di protokol 2.1 untuk pertanyaan 2 |
| Landasan teori | Briot, Storkey, Pearce, Strube, Huron | Storkey keluar. Strube ditambah Preface dan hlm. 174. Briot ditambah satu hal: DeepBach menerima fermata, Coconet tidak |
| Analisis sensitivitas | a, b, c, d | Tetap |
| Uji coba | 3 melodi Bach + 3 melodi Strube | 3 melodi Bach di luar sampel |
| Kerja manual peneliti | Mengetik 71 melodi dan 9 contoh cetak | Mencocokkan 9 contoh cetak yang disiapkan asisten; menulis progresi akor 5 contoh acak |

## 3. Masukan Pak Gathut yang diambil

| Kode | Masukan | Diambil? | Di v5 |
| --- | --- | --- | --- |
| G01–G02 | Setiap soal Strube punya konteks bab; mesin memperlakukannya sama | Ya | Soal dari sepuluh bab tidak digabung lagi; semua melodi dari konteks *chorale* |
| G03 | Keluaran acak, untuk apa? | Ya | Lima harmonisasi per melodi dirata-rata (sudah di v4); dijelaskan di BAB III |
| G04 | Strube dipakai untuk apa? | Ya | Strube = sumber kaidah, definisi konteks (fermata sebagai kadens, hlm. 174), dan dasar memakai melodi Bach (hlm. 174) |
| G05 | Batasi | Ya | Satu konteks, tanpa pengetikan |
| G06 | Konteks *chorale*; lacak kemiripan dengan Bach | Ya | Melodi *chorale* Bach; harmonisasi Bach sebagai pembanding; `copy_share` |
| G07 | Satu sampel; dua AI terlalu banyak "untuk sekarang" | Tidak | Dua model tetap (alasan di bawah) |
| G08 | Di bagian mana kesalahan cenderung terjadi | Ya | Pertanyaan 3 |
| G09 | Paralel dibaca bersama progresi akornya | Sebagian | Lima contoh acak dibahas dengan progresi akornya, seperti rencana v4 |
| G10 | Mesin tanpa rasa | Ya | Batas penelitian |
| G11 | Sisanya ke saran | Ya | Asal melodi, soal Strube per bab, studi kasus satu melodi, pedoman *chorale* yang perlu analisis akor |
| G12 | Kaidah apa yang dibawa untuk *chorale* | Sebagian | Fermata sebagai kadens dan persilangan di bawah sopran (hlm. 174). Pedoman yang perlu penentuan akor tidak diukur |
| G13 | Pemeriksa berbasis aturan + keluaran AI | Ya | Sudah: instrumen 2.0 |
| G14 | Jangan terlalu berat di ilmu komputer | Ya | Penjelasan model tetap ringkas |
| G15 | Sebut *chorale* | Ya | Judul |

Alasan tetap dua model (G07): penelitian ini meneruskan evaluasi yang sebelumnya dilakukan per model (DeepBach oleh Hadjeres dkk.; Coconet oleh Huang dkk. 2017, 2019). Perbandingan keduanya pada melodi yang sama adalah sumbangan utama sejak v3. Di transkrip, Pak Gathut menilai perbandingan dua AI "terlalu" untuk sekarang, tetapi juga menyebut "kalau misalnya kamu mau bisa". Usulan ini memilih yang kedua, dan pembatasannya diterapkan pada konteks dan bahan, bukan pada model. Butir ini yang paling perlu beliau setujui. Model kedua tidak menambah kerja manual, karena pipeline untuk keduanya sudah jadi.

## 4. Pertanyaan, variabel, hipotesis

1. Bagaimana tingkat kepatuhan harmonisasi DeepBach dan Coconet terhadap kaidah gerak suara Strube pada melodi *chorale* Bach, dibandingkan dengan harmonisasi Bach untuk melodi yang sama?
2. Bagaimana perbedaan tingkat kepatuhan terhadap kaidah gerak suara Strube antara harmonisasi DeepBach dan Coconet pada melodi yang sama?
3. Bagaimana letak pelanggaran kaidah gerak suara Strube pada harmonisasi DeepBach dan Coconet, di sekitar fermata atau di dalam frasa, dibandingkan dengan harmonisasi Bach?

Pertanyaan 1 dijawab dengan statistik deskriptif, seperti di v4. Hipotesis diuji per kaidah dengan koreksi Holm atas lima kaidah:

- **H1 (pertanyaan 2, sama dengan v4).** Terdapat perbedaan pelanggaran per birama antara DeepBach dan Coconet pada melodi yang sama. Dua arah.
- **H2 (pertanyaan 3).** Pada setiap model, laju pelanggaran per kesempatan di sekitar fermata berbeda dari laju di dalam frasa. Dua arah. Pola Bach pada melodi yang sama dilaporkan secara deskriptif sebagai pembanding.

Zona fermata: gerak yang berawal atau tiba di dalam nada sopran berfermata; untuk jarak dan persilangan, peristiwa bunyi di dalam nada itu. Batas ini ditetapkan di protokol sebelum data dikumpulkan. Letak tidak dimanipulasi, jadi hasil pertanyaan 3 dibaca sebagai hubungan, bukan sebab. Bedanya, DeepBach menerima fermata dan Coconet tidak. Perbedaan pola keduanya dibahas sebagai salah satu kemungkinan penjelasan, bukan sebab tunggal, karena kedua model berbeda dalam banyak hal sekaligus (Briot dkk.).

## 5. Kenapa letak pelanggaran

- Menjawab pertanyaan Pak Gathut yang paling praktis: di bagian mana kesalahan cenderung terjadi (G08).
- Huang dkk. menghitung paralel per birama saja. Mereka menyebut banyak paralel pada *chorale* Bach dapat dimaklumi di batas frasa (hlm. 798), tetapi tidak mengukur letak pelanggaran pada keluaran model.
- Strube memperlakukan fermata sebagai kadens (hlm. 174). Pak Gathut mengingatkan bahwa buku Strube adalah rangkuman dengan keterbatasan. Letak di mana Bach sendiri menyimpang menunjukkan batas rangkuman itu.
- Pemeriksaan instrumen 2.0 pada harmonisasi Bach sendiri, 318 *chorale*, menunjukkan letak memang penting. Ini eksplorasi, bukan data penelitian (`research/experiments/scripts/explore_fermata_zone_bach.py`).

| Kaidah | Porsi kesempatan di zona fermata | Porsi pelanggaran Bach di zona fermata | Laju di zona fermata dibanding di dalam frasa |
| --- | --- | --- | --- |
| Kuint sejajar | 17,2% | 27,5% (11 dari 40) | 1,8 kali |
| Oktaf sejajar | 17,2% | 38,5% (5 dari 13) | 3,0 kali |
| Jarak suara atas | 9,7% | 1,9% (7 dari 360) | 0,18 kali |
| Persilangan di atas sopran | 9,8% | 10,0% (5 dari 50) | 1,0 kali |
| Tumpang tindih | 17,1% | 54,8% (257 dari 469) | 5,9 kali |

Hitungan kuint dan oktaf kecil, jadi keduanya dibaca hati-hati.

## 6. Pertanyaan yang mungkin muncul

| Pertanyaan | Jawaban singkat |
| --- | --- |
| Kenapa soal Strube tidak dipakai lagi? | Soal dari sepuluh bab punya konteks berbeda (G02). Strube sendiri mengambil soal *chorale*-nya dari Bach (hlm. 174), dan korpus menyediakan melodi itu beserta jawaban Bach. Asal melodi masuk saran |
| Pak Gathut menyarankan satu model dan satu sampel | Bagian 3: pembatasan pada konteks dan bahan; beliau sendiri menyebut perbandingan dua model bisa dilakukan |
| Model tidak diajari kaidah, kok diuji pakai kaidah? | Patokannya praktik Bach, guru tempat model belajar, bukan nol pelanggaran. Kaidah Strube adalah lensa yang eksplisit untuk membaca keduanya (Pearce dkk.; Huang dkk. memakai pembanding yang sama) |
| Melodinya ada di data latih? | Kemungkinan besar. Untuk DeepBach, keanggotaan data latihnya dihitung (analisis sensitivitas b). Untuk Coconet tidak diketahui, jadi `copy_share` dilaporkan |
| Mana variabel bebas yang diatur peneliti (F06)? | X1 model dan X2 letak. Bila diminta variabel yang benar-benar dimanipulasi, pakai tambahan di bagian 7 |
| Pedoman *chorale* lain tidak diukur? | Perlu penentuan akor dan tangga nada, yang bisa berbeda antaranalis. Alasannya sama sejak v3; pedoman itu masuk saran |
| Validitas instrumen? | Langkah 3–5 sudah dijalankan. Langkah 2 (contoh cetak Strube) diselesaikan sebelum uji coba |
| Hasil berlaku untuk apa? | *Checkpoint* yang diuji, pengaturan bawaan, melodi *chorale* Bach. Tidak untuk arsitektur secara umum |

## 7. Tambahan opsional: DeepBach dengan dan tanpa fermata

Bila Bu Yoni atau Pak Gathut meminta variabel yang benar-benar diatur peneliti (F06), atau ingin menguji kalimat Pak Gathut "kecuali kalau mesinnya diberi konteks": DeepBach dijalankan sekali lagi pada 40 melodi yang sama dengan informasi fermata dihapus. Model dan melodinya sama, hanya konteksnya yang berbeda, jadi perbedaannya boleh dibaca sebagai pengaruh informasi fermata. Kerjanya satu pilihan di adaptor dan 200 generasi tambahan, tanpa kerja manual. Tidak dimasukkan ke usulan utama karena v5 diminta tetap dekat dengan v4.

## 8. Kerja yang tersisa

Kerja manual peneliti:

1. Mencocokkan sembilan contoh cetak Strube, yang disiapkan asisten dari pindaian dan terjemahan, dengan buku cetak (validasi langkah 2).
2. Menulis progresi akor untuk lima contoh acak di BAB IV.
3. Mengisi form bimbingan setelah setiap pertemuan.

Kerja asisten yang sudah selesai pada 8 Oktober 2026, atas permintaan peneliti dan sebelum bimbingan:

- Protokol versi 3.0, dengan versi 2.1 disimpan sebagai riwayat.
- Pipeline: kelompok Strube dihapus, sampel 40 melodi Bach.
- Perhitungan zona di evaluasi, beserta uji perangkat lunaknya.
- Analisis H2.
- Revisi BAB I–III dan `perubahan-v4-ke-v5.md`.

Yang belum: draf sembilan contoh cetak. Bila pembimbing meminta perubahan, naskah dan protokol disesuaikan lagi sebelum diberi tag `thesis/v5`. Model dipasang dan dijalankan hanya atas permintaanmu.

## 9. Bimbingan dengan Bu Yoni dan administrasi

Dari form bimbingan skripsi Jurusan Musik: konsultasi dengan **setiap** pembimbing minimal 12 kali; bila kurang, mahasiswa tidak boleh maju ujian. Form diserahkan saat mendaftar ujian dan sekarang memuat judul v4.

1. Isi baris pertama untuk Pak Gathut. Berkas form dibuat 6 Oktober pukul 14.32 dan transkrip 16.18, jadi pertemuannya kemungkinan 6 Oktober. Pastikan, lalu catat juga di `feedback.md`.
2. Bawa [bimbingan-arah-v5.md](bimbingan-arah-v5.md) (cetakan `scratch/bimbingan-arah-v5.pdf`), form bimbingan, dan PDF draf v5 (`scratch/Skripsi_v5_23104810131_Vincent.pdf`) di laptop.
3. Pembuka, dengan kata-katamu sendiri:

> Bu, naskah v4 sudah saya bawa ke Pak Gathut. Masukan utama beliau: soal Strube dari bab yang berbeda tidak bisa digabung begitu saja, karena setiap soal punya konteks yang tidak diketahui model AI. Jadi di v5 saya tetap membandingkan DeepBach dan Coconet, tetapi semua melodinya dari satu konteks, yaitu *chorale* Bach, karena Strube sendiri mengambil soal *chorale*-nya dari Bach. Pertanyaan tentang asal melodi saya ganti dengan pertanyaan yang beliau anggap berguna untuk pengajar: di bagian frasa mana model paling sering melanggar. Saya mohon masukan Ibu tentang pendekatan, judul, dan jadwal bimbingan.

4. Sesudahnya, catat jawaban beliau di lembar, isi form, lalu bawa lembar yang sama ke Pak Gathut. Butir dua model (bagian 3) perlu beliau setujui secara eksplisit. Setelah keduanya setuju, kesepakatan dicatat dengan tanggal di `feedback.md`.

## 10. Catatan dari transkrip yang belum tercatat di G01–G15

Di tengah bimbingan kamu bertanya apakah kamu boleh menentukan kaidah siapa yang dipakai. Jawaban yang tercatat kira-kira: "Bisa. Misalnya nanti ternyata koral dibahas di buku lain juga." Label pembicara di transkrip sering tertukar, jadi atribusinya tidak pasti. Rekomendasi: tetap pakai Strube sebagai satu-satunya sumber kaidah, karena judul, F01, dan F05 sudah mengikat Strube. Buku lain masuk saran.

## Riwayat usulan 8 Oktober

Dua usulan sebelumnya pada hari yang sama ditinggalkan atas arahan peneliti. Rinciannya di [research-log.md](../records/research-log.md):

- **Studi kasus Model 235:** Coconet saja, satu melodi 100 kali. Ditinggalkan karena kerja manualnya paling banyak.
- **Desain hemat:** Coconet saja, 40 melodi. Ditinggalkan karena peneliti ingin tetap dua model, dekat dengan v4.
