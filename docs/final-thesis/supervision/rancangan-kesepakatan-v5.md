# Rancangan kesepakatan revisi v5 setelah pembacaan Strube

Disusun 13 Oktober 2026 untuk Vincent dan kedua pembimbing. Dokumen ini menggantikan usulan 8–9 Oktober tentang 40 melodi dan zona fermata. Usulan lama disimpan utuh dalam [arsip 8 Oktober](rancangan-kesepakatan-v5-2026-10-08.md). Naskah v5 kini telah direvisi mengikuti arah kasus pada 13 Oktober; rencana protokol 4.0 dan instrumen kontekstual 3.0 tertulis di research/protocol.md. Naskah yang sudah ditag `thesis/v5` tetap merupakan draf; pembacaan sumber dan usulan di sini belum berarti persetujuan pembimbing atau perubahan protokol generasi.

## 1. Arah yang direkomendasikan

Skripsi diarahkan menjadi studi kasus evaluatif gerak suara pada harmonisasi chorale hasil AI berdasarkan kaidah Strube yang dibaca bersama konteks dan pengecualiannya. Satu melodi dari bab chorale menjadi bahan utama. MODEL no. 285 menjadi calon utama karena buku mencetak harmonisasi empat suaranya. DeepBach dan Coconet dapat dibandingkan pada melodi yang sama dengan jumlah keluaran yang sanggup diperiksa secara musikal.

Fokus ini menjawab kebutuhan peneliti untuk memahami gerak masing-masing suara dan hubungan antarsuara. Fermata dicatat bila diperlukan untuk membaca kadens atau memasukkan metadata DeepBach. Pertanyaan tentang zona fermata dan percobaan menghilangkan metadata fermata tidak masuk usulan ini.

Dua model dipertahankan dalam rekomendasi agar kebutuhan perbandingan peneliti tetap terwadahi. G07 mencatat saran Pak Gathut untuk kasus kecil dan mempertimbangkan satu model; persetujuan beliau atas dua model masih diperlukan. Jika beliau menghendaki satu model, Coconet menjadi pilihan kerja karena hubungan langsungnya dengan analisis Bach Doodle. Kaidah, material, dan cara membaca partitur tetap sama.

## 2. Apa yang ditemukan pada sumber

| Temuan | Bukti | Akibat bagi desain |
| --- | --- | --- |
| Teks dua scan sudah diproses pada seluruh halaman PDF | Inggris 147/147; terjemahan jilid I 91/91; hash dan jejak gambar tersedia di `references/ocr/` | Pencarian teks sudah tersedia. Angka cakupan ini tidak berarti seluruh teks sudah disunting atau seluruh notasi sudah ditranskripsi |
| Buku ditujukan terutama bagi mahasiswa konservatori dan berasal dari bahan pengajaran Strube | Dedication dan Preface, PDF 4–5; Preface bertanggal Januari 1928 | Buku dibaca sebagai pedoman pedagogis dengan tahap materi, bukan kumpulan larangan tanpa konteks |
| MODEL 285 memuat harmonisasi empat suara pada hlm. 174–176 | Lima sistem SATB pada PDF 136–137 | Sopran dapat dijadikan masukan; tiga suara bawah cetak menjadi acuan pilihan harmonisasi, setelah pembacaan lengkap diverifikasi |
| EXERCISES 286 mulai setelah MODEL pada hlm. 176 | Label dan notasi pada PDF 137 | Melodi latihan bukan daftar jawaban. Tidak ditemukan kunci per latihan dalam scan yang ditinjau |
| MODEL belum menjadi acuan digital lengkap | Cap menutupi awal bas; notasi rendah resolusi; pembacaan durasi sopran akhir perlu salinan lebih jelas | Jangan membekukan input atau memakai baseline SATB lengkap dari hasil OMR mentah. Sumber ini cukup untuk memilih arah kasus, tetapi belum cukup untuk pengumpulan data utama |
| Ada contoh pendek yang jelas untuk memeriksa kriteria | Fig. 33 hlm. 13: panel `good` pertama dan `avoid`, 16 catatan nada ditranskripsi | Deteksi tumpang tindih dapat dibandingkan dengan label buku. Ini dua contoh satu kaidah, bukan validasi seluruh instrumen |
| Pengecualian tersebar pada materi lanjut | Hlm. 34–35, 45, 83, 96, 109, serta pedoman chorale hlm. 174 | Lima hitungan lama harus dibaca sebagai kandidat kejadian sampai konteksnya dinilai |

Peta 14 keluarga kriteria dan alasan pemakaiannya ada dalam [peta kaidah](../study/peta-kaidah-gerak-suara-strube.md). [Audit bahan chorale](../../../research/literature/strube-scores/chorale-source-audit.json) mencatat gambar dan batas keterbacaannya. MODEL tidak disebut sebagai harmonisasi asli Bach sebelum identitas karya dan aransemen dibuktikan. Pencocokan kontur yang dicoba belum mengidentifikasinya; ketiadaan kecocokan belum membuktikan asalnya bukan Bach.

Terjemahan yang tersedia lokal hanya jilid I, sampai hlm. 89. [Katalog resmi ISI](https://opac.isi.ac.id/index.php?id=33547&keywords=&p=show_detail) mencatat jilid II terjemahan A. Gathut Bintarto T., terbit 2016, iv + 142 halaman, nomor panggil `781.3 Str t-II`; halaman katalog yang ditinjau tidak menyediakan lampiran digital. Buku ini merupakan jalur nyata untuk mencocokkan istilah dan memperoleh bagian lanjut, dengan keterbacaan notasinya tetap perlu diperiksa.

## 3. Posisi Strube dan teori lain

Strube menjadi landasan teori musik langsung: penulisan harmoni empat suara, gerak suara, fungsi akor, tahap materi, dan pengecualiannya. Kata “fungsi” di sini berarti peran akor, misalnya tonika, subdominan, dan dominan pada hlm. 6. Peran itu diperlukan ketika menentukan apakah sebuah nada merupakan nada akor, nada hias, atau nada yang sedang menuju resolusi. Preface memang menekankan fungsi akor dalam lingkungannya. Istilah kerja “harmoni tonal fungsional” pada draf lama harus dijelaskan melalui konsep yang diajarkan Strube; istilah tersebut tidak memberi alasan untuk mengganti fokus gerak suara.

Catatan F08/F12 meminta grand theory. Susunan “grand theory → kaidah Strube → definisi operasional” dalam draf merupakan susunan peneliti, bukan pembagian yang ditulis Strube. Usulan untuk bimbingan adalah menyebut kerangka umumnya **teori harmoni Strube tentang fungsi akor dan penulisan empat suara**, kemudian menunjukkan halaman serta contoh yang menghubungkannya dengan kriteria. Penamaan tingkat teori perlu disepakati; isinya harus dapat ditelusuri ke sumber.

Pearce, Meredith, dan Wiggins menjelaskan perlunya evaluasi yang sesuai tujuan model. Briot, Hadjeres, dan Pachet membantu mendeskripsikan perbedaan sistem yang dibandingkan. Huron dapat mendukung tafsiran tentang keterpisahan suara, tanpa mengubah penelitian ini menjadi pengujian persepsi pendengar. Teori pergeseran dataset tidak perlu dipertahankan jika pertanyaan tentang asal melodi dihapus.

Rantai yang dipakai adalah:

> Pedoman Strube dalam konteks chorale → kriteria dan pengecualian → tugas sopran tetap → keluaran A/T/B dari checkpoint tertentu → catatan kejadian dan keputusan musikal → profil kesesuaian pada kasus yang diuji.

Program pemeriksa membantu menemukan dan mencatat kejadian. Kontribusi skripsi adalah pengetahuan tentang gerak suara pada keluaran AI yang diteliti beserta contoh dan penjelasannya.

## 4. Hubungan dengan DeepBach dan Coconet

[DeepBach 2017, §2](https://proceedings.mlr.press/v70/hadjeres17a/hadjeres17a.pdf) menggunakan jaringan rekuren dan pseudo-Gibbs sampling untuk harmonisasi chorale. Implementasi asli menyaring korpus menjadi 352 karya, memperluasnya melalui transposisi menjadi 2.503 contoh, lalu membagi 80% untuk pelatihan dan 20% untuk validasi. [Coconet 2017, §3 dan §6](https://archives.ismir.net/ismir2017/paper/000187.pdf) mempelajari chorale Bach empat suara sebagai piano roll dan melengkapi bagian yang dikosongkan melalui model konvolusional dan sampling. Rincian ini menjelaskan cara sistem belajar pola dari data. Klaim bahwa keduanya dilatih persis seperti otak manusia tidak diperlukan dan tidak didukung makalah tersebut.

Hubungannya dengan Strube ada pada lingkungan musik, tugas harmonisasi empat suara, dan aspek gerak suara yang dapat dibaca dari keluaran. Hubungan ini belum merupakan korelasi statistik yang diukur. Model tidak perlu dilatih dari buku Strube agar keluarannya dapat dievaluasi dengan pedoman eksternal yang relevan. Sebaliknya, kesamaan domain Bach tidak menjamin semua kaidah Strube diterapkan model atau semua contoh buku masuk pelatihan.

Versi yang direncanakan proyek adalah DeepBach PyTorch commit `6d75cb940f3aa53e02f9eade34d58e472e0c95d7` dan `@magenta/music@1.23.1`, checkpoint Coconet `coconet/bach`. Pembagian data implementasi PyTorch berbeda dari angka makalah asli. Artefak checkpoint dan keanggotaan kasus pada train/validation/test belum diperiksa. Penelitian tetap dapat mengevaluasi keluaran pada kasus yang dipilih, tetapi belum boleh menyebutnya kemampuan pada melodi baru atau bukti pemahaman Strube. Perbandingan kedua sistem juga belum mengisolasi pengaruh CNN dan LSTM.

## 5. Desain konkret untuk dibahas

| Komponen | Usulan yang dapat ditinjau |
| --- | --- |
| Objek | Harmonisasi simbolik hasil AI, terutama gerak alto, tenor, bas, dan hubungan ketiganya dengan sopran tetap |
| Kasus | Satu melodi dalam konteks chorale Strube; calon utama sopran MODEL 285, setelah transkripsi lengkap lolos pemeriksaan sumber |
| Acuan | Harmonisasi yang dicetak Strube. Acuan Bach ditambahkan hanya setelah identitas dan kesesuaian versinya dibuktikan |
| Sistem | DeepBach dan Coconet pada versi yang disebut di atas, dengan pengaturan efektif dicatat; pilihan dua model dibawa untuk kesepakatan |
| Skala awal | Usulan 20 percobaan generasi per model, total 40 percobaan pada satu melodi. Ini pilihan beban pemeriksaan, bukan hasil power analysis atau jumlah yang sudah disetujui |
| Pengulangan | Setiap percobaan mulai dari inisialisasi baru; hasil identik dan kegagalan tetap disimpan. Tidak meneruskan rantai keluaran sebelumnya tanpa mencatat perubahan desain |
| Analisis utama | Profil per kaidah dan per lokasi, keputusan konteks pada partitur, variasi antarkeluaran, serta perbedaan deskriptif kedua sistem |
| Inferensi | Kesimpulan pada kasus tetap dan checkpoint yang diuji; tidak memakai uji Wilcoxon antarmelodi atau hipotesis zona fermata dari desain lama |
| Penilai/pendengar | Analisis partitur dilakukan peneliti. Tidak direncanakan survei pendengar atau panel penilai. Pemeriksaan pembimbing atas sumber/kriteria dicatat sebagai pemeriksaan, bukan angka kesepakatan antarpenilai yang belum diukur |

Angka 20 membuat frekuensi biner berubah setiap 5 poin persentase pada 20 keluaran layak. Estimasi dengan jumlah ini dapat masih lebar; tujuan awalnya membaca pola pada satu kasus. Kegagalan mengurangi jumlah keluaran layak dan harus terlihat pada penyebut. Jika ingin mengubah jumlah, alasan teknis dan beban analisis dicatat sebelum pengumpulan utama. Jumlah final ditetapkan setelah pilot yang diminta secara terpisah dan kesepakatan pembimbing.

Satu melodi dengan banyak generasi tetap satu kasus musikal. Keluaran yang diperoleh secara acak dan independen dapat menggambarkan perilaku generator bersyarat pada masukan itu; birama dan transisi dalam satu keluaran tidak otomatis independen. Seed bernomor sama pada dua sistem juga tidak membuat keluaran menjadi pasangan acak yang setara. [Flyvbjerg 2006](https://arxiv.org/pdf/1304.1186) mendukung nilai pengetahuan kontekstual studi kasus, bukan keterwakilan semua chorale. [Lazic 2010](https://link.springer.com/article/10.1186/1471-2202-11-5) menjadi rujukan tentang unit pengamatan dan pseudoreplikasi.

## 6. Kriteria dan penilaian

Lima keluarga yang sudah diimplementasikan tetap berguna sebagai awal: kuint sejajar, oktaf/unisono sejajar, jarak suara atas, persilangan, dan tumpang tindih. Alasan pemakaiannya sekarang ditelusuri dari buku. Jarak suara di atas oktaf dan persilangan suara bawah memerlukan perhatian pada durasi serta syarat sumber; keduanya tidak dinilai melalui hitungan biner lama saja.

Gerak horizontal A/T/B wajib dideskripsikan melalui langkah, lompatan, arah, dan kelanjutan sesudah lompatan bas. Gerak menuju kuint/oktaf tersembunyi dicatat sebagai pola pendamping dengan syarat sumber yang eksplisit. Penggandaan, jenis akor, nada penuntun, septim, suspensi, dan nada bantu dipakai sejauh diperlukan untuk menjelaskan kejadian itu. Menjadikannya seluruhnya sebagai kriteria normatif tersendiri akan memperluas tujuan dan harus dinyatakan sebelum data diambil.

Setiap kandidat kejadian diberi keputusan:

1. **Menyimpang terkonfirmasi**, apabila melanggar kriteria yang berlaku dan tidak memenuhi pengecualian yang relevan.
2. **Diterima menurut syarat/pengecualian**, dengan halaman dan alasan musikal.
3. **Belum dapat diputuskan**, apabila fungsi, ejaan, keterbacaan, atau ruang penafsiran belum cukup jelas.

Kategori ketiga tetap dilaporkan. Jumlahnya tidak disembunyikan dalam nol pelanggaran. Untuk transisi, penyebut adalah kesempatan pasangan suara yang memenuhi syarat. Jarak dan persilangan juga dilaporkan sebagai episode dan durasi; menahan satu keadaan selama banyak langkah tidak boleh diam-diam menjadi banyak kesalahan baru. Definisi episode, langkah diatonis, dan harmonisasi yang dianalisis harus dibekukan pada protokol baru sebelum dipakai.

Ejaan nada keluaran Coconet dan perbedaan antara nada ditahan dan nada sama yang diulang membatasi perbandingan. Ukuran utama mengutamakan informasi bunyi yang tersedia pada kedua sistem. Analisis yang memerlukan ejaan harus mencatat setiap inferensi dan kasus ambigu. Pencocokan nada dengan acuan adalah ukuran kemiripan tersendiri; berbeda dari acuan tidak otomatis berarti salah.

Analisis memeriksa seluruh kandidat kejadian pada keluaran layak dan juga bagian yang tidak ditandai program dengan aturan pemilihan yang dicatat. Dua contoh Fig. 33 belum membuktikan detektor lengkap pada semua jenis kejadian. Instrumen versi 2.0 dan hasil lamanya dipertahankan; definisi serta anotasi baru harus mendapat versi baru ketika diimplementasikan.

## 7. Rumusan penelitian yang diusulkan

Judul kerja, 15 kata:

> Evaluasi Musik Hasil AI DeepBach dan Coconet Berdasarkan Kaidah Gerak Suara Strube dalam Harmonisasi Chorale

Pertanyaan penelitian:

1. Bagaimana kesesuaian gerak suara harmonisasi DeepBach dan Coconet pada melodi chorale yang dipilih dengan kaidah Strube, setelah memperhatikan kondisi penerapan dan pengecualiannya?
2. Bagaimana perbedaan profil gerak suara kedua model pada kasus tersebut, ditinjau dari kejadian yang berulang, lokasi partitur, dan harmonisasi acuan yang tersedia?

Manfaatnya berupa informasi tentang bagian keluaran AI yang perlu diperiksa sebelum dijadikan contoh belajar harmoni. Penelitian tidak mengukur peningkatan hasil belajar atau keindahan musik. Peta contoh dan keputusan musikal dapat memperlihatkan kepada pengajar mengapa suatu gerak perlu dikoreksi atau diterima.

## 8. Kasus kecil dan dataset besar

| Lingkup | Pertanyaan yang dapat dijawab | Pekerjaan yang diperlukan |
| --- | --- | --- |
| Satu kasus, satu model | Pilihan dan penyimpangan gerak suara pada satu tugas yang terlacak | Pemeriksaan sumber dan konteks setiap keputusan |
| Satu kasus, dua model, rekomendasi saat ini | Perbedaan profil dua sistem pada tugas yang sama | Sumber dan kriteria yang sama; pemeriksaan seluruh keluaran kedua sistem |
| Kasus utama dan beberapa kasus pendukung | Apakah pola juga tampak pada bahan lain dalam konteks serupa? | Kriteria pemilihan sebelum melihat hasil; kasus tetap tidak otomatis mewakili repertoar |
| Sampel besar dari kerangka jelas | Kecenderungan lintas melodi | Sampling, alat ukur yang konsisten, pemeriksaan pengecualian pada skala itu, dan analisis data bertingkat |

Dataset besar diletakkan sebagai kemungkinan lanjutan karena pertanyaan sekarang memerlukan pembacaan rinci. Alasan kasus kecil adalah keterlacakan sumber dan kedalaman analisis yang diminta G01–G09. Ukuran skripsi S-1 sendiri tidak mengesahkan definisi yang keliru atau contoh yang dipilih karena menguntungkan hasil.

## 9. Butir kesepakatan dan konsekuensi revisi

| Butir yang dibawa | Rekomendasi | Keputusan/tanggal pembimbing |
| --- | --- | --- |
| Fokus musik | Gerak suara dalam konteks chorale Strube; fermata sebagai konteks | Belum ada |
| Material | MODEL 285 sebagai calon utama, setelah salinan dan transkripsi diverifikasi | Belum ada |
| Lingkup sistem | Dua model pada satu kasus; Coconet saja jika lingkup satu model ditetapkan | Belum ada |
| Kriteria | Peta sumber dan pengecualian; analisis horizontal serta hubungan antarsuara | Belum ada |
| Metode | Studi kasus evaluatif dengan analisis partitur dan ringkasan kuantitatif; bentuk variabel/hipotesis sesuai ketentuan prodi | Belum ada |
| Skala | Usulan 20 percobaan per model; jumlah final setelah kelayakan dan beban analisis diperiksa | Belum ada |
| Teori dan judul | Isi teori ditelusuri ke Strube; judul kerja 15 kata di atas | Belum ada |
| Pemeriksaan | Sumber transkripsi, contoh diterima/ditolak, konteks keputusan dan bagian tanpa flag | Belum ada |

Revisi BAB I–III, judul dan abstrak telah dikerjakan pada 13 Oktober sesuai permintaan peneliti. Konsekuensi revisi yang menjadi dasarnya: BAB I mengganti alasan pemilihan bahan, rumusan, pertanyaan, tujuan, dan manfaat. BAB II memuat tahap Strube dan peta kaidah; kerangka berpikir tidak lagi menempatkan zona fermata sebagai X2. BAB III menjelaskan pemilihan kasus, generasi berulang, keputusan musikal, penyebut, dan batas inferensi. Hipotesis, power analysis, dan pengujian lama tidak dipindahkan otomatis. Sampul dan abstrak diperbarui hanya saat revisi naskah memang dilakukan.

Bahan kesepakatan sudah tersedia. Sebelum kasus dikunci, kebutuhan sumber yang tersisa adalah salinan notasi MODEL yang cukup jelas untuk memulihkan bas yang tertutup cap dan durasi akhir. Halaman cetak 179 juga diperlukan jika latihan terakhir dipilih; halaman itu bukan bagian MODEL. Identitas Bach ditelusuri untuk klaim yang memang memerlukannya. Rencana protokol 4.0 sudah ditulis; setelah arah disepakati, implementasi diselaraskan, transkripsi dan instrumen diperiksa, lalu pilot dijalankan hanya atas permintaan peneliti.
