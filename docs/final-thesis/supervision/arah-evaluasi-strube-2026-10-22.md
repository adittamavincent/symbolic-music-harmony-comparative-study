# Arah penelitian: keluaran AI, evaluasi kontekstual, dan posisi Strube

22 Oktober 2026. Bahan audit: dua konteks percakapan v5 yang dilampirkan peneliti, sumber primer model, dokumentasi/kode music21, dan halaman buku Strube. Peneliti meminta arah ditentukan menurut alasan ilmiah dan kelayakan terkuat. Dokumen ini merupakan rekomendasi konseptual; naskah, protokol, jumlah kasus dan jumlah percobaan belum dimigrasikan. Pernyataan pada percakapan tempelan tidak diperlakukan sebagai fakta sebelum diperiksa.

## 1. Rekomendasi yang dipilih

Pertahankan satu model **Coconet** untuk tugas harmonisasi sopran tetap. Arahkan pertanyaan pada **kesesuaian kontekstual gerak suara keluaran AI menurut pedoman Strube**. Gunakan beberapa melodi dengan sumber lengkap dan terbaca bila hendak membahas variasi konteks antarmelodi. Jumlahnya ditetapkan dari cakupan kondisi musikal dan kemampuan anotasi; audit ini tidak menetapkan angka baru.

Pilihan ini mengikuti kesesuaian tugas dan kesiapan bahan yang sudah tersedia. Penggantian ke NotaGen-X belum mempunyai alasan kelayakan yang lebih kuat untuk mempertahankan sopran yang sama. Kebaruan usia model tidak menyelesaikan masalah pengendalian masukan, pemetaan SATB, atau dasar keputusan musikal. Coconet juga mempunyai preseden masalah gerak sejajar pada penelitian Bach Doodle; kontribusi kita harus lebih khusus daripada mengulangi temuan keberadaan P5/P8.

MODEL 285 tidak perlu menjadi syarat mutlak penelitian. Sumbernya masih belum lengkap. Jika salinan jelas diperoleh, contoh itu dapat menjadi salah satu bahan kajian dengan status asal-usul yang diverifikasi. Jika tidak, pilih melodi lain dari sumber SATB yang dapat ditelusuri, sebelum melihat hasil generasi. Strube dapat menjadi pedoman meskipun seluruh melodi tidak diambil dari bukunya.

Usulan judul kerja: **Evaluasi Kontekstual Gerak Suara Harmonisasi Coconet Berdasarkan Pedoman Strube**.

Usulan pertanyaan penelitian:

1. Bagaimana profil kesesuaian gerak suara harmonisasi Coconet pada melodi yang ditetapkan menurut kriteria Strube beserta syarat dan pengecualiannya?
2. Bagaimana konteks harmoni, gerak melodis dan posisi frasa menjelaskan keputusan atas pola yang terdeteksi serta pengulangannya antarkeluaran?

Hitungan kategori, proporsi dan durasi menjadi hasil kuantitatif deskriptif; contoh partitur dan alasan keputusan menjelaskan dasar pengukurannya. Perubahan dari tanda otomatis ke keputusan kontekstual dapat diringkas pada unit yang sama. Selisih itu merupakan akibat penerapan definisi penilaian, bukan otomatis bukti bahwa penilai atau program lebih benar; ketepatannya memerlukan sumber dan pemeriksaan independen. Tidak diperlukan klaim sebab-akibat arsitektur.

## 2. Koreksi terhadap konteks tempelan

| Klaim atau saran dalam konteks | Hasil audit dan akibat untuk rancangan |
| --- | --- |
| music21 hanya mempunyai pemeriksaan paralel kuint dan oktaf | Tidak benar. `VoiceLeadingQuartet` juga mempunyai `voiceOverlap`, `voiceCrossing`, `hiddenFifth`, `hiddenOctave`, dan informasi interval melodis. Keberadaan fungsi tersebut juga diperiksa secara statis pada instalasi lokal 9.3.0. |
| Acuan cetak bersih dan AI menyimpang membuktikan cacat arsitektur | Kesimpulan kausal tersebut tidak didukung. Data, representasi, masukan, sampling dan pipeline juga dapat berpengaruh. Acuan hanya memberi perbandingan praktik pada kondisi yang dijelaskan. |
| NotaGen belum mendapat evaluasi musik karena pembuatnya orang ilmu komputer | Afiliasi tim mencakup Central Conservatory of Music; artikel melaporkan penilaian dari perguruan tinggi musik. Latar disiplin masing-masing orang tidak dapat disimpulkan hanya dari afiliasi. Kontribusi kita harus ditunjukkan dari bukti yang ditambahkan. |
| Evaluasi NotaGen hanya kemiripan gaya atau uji dengar | Artikel memuat beberapa metrik dan uji preferensi; ketepatan kontrapung juga disebut dalam pertimbangan penilaian. Celah yang mungkin ialah anotasi rinci berbasis sumber pada kejadian tertentu, bukan ketiadaan seluruh evaluasi teori musik. |
| Tidak ada penalti Strube eksplisit berarti model tidak belajar kaidah | Tidak mengikuti secara logis. Model dapat mempelajari keteraturan dari data tanpa aturan eksplisit. Yang perlu diperiksa ialah keluaran, bukan menebak seluruh pengetahuan internalnya. |
| Transparansi lembar keputusan menggantikan kesepakatan antarpenilai | Transparansi membantu audit, tetapi tidak mengukur kesepakatan dua penilai. Pembacaan ulang oleh orang yang sama tetap berbeda dari penilaian independen. |
| Ejaan dengan accidental paling sedikit membuat analisis bebas bias | Ejaan demikian merupakan pilihan editorial dan dapat salah pada modulasi atau akor kromatis. Gunakan ejaan sumber bila tersedia; jika diinferensikan, catat dasar, alternatif yang masuk akal, dan ketidakpastian. |
| NotaGen-X memerlukan sedikitnya 24 GB untuk semua inferensi | Klaim batas universal itu tidak terbukti. README resmi menyebut penerapan lokal dapat memerlukan 8 GB pada konfigurasinya. Kebutuhan perangkat tetap harus diperiksa pada checkpoint dan pipeline aktual. |
| Model paling baru otomatis paling tepat untuk skripsi ini | Tidak ada hubungan otomatis. Daftar model baru pada tempelan belum semuanya diverifikasi; daftar itu tidak dipakai sebagai dasar memilih model atau menyatakan yang paling baru di seluruh bidang. |

## 3. Strube: waktu, konteks, dan pertanyaan yang dapat dijawab

Sumber lokal adalah *The Theory and Use of Chords: A Text-Book of Harmony*. Halaman judul mengaitkan Gustav Strube dengan Peabody Conservatory of Music; halaman hak cipta menyebut 1928. Preface bertanggal Baltimore, Januari 1928, dan menyebut mahasiswa konservatori sebagai pembaca utama. Ini buku pedagogi harmoni awal abad ke-20, bukan teori yang ditulis pada masa hidup Bach.

Preface menyatakan bahwa penulisan harmoni mengikuti penggunaan dan cita rasa, menekankan fungsi akor dalam lingkungan musikalnya, dan mengakui perlunya pertimbangan pengajar pada kasus meragukan. Jadi, mengubah seluruh buku menjadi daftar Boolean universal justru menghilangkan bagian penalarannya. Sumber gambar: [judul](../../../references/ocr/english/source-pages/002.jpg), [hak cipta](../../../references/ocr/english/source-pages/003.jpg), [Preface](../../../references/ocr/english/source-pages/005.jpg).

Pada hlm. 174, bab harmonisasi chorale membicarakan pilihan akor, kadens, perubahan modus dan persilangan. Persilangan suara bawah dapat diterima sesekali jika memperbaiki gerak suara, dengan batas tidak melewati sopran. Ini alasan konkret untuk membedakan keberadaan persilangan dari keputusan bahwa persilangan menyimpang. [Sumber bab chorale](../../../references/ocr/english/source-pages/136.jpg).

Posisi Strube yang dapat dipertahankan adalah **kerangka normatif pedagogis untuk penulisan tonal dalam konteks yang dinyatakan**. Penilaian menghasilkan kesesuaian terhadap kriteria terpilih itu. Hasilnya tidak langsung mengukur keindahan, keaslian gaya Bach, seluruh mutu musik, kemampuan belajar mahasiswa, atau kepatuhan terhadap semua tradisi musik.

Alasan memilih Strube adalah keterlacakan pedoman, contoh dan pengecualiannya, serta bab yang langsung membahas chorale. Audit ini belum membuktikan Strube lebih unggul daripada Piston, Aldwell–Schachter atau buku lain. Penggunaannya sebagai pedoman resmi kelas/prodi juga memerlukan bukti setempat. Jika alasan pemilihannya hanya usia buku, ketersediaan PDF, atau kemudahan membuat tujuh pemeriksaan, alasan itu belum cukup kuat.

Strube dapat memberi pertanyaan: kapan suatu gerak diterima atau dihindari dalam kerangka pengajarannya? Strube tidak menyediakan jawaban otomatis atas penyebab model menghasilkan gerak tersebut. Kajian perseptual Huron dapat membantu penjelasan teoretis; penelitian tanpa data pendengaran tidak menguji prinsip perseptualnya.

## 4. Tujuh aspek dan apa yang sebenarnya tersedia di music21

Tujuh aspek berikut adalah pengelompokan penelitian dari beberapa bagian buku, bukan tujuh hukum yang oleh Strube diterbitkan sebagai satu instrumen berskala tunggal. Pemetaan sumber tetap mengikuti [inventaris kaidah](../study/peta-kaidah-gerak-suara-strube.md).

| Aspek | Bahan yang tersedia di music21 | Pekerjaan musikal yang tetap diperlukan |
| --- | --- | --- |
| Kuint sejajar | `parallelFifth`, interval vertikal dan gerak | Bedakan definisi gerak, ejaan, fungsi dan pengecualian; detektor lokal menerima parallel dan antiparallel, sehingga tidak sama dengan semua keputusan Strube |
| Oktaf/unisono sejajar | `parallelOctave`, `parallelUnisonOrOctave` | Bedakan nada ditahan, gerak, konteks dan rentang struktural |
| Overlap | `voiceOverlap` | Pola overlap belum menentukan penerimaan pada kondisi langkah/lompatan dan tahap kaidah |
| Jarak suara atas | Objek nada/interval; `figuredBass.possibility.upperPartsWithinLimit` | Fungsi figured-bass membatasi rentang seluruh suara atas; tidak identik dengan jarak S–A dan A–T. Syarat sesekali/sementara juga memerlukan keputusan kontekstual |
| Persilangan | `voiceCrossing` | Identitas suara, pengecualian suara bawah dan larangan melewati sopran |
| Gerak melodis | Interval horizontal dan data nada/waktu | Menafsirkan alur, lompatan dan kelanjutan; bukan larangan universal bagi semua lompatan |
| Kuint/oktaf tersembunyi | `hiddenFifth`, `hiddenOctave` | Dokumentasi sendiri membedakan pencarian seluruh hidden interval dari subset yang dilarang dalam suatu gaya |

Dokumentasi publik yang diperiksa kini dapat berbeda API dari instalasi penelitian 9.3.0. Implementasi harus dipatok ke versi aktual dan tidak menyalin panggilan versi baru tanpa pemeriksaan. Audit kali ini hanya membaca kode; fungsi detektor tidak dijalankan.

Kontribusi teknis yang mungkin adalah ekstensi di luar inti music21 untuk menyimpan sumber kaidah, konfigurasi kerangka, kandidat, keputusan, alasan dan ketidakpastian. Primitif yang sudah ada digunakan kembali. Tidak ada dasar untuk mengklaim tujuh detektor baru yang sebelumnya tidak dimiliki music21.

Panduan kontributor music21 menyarankan fitur khusus hidup sebagai proyek yang mengimpor dan memperluas pustaka, sedangkan fitur besar perlu dibahas. Sumbangan ke inti dapat berupa koreksi yang benar-benar umum, dokumentasi atau kasus batas yang terbukti. Penerimaan upstream adalah keputusan pengelola, bukan syarat kelulusan penelitian. Audit ini tidak membuka issue atau menghubungi pengelola.

## 5. NotaGen dan perubahan tugas

Artikel terbit NotaGen ada pada IJCAI 2025, hlm. 10207–10215. Paper, bobot dan kode harus dibedakan dari varian NotaGen-X pada repositori. Deskripsi pelatihan/evaluasi paper tidak boleh langsung dinyatakan sebagai hasil ukur ulang NotaGen-X.

Sumber resmi menunjukkan pengondisian periode–komponis–instrumentasi dan keluaran notasi ABC. Kode Gradio yang diperiksa menerima tiga label tersebut, bukan kontrak masker sopran tetap. Tag `[V:]` menyimpan bagian, tetapi tidak menjamin jumlah bagian empat, monofoni tiap suara, identitas SATB, atau jenis penulisan chorale. Label `Choral` berarti musik paduan suara dalam pengelompokan sumber, sehingga kelayakan SATB harus diperiksa sebelum kaidah khusus SATB diterapkan.

Kemampuan menghasilkan empat bagian berbeda dari kemampuan mempertahankan seluruh sopran masukan sepanjang karya. Memasukkan awal melodi sebagai prefix juga belum membuktikan kemampuan yang kedua. Audit ini tidak menyatakan conditioning sopran mustahil dikembangkan; audit ini belum menemukan jaminan tugas tersebut pada antarmuka resmi yang diperiksa.

Jika prioritas penelitian berubah menjadi NotaGen-X, tugas yang sesuai untuk diperiksa lebih dahulu ialah generasi baru dengan prompt yang dipatok, kemudian pelaporan: berapa keluaran benar-benar memenuhi domain SATB, dan bagaimana profil gerak suara pada subset layak. Seluruh keluaran tidak layak tetap dicatat; jangan memilih empat garis yang tampak paling bagus dari tekstur besar atau mengabaikan tingkat kegagalan. Banyak keluaran tidak layak dapat membuat rancangan evaluasi SATB tidak praktis. Semua itu memerlukan pilot yang belum dilakukan.

Dengan demikian, NotaGen bukan pengganti langsung Coconet dalam metode sekarang. Untuk prioritas alasan ilmiah dan kelayakan, pilihan tetap Coconet pada tugas sopran tetap. Empat suara S/A/T/B merupakan empat bagian satu harmonisasi; empat melodi masukan berarti empat kasus. Keduanya tidak boleh dipertukarkan dalam perhitungan sampel.

## 6. Data latih, korpus acuan dan bukti instrumen

Empat jenis bahan mempunyai peran berbeda:

| Bahan | Pertanyaan yang dijawab | Klaim yang tidak otomatis didukung |
| --- | --- | --- |
| Contoh berlabel pada Strube dan anotasi ahli | Apakah definisi/pencari kandidat/keputusan sesuai contoh dan syarat yang dipilih? | Validitas seluruh buku dari dua contoh; setiap contoh harus dipisahkan menurut fungsi pengembangan/pemeriksaan |
| Korpus praktik manusia yang terverifikasi | Bagaimana pedoman berlaku pada praktik tertulis dalam domain yang cocok? | Semua notasi manusia harus bebas penyimpangan; korpus ini merupakan data latih persis checkpoint |
| Data latih aktual yang teridentifikasi | Apa asal-usul dan cakupan materi yang digunakan pengembang? | Peneliti dapat mengisolasi penyebab setiap keluaran tanpa eksperimen tambahan |
| Keluaran model dari percobaan tercatat | Bagaimana profil kesesuaian pada tugas, input dan konfigurasi penelitian? | Keindahan umum, kualitas semua model, kegagalan meniru Bach, atau sebab arsitektural |

Memeriksa korpus manusia dengan instrumen yang sama berguna, tetapi tidak menjadikannya gold standard untuk semua label. Label keputusan ahli beserta sumber lebih tepat menjadi acuan pemeriksaan anotasi. Harmonisasi cetak untuk melodi yang sama merupakan acuan praktik yang cocok, bukan satu-satunya jawaban benar atau kelompok kontrol kausal.

Pada Coconet, korpus SATB publik yang telah diunduh belum dibuktikan identik dengan seluruh data latih checkpoint Magenta.js. Pada NotaGen, artikel terbit menyebut data pre-training internal dan sumber internal dalam fine-tuning. Tanpa daftar karya dan versi yang cukup lengkap, kita tidak dapat menjamin suatu melodi tidak pernah dilihat model. Menguji sampel Bach yang tersedia tidak menutup kekurangan provenance tersebut. Pemeriksaan kemiripan dapat menandai kandidat salinan, tetapi hasil negatif tidak membuktikan bebas paparan data latih.

Karena itu, jangan menyebut desain sebagai pengujian generalisasi ke melodi yang pasti baru jika belum terbukti. Evaluasi terhadap norma eksternal Strube tetap mungkin dilakukan, dengan kesimpulan tentang keluaran yang benar-benar diamati. Ketidakpatuhan terhadap norma eksternal tidak otomatis merupakan kegagalan terhadap tujuan pelatihan model.

## 7. Kontribusi peneliti musik yang layak dituju

Kontribusi utama yang diusulkan adalah **pengetahuan tentang keputusan gerak suara pada keluaran AI dalam kerangka musik yang eksplisit**. Buktinya berupa lokasi partitur, fungsi harmoni, hubungan antarsuara, keputusan, dan alasan yang dapat diuji pembaca lain. Pengetahuan tersebut tetap bernilai ketika model dan perangkat lunak berubah, sepanjang domain dan batas penerapannya jelas.

Luaran pendukung yang dapat disiapkan ialah korpus anotasi dengan provenance sumber, contoh yang diterima dan menyimpang, kasus belum pasti, catatan ketidaksepakatan penilai serta versi rubrik. Keterbukaan data mengikuti hak sumber; hak atas buku/edisi/gambar/korporus tidak dianggap seragam. Ekstensi music21 membantu mereproduksi data dan keputusan, tetapi menerjemahkan tujuh rumus yang sudah tersedia bukan kontribusi ilmiah dengan sendirinya.

Di antara sumber primer yang diperiksa, terdapat alasan untuk mengeksplorasi anotasi kontekstual berbasis Strube sebagai tambahan jenis bukti. Audit ini belum membuktikan belum pernah ada penelitian serupa di seluruh literatur. Penambahan label Strube dan penggunaan model baru saja menghasilkan kebaruan yang lemah; kekuatannya harus datang dari cakupan kondisi, mutu anotasi dan temuan musikal aktual.

Jika seluruh penelitian hanya menghasilkan daftar P5/P8 tanpa menambah keputusan kontekstual atau bukti baru yang dapat ditelusuri, kontribusinya akan sangat terbatas karena masalah itu sudah dilaporkan pada Coconet. Tidak ada alasan untuk menjanjikan temuan yang lebih kuat sebelum data diperiksa.

## 8. Rancangan pelaksanaan yang lebih terarah

1. Tetapkan domain harmonisasi tonal empat suara, satu model/checkpoint, dan tugas sopran tetap. Tentukan rentang kasus serta klaim yang hendak didukung.
2. Pilih sumber melodi lengkap sebelum generasi. Buat matriks kondisi musikal yang relevan, misalnya keberadaan nada nonakor, batas frasa dan pola kadens. Pilihan kasus mengikuti cakupan tersebut; jangan memilih kasus setelah tahu AI banyak menyimpang.
3. Bekukan rubrik dan sumber halaman. Pertahankan tujuh aspek sebagai peta pemeriksaan, dengan peran berbeda: sebagian menghasilkan keputusan penyimpangan, sebagian profil/konteks. Jangan menyatakan semua aspek sebagai tujuh penalti yang setara atau seluruh aturan Strube.
4. Pisahkan bahan pengembangan instrumen dari bahan pemeriksaan dan data utama. Gunakan penilai independen yang kompeten pada unit yang sama; simpan keputusan awal sebelum diskusi/adjudikasi. Keterlacakan sumber tidak menggantikan bukti kesepakatan.
5. Implementasikan pembacaan nada/waktu dan pencari kandidat sesuai protokol baru; lakukan pemeriksaan instrumen dan pilot tersendiri. Tetapkan jumlah percobaan dan aturan penghentian sebelum data utama. Tidak ada angka sampel baru yang disahkan oleh audit ini.
6. Simpan semua percobaan, output mentah, kegagalan, duplikat, konversi dan keputusan kelayakan. Pada kode NotaGen yang ditinjau, nomor berkas bertambah setelah hasil diproses/disimpan; jumlah berkas bukan penghitung semua usaha generasi. Adapter penelitian kelak harus mencatat usaha yang gagal jika model itu dipakai.
7. Periksa seluruh kesempatan yang masuk penyebut, termasuk yang tidak ditandai program. Gunakan akuntansi C/A/D/U dan penyebut sesuai jenis peristiwa. Pisahkan kasus, generasi dan kejadian bersarang; angka yang digabung tidak otomatis mendukung inferensi lintas melodi.
8. Laporkan profil per kriteria dan masukan, bukan satu skor mutu universal. Jelaskan cuplikan yang memperlihatkan hubungan antara pola, konteks dan keputusan. Manfaat pembelajaran dinyatakan sebagai kemungkinan penggunaan; efektivitas pembelajaran memerlukan penelitian lain.

## 9. Pertanyaan kritis dan batas jawaban

**Mengapa Strube, bukan aturan Bach yang diperoleh dari data?** Kita menguji kesesuaian terhadap pedoman pedagogis yang ditetapkan dan dapat ditelusuri. Keaslian gaya Bach merupakan konstruk lain yang memerlukan instrumen berbeda. Pilihan Strube harus masuk akal untuk domain yang dinilai dan tidak diklaim sebagai norma universal.

**Bukankah norma lama tidak relevan untuk AI baru?** Usia norma tidak menentukan kesesuaian domain. Pedoman tersebut relevan ketika tugas dan penggunaan yang dituju memang penulisan tonal empat suara. Tidak ada dasar menerapkannya sebagai standar seluruh generasi musik kontemporer.

**Apakah kita sekadar membangun evaluator?** Penelitian yang direkomendasikan berpusat pada hasil musik dan keputusan musikalnya. Bila tujuan utama bergeser menjadi membuktikan akurasi/generalitas alat, desain harus ikut berubah menjadi penelitian instrumen, dengan anotasi acuan dan evaluasi kinerja alat yang lebih luas.

**Mengapa tidak segera NotaGen-X?** Belum ada bukti yang cukup bahwa tugas sopran tetap dan keluaran SATB dapat dijaga oleh antarmuka yang ditinjau. Mengganti tugas ke generasi baru mungkin sah, tetapi menambah pertanyaan kelayakan dan menghapus perbandingan pada input melodi yang sama.

**Kalau acuan manusia juga menyimpang, apa penelitian gagal?** Tidak otomatis. Periksa salah transkripsi, salah operasionalisasi, perbedaan domain norma dan pengecualian terlebih dahulu. Setelah itu, laporkan temuan sebagai hubungan praktik dan norma yang teramati, tanpa menyimpulkan penyebab arsitektur.

**Apa yang belum cukup kuat?** Belum ada bukti instrumen kontekstual lengkap, penilaian independen, pilot, data utama, cakupan sampel baru, jaminan ketidakpaparan data latih atau kebaruan universal. Alasan memilih Strube sebagai pedoman terbatas didukung sumber; alasan menjadikannya ukuran seluruh mutu musik tidak didukung. Alasan mengganti model demi usia paling baru juga belum kuat.

## 10. Sumber dan bukti pemeriksaan

- Strube (1928): halaman judul, hak cipta dan Preface diperiksa kembali secara visual; hlm. 174–175 untuk bab chorale. [Peta sumber](../study/peta-kaidah-gerak-suara-strube.md) menyimpan detail kondisi lain. Ini pembacaan asisten, bukan konfirmasi pembacaan peneliti.
- [NotaGen, IJCAI 2025](https://www.ijcai.org/proceedings/2025/1134), [PDF terbit](https://www.ijcai.org/proceedings/2025/1134.pdf): §3.1/3.3 dan §4–5. Paper terbit diperiksa karena keterangan data pre-training lebih spesifik daripada ringkasan preprint.
- [Repositori resmi NotaGen](https://github.com/ElectricAlexis/NotaGen/tree/4553cd743b6b449732baf2a6cc58885fe853b11d), commit `4553cd743b6b449732baf2a6cc58885fe853b11d`: README, konfigurasi dan dua antarmuka inferensi, serta daftar prompt diunduh untuk pembacaan statis. Bobot NotaGen tidak diunduh atau dijalankan.
- [Dokumentasi voiceLeading](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html), [figuredBass.checker](https://music21.org/music21docs/moduleReference/moduleFiguredBassChecker.html), [panduan kontributor](https://music21.org/music21docs/developerReference/developerGuidelines.html): fungsi deteksi berbeda dari penerapan seluruh norma Strube. Kode 9.3.0 yang terpasang diperiksa secara statis untuk memastikan fungsi tidak hanya ada pada dokumentasi versi baru.
- [Huang dkk. (2019), §6.3](https://arxiv.org/html/1907.06637v1): preseden Coconet dan pengecualian P5/P8 yang sudah dicatat dalam reading-notes; bukan temuan penelitian ini.

Rencana OpenAlex diperbarui sebelum seluruh 41 kueri dijalankan. Batch `20261022T073501326746Z-batch` selesai dengan 791 karya unik. Q37 menemukan rekaman IJCAI 2025 yang dikonfirmasi pada penerbit, tetapi juga metadata tahun/rekaman lain yang tidak otomatis benar. Rekaman berjudul NotaGen2 tidak dikonfirmasi sebagai rilis resmi dan tidak digunakan. Q40 tanpa hasil tidak membuktikan NotaGen-X tidak ada; varian tersebut diperiksa langsung di repositori resmi. Hasil pencarian bukan bukti bahwa celah literatur sudah tertutup atau kebaruan telah terbukti.

Snapshot sumber, hash dan catatan pembacaan statis disimpan pada `research/outputs/source-audit-2026-10-22/`. Folder proyek berpindah selama sesi ke `projects/isi-yogyakarta/symbolic-music-harmony-comparative-study`; audit melanjutkan pada lokasi yang telah ditemukan dan tidak melakukan pemindahan tersebut. Path historis pada manifest lama dipertahankan sebagai provenance.

### Perubahan dari usulan sebelumnya

Rekomendasi tetap satu Coconet, tetapi mengurangi ketergantungan pada MODEL 285 dan mengusulkan cakupan beberapa masukan yang dipilih menurut kondisi musikal. Kontribusi dipusatkan pada analisis keluaran dan anotasi yang dapat diperiksa; ekstensi pustaka menjadi luaran pendukung. Ini belum merupakan revisi naskah, protokol baru yang dibekukan, atau bukti hasil penelitian.
