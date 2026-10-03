# Audit substansi, struktur, metode, dan referensi Bab I–III

Tanggal: 3 Oktober 2026. Revisi aktif: skripsi v3. Laporan ini dibuat atas permintaan audit menyeluruh. Ketika ditemukan perubahan berkas oleh chat lain, peneliti meminta agar pekerjaan difokuskan pada laporan terlebih dahulu. Audit ini tidak mengubah bab, front matter, bibliografi bersama, protokol, atau instrumen. Identitas berkas saat pemeriksaan dicatat dalam [baseline.json](baseline.json). Perubahan berikutnya dapat menutup sebagian temuan; cocokkan kembali sebelum menerapkan usulan.

Penelitian mempunyai objek dan tugas yang dapat dipertahankan: keluaran harmonisasi simbolik dua sistem untuk melodi sopran bersama. Bagian yang paling rentan adalah hubungan asal melodi dengan sebab-akibat, arti musikal penandaan otomatis, kesepadanan representasi, dan dasar inferensi statistik. Memperbaiki kalimat saja tidak menutup masalah yang membutuhkan keputusan operasional atau bukti pilot.

## Cakupan dan batas pemeriksaan

- Bab I–III dibaca lengkap; versi yang berubah selama audit dibaca kembali pada bagian yang relevan. Judul, metadata, protokol, panduan peneliti, catatan bimbingan, catatan bacaan, inventaris Strube, instrumen v2, jalur MusicXML, dan keluaran pemeriksaan korpus ikut diperiksa.
- Struktur tujuh contoh skripsi lokal diperiksa melalui teks PDF dan daftar isi. Uraian kaidah pada scan Strube hlm. 9, 12–13, 20, dan 174 diperiksa sebagai gambar. Isi semua halaman buku dan seluruh contoh skripsi tidak diaudit sebagai penelitian tersendiri.
- Sumber primer DeepBach, Coconet, Bach Doodle, Yan beserta suplemennya, MusPy, Choi, serta dokumentasi statistik diperiksa pada bagian yang diperlukan. Status setiap sitasi bab ditelusuri dalam [citation-checks.csv](citation-checks.csv); status yang belum terverifikasi tetap ditulis demikian.
- Rencana OpenAlex diperbarui sebelum menjalankan seluruh 21 kueri dengan `uv run research/scripts/openalex_search.py --batch`. Diperoleh 532 rekaman unik. Ini penemuan literatur, bukan 532 sumber yang sudah dibaca atau tinjauan sistematis yang selesai. Rekaman kueri dan hasil ada dalam manifest `research/outputs/openalex/20261003T070513511032Z-batch/`.
- Empat probe sintetis dijalankan pada instrumen lokal, ditambah satu perbandingan nada tahan dan nada ulang. Hasilnya menjelaskan perilaku program; probe tersebut bukan data pilot model atau data utama. Kode dan keluaran ada pada [probes.py](probes.py) dan [probe-results.json](probe-results.json).
- Tidak ada inferensi model, pengumpulan data utama, validasi dengan manusia, atau pengujian hipotesis terhadap keluaran model pada audit ini. PDF aktif tidak dibangun ulang karena bab sedang berubah dari chat lain.

## Pilihan yang layak dipertahankan

Tugas sopran tetap memberi masukan musikal bersama bagi kedua sistem, dan setiap pasangan yang dinilai melibatkan sedikitnya satu suara yang dihasilkan. Naskah sudah membatasi perbandingan arsitektur dan merencanakan agregasi generasi pada tingkat melodi. Pemisahan lima indikator membantu melihat pola yang akan hilang bila hanya satu indeks dipakai. Kebijakan versi instrumen dan penyimpanan data mentah mendukung penelusuran perubahan. Pilihan tersebut tetap membutuhkan bukti pelaksanaan; ia memberi kerangka yang bisa diperbaiki tanpa mengganti objek penelitian.

## Temuan yang perlu ditangani lebih dahulu

Prioritas P1 berarti masalah dapat mengubah arti hasil atau kelayakan pengumpulan data. P2 berarti penjelasan dan pelaporan perlu diperbaiki sebelum naskah diajukan. P3 berarti pemadatan atau penyajian. Nomor menunjukkan temuan, bukan skor mutu skripsi.

| ID | Prioritas | Lokasi | Temuan dan akibat | Tindakan yang disarankan |
| --- | --- | --- | --- | --- |
| A01 | P1 | I.C–D; II.D; III.A | Kata *pengaruh* dan *asosiatif kausal* melampaui desain. Melodi tidak diacak ke asal, dan tidak ada intervensi satu ciri pada melodi yang sama. Menjalankan masukan pada komputer tidak otomatis mengisolasi sebab. | Gunakan *perbedaan antar-asal melodi* dan desain kuantitatif deskriptif-komparatif. Selaraskan judul setelah pembimbing meninjau. |
| A02 | P1 | II.B.1; posisi penelitian | Asal Strube diperlakukan sebagai wakil di luar distribusi. Asal repertoar, status pernah dilatih, dan batas MIDI/lompatan merupakan informasi berbeda. | Ukur ciri masukan; jangan menyamakan asal dengan status OOD. Nyatakan adaptasi gagasan Huang, bukan uji ulang persis hipotesisnya. |
| A03 | P1 | II.D; III.D | Hipotesis satu arah Strube lebih buruk untuk paralel bergantung pada A02. Soal buku ajar dapat lebih sederhana dan masih di dalam batas Huang. | Rekomendasi: dua arah untuk semua indikator. Pilihan arah dibekukan sebelum data utama, dengan alasan yang benar-benar cocok dengan variabel. |
| A04 | P1 | II.B.2; III.C.4 | Jarak > satu oktaf dinamai pelanggaran Strube, padahal hlm. 20 membolehkan sopran–alto sesekali lebih jauh dan menjelaskan alto–tenor dengan batas waktu yang tidak diukur detektor. | Sebut kejadian jarak di atas ambang; pisahkan S–A dan A–T dalam uraian. Hindari menyatakan semua penandaan salah secara musikal. |
| A05 | P1 | III.C.3–4 | Onset berbeda menurut representasi. Probe urutan tinggi nada dan durasi bunyi yang sama: nada tahan menghasilkan 1 penandaan jarak, serangan ulang 4. Artikulasi berbeda; format tidak selalu menyimpan perbedaan itu. Coconet menggabungkan nada sama; DeepBach dapat mempertahankan serangan ulang. | Tetapkan pemeriksaan kepekaan dengan representasi bunyi bersama, simpan data asli, dan bandingkan laju per kesempatan. Pilihan ini mengubah protokol pengukuran tambahan. Pada probe, kesempatan gerak paralel juga berubah dari 0 menjadi 18; meskipun hitungan paralelnya tetap nol, penyebut per kesempatan turut berubah. |
| A06 | P1 | III.C.4; fungsi `evaluate_grids` | Penghapusan fermata tidak hanya menghapus gerak setelah batas frasa. Kode menghapus gerak jika titik awalnya masih berada di nada sopran berfermata. Probe menghapus 3 paralel di tengah nada panjang menjadi 0. | Pilih: namai opsi sesuai perilaku aktual, atau ubah definisi menjadi transisi melintasi akhir frasa dengan versi instrumen baru. Jangan mempertahankan klaim yang lebih sempit daripada kode. |
| A07 | P1 | III.C.6; `quality_check` | Alto kosong dan bas dua kali durasi melodi sama-sama lolos probe kontrol kualitas. Kehadiran empat part tidak menjamin harmonisasi lengkap. | Tambahkan kebijakan suara kosong, rentang waktu, pemotongan, dan kelengkapan keluaran sebelum pilot. Definisikan diam yang sah agar tidak mewajibkan semua suara terus berbunyi. |
| A08 | P1 | III.C.5; pemeriksaan korpus | Kecocokan dengan music21 bukan validasi musikal menyeluruh. Kode pemeriksaan silang membandingkan persilangan pada pasangan bersebelahan di salah satu dari dua titik, dan tumpang tindih mentah sebelum pengecualian. Ini berbeda dari indikator akhir. | Pisahkan penelusuran sumber, verifikasi predikat dasar, kesesuaian pada kasus buku, dan batas validitas konstruk. Jangan menyebut predikat mentah sebagai seluruh detektor tervalidasi. |
| A09 | P1 | III.B.2 | Pendekatan daya uji t dibagi efisiensi asimtotik 0,864 tidak membuktikan daya 0,8 pada sampel kecil, laju diskret dengan banyak nol, dan koreksi berganda. | Perlakukan 30 sebagai target awal yang bergantung kelayakan, atau lakukan simulasi daya sesuai hasil pilot dan uji akhir. Hindari *minimum yang cukup* dan *achieved power* dari efek teramati. |
| A10 | P1 | III.D | Wilcoxon dipilih hanya karena berpasangan. Interpretasi perbedaan lokasi memerlukan perhatian pada simetri selisih; nol dan ties memengaruhi perhitungan. [Dokumentasi Wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html). | Tetapkan sasaran uji, penanganan nol, metode nilai p, asumsi, serta kasus semua selisih nol. Pertimbangkan uji tanda sebagai pemeriksaan alternatif bila simetri tidak layak. |
| A11 | P1 | III.D | Mann–Whitney dapat menanggapi bentuk distribusi, bukan hanya median atau laju rata-rata. [Dokumentasi Mann–Whitney](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html). Kelompok Strube merupakan kumpulan latihan dari satu buku. | Laporkan distribusi, ukuran efek, dan batas inferensi. Jangan memperlakukan sensus buku sebagai sampel acak semua buku harmoni. |
| A12 | P1 | III.D | Lima uji Q2 dan sepuluh uji Q3 dikoreksi per keluarga. Ringkasan tambahan diuji di luar keluarga, sehingga klaim perlindungan seluruh penelitian tidak berlaku. | Nyatakan keluarga secara eksplisit. Opsi sederhana: Holm untuk 15 uji utama, indeks hanya deskriptif. Opsi tiga keluarga sah bila klaim dan cakupannya dijelaskan. |

## Substansi dan teori

**A13, P2. Kedudukan teori.** Harmoni fungsional dipasang sebagai grand theory, kaidah Strube sebagai middle theory, dan rumus sebagai applied theory. Hierarki itu merupakan penyusunan peneliti, bukan klasifikasi yang telah ditunjukkan sumber. Creswell sebagai rujukan penelitian kuantitatif tidak otomatis membuktikan hierarki teori musik tersebut. Pertahankan penjelasan kerangka umum harmoni tonal/fungsional dan acuan langsung gerak suara; jelaskan rumus sebagai definisi operasional. Kebutuhan dosen terhadap grand theory dapat dijawab tanpa membuat rumus menjadi teori tersendiri.

**A14, P2. Rubrik Yan berubah cukup jauh.** Tugas asli memberi bas tetap dan memakai penilai manusia. Penelitian ini memberi sopran tetap, mengambil sebagian kategori, memisahkan paralel kuint/oktaf, mempersempit persilangan, memberi pengecualian overlap, serta mengubah penyebut menjadi birama. Kategori dan bobot memiliki preseden; validitas dan skala rubrik asli tidak dapat dipindahkan begitu saja. Indeks harus dinamai indeks adaptasi peneliti, bukan skor Yan yang sama atau Strube Score.

**A15, P2. Pemilihan lima kategori belum menjadi alasan musikal lengkap.** Tiga syarat sudah transparan, tetapi syarat masuk rubrik Yan otomatis mengeluarkan kaidah tersembunyi dan wilayah suara yang juga dapat dihitung. Nyatakan seleksi sebagai cakupan terbatas yang memiliki preseden, bukan daftar seluruh kaidah yang relevan atau dapat diotomatisasi. Hindari pembenaran bahwa semua kategori lain mustahil dihitung tanpa manusia; beberapa dapat diotomatisasi setelah definisi dan validasi tambahan.

**A16, P2. Cakupan aturan lintas tahap pengajaran.** Persilangan diambil dari bab chorale hlm. 174, sementara soal Strube diambil dari bab awal hlm. 11–80. Itu dapat dipertahankan sebagai norma keluaran chorale, tetapi bukan klaim bahwa detektor menilai setiap soal tepat menurut seluruh instruksi bab asalnya. Hubungan antara tahap latihan dan norma penilaian harus dijelaskan. Perbedaan terjemahan juga perlu dibahas, bukan diselesaikan dengan anggapan bahwa satu wording pasti salah.

**A17, P2. Pelanggaran, penandaan, kepatuhan, dan mutu masih saling bergeser.** Istilah tingkat kepatuhan dipakai untuk laju kejadian yang sebagian masih dapat diterima. Tidak ada persentase kesempatan bersih yang dihitung, dan indeks tidak mengukur mutu estetis. Pakai *penandaan menurut definisi operasional* ketika menjelaskan data, lalu jelaskan batas penggunaan kata kepatuhan sekali secara jelas.

**A18, P2. Kebaruan dan manfaat.** Kontribusi perbandingan dua sistem pada tugas bersama masuk akal. Klaim menguji ulang OOD secara terkendali terlalu jauh. Manfaat bagi pengajar berupa informasi tentang keluaran, bukan bukti perbaikan hasil belajar, kemampuan pedagogis, atau keamanan memakai AI untuk tugas. Instrumen untuk model lain memerlukan pemeriksaan format dan domain lagi.

## Sampel, prosedur, dan keterulangan

**A19, P2. Jumlah kandidat bukan jumlah sampel layak.** Inventaris mencatat 71 kandidat sopran dan 47 latihan bas. Nada, ejaan, durasi, meter, panjang, serta penerimaan model belum lengkap. Jumlah 600 adalah skenario perencanaan jika masing-masing kelompok memiliki 30 melodi dan semua percobaan direncanakan lima kali per model; bukan jumlah data yang sudah tersedia. Versi naskah terbaru sudah memperbaiki klaim bahwa semua kandidat pasti layak; pertahankan perbaikan itu.

**A20, P2. Kemandirian melodi.** Mengagregasi lima generasi sudah mencegah pseudoreplikasi antargenerasi. Namun dua chorale dapat memakai melodi himne yang sama atau sangat berdekatan, dan latihan dapat merupakan varian pola. Rekam identitas melodi dasar, duplikasi literal, dan lintas-kelompok; tetapkan cara menangani ketergantungan sebelum memilih sampel. Random seed tidak membuktikan independensi.

**A21, P2. Kelompok Bach mungkin pernah dilatih.** Kode pembagian DeepBach master belum memastikan bobot yang diunduh memakai pembagian itu. Status seen/unseen tidak boleh menjadi fakta checkpoint hanya dari kode default. Simpan kategori *tidak diketahui* bila provenance tidak dapat dipastikan; jangan menjalankan atau menjanjikan analisis seen/unseen pada label yang belum sah. Coconet bukan held-out hanya karena memakai MusicXML dari korpus lain.

**A22, P2. Metadata dan pengaturan tidak identik.** DeepBach mendapat metadata key/fermata/tick; Coconet mendapat piano roll dan mask. Jumlah iterasi dan suhu juga berbeda. Melodi yang sama berarti tugas nadanya sama, bukan paket informasi dan beban komputasi identik. Perbandingan sistem default sah bila dilaporkan sebagai perbandingan sistem, dengan pengaturan efektif dibekukan per model.

**A23, P2. Tidak ada mask berarti sopran dapat berubah.** Jalur baru sudah membuat mask A–T–B dan memulihkan sopran ketika pitch bunyi cocok. Audit perlu memastikan runner benar-benar memakai jalur baru, bukan adapter lama yang hanya memproses dua birama. Ekspor MusicXML tidak membuktikan model sudah menerima masukan tersebut.

**A24, P2. Seleksi keluaran layak dapat menyeleksi model yang lebih mudah gagal.** Rata-rata atas satu keluaran layak dibandingkan dengan lima keluaran layak mempunyai ketidakpastian berbeda. Kegagalan tidak boleh diperlakukan sebagai nol kejadian. Laporkan k dari lima per sel, alasan gagal, jumlah melodi tersisa, dan analisis melodi dengan kelima keluaran layak. Kesimpulan utama bersyarat pada keluaran yang lolos.

**A25, P2. Penyebut dan kesempatan.** Satu birama 3/4, 4/4, dan pickup tidak sama durasinya. Penandaan vertikal dapat berulang tanpa berubahnya kondisi jarak. Menyimpan kesempatan sudah membantu, tetapi belum ada kebijakan O=0, laju per kesempatan, atau durasi terpapar. Rekomendasi: pertahankan per birama sebagai ukuran utama terbatas; laporkan jumlah ketukan/durasi dan kesempatan sebagai pemeriksaan tambahan. Penanganan birama harus konsisten antara model dan acuan.

**A26, P2. Tanda diam di antara dua onset.** `_pair_events` tidak memasukkan awal tanda diam. Probe menunjukkan kuint sebelum dan sesudah jeda tetap dihitung sebagai satu paralel. Ini perilaku teramati, bukan otomatis salah menurut semua teori. Tetapkan apakah rangkaian gerak terputus oleh diam dan cocokkan dengan contoh musikal. Perubahan harus diberi versi; jangan mengubah angka lama diam-diam.

**A27, P2. Ejaan dan batas overlap.** Semiton menyamakan kuint dengan interval enharmonik dan menetapkan langkah sebagai 1–2 semiton, sehingga sekon diperbesar berejaan diperlakukan berbeda dari pengertian langkah diatonis. Memakai MusicXML tidak mengembalikan ejaan musikal yang tidak dibuat Coconet. Syarat tidak bersilangan pada titik baru juga hanya mencegah sebagian penghitungan ganda; semua kategori dan pasangan tidak dijamin saling lepas. Klaim independensi komponen indeks perlu dihindari.

**A28, P2. Referensi angka Huang belum memvalidasi pemisahan model lokal.** Angka Bach lokal berasal dari instrumen, tetapi angka Coconet Huang berasal dari korpus dan model lain. Pernyataan dalam protokol bahwa selisih >20 kali membuktikan instrumen memisahkan Bach dari model tidak didukung eksperimen model lokal. Selisih tersisa dengan Huang tidak boleh dinyatakan sepenuhnya terjelaskan tanpa kode/himpunan data sumber yang sama. Jadikan pemeriksaan kewajaran terbatas.

**A29, P2. Reliabilitas deterministik berbeda dari validitas.** Dua hash identik membuktikan keterulangan hasil pada berkas dan lingkungan itu. Detektor dengan asumsi salah juga dapat selalu memberi hasil identik. Tidak ada estimasi kesalahan deteksi pada keluaran model baru sebelum data dan label acuan tersedia. Kebijakan tanpa penilai manusia dapat dipertahankan dengan mempersempit klaim; audit ini tidak memasukkan manusia sebagai syarat baru.

**A30, P2. Contoh diskusi perlu bisa menjelaskan mekanisme.** Pengambilan acak hanya dari flag tidak menunjukkan false negative atau bagian yang tidak ditandai. Satu sampel acak juga dapat melewatkan kasus jarang. Rekomendasi: contoh acak per indikator untuk ilustrasi, dengan batas jumlah dan seed; kasus batas tambahan yang dipilih peneliti diberi label tujuan pemilihan. Jangan memperlakukan ilustrasi sebagai estimasi prevalensi.

**A31, P2. Rencana inferensi belum lengkap.** Tetapkan sign ukuran efek, interval ketidakpastian, pembulatan yang mencegah ties numerik palsu, versi SciPy, metode p-value, zero-method, dan keluarga koreksi. Nilai p tidak mengukur besarnya perbedaan; tidak signifikan bukan setara; dua hasil dengan status signifikan berbeda bukan bukti interaksi. Perbandingan selisih model antar-asal dapat menjadi analisis eksploratif yang dibekukan terlebih dahulu, tetapi tidak wajib ditambahkan ke pertanyaan utama.

## Struktur, bahasa, dan rujukan

**A32, P3. Tinjauan pustaka masih cenderung katalog.** Banyak paragraf menjelaskan satu sumber lalu beralih ke sumber lain. Kelompokkan berdasarkan persoalan evaluasi: tugas bersama; indikator kaidah; evaluasi distribusi; penggunaan oleh musisi; dan keputusan instrumen. Setelah setiap kelompok, jelaskan pilihan metode yang didukung dan yang tidak. Tabel ringkas Huang–Yan–Fang–Choi–penelitian ini dapat memperjelas posisi tanpa menambah survei arsitektur yang panjang.

**A33, P2. Studi paling langsung belum dimanfaatkan.** Choi et al. (2023) ada dalam bibliografi tetapi tidak dikutip Bab II pada snapshot. PDF asli diperiksa: bagian 4.3–4.4, hlm. 192–194, membahas evaluasi dan konsekuensi pencegahan paralel. Penelitian ini relevan untuk mencegah klaim bahwa pengurangan paralel otomatis memperbaiki semua aspek musikal. Masukkan ringkasan singkat setelah Huang dan jelaskan perbedaan tugas serta ukuran. Entri awal juga salah menulis dua nama: yang benar Eunjin Choi dan Hyerin Kim, berdasarkan halaman judul [makalah/rekaman penulis](https://zenodo.org/records/10112462).

**A34, P2. Jejak dukungan sitasi belum menyeluruh.** Inventaris sitasi pada saat pemeriksaan mencatat 50 kunci aktif; 28 belum mempunyai baris sumber yang cocok dalam ledger aktif, termasuk catatan turunan yang berkaitan. Sebagian catatan yang tersedia hanya memeriksa abstrak atau metadata. Tidak adanya baris ledger bukan bukti bahwa sumber itu salah atau bahwa peneliti belum membacanya; jejak pemeriksaannya belum tercatat. Nomor halaman yang baru ditambahkan oleh chat lain perlu disertai catatan halaman sumber yang benar-benar diperiksa. Lihat [citation-checks.csv](citation-checks.csv) untuk setiap kunci aktif. Metadata benar tidak membuktikan dukungan klaim.

**A35, P2. Generalisasi sumber beda domain.** Kesepakatan label akor lagu populer pada Koops tidak langsung mengukur kesepakatan penilaian chorale, dan hasil studi dengar Yin tidak berarti seluruh deep learning musik setara metode lama. Pakai sumber tersebut untuk alasan kehati-hatian yang terbatas pada konteksnya. Kata *memerlukan manusia* dapat diganti dengan *memerlukan analisis dan validasi tambahan yang tidak dicakup penelitian ini*.

**A36, P3. Bahasa yang perlu dipangkas.** Pola *interpretive metadiscourse* pada I.A berbunyi “Temuan terpenting bagi penelitian ini adalah ...”; langsung tulis temuannya. Kalimat berikutnya, “Dengan kata lain, kepatuhan model terhadap kaidah dapat menurun ketika model menerima melodi yang tidak menyerupai data yang dipelajarinya”, mengulang temuan sambil memperluasnya dari batas nada/lompatan menjadi kemiripan umum; hapus atau pertahankan batas operasionalnya. Pola *robotic rhythm* pada II.A mengulang “Berbeda dari Yan et al. ...”, “Berbeda dari ukuran distribusional ...”, dan “Berbeda dari studi dengar ...” dalam satu paragraf; nyatakan pilihan pengukuran langsung atau ringkas dalam tabel. Ini bukti pola tulisan, bukan dugaan siapa penulisnya.

**A37, P2. Pedoman dan contoh tidak seragam.** Tiga contoh Prodi Musik memisahkan pertanyaan penelitian, sedangkan empat menyatukannya dengan rumusan masalah. Berkas DOCX yang disediakan berisi contoh interior/ergonomi dan mencakup struktur prodi lain; ia tidak otomatis menjadi aturan skripsi Musik. Jangan mengganti seluruh struktur A–F mengikuti satu contoh. Pertahankan ID heading dan catat keputusan format yang masih memerlukan konfirmasi.

| Contoh lokal | Pola Bab I yang terlihat dalam PDF |
| --- | --- |
| Benadito Anicheto Manek | Rumusan Masalah, Pertanyaan Penelitian, Tujuan, Manfaat terpisah |
| Intan Rama Wijaya | Rumusan Masalah, Pertanyaan Penelitian, Tujuan terpisah |
| Nourmalita Alya Putri | Rumusan Masalah, Pertanyaan Penelitian, Tujuan terpisah |
| Arinii 'Ilmal Haqqi | Rumusan, Tujuan, Manfaat, Sistematika; tanpa heading pertanyaan tersendiri |
| Cinta Angelica Paradise | Rumusan, Tujuan, Manfaat, Sistematika; tanpa heading pertanyaan tersendiri |
| Yazid Fauzan Ath Thaariq | Rumusan, Tujuan, Manfaat, Sistematika; tanpa heading pertanyaan tersendiri |
| Stanislaus Anata Warnabinarja Sihombing | Rumusan, Tujuan, Manfaat, Sistematika; tanpa heading pertanyaan tersendiri |

**A38, P2. Bagian awal belum konsisten dengan kesiapan.** Judul memuat pengaruh, sedangkan usulan perbaikan A01 membatasi perbandingan. Metadata tanggal pengajuan “3 Juli 2026” dan tahun akademik “Gasal 2026/2027” perlu dikonfirmasi terhadap pengajuan sebenarnya; tanggal tidak boleh diganti dengan tanggal audit secara otomatis. Bab IV–V boleh dijelaskan sebagai sistematika yang direncanakan tanpa mengarang bab atau hasil. Front matter dibiarkan sesuai batas instruksi peneliti.

**A39, P2. Panduan sidang lama ikut membawa klaim lemah.** `study/defense-qa.md` Q3/4/25/30/33/38/44/64/70/75 perlu diselaraskan setelah metode diperbaiki. “Hipotesis satu arah ditolak” jika arah hasil berlawanan, “Kruskal–Wallis hanya untuk tiga kelompok atau lebih”, dan “nilai p menjawab apakah ada perbedaan” perlu diluruskan. Kruskal–Wallis juga dapat digunakan untuk dua kelompok independen; keterpasangan dan sasaran uji lebih menentukan pilihan. Jangan melatih peneliti dengan jawaban yang lebih yakin daripada buktinya.

## Bukti program yang dapat diulang

Jalankan dari root repositori:

```bash
uv run python docs/final-thesis/records/audit-2026-10-03/probes.py
```

| Probe | Hasil pada instrumen 2.0 | Arti terbatas |
| --- | --- | --- |
| Nada tahan versus empat serangan ulang, urutan tinggi nada dan durasi bunyi sama | Spacing 1 versus 4 | Satuan peristiwa bergantung artikulasi yang tersedia dalam representasi |
| Tiga gerak A–T selama sopran menahan fermata | P5 utama 3; opsi pengecualian 0 | Opsi menghapus gerak saat nada fermata masih berbunyi, bukan hanya setelah frasa |
| Kuint sebelum dan sesudah satu ketukan jeda | P5 1 | Titik diam tidak memutus daftar onset pasangan secara otomatis |
| Alto tanpa nada pada empat part | QC `true` | Pemeriksaan tidak mewajibkan isi musikal pada tiap suara |
| Bas delapan ketukan, melodi empat ketukan | QC `true` | Pemeriksaan tidak memastikan seluruh durasi keluaran sama dengan masukan |

Kode dan hasil asli dipertahankan. Jika definisi berubah, beri nomor versi dan ulangi analisis yang terdampak. Probe tidak membuktikan bahwa semua keluaran model mengalami masalah tersebut.

## Paket revisi yang disarankan

Usulan paragraf dan keputusan terdapat dalam [usulan-revisi-bab-1-3.md](usulan-revisi-bab-1-3.md), sementara latihan penguji terdapat dalam [simulasi-sidang.md](simulasi-sidang.md). Urutan yang menghindari revisi silang:

1. Tetapkan estimand: profil penandaan dan perbedaan dua sistem pada dua sumber melodi.
2. Selaraskan pertanyaan, tujuan, hipotesis, dan klasifikasi desain. Setelah itu tinjau judul bersama pembimbing.
3. Selesaikan definisi waktu, fermata, diam, artikulasi, dan QC; versi pengukuran hanya berubah bila perilaku/aturan benar-benar berubah.
4. Ketik dan uji kasus buku; jalankan pilot nyata; tetapkan sampel, pengaturan, dan rencana statistik dari informasi itu tanpa memilih hasil yang menguntungkan.
5. Bekukan protokol sebelum data utama. Baru kemudian cocokkan Bab III dengan yang dijalankan, dan Bab I–II dengan batas kesimpulannya.

Tidak ada temuan penguji yang dapat dipastikan mencakup “semua kemungkinan” percakapan sidang. Simulasi mencakup pertanyaan pokok, keberatan lanjutan, dan cabang hasil yang paling relevan dengan desain ini; jawaban tetap harus dicocokkan dengan bukti final.
