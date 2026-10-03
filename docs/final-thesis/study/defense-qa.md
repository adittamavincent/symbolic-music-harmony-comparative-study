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

Diperbarui 3 Oktober 2026. Celah yang sudah tertutup penuh dihapus dari tabel.

| Celah | Kenapa berbahaya | Cara menutup | Status |
| --- | --- | --- | --- |
| Halaman Strube untuk lima kaidah | Pertanyaan "di halaman berapa?" | Kaidah ditemukan: paralel hlm. 9 dan 12, jarak hlm. 20, persilangan hlm. 174, tumpang tindih hlm. 12–13 (`strube-rule-pages.csv`) | Tertutup; cocokkan sekali dengan buku cetak |
| Jumlah latihan melodi Strube | Separuh desain | 71 latihan melodi bernomor di hlm. 11–80. Latihan 67–68 (hlm. 48, tidak ada di PDF 1928) terlihat di terjemahan 2015 hlm. 58 sebagai latihan melodi | Tertutup; cocokkan hlm. 48 dengan buku 1928 cetak bila tersedia |
| Contoh cetak Strube sebagai kasus uji | Validasi langkah 2 | Sembilan gambar terdaftar di `strube-example-fixtures.csv`; perlu diketik ke MusicXML | Terbuka (kerja peneliti, sekitar 20–30 menit) |
| Kode instrumen dan format data | Klaim BAB III belum ada wujudnya | `research/voice_leading_v2.py` (20 uji perangkat lunak; validasi langkah 3–5 sudah dijalankan) dan `research/harmonization_io.py` (masukan dan keluaran MusicXML untuk kedua model, 27 uji perangkat lunak) | Tertutup untuk instrumen dan format data; runner generasi belum |
| Pilot | Batas panjang melodi, kosakata DeepBach, dan memori Coconet belum diuji pada model | Runner generasi di atas adapter MusicXML, perbaikan pipeline lain, pilot | Terbuka (tahap penelitian setelah proposal disetujui) |
| Persetujuan pembimbing | Desain berubah besar dari proposal | Bawa naskah v3 dan `bimbingan-v3.md` | Terbuka |
| Terjemahan Strube oleh Pembimbing I | Pembimbing I menerjemahkan buku Strube (2015); tiga kalimat kaidah berbeda dari edisi 1928 | Pelajari [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md) bagian 1; tanyakan cara mengutip terjemahan | Terbuka |
| Jarak dan persilangan dihitung per peristiwa bunyi | Coconet tidak dapat mengulang nada, sehingga lajunya untuk dua kaidah ini lebih rendah karena cara pengukuran (Q92) | Samakan perlakuan nada ulang untuk semua keluaran, atau hitung per rentang; jadikan instrumen versi 3 | Terbuka (ditemukan 3 Oktober 2026) |
| Halaman Cohen, Hodges–Lehmann, Creswell, Sugiyono | Penguji bisa minta halaman | Buka sumber, catat di `reading-notes.csv` | Terbuka (kecil) |

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
Catatan review proposal meminta penelitian ini merujuk Strube. Terjemahan Indonesianya, *Teori dan Penggunaan Akor* jilid I (UPT Perpustakaan ISI Yogyakarta, 2015), diterjemahkan oleh A. Gathut Bintarto T., yaitu Pembimbing I. Edisi yang dirujuk adalah edisi asli 1928 (Oliver Ditson). Buku ini menyediakan dua hal yang dibutuhkan desain: uraian kaidah beserta pengecualiannya, dan latihan harmonisasi melodi yang dapat diberikan kepada model. Jika Strube memang buku ajar mata kuliah harmoni di program studi, sebutkan itu setelah faktanya dipastikan.
*Bukti:* Strube hlm. 8 (latihan bas dan melodi), hlm. 9, 12–13, 20, 174 (kaidah).

**13. Rubrik Yan berasal dari tradisi buku Amerika, Strube lain lagi. Kenapa dicampur?**
Keduanya dari tradisi yang sama, yaitu penulisan empat suara dalam harmoni tonal Barat. Yan sendiri menyebut rubriknya lazim dalam buku ajar dan kelas teori musik. Pembagiannya jelas: Yan menentukan kategori mana yang punya preseden untuk menilai harmonisasi model; Strube menentukan rumusan dan pengecualian yang dipakai. Setiap kaidah dicatat sumbernya di lembar definisi.

**14. Strube punya banyak kaidah. Kenapa hanya lima?**
Tiga syarat, ditetapkan sebelum data: (1) termasuk kategori rubrik Yan, (2) diuraikan Strube, (3) pelanggarannya dapat ditentukan dari tinggi nada dan waktu bunyi tanpa menafsirkan akor atau tonalitas. Syarat ketiga diperlukan karena analisis akor bisa berbeda antar-ahli; Koops dkk. mencatat kesepakatan rata-rata hanya 73 persen untuk label akor mayor–minor. Kaidah yang bergantung pada akor membutuhkan penilai manusia, sedangkan penelitian ini sepenuhnya komputasional. Hasilnya dinyatakan untuk lima kaidah itu saja, bukan untuk seluruh teori harmoni.
*Bukti:* BAB I paragraf "Buku Strube menjadi acuan..."; BAB II paragraf kategori yang dikeluarkan.

**15. Di proposal ada resolusi nada penuntun. Kenapa dihapus?**
Dua alasan. Pertama, dalam tugas ini sopran diberikan sebagai soal, sehingga resolusi nada penuntun di sopran bukan keputusan model; Yan juga membatasi kategori itu pada sopran. Kedua, nada penuntun pada suara lain membutuhkan penentuan tonalitas dan akor. Versi lama mendeteksi tonalitas secara otomatis dengan cadangan diam-diam ke C mayor, dan itu tidak dapat dipertahankan.

**16. Bach sendiri melanggar kaidah. Kenapa Bach dijadikan acuan?**
Justru karena itu. Huang menemukan 132 kuint sejajar dan 51 oktaf sejajar pada 382 chorale, dan Yan mencatat bahwa kaidah buku ajar tidak diikuti Bach secara ketat. Acuan Bach bukan nol, melainkan pembanding realistis: berapa laju pelanggaran harmonisasi manusia ahli untuk melodi yang sama. Hasil model dibaca relatif terhadap acuan ini.

**16a. Kenapa persilangan hanya dihitung bila melewati sopran?**
Karena Strube sendiri membolehkan persilangan sesekali bila menghasilkan gerak suara yang lebih baik, asalkan tidak melewati sopran (hlm. 174). Menghitung semua persilangan berarti menghukum sesuatu yang dibolehkan sumber teori. Rubrik Yan menghitung semua persilangan; penyempitan ini disebutkan terbuka di BAB II.

**16b. Kenapa tumpang tindih dengan gerak melangkah tidak dihitung?**
Strube mendefinisikan tumpang tindih dan menyatakan gerak itu hanya dipakai bila salah satu suara bergerak melangkah (hlm. 12); Gambar 33 hlm. 13 menandai kasus kedua suara melompat sebagai "avoid". Instrumen mengikuti batas itu: melangkah berarti satu atau dua semiton.

**16c. Kenapa kuint dengan gerak berlawanan tidak dihitung, padahal music21 menghitungnya?**
Strube hlm. 9 menyatakan kuint dan oktaf berurutan dengan gerak berlawanan tidak bermasalah. Pada 345 chorale Bach yang memenuhi syarat (dari 371 di korpus music21), semua 69 penandaan tambahan music21 adalah kasus gerak berlawanan; untuk kasus lain kedua implementasi identik.

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

**28. Berapa latihan melodi di buku Strube, dan kenapa tidak semua dipakai?**
Latihan 1–118 (hlm. 8–81) sudah diinventaris: 71 memberi melodi sopran dan 47 memberi bas. Latihan 67–68 ada di hlm. 48, yang tidak ada di scan 1928; keduanya dibaca dari terjemahan 2015 hlm. 58 sebagai latihan melodi. Yang dipakai adalah latihan melodi bernomor sampai bab mode minor (hlm. 11–80). Latihan bas tidak dipakai karena tugasnya memberi sopran. Latihan melodi sesudah bab mode minor dirancang untuk melatih suspensi, nada sisipan, dan antisipasi; pelanggaran yang dimaklumi karena nada non-akor butuh analisis akor, sehingga instrumen akan salah menghitungnya. Strube sendiri menyebut nada non-akor dinilai dari sudut pandang berbeda (hlm. 35). Melodi di bab chorale tidak dipakai karena diambil dari Bach (hlm. 174). Kriteria ini berdasarkan isi bab, bukan hasil.
*Rawan bila:* hlm. 48 edisi 1928 belum dicocokkan dengan buku cetak.

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
Empat langkah validitas dan satu uji reliabilitas. (1) Validitas isi: setiap kaidah dikaitkan dengan halaman Strube dan kategori Yan sebelum data. (2) Contoh cetak Strube dipakai sebagai kunci: program harus menandai contoh yang disebut salah oleh buku dan tidak menandai contoh yang benar; label benar/salahnya datang dari penulis buku, bukan dari peneliti. (3) Pemeriksaan silang dengan fungsi `VoiceLeadingQuartet` music21 pada chorale korpus music21. (4) Laju kuint dan oktaf sejajar pada chorale Bach dibandingkan dengan angka terbitan Huang (0,023 dan 0,009 per birama). (5) Pengukuran ulang pada berkas yang sama harus memberi hasil identik.
Langkah 3–5 sudah dijalankan pada 345 dari 371 chorale Bach yang memenuhi syarat: tidak ada perbedaan dengan music21 untuk persilangan dan tumpang tindih; perbedaan paralel hanya kasus gerak berlawanan; dua kali run menghasilkan hash identik.
*Rawan bila:* langkah 2 belum ada karena gambar Strube belum diketik. Tutup dengan mengetik sembilan gambar di `strube-example-fixtures.csv`.

**34. Pelanggaran yang sebenarnya bisa dimaklumi ikut terhitung. Bukankah hasilnya bias?**
Penghitungan utama mengikuti Huang, yaitu semua kejadian dihitung. Penghitungan tambahan mengecualikan gerak pada batas frasa (fermata), yang memang disebut Huang sebagai salah satu alasan pemakluman. Pengecualian karena nada non-akor tidak diterapkan karena butuh analisis akor; ini dinyatakan sebagai batas. Instrumen yang sama dipakai untuk semua model, semua melodi, dan untuk harmonisasi Bach, sehingga perbandingannya tetap setara. Hasil disebut "pelanggaran menurut definisi operasional", bukan "kesalahan musikal".

**35. Kenapa per birama, bukan per akor?**
Satuan per birama dipakai Huang, sehingga angka penelitian ini dapat dibandingkan dengan angka terbitan. Jumlah kejadian dan jumlah kesempatan (gerak atau peristiwa bunyi yang diperiksa) juga disimpan, sehingga laju per kesempatan dapat dihitung bila diminta.

**36. Kenapa kisi seperenam belas?**
Itu resolusi waktu kedua model: DeepBach membagi satu ketukan menjadi empat, Coconet memakai langkah seperenam belas. Yan juga memakai kuantisasi seperenam belas. Melodi dengan nilai lebih pendek atau triol dikeluarkan dari sampel.

**37. Instrumen menghitung semiton. Bagaimana membedakan kuint murni dari sekst berkurang?**
Tidak dibedakan. Tujuh semiton selalu dihitung sebagai kuint. Melodi masukan disimpan sebagai MusicXML sehingga ejaannya terjaga, dan keluaran DeepBach juga berejaan. Keluaran Coconet hanya berupa nomor nada MIDI, sehingga ejaan alto, tenor, dan bas Coconet ditentukan music21, bukan oleh model. Agar kedua model diukur dengan aturan yang sama, instrumen tidak memakai ejaan. Dalam tekstur chorale tonal, sekst berkurang jarang muncul, dan keterbatasan ini dicatat. Alasan yang sama membuat kategori sekon berlebih tidak diukur.

**38. Angka Bach Anda tidak sama dengan Huang. Kenapa?**
Dengan definisi Strube, laju Bach 0,0078 kuint dan 0,0030 oktaf per birama. Dengan definisi music21 yang ikut menghitung gerak berlawanan, 0,0176 dan 0,0059; Huang melaporkan 0,023 dan 0,009. Sebagian besar selisih berasal dari definisi gerak berlawanan, yang tidak dianggap bermasalah oleh Strube. Sisanya wajar karena versi data berbeda (382 karya JSB, termasuk duplikat, tanpa fermata) dan pengaturan penghitungan Huang tidak diterbitkan. Semua angka itu lebih dari 20 kali lebih rendah daripada 0,365 kuint per birama pada Coconet, jadi instrumen jelas membedakan tingkat Bach dari tingkat model.

**39. Bobot 1 dan 0,5 dari mana? Kenapa tidak jadi skor utama?**
Dari rubrik Yan: kategori paralel berbobot 1; jarak, persilangan, dan tumpang tindih masing-masing 0,5. Indeks tertimbang hanya ringkasan tambahan. Pengujian utama dilakukan per kaidah karena dua harmonisasi dengan skor sama bisa punya masalah yang berbeda.

**40. Reliabilitas instrumen mesin? Bukankah pasti sama?**
Ya, dan itu justru yang dibuktikan: menjalankan ulang berkas yang sama dengan versi instrumen yang sama harus menghasilkan penandaan identik, diperiksa dengan membandingkan hash keluaran. Variasi yang ada berasal dari generasi model dan ditangani dengan lima harmonisasi per melodi.

**41. Bagaimana jika model mengubah sopran yang diberikan?**
Harmonisasi itu tidak layak dianalisis. Sopran harus identik dengan masukan dalam tinggi nada dan saat mulai. Kegagalan dicatat dan dilaporkan per model dan per asal melodi, karena tingkat kegagalan juga merupakan hasil.

## G. Statistik

**41a. Kenapa melodi dan hasil disimpan sebagai MusicXML, bukan MIDI?**
MusicXML menyimpan ejaan nada, fermata, tangga nada, birama, birama gantung, dan pemisahan suara. MIDI tidak menyimpan ejaan dan fermata, sedangkan tangga nada dan birama hanya opsional. DeepBach memakai fermata dan tangga nada sebagai masukan, dan instrumen membaca fermata untuk penghitungan tambahan. Setiap model mempunyai penerjemah sendiri dari MusicXML ke format internalnya, lalu kembali ke MusicXML. Setiap berkas yang ditulis dibaca ulang dan dibandingkan dengan isi aslinya. Pada 345 chorale Bach, harmonisasi asli Bach yang ditulis ulang melalui jalur ini menghasilkan jumlah pelanggaran dan jumlah birama yang sama dengan aslinya. Berkas MIDI tetap disimpan untuk didengarkan.
*Bukti:* `research/harmonization_io.py`; `research/protocol.md`, bagian *Shared input and output*.
*Rawan bila:* ditanya apakah model sudah dijalankan lewat jalur ini. Jawab: belum; apakah kedua model menerima masukannya diperiksa saat pilot.

**41b. Coconet tidak membedakan nada yang diulang dari nada yang ditahan. Apa akibatnya?**
Keluaran Coconet berupa *piano roll*: setiap langkah seperenam belas hanya mencatat nada yang berbunyi, sehingga dua nada sama yang berurutan tidak dapat dibedakan dari satu nada panjang. Nada sama yang berurutan pada alto, tenor, dan bas Coconet karena itu digabung menjadi satu nada. Suara hasil Coconet tidak pernah mengulang nada, dan peristiwa bunyinya bisa lebih sedikit daripada DeepBach, sehingga kaidah yang dihitung per peristiwa (jarak dan persilangan) dapat tercatat lebih jarang. Ini batas representasi model dan dilaporkan sebagai keterbatasan perbandingan. Untuk sopran, bila tinggi nada keluaran sama dengan melodi pada setiap langkah, nada asli melodi dipakai kembali, mengikuti cara yang disediakan Magenta.js untuk memulihkan suara masukan (`replaceVoice`). Sopran yang berbeda pada satu langkah saja tetap gagal kontrol kualitas.
*Rawan bila:* penguji menganggap penggabungan mengubah data. Jawab: penggabungan tidak mengubah tinggi nada atau waktu bunyi; ia hanya mengikuti apa yang dapat dinyatakan keluaran model.

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
Hanya dua model dan checkpoint yang diuji; hanya lima kaidah tanpa analisis akor; pengecualian Strube yang butuh analisis akor (kuint lewat, pengulangan akor, kuint akibat suspensi) tidak diterapkan; melodi Strube terbatas pada bab sebelum nada non-akor; asal melodi dibaca sebagai satu paket ciri; tidak ada klaim tentang arsitektur; kepatuhan kaidah Strube adalah ukuran kesesuaian dengan satu tradisi, bukan mutu musik secara umum.

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

## J. Pertanyaan untuk bimbingan Pembimbing I

Ditambahkan 2 Oktober 2026 setelah membaca terjemahan Strube oleh Pembimbing I, dipindahkan dari `persiapan-pembimbing-1.md` pada 3 Oktober 2026. Latar belakang, peta halaman, dan tiga perbedaan teks ada di bagian 1 berkas itu.

### Strube dan terjemahan Pembimbing I

**59. Kenapa mengutip edisi 1928, bukan terjemahan saya?**
Kaidah persilangan (1928 hlm. 174) dan latihan bab mode minor tidak ada di jilid I yang saya miliki. Saya memakai satu edisi agar semua halaman konsisten dan rumusan kaidah dapat dicocokkan dengan teks asli. Saya ingin juga mengutip terjemahan Bapak untuk istilah dan kaidah yang ada di jilid I. Apakah Bapak setuju dengan cara itu, dan apakah ada jilid II?
*Rawan bila:* belum pernah membuka terjemahan. Baca hlm. 10, 12–18, 27, dan 43–44 sebelum bimbingan.

**60. Di terjemahan saya, sopran "biasanya" boleh lebih dari satu oktaf dari alto. Kenapa dihitung sebagai pelanggaran?**
Edisi 1928 menulis "occasionally even farther", dan naskah mengikuti teks itu. Instrumen tidak menilai satu kejadian sebagai salah; instrumen menghitung seberapa sering jarak itu terjadi, dan "kadang-kadang" memang soal frekuensi. Laju model dibaca terhadap acuan Bach: pada chorale Bach, sopran–alto melebihi satu oktaf sekitar 0,022 kali per birama. Sopran–alto dan alto–tenor juga dapat dilaporkan terpisah. Setelah itu, tanyakan bagaimana Bapak membaca kalimat tersebut.
*Rawan bila:* jawaban terdengar menyalahkan terjemahan. Ajukan sebagai pertanyaan, bukan koreksi.

**61. Strube berkata tumpang tindih dipakai bila satu suara bergerak seperti pada gambar. Dari mana syarat satu atau dua semiton?**
Teks 1928 hlm. 12 menulis "moves stepwise". Gambar 32 a–c menunjukkan satu suara melangkah dan suara lain melompat. Gambar 33 menandai kasus kedua suara melompat sebagai yang harus dihindari. Langkah berarti interval sekon, yaitu satu atau dua semiton.
*Lanjutan yang mungkin:* "Sekon berlebih tiga semiton juga langkah." Benar menurut ejaan, tetapi MIDI tidak menyimpan ejaan sehingga sekon berlebih tidak dapat dibedakan dari terts kecil. Instrumen memperlakukannya sebagai lompatan, dan ini dicatat sebagai keterbatasan, sama seperti alasan kategori sekon berlebih tidak diukur.

**62. Banyak kaidah Strube berlaku "untuk saat ini", yaitu untuk tahap awal belajar. Kenapa kaidah tahap awal dipakai untuk menilai harmonisasi chorale?**
Melodi Strube yang dipakai berasal dari bab-bab yang sama (hlm. 11–80), jadi tahap kaidahnya sesuai dengan soal yang diberikan. Kaidah yang sama diterapkan tanpa perbedaan pada kedua model dan pada harmonisasi Bach, sehingga perbandingannya tetap setara. Hasilnya dibaca sebagai kesesuaian dengan norma buku ajar, bukan sebagai nilai musikal.

**63. Kenapa kuint dan oktaf tersembunyi tidak diukur? Strube membahasnya di hlm. 12 (terjemahan hlm. 16).**
Kaidah itu tidak termasuk rubrik Yan, sehingga tidak memenuhi syarat pertama. Akuilah bahwa kaidah ini dapat ditentukan dari tinggi nada dan waktu saja. Tawarkan untuk menambahkannya sebagai ukuran tambahan bila Pembimbing I menghendaki, dengan catatan bahwa penambahan itu mengubah instrumen dan harus dicatat sebagai versi baru sebelum data utama.

### Teori

**64. Grand theory Anda harmoni fungsional, tetapi kaidah yang diukur justru dipilih karena tidak memerlukan fungsi akor. Bukankah itu bertentangan?**
Harmoni fungsional menjelaskan mengapa empat suara bergerak: suara-suara itu mewujudkan progresi akor dalam tonalitas, dan kaidah gerak suara lahir dari praktik itu. Strube sendiri menempatkan larangan paralel dalam kerangka fungsi. Contohnya, bahaya paralel disebut terutama pada koneksi IV ke V (terjemahan hlm. 13), pembatasan ketat dikaitkan dengan perubahan fungsi harmoni (hlm. 44), dan akor dikelompokkan dalam keluarga seperti Subdominan Mayor (hlm. 60). Penelitian ini memakai teori itu sebagai sumber norma, tetapi sengaja mengukur wujud permukaannya saja, yaitu tinggi nada dan waktu. Tujuannya agar hasil tidak bergantung pada tafsir akor tanpa penilai manusia. Konsekuensinya, pengecualian yang memerlukan fungsi tidak diterapkan, dan hal itu dinyatakan sebagai batas.
*Rawan bila:* ditanya teori lain yang lebih cocok, misalnya teori gerak suara berbasis persepsi. Huron (2001), "Tone and Voice", *Music Perception* 19(1), sering dirujuk untuk itu, tetapi belum ada di naskah dan belum dibaca. Jangan menyebutnya sebagai dasar sebelum membacanya.

**65. Kaidah dipilih karena mudah dihitung mesin. Bukankah itu memilih yang mudah, bukan yang penting?**
Ini batas lingkup yang disengaja dan dinyatakan. Lima kaidah ini mencakup gerak paralel, yaitu kaidah yang dihitung Huang dan dikeluhkan pengguna Bach Doodle. Jarak antar-suara juga relevan bagi pengajaran: dalam studi Yan, mahasiswa lebih sering daripada model melampaui jarak satu oktaf antara suara atas yang berdekatan. Kategori lain memerlukan penilai manusia untuk tafsir akor, dan itu berada di luar cakupan penelitian ini. Kesimpulan hanya berlaku untuk lima kaidah ini.

**66. Di terjemahan saya, bas tidak boleh lebih tinggi dari tenor. Kenapa persilangan hanya dihitung di atas sopran?**
Kalimat pada edisi 1928 hlm. 7 hanya mengatakan bahwa bas boleh ditempatkan di mana saja dalam wilayahnya. Kaidah persilangan diambil dari bab harmonisasi chorale (hlm. 174), yang membolehkan persilangan sesekali kecuali melewati sopran. Bab itu dipilih karena tugasnya sama dengan tugas model. Instrumen dapat menghitung persilangan alto–tenor dan tenor–bas tanpa biaya tambahan, jadi tawarkan untuk melaporkannya sebagai data deskriptif tambahan. Tanyakan bagaimana Bapak membaca kalimat di hlm. 10.

**67. Kenapa wilayah suara tidak diukur?**
Wilayah suara tidak termasuk rubrik Yan. Kaidah ini bisa diukur tanpa analisis akor, tetapi keluaran model sudah dibatasi wilayah data latihnya (Coconet hanya memakai nada MIDI 36–81), sehingga pelanggarannya kemungkinan jarang. Kaidah ini dapat ditambahkan sebagai data deskriptif bila diminta.

### Desain

**68. Untuk melodi Strube tidak ada harmonisasi ahli. Bagaimana Anda tahu laju model di sana tinggi atau rendah?**
Acuan Bach hanya tersedia untuk melodi Bach. Pertanyaan 3 membandingkan model yang sama pada dua asal melodi, jadi pembandingnya adalah perilaku model itu sendiri pada melodi Bach. Jika Pembimbing I mempunyai atau mengetahui contoh harmonisasi untuk latihan Strube, contoh itu bisa menjadi acuan tambahan, tetapi sumbernya harus dicatat.

**69. Chorale Bach memiliki fermata, sedangkan latihan Strube mungkin tidak. Bukankah DeepBach mendapat informasi kadens lebih banyak pada melodi Bach?**
Benar. DeepBach memakai fermata sebagai informasi masukan, sedangkan Coconet tidak. Perbedaan ini bagian dari "asal melodi sebagai satu paket", sama seperti perbedaan panjang dan wilayah. Kolom `has_fermata_or_phrase_marks` di inventaris perlu diisi saat mengetik, dan jumlah melodi bertanda frasa dilaporkan per kelompok. Analisis kepekaan tanpa batas frasa juga hanya berlaku pada melodi yang memiliki tanda frasa, dan hal itu perlu dilaporkan.
*Belum diputuskan:* apakah DeepBach juga dijalankan pada melodi Bach tanpa fermata sebagai pemeriksaan tambahan. Diskusikan sebelum protokol dibekukan.

**70. Melodi tidak diacak ke dalam kelompok. Bukankah ini komparatif kausal, bukan eksperimen?**
Yang dikendalikan peneliti adalah masukan yang diberikan kepada model yang sama. Namun kelompok melodi berbeda dalam beberapa ciri sekaligus, sehingga pengaruhnya dibaca sebagai pengaruh asal melodi secara keseluruhan (BAB II Hipotesis, paragraf terakhir). Bila Pembimbing I lebih suka istilah lain, misalnya kuasi-eksperimen, substansinya tidak berubah. Cocokkan istilah dengan halaman Sugiyono yang dipakai.

**71. Latihan Strube lebih pendek daripada chorale. Apakah laju per birama adil?**
Laju per birama mengikuti Huang. Pada melodi pendek, satu kejadian mengubah laju lebih banyak, dan birama gantung dihitung satu birama penuh. Panjang melodi dilaporkan sebagai ciri kelompok. Jumlah kejadian dan jumlah kesempatan juga disimpan, sehingga laju per kesempatan dapat dihitung sebagai pemeriksaan.

**72. Melodi yang tidak dapat diproses model dikeluarkan. Bukankah yang terbuang justru melodi Strube yang paling tidak lazim?**
Mungkin. DeepBach hanya menerima nada sopran yang ada di kosakata data latihnya, dan Coconet hanya nada MIDI 36–81. Kosakata DeepBach memakai nama nada berejaan, jadi F♯4 dan G♭4 adalah dua entri berbeda; ejaan yang diketik di MusicXML ikut menentukan kelayakan. Melodi yang dikeluarkan dapat membuat kedua kelompok lebih mirip daripada aslinya. Karena itu, setiap pengeluaran dicatat beserta alasannya dan dilaporkan. Melodi tidak ditransposisi (Q31).

**73. Pertanyaan 2 menggabungkan melodi Bach dan Strube. Bagaimana jika perbedaan model hanya muncul pada salah satu asal?**
Statistik deskriptif per model dan per asal melodi tetap dilaporkan, jadi pola seperti itu akan terlihat. Uji interaksi formal belum ada di protokol. Salah satu pilihan sederhana adalah menghitung selisih DeepBach dikurangi Coconet untuk setiap melodi, lalu membandingkan selisih itu antara kedua asal melodi dengan Mann–Whitney. Pilihan ini perlu disetujui sebelum protokol dibekukan.

**74. Bisakah Coconet mengharmonisasi melodi utuh?**
Belum diketahui. Adapter MusicXML yang baru memberikan melodi dengan panjang penuh; adapter versi 1 hanya memakai 32 langkah seperenam belas, yaitu dua birama 4/4. Apakah Coconet sanggup memproses melodi penuh dalam batas memori diperiksa saat pilot. Jika melodi harus dipotong, kedua model harus menerima potongan yang sama, dan perubahan itu dicatat sebagai perubahan protokol. Lihat risiko di `research/protocol.md`.

### Statistik

**75. Persilangan jarang terjadi. Bagaimana Wilcoxon menangani banyak selisih nol?**
Secara bawaan, uji Wilcoxon di SciPy membuang pasangan yang selisihnya nol, sehingga jumlah pasangan efektif turun. Jumlah pasangan yang selisihnya bukan nol perlu dilaporkan. Cara menangani nol, yaitu dibuang atau metode Pratt, belum ditulis di protokol dan perlu ditetapkan sebelum data dikumpulkan. Mann–Whitney juga memerlukan koreksi nilai kembar (*ties*) karena banyak laju bernilai nol.

### Praktis

**76. Apa langkah berikutnya, dan kapan selesai?**
Urutannya: mengetik 71 kandidat melodi dan sembilan contoh cetak Strube; menjalankan validasi langkah 2; menulis runner generasi versi 2 di atas adapter MusicXML yang sudah ada, dengan folder per run dan catatan setiap percobaan; memperbaiki cacat pipeline lain di `docs/maintenance.md`; pilot; membekukan protokol; generasi utama; analisis. Siapkan perkiraan waktu sendiri sebelum bimbingan. Berkas ini tidak menetapkan tanggal.

**77. Bagian mana yang Anda kerjakan dengan bantuan AI?**
Lihat Q53. PROGRESS.md mencatat bahwa motto, halaman persembahan, dan kata pengantar dirancang dengan bantuan AI. [research-log.md](../records/research-log.md) mencatat bahwa penulisan ulang BAB I–III, kode instrumen versi 2, dan adapter MusicXML dikerjakan asisten AI atas permintaan peneliti. Jawab jujur dan ikuti aturan prodi. Pastikan setiap kalimat di naskah dapat dijelaskan sendiri.

**78. Kenapa mahasiswa musik mengerjakan penelitian komputasi? Apa sumbangannya bagi musik?**
Yan dkk. menilai evaluasi model musik umumnya kurang ketat dari sudut teori musik. Keahlian musik dalam penelitian ini ada pada pemilihan dan perumusan kaidah, pembacaan pengecualian Strube, pemilihan soal latihan, dan penafsiran contoh partitur. Hasilnya berguna bagi pengajar harmoni yang mahasiswanya memakai alat semacam ini.

## K. Simulasi penguji per sudut pandang (audit 3 Oktober 2026)

Ditambahkan setelah audit BAB I–III pada 3 Oktober 2026. Pertanyaan disusun menurut sudut pandang yang biasa muncul di sidang: format dan bahasa, teori musik, metodologi dan statistik, serta konsistensi naskah. Sudut pandang ini bukan perkiraan tentang dosen tertentu. Pertanyaan yang sudah dijawab di bagian A–J tidak diulang.

### Format, bahasa, dan sumber

**79. Template prodi meminta latar belakang 2–3 halaman dan menggabungkan rumusan masalah dengan pertanyaan penelitian. Kenapa naskah Anda berbeda?**
Struktur BAB I mengikuti skripsi S-1 Musik 2026 yang sudah disetujui: Intan dan Nourmalita menulis rumusan masalah sebagai prosa lalu pertanyaan penelitian sebagai bagian tersendiri, dan empat dari enam skripsi memuat sistematika penulisan. Latar belakang sekarang sekitar empat halaman (sekitar 1.100 kata); skripsi acuan memakai sekitar 1.570–2.410 kata.
*Bukti:* `records/research-log.md`, entri 2026-10-02 tentang perbandingan BAB I dengan skripsi acuan.
*Rawan bila:* penguji memegang template sebagai aturan wajib. Tanyakan kepada pembimbing sebelum sidang bentuk mana yang dipakai prodi untuk skripsi.

**80. Kenapa memakai "et al." dalam teks berbahasa Indonesia, bukan "dkk."?**
Gaya sitasi mengikuti format APA yang dipakai kelas dokumen. Penggantiannya mudah dilakukan di seluruh naskah bila pedoman prodi meminta "dkk.".

**81. Judul menyebut "musik hasil AI", padahal yang diteliti hanya harmonisasi empat suara dari dua model. Bukankah terlalu luas?**
Frasa "evaluasi musik hasil ..." berasal dari catatan review proposal (F01), dan judul langsung menyebut DeepBach dan Coconet, sehingga objeknya terbatas pada keluaran kedua model itu. Subjudul menyebut variabel bebas kedua, variabel terikat, dan Strube.
*Rawan bila:* penguji meminta judul yang lebih sempit. Jangan berjanji mengganti judul di ruang sidang; catat usulan itu dan putuskan bersama pembimbing.

**82. Apakah ada penelitian sejenis di Indonesia atau di ISI? Sumber berbahasa Indonesia hampir hanya Sugiyono dan Rangkuti.**
Di antara sumber yang ditinjau belum ditemukan penelitian Indonesia tentang kepatuhan kaidah gerak suara pada harmonisasi model AI. Penelusuran yang tercatat dilakukan melalui OpenAlex dengan kata kunci bahasa Inggris.
*Rawan bila:* penguji bertanya apakah repositori ISI, Garuda, atau SINTA sudah ditelusuri. Belum. Lakukan penelusuran berbahasa Indonesia, catat kata kunci dan tanggalnya, dan masukkan sumber yang relevan sebelum sidang.

**83. Template meminta tinjauan pustaka dari jurnal terakreditasi atau bereputasi. Banyak sumber Anda berupa prosiding konferensi dan terbit 2025–2026.**
Dalam bidang *music information retrieval*, prosiding ISMIR dan konferensi pembelajaran mesin adalah tempat terbit utama yang ditelaah sejawat. Huang dkk. (2019) dan Yan dkk. (2018), dua sumber terpenting, terbit di ISMIR.
*Rawan bila:* penguji menanyakan isi sumber yang hanya diperiksa dari abstrak. Ketahui sumber mana yang sudah dibaca penuh (lihat `records/reading-notes.csv` dan bagian *Citation checks* di `PROGRESS.md`).

### Teori dan musik

**84. Siapa Gustav Strube, dan kenapa buku Amerika tahun 1928 relevan bagi mahasiswa ISI pada 2026?**
Buku ini dipakai karena memuat rumusan kaidah beserta pengecualian, contoh benar dan salah yang dapat dijadikan kasus uji, dan latihan harmonisasi melodi yang dapat dijadikan masukan model. Jilid I buku ini sudah diterjemahkan ke bahasa Indonesia oleh Pembimbing I dan diterbitkan UPT Perpustakaan ISI Yogyakarta pada 2015.
*Rawan bila:* ditanya biodata Strube. Biodatanya belum dicatat di naskah atau di catatan bacaan. Cari dari sumber yang dapat diperiksa sebelum sidang; jangan menjawab dari ingatan.

**85. Larangan kuint sejajar berasal dari tradisi kontrapung, jauh sebelum teori fungsi harmoni. Kenapa teori utamanya harmoni fungsional?**
Lihat juga Q64. BAB II sekarang menyatakan bahwa kelima kaidah dipilih karena dapat diperiksa tanpa menentukan fungsi akor, sedangkan harmoni fungsional tetap menjadi kerangka karena sebagian pengecualian Strube (kuint lewat, kuint pada pengulangan akor) bergantung pada fungsi harmoni dan membatasi penafsiran hasil. Akui bahwa asal-usul larangan paralel memang lebih tua daripada teori fungsi.
*Rawan bila:* penguji mengusulkan teori kontrapung atau "harmoni tonal praktik umum" sebagai teori utama. Tidak ada sumber kontrapung di daftar pustaka. Diskusikan dengan Pembimbing I sebelum sidang, jangan mengganti kerangka teori di ruang sidang.

**86. Melodi chorale umumnya adalah melodi nyanyian jemaat yang lebih tua, bukan karangan Bach. Jadi apa maksud "melodi Bach"?**
Benar. BAB I menyebut chorale Bach sebagai harmonisasi empat suara yang ditulis Bach untuk melodi nyanyian jemaat. "Kelompok Bach" adalah label untuk melodi sopran dari korpus chorale yang diharmonisasi Bach, yaitu korpus yang dipelajari kedua model. Label itu tidak menyatakan bahwa Bach mengarang melodinya.

**87. Kalau model hanya menyalin harmonisasi Bach yang sudah dihafalnya, kepatuhan pada melodi Bach tinggi karena hafalan, bukan karena melodinya "dalam distribusi". Bagaimana membedakannya?**
Untuk DeepBach, status data latih setiap melodi dicatat dan dianalisis kepekaannya (melodi yang pernah dilihat dan yang tidak). Untuk Coconet, status itu tidak diketahui.
*Rawan bila:* penguji meminta bukti langsung. Pemeriksaan yang belum ada di protokol: hitung proporsi nada alto, tenor, dan bas keluaran model yang sama dengan harmonisasi asli Bach pada langkah waktu yang sama. Kemiripan yang sangat tinggi menunjukkan penyalinan. Putuskan apakah pemeriksaan ini ditambahkan sebelum protokol dibekukan.

**88. Kenapa tidak memakai melodi lokal, misalnya melodi nyanyian jemaat berbahasa Indonesia, sebagai asal melodi ketiga?**
Penelitian ini membatasi diri pada dua asal melodi agar desainnya sesuai dengan analisis Huang dkk. dan jumlah sampelnya terpenuhi. Kaidah Strube adalah norma tradisi Barat, dan BAB III menyatakannya. Melodi lokal adalah saran yang baik untuk penelitian lanjutan, dengan kriteria kelayakan yang sama.

### Metodologi dan statistik

**89. Populasi Anda harmonisasi atau melodi?**
Melodi. Populasi pertama adalah melodi sopran 371 chorale dalam korpus music21; populasi kedua adalah latihan harmonisasi melodi dalam buku Strube. Harmonisasi adalah pengamatan berulang untuk setiap melodi dan dirata-ratakan menjadi satu nilai per melodi per model.
*Bukti:* BAB III Populasi dan Sampel (direvisi 3 Oktober 2026; sebelumnya populasi ditulis sebagai harmonisasi, padahal unit analisisnya melodi).

**90. Semua latihan Strube yang layak dipakai. Kalau itu sensus, untuk apa uji statistik?**
Kelompok Strube memang sensus atas latihan dalam buku itu, dan BAB III sekarang menyatakannya. Uji statistik memperlakukan melodi-melodi itu sebagai wakil soal latihan harmonisasi melodi dalam buku ajar harmoni. Karena itu generalisasi di luar buku Strube dinyatakan secara terbatas.
*Rawan bila:* penguji menilai generalisasi ini lemah. Akui. Klaim yang aman adalah tentang latihan Strube dan soal sejenis, bukan semua soal harmonisasi.

**91. Laju dihitung per birama. Birama 3/4 lebih pendek daripada 4/4. Kalau kedua kelompok berbeda komposisi biramanya, perbedaan laju bisa berasal dari birama, bukan dari asal melodi.**
Birama dicatat sebagai ciri melodi, dan jumlah kesempatan (gerak atau peristiwa bunyi yang diperiksa) disimpan untuk setiap kaidah.
*Rawan bila:* ditanya analisis apa yang menangani hal ini. Rencana analisis belum memuatnya. Usulan: tambahkan laju per kesempatan atau per ketukan sebagai analisis kepekaan, dan laporkan komposisi birama kedua kelompok. Putuskan sebelum protokol dibekukan.

**92. Jarak dan persilangan dihitung pada setiap peristiwa bunyi. Nada yang ditahan dihitung sekali, sedangkan nada yang diulang dihitung lagi. Coconet tidak dapat mengulang nada. Bukankah laju jarak dan persilangan Coconet menjadi lebih rendah karena cara pengukuran?**
Benar, dan ini ditemukan saat audit 3 Oktober 2026. Dalam `evaluate_grids` (`research/voice_leading_v2.py`), jarak dan persilangan dihitung pada setiap peristiwa bunyi pasangan suara. Nada yang diulang pada keluaran DeepBach atau Bach menambah peristiwa, sedangkan pada Coconet nada itu digabung. Kuint, oktaf, dan tumpang tindih tidak terpengaruh, karena nada yang diulang tidak mengubah tinggi nada.
*Wajib diputuskan sebelum pilot:* pilihan paling sederhana adalah menggabungkan nada sama yang berurutan pada alto, tenor, dan bas untuk semua keluaran (DeepBach, Coconet, dan Bach) sebelum diukur, sehingga ketiganya diperlakukan sama. Pilihan lain adalah menghitung satu kejadian untuk setiap rentang jarak atau persilangan yang tidak terputus. Keduanya mengubah definisi, sehingga menjadi instrumen versi 3; hasil versi 2 disimpan.

**93. Batas efisiensi 0,864 dari Hodges dan Lehmann berlaku untuk distribusi kontinu. Data Anda banyak bernilai nol.**
Benar. BAB III sekarang menyatakan bahwa angka 30 melodi adalah perkiraan minimum dan bahwa ukuran efek terkecil yang dapat dideteksi dilaporkan berdasarkan jumlah melodi yang benar-benar dianalisis. Rata-rata lima generasi mengurangi nilai yang persis sama, tetapi kaidah yang jarang terjadi, seperti persilangan di atas sopran, tetap dapat banyak bernilai nol.

**94. Dengan koreksi Holm atas lima kaidah, ambang terkecil menjadi 0,01. Apakah 30 melodi masih cukup?**
Untuk efek d = 0,8 dengan daya 0,8, uji t dua arah pada α = 0,01 memerlukan 38,2 melodi per kelompok, atau 44,2 setelah dibagi 0,864. Pada uji satu arah, angkanya 32,8 dan 37,9. Dengan 30 melodi per kelompok, efek terkecil yang terdeteksi pada α = 0,01 sekitar d = 0,98 (dihitung dengan statsmodels pada 3 Oktober 2026). Jadi 30 melodi cukup untuk pengujian pertama pada urutan Holm hanya bila efeknya sangat besar. Jika kelompok Strube yang layak lebih dari 30, semuanya dipakai, dan itu menaikkan daya.

**95. Mann–Whitney sebenarnya menguji apa? Median?**
Uji ini memeriksa apakah nilai dari satu kelompok cenderung lebih besar daripada nilai dari kelompok lain. Uji ini menjadi uji median hanya bila bentuk kedua distribusi sama. Karena itu median, rentang antarkuartil, dan korelasi peringkat biserial dilaporkan bersama nilai p.

**96. Di diagram alur ada keputusan "Apakah valid?". Kapan instrumen dinyatakan tidak valid?**
Langkah 2: setiap ketidaksesuaian dengan contoh cetak Strube harus diperbaiki atau dijelaskan sebelum instrumen dipakai. Langkah 3: setiap jenis perbedaan dengan music21 harus dijelaskan dengan perbedaan definisi. Langkah 4: selisih dengan angka Huang harus dapat dijelaskan.
*Rawan bila:* ditanya angka Bach Anda. Dengan definisi Strube, lajunya 0,0078 kuint dan 0,0030 oktaf per birama, sedangkan Huang melaporkan 0,023 dan 0,009. Dengan definisi music21, lajunya 0,0176 dan 0,0059. Sisa selisihnya baru dijelaskan sebagai kemungkinan (versi data dan pengaturan yang tidak diterbitkan). Tetapkan di protokol apa yang dianggap "dapat dijelaskan" sebelum pilot.

**97. Apakah melodi yang dipakai saat uji coba dipakai lagi dalam data utama?**
Protokol memisahkan hasil uji coba dari data utama, tetapi belum menetapkan apakah melodinya boleh dipakai lagi.
*Rawan bila:* belum diputuskan. Usulan: catat melodi uji coba; jika dipakai lagi, harmonisasi data utama dihasilkan ulang dan keluaran uji coba tidak masuk analisis.

**98. Paradigma penelitian Anda apa?**
Pendekatan kuantitatif yang menguji hipotesis secara deduktif dari teori (BAB III Metode Pendekatan, Creswell dan Creswell). Creswell mengaitkan pendekatan kuantitatif dengan pandangan pascapositivis.
*Rawan bila:* diminta halamannya. Halaman Creswell belum dicatat di `reading-notes.csv`.

**99. Variabel terikat Anda satu atau lima?**
Satu konstruk, yaitu tingkat kepatuhan, dengan lima indikator. Setiap indikator dianalisis dan diuji terpisah; indeks penalti tertimbang hanya ringkasan tambahan (BAB III Variabel Penelitian).

**100. Kenapa memakai kata "pengaruh" padahal analisisnya bukan regresi?**
Dalam pertanyaan ketiga, peneliti menentukan masukan yang diberikan kepada model yang sama, lalu membandingkan keluaran pada dua kondisi masukan. Pengaruh di sini adalah perbedaan keluaran akibat kondisi masukan, diuji dengan perbandingan dua kelompok (Mann–Whitney), bukan dengan koefisien regresi. Bentuk pertanyaan ini mengikuti catatan F06.

### Konsistensi naskah

**101. Rumus tumpang tindih mensyaratkan tidak ada suara yang melangkah. Bagaimana jika satu suara menahan nada?**
Suara yang menahan nada tidak bergerak, sehingga tidak dihitung melangkah. Jika suara bawah naik melewati nada suara atas yang ditahan, kedua suara bersilangan pada peristiwa baru, sehingga gerak itu tidak dihitung sebagai tumpang tindih. Gerak itu dihitung sebagai persilangan hanya bila melibatkan sopran. Persilangan alto dan tenor tidak dihitung sama sekali, sesuai Strube hlm. 174.

### Pertanyaan yang pasti muncul setelah BAB IV ditulis

Belum dapat dijawab karena data utama belum ada. Siapkan jawabannya dari data, bukan dari dugaan:

- Kaidah mana yang paling sering dilanggar setiap model, dan seberapa jauh dari acuan Bach?
- Apakah hasil Coconet pada melodi Bach mendekati angka Huang untuk Coconet (0,365 dan 0,391 per birama)? Jika jauh berbeda, kenapa?
- Berapa melodi yang gagal diproses atau gagal kontrol kualitas pada setiap model dan asal melodi, dan apakah kegagalan itu berkaitan dengan asal melodi?
- Tunjukkan satu contoh penandaan di partitur. Apakah secara musikal itu memang kesalahan?
- Apa yang harus dilakukan pengajar harmoni dengan temuan ini?

## Cara berlatih

1. Ucapkan kalimat pegangan dan jawaban 1, 6, 7, 14, 16a, 24, 28, 33, dan 52 tanpa membaca. Sebelum bimbingan dengan Pembimbing I, pelajari [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md) dan bagian J.
2. Minta teman bertanya acak dari daftar ini dan memotong jawaban yang lebih dari satu menit.
3. Setelah setiap celah di tabel atas ditutup, perbarui jawaban yang terkait dan hapus tanda **Wajib ditutup**.
