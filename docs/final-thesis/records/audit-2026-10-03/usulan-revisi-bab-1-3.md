# Usulan revisi Bab I–III

Tanggal: 3 Oktober 2026. Ini paket revisi untuk ditinjau dan diterapkan setelah chat lain selesai mengedit naskah. Tidak ada perubahan berikut yang telah diterapkan ke bab atau protokol oleh audit ini. Nomor A merujuk [laporan audit](AUDIT.md). Pertahankan ID heading LaTeX yang ada. Jangan memasukkan catatan status dari berkas ini ke dalam skripsi.

## Bab I

Alur latar belakang yang disarankan: tugas harmonisasi dan pengguna → keluaran dua model → apa yang dihitung Huang → cakupan rubrik Yan dan penelitian Choi → kebutuhan membandingkan sistem pada melodi bersama → batas ukuran. Uraian perkembangan AI, hak cipta, dan survei arsitektur dapat dipadatkan karena tidak langsung menjelaskan pertanyaan gerak suara.

### Rumusan masalah, A01–A03 dan A18

Ganti kalimat yang menyamakan asal melodi dengan OOD dan menjanjikan pengujian pengaruh dengan paragraf ini:

> Analisis Bach Doodle menghubungkan ciri melodi masukan dengan kuint dan oktaf sejajar pada keluaran Coconet (Huang et al., 2019). Penelitian ini mengadaptasi penghitungan tersebut untuk membandingkan DeepBach dan Coconet pada melodi sopran yang sama dari dua sumber, yaitu chorale Bach dan latihan Strube. Asal melodi membedakan sumber repertoar, tetapi tidak dengan sendirinya menunjukkan bahwa melodi berada di luar distribusi data latih. Perbandingan kedua kelompok juga tidak memisahkan panjang, wilayah nada, ritme, tonalitas, dan tanda frasa yang mungkin berbeda. Masalah yang diperiksa adalah profil penandaan gerak suara pada keluaran kedua sistem dan perbedaannya menurut sumber melodi.

Kutipan yang dibutuhkan: `huang2019`; sumber Choi dan Yan dijelaskan pada paragraf tinjauan yang terkait. Hindari klaim “belum ada” sebagai penutup wajib. Jika tetap menyebut gap, batasi pada hasil penelusuran yang telah disaring, bukan seluruh dunia penelitian.

### Pertanyaan dan tujuan ketiga, A01

Pertanyaan:

> Bagaimana perbedaan tingkat kepatuhan terhadap kaidah gerak suara Strube antara harmonisasi melodi chorale Bach dan melodi latihan Strube pada masing-masing model?

Tujuan:

> Membandingkan tingkat kepatuhan terhadap kaidah gerak suara Strube antara kedua asal melodi pada masing-masing model.

Pertanyaan pertama dan kedua dapat dipertahankan dengan definisi kepatuhan yang dipersempit. Tujuan pertama harus mengatakan bahwa acuan Bach tersedia untuk kelompok melodi Bach, agar tidak menjanjikan acuan ahli untuk latihan Strube.

### Arti ukuran, A04 dan A17

> Tingkat kepatuhan dalam penelitian ini dinyatakan melalui laju penandaan lima indikator gerak suara per birama. Laju yang lebih rendah berarti lebih sedikit kejadian menurut definisi operasional yang dipakai. Ukuran ini tidak menunjukkan persentase kebenaran harmonisasi. Strube masih membolehkan sopran sesekali berjarak lebih dari satu oktaf dari alto; karena itu, penandaan jarak di atas ambang tidak otomatis menyatakan satu kejadian salah secara musikal. Penafsiran hasil memperhatikan pengecualian yang belum dapat diterapkan instrumen.

Kutipan: `huang2019` untuk satuan dan `strube1928`, hlm. 20, untuk pengecualian. Definisi indikator dan satuan kejadian adalah keputusan peneliti.

### Manfaat, A18

Ganti manfaat “menguji ulang pengaruh melodi di luar data latih”:

> Memperluas pengukuran gerak paralel dalam analisis Bach Doodle ke perbandingan dua sistem pada melodi bersama dari dua sumber, dengan lima indikator yang didefinisikan.

Manfaat instrumen:

> Menyediakan prosedur evaluasi otomatis yang dapat diperiksa dan diadaptasi untuk model lain setelah kesesuaian format, tugas, dan definisinya diuji.

Usulan judul untuk pembimbing, bukan penggantian metadata otomatis:

> Evaluasi Gerak Suara Harmonisasi DeepBach dan Coconet pada Melodi Chorale Bach dan Latihan Strube

Pilihan ini menghindari janji sebab-akibat dan memberi nama objek yang lebih khusus daripada “musik hasil AI”. Judul final tetap keputusan peneliti dan pembimbing.

## Bab II

### Tinjauan pustaka, A32–A35

Pertahankan sumber yang langsung menjelaskan metode. Tabel posisi penelitian dapat berisi Huang (kejadian per birama), Yan (rubrik pedagogis dengan penilai), Fang (kedekatan distribusi terhadap Bach), Choi (pencegahan paralel dan konsekuensinya), serta penelitian ini (perbandingan sistem pada melodi bersama). Jangan menyamakan satuan atau prosedur kelima penelitian.

Paragraf tambahan Choi, setelah metadata nama diperbaiki dan entri disepakati:

> Choi et al. (2023) meneliti pengurangan kuint dan oktaf sejajar melalui tambahan fungsi kerugian pada pelatihan serta pembatasan probabilitas saat inferensi. Evaluasinya memakai ukuran distribusi musikal yang diadaptasi dari Fang et al. Hasil tersebut mengingatkan bahwa mencegah gerak paralel dapat memengaruhi ciri musikal lain. Penelitian ini mengevaluasi checkpoint yang tersedia tanpa melatih ulang model atau memperbaiki keluarannya berdasarkan kaidah.

Dukungan: makalah asli hlm. 192–194, §4.3–4.4. Bobot model dan ukuran distribusi tidak boleh dilaporkan sebagai laju per birama penelitian kita.

### Kerangka teori, A13

> Kerangka umum penelitian ini adalah harmoni tonal Barat, dengan harmoni fungsional sebagai konteks bagi hubungan akor dan kadens. Acuan langsung pengukuran adalah kaidah penulisan dan gerak suara Strube. Definisi operasional pada Bab III menjelaskan cara peneliti mengukur sebagian kaidah tersebut. Pengukuran tidak menentukan fungsi setiap akor, sehingga pengecualian yang memerlukan analisis fungsi menjadi batas penafsiran hasil.

Jika dosen meminta istilah grand theory, jelaskan kedudukan kerangka umum itu sesuai permintaannya. Jangan menyatakan bahwa Creswell menetapkan kaidah Strube sebagai middle theory, atau rumus sebagai applied theory.

### Asal melodi dan OOD, A02

> Asal repertoar dan status terhadap batas data latih merupakan dua informasi yang berbeda. Huang et al. menggunakan wilayah nada dan lompatan sebagai penanda operasional masukan di luar batas sopran data latih. Melodi latihan Strube dapat berada di dalam batas tersebut. Penelitian ini menggunakan asal melodi sebagai faktor pengelompokan dan mencatat ciri musikal kedua kelompok. Hasil perbandingan sumber melodi tidak ditafsirkan sebagai pembuktian umum kemampuan model menghadapi masukan di luar distribusi.

### Adaptasi rubrik, A14–A16

> Kategori dan bobot pengurangan nilai diambil dari rubrik Yan et al., sedangkan rumusan dan pengecualian kaidah dirujuk ke Strube. Penelitian ini mengganti tugas bas tetap dengan sopran tetap, mengambil sebagian kategori, serta mengubah cara penghitungan dan penyebut. Instrumen ini karena itu merupakan adaptasi yang disusun peneliti. Bukti penilaian rubrik asli tidak langsung membuktikan ketepatan adaptasi otomatis ini.

### Hipotesis, A03 dan A10–A12

Rekomendasi arah: seluruh uji dua arah. Untuk model, definisikan selisih DeepBach dikurangi Coconet per melodi. Rumusan nol Wilcoxon menyangkut distribusi selisih yang simetris terhadap nol; interpretasi sebagai perbedaan lokasi memerlukan simetri yang sesuai. Untuk asal, nol Mann–Whitney menyangkut kesamaan distribusi kedua kelompok; hindari menganggapnya otomatis sebagai uji median.

Paragraf alasan:

> Hipotesis diuji dua arah karena belum ada dasar yang sesuai untuk menetapkan arah perbedaan kedua sistem atau kedua asal melodi pada indikator yang digunakan. Temuan Huang et al. menyangkut masukan di luar batas nada dan lompatan, sedangkan variabel penelitian ini adalah asal repertoar. Perbedaan antar-asal menunjukkan hubungan antara kelompok masukan dan hasil pengukuran, tanpa mengisolasi sumber melodi sebagai penyebab.

## Bab III

### Klasifikasi desain, A01

> Penelitian ini menggunakan pendekatan kuantitatif dengan tujuan deskriptif dan komparatif. Pertanyaan pertama menggambarkan profil penandaan. Pertanyaan kedua membandingkan dua sistem pada melodi yang sama sehingga datanya berpasangan. Pertanyaan ketiga membandingkan dua kelompok melodi pada setiap sistem. Asal melodi tidak diacak atau diubah sebagai perlakuan pada melodi yang sama; karena itu, perbandingan antar-asal tidak diposisikan sebagai pengujian sebab-akibat yang terisolasi.

### Sampel dan daya, A09 dan A19–A21

> Seluruh latihan melodi Strube yang memenuhi kriteria diikutsertakan. Jumlah melodi Bach diambil sebanyak jumlah melodi Strube yang layak dari kerangka korpus yang ditetapkan, dengan pemilihan acak dan seed yang dicatat. Target awal 30 melodi per kelompok digunakan untuk merencanakan beban penelitian, bukan sebagai jaminan daya statistik. Kelayakan akhir ditentukan setelah pengetikan dan pilot. Keterbatasan jumlah melodi, nilai nol, ties, serta koreksi pengujian berganda diperhitungkan ketika menetapkan kemampuan analisis mendeteksi perbedaan.

Angka pendekatan uji t lama boleh dipertahankan dalam catatan perencanaan sebagai riwayat, dengan batasnya. Jika ingin mempertahankan klaim daya 0,8 dalam naskah, diperlukan perhitungan yang cocok dengan uji, distribusi, koreksi, dan efek yang dipilih. Jangan menghitung daya pascahoc dari efek data utama untuk mengesahkan hasil.

### Generasi, A22–A24

> Kedua sistem menerima melodi sopran yang sama melalui penerjemah format masing-masing. DeepBach menggunakan metadata tambahan yang tersedia pada notasi, sedangkan Coconet menggunakan piano roll dan mask. Pengaturan setiap sistem dibekukan dan dicatat untuk seluruh melodi; pengaturan antar-sistem tidak dianggap identik. Setiap percobaan mempunyai identitas melodi, sistem, indeks generasi, konfigurasi efektif, keluaran mentah, dan status keberhasilan. Seed dicatat jika tersedia. Pengukuran dapat diulang dari keluaran yang diarsipkan meskipun generasi baru tidak selalu dapat direproduksi bit demi bit.

### Representasi dan satuan kejadian, A05 dan A25–A27

> Peristiwa bunyi ditetapkan per pasangan suara sebagai titik ketika sedikitnya satu suara memulai nada baru. Pada penandaan jarak dan persilangan, kondisi yang terus berlangsung dapat dihitung kembali pada onset berikutnya. Jumlah kejadian karena itu bergantung pada artikulasi yang tersedia dalam representasi, selain tinggi nada dan durasi bunyi. Keluaran Coconet tidak membedakan serangan ulang dari nada tahan yang sama. Perbedaan ini diperiksa melalui analisis kepekaan dengan representasi bunyi bersama, tanpa mengganti keluaran mentah.

Implementasi analisis kepekaan harus ditetapkan dan diberi versi sebelum disebut prosedur yang telah dijalankan. Salah satu pilihan adalah menggabungkan pitch sama yang bersebelahan tanpa jeda pada semua keluaran dan acuan, lalu membandingkan penghitungan terhadap representasi asli. Pilihan ini sengaja mengabaikan artikulasi dan mempunyai batas musikal sendiri.

### Fermata, A06

Dua pilihan yang dapat ditinjau:

1. Pertahankan kode 2.0 dan jelaskan bahwa analisis tambahan mengecualikan gerak yang berawal saat sopran sedang membunyikan nada berfermata. Ini penyaringan lebih luas dari transisi setelah frasa.
2. Definisikan titik akhir frasa secara eksplisit, ubah kode, naikkan versi instrumen, tambahkan kasus acuan, dan ukur ulang korpus. Setelah itu baru gunakan istilah “melintasi batas frasa”.

Jangan mengubah hanya kalimat menjadi “setelah fermata” sementara kode masih menghapus seluruh gerak selama nada berfermata.

### Verifikasi dan validitas, A08 dan A28–A29

> Pemeriksaan instrumen mencakup penelusuran isi kaidah, kesesuaian dengan kasus buku, pemeriksaan silang predikat dasar, dan keterulangan hasil. Kesepakatan dengan music21 menunjukkan kecocokan implementasi pada predikat dan data yang dibandingkan. Perbandingan dengan angka Huang et al. digunakan sebagai pemeriksaan kewajaran dengan mempertimbangkan perbedaan korpus dan penghitungan. Pemeriksaan tersebut tidak membuktikan bahwa semua penandaan merupakan kesalahan musikal pada konteks baru, terutama ketika pengecualian memerlukan analisis akor. Batas ini menentukan ruang kesimpulan penelitian tanpa penilai manusia.

### Kontrol kualitas, A07 dan A24

Tambahkan ketentuan yang tidak melarang diam musikal yang sah: setiap part benar-benar mempunyai isi yang dapat dinilai, keluaran mencakup durasi tugas yang ditetapkan, dan tidak dipotong atau diperpanjang tanpa kebijakan tercatat. Pemeriksaan pitch/onset/durasi sopran harus mencakup seluruh durasi. Catat k keluaran layak dari lima per melodi–model. Jangan menjanjikan ketentuan tersebut sudah ditegakkan sampai pemeriksaan kode dan kasus acuannya lulus.

### Statistik dan penyajian, A10–A12 dan A31

Keputusan yang harus masuk protokol sebelum generasi utama:

- Selisih berpasangan, penanganan nol, ties, dan metode nilai p. Kasus semua selisih nol dicatat sebagai tanpa informasi arah untuk statistik berbasis selisih nonnol; bukan bukti kesetaraan.
- Sasaran Mann–Whitney, orientasi ukuran efek, serta pelaporan perbedaan bentuk distribusi. Uji nonparametrik tetap mempunyai asumsi.
- Keluarga koreksi: tiga keluarga seperti semula dengan klaim terbatas, atau satu keluarga 15 uji utama. Pilih satu; jangan mengklaim keduanya.
- Indeks tertimbang hanya deskriptif sebagai rekomendasi sederhana. Jika diuji, masukkan kebijakan koreksinya dan sebut analisis sekunder/eksploratif.
- Pelaporan hitungan, penyebut, kesempatan, laju per birama, distribusi, selisih berpasangan, dan interval ketidakpastian. O=0 untuk laju per kesempatan adalah tidak terdefinisi, bukan otomatis nol.
- Analisis kepekaan: representasi bunyi bersama, keluaran lengkap lima generasi, definisi fermata yang disepakati, dan status pelatihan hanya jika provenance sah. Analisis perubahan selisih model antar-asal boleh ditambahkan sebagai eksploratif bila pertanyaan interaksi memang dibutuhkan.

## Yang berubah dalam usulan ini

Usulan mempertahankan objek, dua model, sopran tetap, lima indikator, serta batas tanpa penilai manusia. Klaim sebab-akibat dan OOD dipersempit; kategori, ukuran, dan bukti validitas dipisahkan; statistik dan kontrol kualitas dibuat lebih jelas. Urutan tinjauan pustaka diusulkan untuk menunjukkan hubungan sumber dengan keputusan metode. Tidak ada hasil, persetujuan dosen, sampel layak, atau sitasi baru yang dinyatakan sudah tersedia hanya melalui usulan ini.
