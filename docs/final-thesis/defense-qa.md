# Simulasi pertanyaan sidang

Disusun 2 Oktober 2026 untuk desain v3 (protokol versi 2). Berkas ini untuk latihan menjawab, bukan bagian naskah. Jawaban mengikuti BAB I–III dan `research/protocol.md`. Bagian **Rawan bila** menunjukkan kapan jawaban bisa patah dan apa yang harus dilakukan sebelum sidang.

## Pegangan

Kalimat yang perlu bisa diucapkan tanpa membaca:

> Penelitian ini melanjutkan analisis Huang dkk. (2019) pada Bach Doodle. Mereka menghitung kuint dan oktaf sejajar secara otomatis pada harmonisasi Coconet dan menemukan bahwa pelanggaran lebih sering terjadi ketika melodi pengguna tidak menyerupai data latih. Saya menguji temuan itu secara terkendali: melodi yang sama diberikan kepada DeepBach dan Coconet, melodinya berasal dari chorale Bach dan dari latihan buku Strube, dan pelanggarannya dihitung untuk lima kaidah gerak suara.

Peran setiap sumber:

| Sumber | Perannya dalam penelitian |
| --- | --- |
| Huang dkk. (2019), §6.3 | Desain dan ukuran: hitung paralel per birama dengan music21, gagasan "di luar distribusi data latih", uji Mann–Whitney, angka Bach sebagai acuan |
| Yan dkk. (2018) | Daftar kategori kesalahan dan bobotnya (kategori 3, 9, 10, 11) |
| Strube | Teori: rumusan kaidah, pengecualian, contoh cetak untuk uji instrumen, dan melodi latihan |
| music21 | Alat pengurai dan pemeriksa silang |

## Celah yang harus ditutup sebelum sidang

| Celah | Kenapa berbahaya | Cara menutup | Status |
| --- | --- | --- | --- |
| Halaman Strube untuk lima kaidah belum dibaca | Pertanyaan "di halaman berapa Strube menulis ini?" tidak bisa dijawab; klaim "dirumuskan dari Strube" belum terbukti | Baca edisi yang dipakai, isi `research/literature/strube-rule-pages.csv` | Terbuka |
| Belum diketahui apakah Strube memuat larangan tumpang tindih suara | Satu dari lima kaidah bisa kehilangan dasar Strube | Cek saat membaca; jika tidak ada, putuskan: tetap dengan Yan saja (dan tulis begitu) atau dihapus | Terbuka |
| Jumlah latihan melodi Strube belum diketahui | Kelompok Strube adalah separuh desain | Inventaris di `strube-exercise-inventory.csv` | Terbuka |
| Contoh cetak Strube belum diketik | Validasi langkah 2 belum ada | Isi `strube-example-fixtures.csv` dan ketik MusicXML | Terbuka |
| Abstrak masih menjelaskan desain lama (tiga arsitektur, NotaGen, nada penuntun) | Penguji membaca abstrak lebih dulu; kontradiksi langsung terlihat | Minta abstrak ditulis ulang, atau tulis setelah hasil | Menunggu keputusan peneliti |
| Kode masih instrumen versi 1 | Klaim BAB III belum diimplementasikan | Implementasi v2 dan empat langkah validasi | Terbuka |
| Pilot belum dijalankan | Batas panjang melodi Coconet dan kosakata sopran DeepBach belum diketahui | Pilot beberapa melodi tiap kelompok | Terbuka |
| Persetujuan pembimbing atas desain baru | Desain berubah besar dari proposal | Bawa BAB I–III dan berkas ini ke bimbingan | Terbuka |
| Halaman Cohen (1988), Hodges dan Lehmann (1956), Creswell, Sugiyono belum dicatat | Penguji bisa minta halaman | Buka sumber dan catat di `reading-notes.csv` | Terbuka |

## A. Judul, masalah, dan tujuan

**1. Sebenarnya apa yang Anda teliti?**
Apakah model AI yang mengharmonisasi melodi lebih banyak melanggar kaidah gerak suara ketika melodinya berasal dari soal latihan buku harmoni dibanding ketika melodinya berasal dari chorale Bach, dan apakah DeepBach dan Coconet berbeda dalam hal itu.
*Bukti:* BAB I, Rumusan Masalah dan Pertanyaan Penelitian.

**2. Kenapa ini penting bagi musik atau pendidikan musik?**
Model harmonisasi sudah dipakai orang awam: Bach Doodle menerima lebih dari 55 juta permintaan dalam tiga hari, dan DeepBach tersedia sebagai plugin MuseScore. Pemula cenderung lebih menghargai bantuan sistem harmonisasi daripada profesional (Zacharakis dkk.). Jika mahasiswa memakai model untuk mengerjakan soal latihan, pengajar perlu tahu kaidah mana yang paling sering dilanggar model pada soal semacam itu. Pengembang model menilai modelnya pada data Bach, bukan pada soal buku ajar.
*Bukti:* BAB I paragraf 2–3 dan paragraf terakhir Latar Belakang.

**3. Apa itu "asal melodi" dan kenapa dijadikan variabel bebas?**
Asal melodi adalah sumber melodi sopran yang diberikan kepada model: chorale Bach atau latihan Strube. Variabel ini mewakili konsep "di luar distribusi data latih" yang dipakai Huang dkk. untuk menjelaskan kenaikan gerak paralel. Peneliti menentukan melodi mana yang diberikan kepada model yang sama, sehingga perbedaan hasil berasal dari masukan. Itu sebabnya pertanyaan ketiga memakai bentuk "pengaruh X terhadap Y".
*Bukti:* BAB II Landasan Teori subbab pertama; BAB III Variabel Penelitian.
*Rawan bila:* penguji menuntut satu ciri penyebab. Jawab: kedua kelompok bisa berbeda dalam beberapa ciri sekaligus, jadi pengaruhnya dibaca sebagai pengaruh asal melodi secara keseluruhan; ciri-cirinya diukur dan dilaporkan (panjang, wilayah, lompatan, batas Huang).

**4. Apa beda pertanyaan 2 dan 3?**
Pertanyaan 2 membandingkan dua model pada melodi yang sama, jadi datanya berpasangan dan sifatnya komparatif. Pertanyaan 3 membandingkan dua kelompok melodi pada model yang sama, dan peneliti yang menentukan masukannya, jadi memakai logika eksperimen.
*Bukti:* BAB III Metode Pendekatan paragraf 2.

**5. Kenapa judul tidak menyebut LSTM, CNN, atau Transformer seperti di proposal?**
Karena desainnya tidak bisa memisahkan pengaruh arsitektur. DeepBach dan Coconet berbeda dalam data latih, representasi, dan prosedur generasi sekaligus. Menyebut arsitektur di judul akan menjanjikan kesimpulan yang tidak bisa dibuktikan.
*Bukti:* BAB III Metode Pendekatan paragraf 5.

## B. Penelitian terdahulu dan kebaruan

**6. Penelitian Anda melanjutkan siapa, dan kenapa?**
Huang dkk. (2019), bagian 6.3. Alasannya: mereka sudah menghitung kuint dan oktaf sejajar secara otomatis dengan music21, melaporkan satuan per birama, punya angka acuan untuk chorale Bach (0,023 kuint dan 0,009 oktaf per birama), dan menemukan pola yang bisa diuji ulang, yaitu kenaikan paralel pada melodi di luar batas data latih (wilayah MIDI 60–81, lompatan maksimum satu oktaf). Semua itu bisa dilakukan tanpa penilai manusia.
*Bukti:* BAB II subbab Evaluasi Keluaran Model, paragraf Huang dkk.; Posisi Penelitian.

**7. Apa yang baru? Bukankah ini hanya mengulang Huang?**
Huang mengamati data penggunaan yang tidak dikendalikan, pada satu model, untuk dua kaidah. Penelitian ini (1) memberikan melodi yang sama kepada dua model, (2) mengendalikan asal melodi, (3) menambah tiga kaidah dari rubrik Yan yang dapat diukur tanpa analisis akor, (4) mengukur harmonisasi asli Bach pada melodi yang sama sebagai acuan, dan (5) memvalidasi instrumen terhadap contoh buku Strube dan angka Huang. Melanjutkan penelitian terdahulu dengan kondisi yang lebih terkendali adalah bentuk kontribusi yang sah.
*Bukti:* BAB II Posisi Penelitian; BAB I Manfaat Teoretis butir 1.

**8. Anda yakin belum ada yang melakukan ini?**
Klaimnya terbatas: di antara sumber yang ditinjau di BAB II, belum ditemukan pengukuran kepatuhan DeepBach dan Coconet terhadap kaidah Strube dengan asal melodi yang dikendalikan. Penelusuran tercatat di `research/literature/` dan manifest OpenAlex. Penelitian ini tidak mengklaim bahwa tidak ada seorang pun di dunia yang pernah melakukannya.
*Rawan bila:* penguji menyebut satu paper yang mirip. Jawab dengan membandingkan model, kaidah, dan kendali melodi; tidak perlu membela klaim "pertama".

**9. Kenapa memakai rubrik Yan tetapi tidak memakai penilai manusia seperti Yan?**
Dari Yan yang diambil adalah daftar kategori kesalahan yang sudah terbukti dipakai untuk menilai harmonisasi model, beserta bobotnya. Penilaian manusia tidak diambil karena penelitian ini membatasi diri pada kaidah yang dapat ditentukan dari tinggi nada dan waktu bunyi saja. Kategori yang butuh penafsiran akor justru dikeluarkan karena alasan itu. Huang dkk. sudah menunjukkan bahwa penghitungan otomatis kaidah semacam ini sah dipakai.
*Bukti:* BAB II paragraf Yan dkk. (kalimat terakhir); Landasan Teori daftar kaidah dan paragraf kategori yang dikeluarkan.

**10. Paper 2018 dan 2019 sudah lama. Kenapa masih jadi acuan?**
Yang dilanjutkan adalah desain evaluasi dan temuannya, bukan modelnya. Desain evaluasi tidak kedaluwarsa. Temuan Huang tentang melodi di luar distribusi belum diuji ulang secara terkendali pada sumber yang ditinjau. Coconet yang diuji adalah model yang dianalisis Huang, sehingga kesinambungan terjaga.

## C. Teori

**11. Apa grand theory, middle theory, dan applied theory Anda?**
Grand theory: harmoni fungsional (tonalitas, fungsi tonika–dominan–subdominan, progresi). Middle theory: kaidah gerak suara Strube yang menurunkan harmoni fungsional ke aturan penulisan empat suara. Applied theory: definisi operasional lima kaidah pada data simbolik. Teori pendukung dari komputasi: musik simbolik, model generatif, dan konsep distribusi data latih.
*Bukti:* BAB II Landasan Teori, subbab kedua paragraf 1.

**12. Kenapa Strube, bukan Piston, Kostka, atau Laitz?**
Terjemahan Indonesia buku Strube tersedia di perpustakaan ISI Yogyakarta, dan catatan review proposal meminta penelitian ini merujuk Strube. Jika Strube memang menjadi buku ajar mata kuliah harmoni di program studi, sebutkan itu; pastikan dulu faktanya. Kelima kaidah yang diukur adalah kaidah umum penulisan empat suara dalam tradisi buku ajar tonal, sehingga pemilihan Strube tidak mengubah jenis kaidah yang diukur.
*Rawan bila:* belum bisa menyebut edisi dan halaman. **Wajib ditutup** (lihat tabel celah). Jangan menyebut nama penerjemah sebagai argumen sebelum dipastikan.

**13. Rubrik Yan berasal dari tradisi buku Amerika, Strube lain lagi. Kenapa dicampur?**
Keduanya dari tradisi yang sama, yaitu penulisan empat suara dalam harmoni tonal Barat. Yan sendiri menyebut rubriknya lazim dalam buku ajar dan kelas teori musik. Pembagiannya jelas: Yan menentukan kategori mana yang punya preseden untuk menilai harmonisasi model; Strube menentukan rumusan dan pengecualian yang dipakai. Setiap kaidah dicatat sumbernya di lembar definisi.

**14. Strube punya banyak kaidah. Kenapa hanya lima?**
Tiga syarat, ditetapkan sebelum data: (1) termasuk kategori rubrik Yan, (2) diuraikan Strube, (3) pelanggarannya dapat ditentukan dari tinggi nada dan waktu bunyi tanpa menafsirkan akor atau tonalitas. Syarat ketiga diperlukan karena analisis akor bisa berbeda antar-ahli; Koops dkk. mencatat kesepakatan rata-rata hanya 73 persen untuk label akor mayor–minor. Kaidah yang bergantung pada akor membutuhkan penilai manusia, sedangkan penelitian ini sepenuhnya komputasional. Hasilnya dinyatakan untuk lima kaidah itu saja, bukan untuk seluruh teori harmoni.
*Bukti:* BAB I paragraf "Buku Strube menjadi acuan..."; BAB II paragraf kategori yang dikeluarkan.

**15. Di proposal ada resolusi nada penuntun. Kenapa dihapus?**
Dua alasan. Pertama, dalam tugas ini sopran diberikan sebagai soal, sehingga resolusi nada penuntun di sopran bukan keputusan model; Yan juga membatasi kategori itu pada sopran. Kedua, nada penuntun pada suara lain membutuhkan penentuan tonalitas dan akor. Versi lama mendeteksi tonalitas secara otomatis dengan cadangan diam-diam ke C mayor, dan itu tidak dapat dipertahankan.

**16. Bach sendiri melanggar kaidah. Kenapa Bach dijadikan acuan?**
Justru karena itu. Huang menemukan 132 kuint sejajar dan 51 oktaf sejajar pada 382 chorale, dan Yan mencatat bahwa kaidah buku ajar tidak diikuti Bach secara ketat. Acuan Bach bukan nol, melainkan pembanding realistis: berapa laju pelanggaran harmonisasi manusia ahli untuk melodi yang sama. Hasil model dibaca relatif terhadap acuan ini.

**17. Apa beda persilangan dan tumpang tindih suara?**
Persilangan terjadi pada satu saat: suara bawah berbunyi lebih tinggi daripada suara atas. Tumpang tindih terjadi pada perpindahan: suara bergerak melewati nada yang baru saja dibunyikan suara di sebelahnya, walaupun pada saat baru keduanya tidak bersilangan. Definisi tumpang tindih sengaja mensyaratkan tidak ada persilangan agar satu kejadian tidak dihitung dua kali.
*Bukti:* BAB III rumus Silang dan Tumpang.

**18. Unisono sejajar dihitung sebagai oktaf sejajar?**
Ya. Unisono dan oktaf sama-sama berjarak kelipatan 12 semiton dan sama-sama menghilangkan kemandirian satu suara. Fang dkk. juga memasukkan unisono dalam fitur kesalahan paralel. Pilihan ini dicatat sebagai bagian definisi; penghitungan dapat dipisah jika penguji meminta.

**19. Kenapa kuint dan oktaf tersembunyi tidak diukur?**
Tidak termasuk kategori rubrik Yan, sehingga tidak memenuhi syarat pertama. Dapat menjadi saran penelitian lanjutan jika Strube menguraikannya.

## D. Model

**20. Kenapa DeepBach dan Coconet? Kenapa tidak model terbaru?**
Tiga kriteria: kode dan bobot terbuka; bisa menerima melodi sopran yang ditetapkan lalu mengisi alto, tenor, bas; dilatih pada chorale Bach sehingga melodi Bach berasal dari jenis musik yang dipelajarinya. Coconet adalah model yang dianalisis Huang. Tujuan penelitian bukan meranking model terbaru, tetapi menguji temuan Huang lintas model dan kaidah. Model harmonisasi yang lebih baru, misalnya AI Harmonizer berbasis Transformer (NIME 2025), dapat diuji dengan instrumen yang sama sebagai penelitian lanjutan.

**21. Kenapa NotaGen dikeluarkan?**
Antarmuka resmi NotaGen menerima petunjuk periode, komponis, dan instrumentasi, bukan melodi tertentu yang harus dipertahankan. Pada desain lama, kondisi "sopran tetap" dan "sopran dan bas tetap" untuk NotaGen ternyata memakai metadata yang identik. Karena pertanyaan penelitian mensyaratkan melodi yang sama untuk semua model, NotaGen tidak memenuhi kriteria.

**22. Kalau DeepBach lebih patuh, berarti LSTM lebih baik dari CNN?**
Tidak. Yang bisa disimpulkan hanya bahwa checkpoint DeepBach yang diuji lebih patuh daripada checkpoint Coconet yang diuji pada melodi tersebut. Data latih, representasi, dan prosedur pengambilan sampel ikut berbeda. Yin dkk. juga mengingatkan bahwa keunggulan jenis model harus ditunjukkan, bukan diandaikan.

**23. Coconet yang Anda pakai sama dengan yang di Bach Doodle?**
Yang dipakai adalah checkpoint `coconet/bach` di Magenta.js yang disediakan Google. Hubungan persisnya dengan model produksi Bach Doodle tidak didokumentasikan dalam sumber yang diperiksa, sehingga penelitian ini tidak mengklaim modelnya identik. Karena itu angka Huang dipakai sebagai pembanding instrumen pada chorale Bach, bukan sebagai pembanding langsung hasil Coconet.

**24. Model mungkin sudah menghafal chorale Bach. Bukankah itu tidak adil?**
Kelompok Bach memang didefinisikan sebagai melodi dari jenis musik yang dipelajari model, yang mungkin sudah pernah dilihat. Itu kondisi "dalam distribusi" yang paling jelas, dan justru itu yang dibandingkan dengan melodi buku ajar. Untuk DeepBach, kode resminya menunjukkan pembagian data latih berurutan (85 persen awal untuk latihan), sehingga status setiap melodi dicatat dan dianalisis kepekaannya (dilihat vs tidak dilihat). Untuk Coconet, pembagiannya tidak didokumentasikan dan dicatat sebagai tidak diketahui.
*Bukti:* BAB III Sampel paragraf terakhir; analisis kepekaan kedua.

## E. Melodi dan sampel

**25. Kenapa 30 melodi per kelompok?**
Dari analisis daya. Untuk mendeteksi efek besar (d = 0,8 menurut Cohen) dengan α = 0,05 dua arah dan daya 0,8, uji t membutuhkan 25,5 per kelompok. Efisiensi uji peringkat terhadap uji t paling rendah 0,864 untuk distribusi kontinu apa pun (Hodges dan Lehmann), jadi 25,5 / 0,864 = 29,5, dibulatkan menjadi 30.
*Rawan bila:* ditanya kenapa efek besar, bukan sedang. Jawab: jumlah latihan dalam satu buku terbatas; dengan 30 per kelompok efek terkecil yang terdeteksi sekitar d = 0,78; efek sedang butuh sekitar 74 per kelompok. Efek terkecil yang dapat dideteksi dilaporkan dengan n yang benar-benar tercapai.

**26. Ada 600 harmonisasi. Kenapa n bukan 600?**
Lima harmonisasi dari melodi yang sama tidak independen. Menghitungnya sebagai 600 observasi akan membuat uji terlalu mudah signifikan. Laju kelima harmonisasi dirata-ratakan menjadi satu nilai per melodi per model; unit analisisnya melodi. Angka lima dipilih untuk meredam hasil acak satu kali generasi dengan beban komputasi yang terjangkau; menambah generasi tidak menambah jumlah observasi independen, yang ditentukan oleh jumlah melodi.

**27. Bagaimana memilih melodi Bach? Bisa saja Anda memilih yang menguntungkan.**
Kriteria kelayakan sama untuk kedua kelompok, lalu melodi Bach diambil secara acak dengan bilangan acak yang dicatat sebelum generasi. Untuk Strube, semua latihan melodi yang layak diikutsertakan, bukan dipilih.

**28. Bagaimana jika buku Strube tidak punya cukup latihan melodi?**
Jika kurang dari 30, semuanya tetap dipakai dan efek terkecil yang dapat dideteksi dilaporkan. Jika jauh lebih sedikit (sekitar kurang dari 10), desain diubah bersama pembimbing sebelum generasi, misalnya menambah latihan melodi dari buku harmoni lain, dan perubahan itu dicatat di protokol.
*Rawan bila:* inventaris belum dilakukan saat sidang. **Wajib ditutup.**

**29. Melodi Strube bisa berbeda dalam panjang, wilayah, dan tangga nada. Bagaimana tahu yang berpengaruh adalah asalnya?**
Penelitian ini tidak mengklaim satu ciri sebagai penyebab. Variabelnya adalah asal melodi sebagai satu paket, sama seperti kelompok "di luar batas" pada Huang. Ciri-ciri melodi diukur dan dilaporkan supaya pembaca tahu perbedaan apa saja yang ada di antara kedua kelompok.

**30. Melodi Strube mungkin masih berada dalam batas Huang (MIDI 60–81, lompatan ≤ satu oktaf). Lalu apa artinya "di luar distribusi"?**
Batas Huang hanya mengukur wilayah dan lompatan. Melodi buku ajar tetap bukan chorale Bach: sumbernya lain, panjangnya berbeda (Yan mencatat soal 4 birama berbeda dari panjang data latih), dan polanya tidak dipelajari model. Proporsi melodi yang di luar batas Huang dilaporkan. Jika kedua kelompok sama-sama di dalam batas tetapi hasilnya berbeda, itu temuan bahwa batas wilayah dan lompatan saja tidak cukup menggambarkan distribusi. Jika hasilnya tidak berbeda, itu juga informatif.

**31. Kenapa melodi tidak ditransposisi agar setara?**
Transposisi mengubah jarak melodi terhadap data latih, sehingga mengubah variabel yang sedang diuji. Melodi yang memuat nada di luar wilayah masukan model dikeluarkan dan dicatat, bukan ditransposisi.

## F. Instrumen, validitas, reliabilitas

**32. Rumus Anda dari mana?**
Kaidahnya dari Strube dan kategorinya dari rubrik Yan. Rumusnya disusun peneliti sebagai definisi operasional, dan BAB III menyatakan itu secara terbuka. Setiap simbol didefinisikan, dan rumus diuji terhadap contoh buku serta fungsi music21.
*Bukti:* BAB III Instrumen Pengukuran paragraf 1.

**33. Tanpa penilai manusia, bagaimana Anda tahu program Anda benar?**
Empat langkah. (1) Validitas isi: setiap kaidah dikaitkan dengan halaman Strube dan kategori Yan sebelum data. (2) Contoh cetak Strube dipakai sebagai kunci: program harus menandai contoh yang disebut salah oleh buku dan tidak menandai contoh yang benar; label benar/salahnya datang dari penulis buku, bukan dari peneliti. (3) Pemeriksaan silang dengan fungsi `VoiceLeadingQuartet` music21 pada 371 chorale. (4) Laju kuint dan oktaf sejajar pada chorale Bach dibandingkan dengan angka terbitan Huang (0,023 dan 0,009 per birama).
*Rawan bila:* langkah 2 belum ada karena contoh Strube belum diketik. **Wajib ditutup.**

**34. Pelanggaran yang sebenarnya bisa dimaklumi ikut terhitung. Bukankah hasilnya bias?**
Penghitungan utama mengikuti Huang, yaitu semua kejadian dihitung. Penghitungan tambahan mengecualikan gerak pada batas frasa (fermata), yang memang disebut Huang sebagai salah satu alasan pemakluman. Pengecualian karena nada non-akor tidak diterapkan karena butuh analisis akor; ini dinyatakan sebagai batas. Instrumen yang sama dipakai untuk semua model, semua melodi, dan untuk harmonisasi Bach, sehingga perbandingannya tetap setara. Hasil disebut "pelanggaran menurut definisi operasional", bukan "kesalahan musikal".

**35. Kenapa per birama, bukan per akor?**
Satuan per birama dipakai Huang, sehingga angka penelitian ini dapat dibandingkan dengan angka terbitan. Jumlah kejadian dan jumlah kesempatan (gerak atau peristiwa bunyi yang diperiksa) juga disimpan, sehingga laju per kesempatan dapat dihitung bila diminta.

**36. Kenapa kisi seperenam belas?**
Itu resolusi waktu kedua model: DeepBach membagi satu ketukan menjadi empat, Coconet memakai langkah seperenam belas. Yan juga memakai kuantisasi seperenam belas. Melodi dengan nilai lebih pendek atau triol dikeluarkan dari sampel.

**37. MIDI tidak menyimpan ejaan nada. Bagaimana membedakan kuint murni dari sekst berkurang?**
Tidak bisa dibedakan dari MIDI. Tujuh semiton dihitung sebagai kuint. Dalam tekstur chorale tonal, sekst berkurang jarang muncul, dan keterbatasan ini dicatat. Alasan yang sama membuat kategori sekon diperbesar tidak diukur.

**38. Bagaimana kalau angka Bach Anda tidak sama dengan Huang?**
Tidak diharapkan sama persis: Huang memakai versi data latih Coconet tanpa fermata dan tidak menjelaskan pengaturan music21-nya, sedangkan penelitian ini memakai 371 chorale korpus music21. Yang disyaratkan adalah perbedaannya dapat dijelaskan. Jika perbedaannya besar dan tidak dapat dijelaskan, instrumen diperiksa ulang sebelum dipakai, dan perubahan dicatat sebagai versi baru.

**39. Bobot 1 dan 0,5 dari mana? Kenapa tidak jadi skor utama?**
Dari rubrik Yan: kategori paralel berbobot 1; jarak, persilangan, dan tumpang tindih masing-masing 0,5. Indeks tertimbang hanya ringkasan tambahan. Pengujian utama dilakukan per kaidah karena dua harmonisasi dengan skor sama bisa punya masalah yang berbeda.

**40. Reliabilitas instrumen mesin? Bukankah pasti sama?**
Ya, dan itu justru yang dibuktikan: menjalankan ulang berkas yang sama dengan versi instrumen yang sama harus menghasilkan penandaan identik, diperiksa dengan membandingkan hash keluaran. Variasi yang ada berasal dari generasi model dan ditangani dengan lima harmonisasi per melodi.

**41. Bagaimana jika model mengubah sopran yang diberikan?**
Harmonisasi itu tidak layak dianalisis. Sopran harus identik dengan masukan dalam tinggi nada dan saat mulai. Kegagalan dicatat dan dilaporkan per model dan per asal melodi, karena tingkat kegagalan juga merupakan hasil.

## G. Statistik

**42. Kenapa non-parametrik?**
Laju pelanggaran tidak bisa negatif, banyak bernilai nol, dan tidak dapat diasumsikan normal. Huang juga memakai uji non-parametrik (Kruskal–Wallis dan Mann–Whitney).

**43. Kenapa Wilcoxon untuk pertanyaan 2 dan Mann–Whitney untuk pertanyaan 3?**
Pertanyaan 2 berpasangan: setiap melodi diharmonisasi kedua model, jadi dipakai uji peringkat bertanda Wilcoxon. Pertanyaan 3 membandingkan dua kelompok melodi yang berbeda, jadi dipakai Mann–Whitney.

**44. Kenapa hipotesis satu arah untuk kuint dan oktaf? Supaya mudah signifikan?**
Arahnya berasal dari temuan Huang dan ditetapkan sebelum data dikumpulkan di protokol. Untuk tiga kaidah lain tidak ada dasar arah, sehingga diuji dua arah. Nilai p dua arah juga dilaporkan untuk transparansi.

**45. Koreksi Holm itu apa?**
Ketika lima kaidah diuji sekaligus, peluang mendapat satu hasil signifikan secara kebetulan meningkat. Holm mengurutkan nilai p dan menyesuaikan ambangnya bertahap, sehingga kesalahan keseluruhan tetap 0,05. Holm dipakai per kelompok pengujian: lima kaidah untuk pertanyaan 2, dan lima kaidah per model untuk pertanyaan 3.

**46. Kalau tidak signifikan, berarti kedua model sama?**
Tidak. Tidak signifikan berarti data tidak cukup untuk menolak H0. Menyimpulkan kesetaraan butuh pendekatan lain, misalnya uji Bayesian non-parametrik seperti yang dipakai Yin dkk.

**47. Kenapa tidak Kruskal–Wallis seperti di proposal dan di Huang?**
Kruskal–Wallis untuk tiga kelompok atau lebih. Desain sekarang membandingkan dua kelompok pada setiap pengujian. Huang sendiri melanjutkan Kruskal–Wallis dengan Mann–Whitney antar-pasangan kelompok.

**48. Ukuran efek itu apa, dan kenapa dilaporkan?**
Nilai p hanya menjawab apakah ada perbedaan; ukuran efek menunjukkan seberapa besar. Korelasi peringkat biserial dilaporkan agar perbedaan kecil yang kebetulan signifikan tidak dibesar-besarkan.

## H. Posisi peneliti, etika, dan batas

**49. Anda mahasiswa musik yang meneliti musik. Bagaimana menghindari bias?**
Posisi peneliti adalah orang dalam terhadap tradisi teori dan orang luar terhadap model. Pengendaliannya: definisi kaidah, kriteria melodi, dan rencana analisis ditetapkan sebelum generasi; melodi Bach diambil acak dengan bilangan acak tercatat; semua latihan Strube yang layak diikutsertakan; pengukuran otomatis dengan instrumen yang sama; contoh pembahasan dipilih acak.
*Bukti:* BAB III Metode Pendekatan paragraf terakhir.

**50. Kenapa tidak ada izin etik?**
Penelitian ini tidak melibatkan manusia sebagai subjek, penilai, atau pendengar. Data berupa partitur publik (korpus music21), latihan buku yang diketik untuk penelitian, dan keluaran model. Pindaian buku tidak disebarkan.

**51. Apa batas utama penelitian?**
Hanya dua model dan checkpoint yang diuji; hanya lima kaidah tanpa analisis akor; pengecualian nada non-akor tidak diterapkan; asal melodi dibaca sebagai satu paket ciri; tidak ada klaim tentang arsitektur; kepatuhan kaidah Strube adalah ukuran kesesuaian dengan satu tradisi, bukan mutu musik secara umum.

**52. Kenapa desain berubah jauh dari proposal?**
Evaluasi atas desain proposal menunjukkan tiga masalah: tingkat kendali A–D tidak setara antar-model (kondisi NotaGen C dan D identik), pemilihan tiga kaidah dan rumus skor tidak punya dasar sumber, dan pengukuran nada penuntun bergantung pada deteksi tonalitas otomatis. Desain baru mengikatkan setiap pilihan pada penelitian terdahulu: Huang untuk desain dan ukuran, Yan untuk kategori, Strube untuk kaidah. Perubahan dicatat di protokol beserta alasannya, dan desain lama disimpan sebagai versi historis.
*Rawan bila:* pembimbing belum menyetujui. **Wajib ditutup** sebelum sidang.

**53. Bagian mana yang Anda kerjakan sendiri? Apakah memakai bantuan AI?**
Jawab jujur dan sesuai aturan departemen tentang penggunaan AI; sepakati bentuk pengungkapannya dengan pembimbing. Yang harus bisa dijelaskan sendiri tanpa catatan: pertanyaan penelitian, alasan setiap kaidah dan halaman Strube-nya, cara kerja setiap rumus, alasan setiap uji statistik, dan contoh partitur yang dibahas.

## I. Pertanyaan lanjutan dan jebakan

**54. Bagaimana jika model ternyata lebih patuh pada melodi Strube?**
Hipotesis satu arah ditolak dan hasil dilaporkan apa adanya. Penjelasan yang mungkin dibahas: melodi buku ajar lebih sederhana dan bergerak bertahap, sehingga lebih mudah diharmonisasi tanpa paralel. Ciri melodi yang dilaporkan membantu menguji penjelasan itu.

**55. Bagaimana jika Coconet gagal memproses banyak melodi?**
Tingkat kegagalan dilaporkan sebagai hasil per model dan per asal melodi. Melodi yang gagal dikeluarkan dari perbandingan berpasangan dan pengeluarannya dicatat. Jika kegagalan berkaitan dengan panjang melodi, hal itu ditemukan saat pilot dan kriteria panjang ditetapkan sebelum data utama.

**56. Apa manfaat nyata bagi pengajar?**
Pengajar mendapat gambaran kaidah mana yang paling sering dilanggar model ketika diberi soal latihan, lengkap dengan lokasi birama, dan seberapa jauh dibanding Bach. Itu bisa dipakai untuk membahas keluaran AI di kelas harmoni atau menilai tugas yang dibantu AI.

**57. Kenapa tidak membandingkan dengan jawaban mahasiswa seperti Yan?**
Membandingkan dengan mahasiswa membutuhkan partisipan manusia, izin, dan penilai, yang berada di luar cakupan penelitian komputasional ini. Harmonisasi asli Bach dipakai sebagai acuan manusia ahli untuk melodi Bach. Perbandingan dengan jawaban mahasiswa dapat menjadi saran lanjutan.

**58. Bagaimana orang lain mengulang penelitian Anda?**
Identitas model dan checkpoint, pengaturan generasi, daftar melodi beserta halaman Strube, bilangan acak, keluaran mentah, kode instrumen, dan berkas hasil disimpan. Instrumen yang sama dijalankan ulang menghasilkan penandaan identik.

## Cara berlatih

1. Ucapkan kalimat pegangan dan jawaban 1, 6, 7, 14, 24, 33, dan 52 tanpa membaca.
2. Minta teman bertanya acak dari daftar ini dan memotong jawaban yang lebih dari satu menit.
3. Setelah setiap celah di tabel atas ditutup, perbarui jawaban yang terkait dan hapus tanda **Wajib ditutup**.
