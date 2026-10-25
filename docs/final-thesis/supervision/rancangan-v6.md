# V6: satu model dan analisis kasus Strube

Keputusan kerja peneliti, 21 Oktober 2026, setelah kelas Seminar Musikologi 2. Masukan Pak Galih tentang satu model dilaporkan peneliti dalam percakapan; ini tidak mencatat persetujuan Pembimbing I/II atas seluruh rancangan. Sumber v5 tetap tersedia pada tag `thesis/v5` dan commit `86e1887`. Perubahan berikut menyangkut naskah dan rencana; pengumpulan data belum dilaksanakan.

## Dasar perubahan

Peneliti meminta satu model yang relevan dengan analisis, pendekatan dan sumber yang jelas, alur analisis sampai jawaban penelitian, serta BAB I–IV siap. Perbandingan arsitektur dihapus dari tujuan. V5 sebenarnya sudah membatasi klaim pada konfigurasi sistem, tetapi kebutuhan membandingkan dua sistem belum memberi alasan musikal yang cukup bagi peneliti. V6 memusatkan perhatian pada keluaran Coconet menurut Strube.

## Pemilihan model

| Pertimbangan | Bukti | Keputusan untuk v6 |
| --- | --- | --- |
| Persoalan gerak suara sudah didokumentasikan | Huang dkk. 2019, hlm. 798, menghitung kuint dan oktaf sejajar pada keluaran Coconet; contoh acuan juga membawa konteks nada nonakor dan batas frasa | Coconet memberi kesinambungan langsung dengan persoalan yang hendak diperiksa |
| Tugas sesuai dengan objek musikal | Huang dkk. 2017, hlm. 211–215; dokumentasi Coconet menjelaskan pelengkapan empat suara | Satu sopran ditetapkan, alto/tenor/bas dihasilkan |
| Pembagian suara dapat dicatat | Dokumentasi resmi `@magenta/music` 1.23.1 menetapkan instrumen 0/1/2/3 sebagai S/A/T/B dan menyediakan konfigurasi mask | Mask eksplisit hanya mencakup A/T/B; pemeliharaan sopran diperiksa pada keluaran |
| Informasi notasi terbatas | Piano roll tidak membedakan nada ulang dan nada tahan; ejaan asli tidak tersedia | Analisis gerak memakai lintasan bunyi; inferensi ejaan dan ambiguitas dicatat |
| Ada alternatif yang juga layak | DeepBach menerima bagian tetap, menurut Hadjeres dkk. 2017 | DeepBach tetap dibahas sebagai penelitian terdahulu; kemampuan ini tidak mewajibkan perbandingan |
| Model lebih baru belum tentu sesuai tugas | Antarmuka NotaGen yang telah dibaca dalam tinjauan tidak menyediakan tugas tetap yang sama | Kebaruan tahun model tidak menjadi dasar pemilihan |

Pemilihan Coconet adalah penilaian kesesuaian untuk pertanyaan ini, bukan bukti bahwa model tersebut terbaik untuk semua evaluasi harmoni. Identitas bobot Magenta.js dan model produksi Bach Doodle tidak disamakan. Keanggotaan MODEL 285 dalam data latih masih tidak diketahui. Riwayat populer sebuah produk tidak membuktikan kesesuaian instrumen.

Sumber primer yang diperiksa 21 Oktober 2026:

- [Huang dkk. 2017, Counterpoint by Convolution](https://archives.ismir.net/ismir2017/paper/000187.pdf).
- [Huang dkk. 2019, The Bach Doodle](https://archives.ismir.net/ismir2019/paper/000097.pdf), terutama hlm. 795–798.
- [Hadjeres dkk. 2017](https://proceedings.mlr.press/v70/hadjeres17a.html).
- [Dokumentasi Coconet v1.23.1](https://magenta.github.io/magenta-js/music/classes/_coconet_model_.coconet.html) dan sumber `model.ts`/`coconet_utils.ts` pada repositori pengembang. Kode distribusi paket 1.23.1 juga diperiksa tanpa instalasi atau inferensi: `node/coconet.js` SHA-256 `64bafc2e04340300147e722674a644fed671fc9f3888a178aa50ba5fc43ee3ac`. Pemeriksaan sumber daring bukan uji inferensi atau bukti bahwa bobot dapat dijalankan pada perangkat ini.

## Pendekatan, teori, dan alat

Pendekatan yang ditulis untuk v6 adalah **kualitatif dengan desain studi kasus evaluatif**, menggunakan analisis partitur deduktif menurut Strube dan ringkasan numerik pendukung. Sasaran utama adalah alasan keputusan musikal pada kasus tertentu. Angka membantu memeriksa pengulangan dan cakupan bukti. Ini keputusan rancangan yang perlu dibahas secara akademik; tidak dilaporkan sebagai keputusan dosen yang sudah disetujui.

| Sumber | Fungsi dalam penelitian | Batas pemakaian |
| --- | --- | --- |
| Strube 1928, Preface dan hlm. 6–7 | Kerangka harmoni, fungsi akor, penulisan empat suara | Susunan tingkat teori adalah penjelasan peneliti, bukan istilah yang diklaim berasal dari Strube |
| Strube, halaman tiap kaidah dan hlm. 174 | Dasar keputusan beserta tahap, syarat dan pengecualian | Ambang program tidak menggantikan pertimbangan sumber |
| Yin 2018, hlm. 15–21; Flyvbjerg 2006 | Batas kasus, hubungan bukti dengan pertanyaan, pembacaan kontekstual | Studi kasus tidak otomatis kualitatif; pemilihan pendekatan di sini mengikuti tujuan analisis |
| Maxwell 2010, hlm. 475–478 | Alasan hitungan pendukung dalam penelitian kualitatif | Adanya angka tidak otomatis berarti metode campuran; angka tidak membuktikan mutu estetis |
| Briot dkk. 2020 | Tujuan, representasi dan strategi model | Tidak menjadi teori penyebab penyimpangan |
| Pearce dkk. 2002 | Kesesuaian tujuan evaluasi dengan aspek yang dinilai | Penilaian gerak suara hanya mencakup satu aspek keluaran |
| Huron 2001 | Penjelasan perseptual dalam pembahasan | Tidak menggantikan uji dengar yang tidak dilakukan |
| Cuthbert dan Ariza 2010 / music21 | Membaca dan mengolah data simbolik | music21 bukan instrumen Strube yang sudah tervalidasi |
| Yan dkk. 2018 | Contoh penilaian harmonisasi dengan kategori buku ajar | Bobot dan validitas rubrik tidak dipindahkan ke Strube |
| Lazic 2010 | Pembedaan unit kasus, keluaran, dan kejadian | Penerapannya pada generasi model adalah penalaran peneliti |

[Yin, sampel resmi penerbit](https://au.sagepub.com/sites/default/files/upm-assets/87275_book_item_87275.pdf) berhak cipta 2018; halaman katalog mencatat rilis September 2017. Sitasi buku menggunakan tahun edisi 2018. [Maxwell, teks artikel penerbit](https://journals.sagepub.com/doi/pdf/10.1177/1077800410364740) diperiksa pada bagian terkait. Creswell dan Leedy yang belum dibuka pada catatan v4 tidak dipakai sebagai penyangga utama definisi metode baru. Penelusuran Bowen hanya memperoleh abstrak penerbit sehingga tidak ditambahkan sebagai dasar prosedur rinci.

Tidak ada variabel perlakuan atau kelompok pembanding. Aspek dan indikator pengamatan dijelaskan di BAB III. Tidak ada H0/H1 populasi; dua pertanyaan analitis tetap mengarahkan penelitian. Pernyataan bahwa model pasti melanggar tidak dijadikan asumsi. Semua keluaran yang diterima menurut kriteria juga merupakan hasil yang sah.

## Alur analisis sampai jawaban

1. Verifikasi sumber dan transkripsi satu kasus sebelum melihat hasil model. MODEL 285 masih calon; cap pada bas pembuka dan durasi sopran akhir belum terpecahkan.
2. Bekukan kriteria dan definisi kesempatan, keadaan, episode, segmen keputusan, serta cara membaca konteks. Nilai 96 iterasi dan temperature 0,99 mengikuti antarmuka yang dipilih dan perlu diperiksa pada pilot.
3. Siapkan satu model, satu masukan dan satu konfigurasi. Rencana tetap 20 percobaan, berasal dari keputusan beban kerja peneliti pada v5; angka ini tidak diklaim sebagai persetujuan dosen, perhitungan daya, atau kejenuhan.
4. Catat seluruh percobaan, keluaran identik dan kegagalan. Pisahkan keluaran pilot dari utama. Periksa pemeliharaan sopran dan pemetaan suara sebelum analisis musikal.
5. Program menyiapkan data nada/waktu dan kandidat. Peneliti memeriksa **seluruh kesempatan yang dihitung**, termasuk yang tidak ditandai program. Simpan catatan keputusan tanpa pola sasaran, diterima bersyarat, menyimpang, dan belum diputuskan.
6. Untuk setiap keluaran dan kriteria transisi, pastikan `O = C + A + D + U` dan semua O sudah diperiksa sebelum melaporkan D/O serta U/O. Ini akuntansi keputusan buatan peneliti. Instrumen lama hanya memeriksa sebagian bagian tanpa tanda; rencana baru memerlukan perubahan versi.
7. Catat keadaan jarak/persilangan sebagai episode fisik dan durasi. Perubahan status selama satu episode membuat segmen keputusan, bukan episode baru. Jangan menjumlahkan episode yang berstatus ganda sebagai episode unik.
8. Uraikan gerak horizontal A/T/B dan pola struktural lintas nada hias secara terpisah. Jangan memindahkan hitungan rentang struktural ke penyebut transisi langsung.
9. Kelompokkan lokasi dan keputusan yang berulang antarkeluaran. Frekuensi keluaran adalah jumlah keluaran layak yang memuat pola / jumlah keluaran layak; beberapa kejadian pada satu keluaran hanya menambah satu pembilang untuk pola itu.
10. Jawab pertanyaan pertama dengan alasan penerimaan/penyimpangan menurut sumber. Jawab pertanyaan kedua dengan pola, variasi dan lokasi. Hubungkan tiap uraian dengan cuplikan partitur dan seluruh catatan keputusan.

Seluruh keluaran gagal berarti kesesuaian musikal belum dapat dijawab. Semua keputusan belum pasti berarti batas informasi harus dilaporkan, bukan dianggap tanpa penyimpangan. Proporsi rendah dengan ketidakpastian tinggi tidak dibaca sebagai bukti kesesuaian tinggi. Perbedaan dari acuan cetak tidak otomatis salah.

## BAB IV dan batas kesiapan

[Rancangan BAB IV](../study/rancangan-bab-iv-v6.md) menetapkan isi, artefak, tabel, dan syarat penulisan hasil. [Templat data](../../../research/experiments/v6/) menyiapkan format pencatatan tanpa baris hasil rekaan.

Permintaan BAB I–IV siap belum dapat dinyatakan terpenuhi: sumber kasus lengkap, instrumen kontekstual yang diterapkan, pilot dan data utama belum tersedia. Hasil lama dari korpus Bach, contoh Fig. 33 dan uji program tidak boleh dipakai sebagai hasil Coconet v6. BAB IV hasil tidak ditambahkan ke PDF hanya untuk memenuhi nomor bab. Persiapan struktur dan format data tidak menutup kebutuhan bukti tersebut.

Tidak ada naskah yang dapat dijamin bebas dari seluruh kemungkinan kritik. Revisi ini menutup ketidakselarasan dua model, kedudukan metode, hubungan alat dan teori, serta ketidaksesuaian pemeriksaan dengan penyebut. Item bukti yang masih terbuka dicatat di PROGRESS.md, bukan disembunyikan dalam klaim kesiapan.

## Rekam penelusuran

Rencana kueri diperbarui sebelum pencarian; seluruh 33 kueri dijalankan dengan `uv run research/scripts/openalex_search.py --batch`. Manifest: `research/outputs/openalex/20261021T054123948242Z-batch/batch_manifest.json`; 731 karya unik tersimpan. Hasil kueri q31–q33 luas dan tidak semuanya mengembalikan sumber sasaran; hasil q33 teratas adalah ulasan buku, bukan buku Yin. Sumber sasaran diverifikasi langsung pada penerbit/penulis dan tidak dipilih dari hitungan sitasi atau kemiripan judul. Artefak sumber yang berhasil diunduh dan catatan akses berada di `research/outputs/source-verification-v6-2026-10-21/`; catatan dukungan klaim ditambahkan ke reading-notes.csv. Status pembacaan mandiri peneliti tetap belum dicatat.
