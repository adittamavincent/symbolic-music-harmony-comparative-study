# Adaptasi evaluasi harmonisasi Yan dkk.

Tanggal: 1 Oktober 2026. Catatan eksplorasi untuk menentukan metode v3. Desain, jumlah sampel, pemeriksa, dan pemilihan model di bawah merupakan usulan. Belum ada perubahan pada instrumen aktif atau bukti generasi model baru.

## Rekomendasi

Gunakan Yan dkk. sebagai acuan utama desain evaluasi dan pemilihan kategori. Mulai dengan pemeriksaan partitur oleh manusia, dengan seluruh 11 kategori sebagai daftar kandidat. Program dapat membantu menemukan lokasi kejadian, tetapi hasilnya diperiksa manusia sampai ketepatan deteksinya terbukti. Menilai hasil musik AI tidak mengharuskan peneliti mengembangkan seluruh pemeriksaan secara otomatis.

Jika prioritasnya mempertahankan rubrik sumber sedekat mungkin, pilih harmonisasi bas tetap. Jika prioritasnya membandingkan model harmonisasi melodi termasuk Transformer yang lebih baru, pilih sopran tetap dan nyatakan perubahan cakupan rubrik. Ketersediaan tugas pada checkpoint yang benar-benar dipakai menentukan model akhir.

## Sumber utama dan lokasi bukti

[Yan, Lustig, VanderStel, dan Duan (2018), ISMIR, hlm. 204–210](https://labsites.rochester.edu/air/publications/Yan2018partInvariant.pdf), §4.2: tiga soal bas dengan tingkat kromatisme berbeda; 30 keluaran model per soal, dibandingkan dengan jawaban 27 mahasiswa. Tiga pemeriksa partitur dan tiga pendengar berbeda menilai secara buta dengan urutan acak. Catatan kaki 5 menghubungkan dua soal dengan latihan Laitz; catatan kaki 6 menjelaskan asal pedagogis rubrik. Korelasi skor antarpemeriksa dilaporkan, bukan bukti validitas instrumen otomatis kita.

[Suplemen penulis, bagian Rubrics For Objective Evaluation](https://labsites.rochester.edu/air/projects/model0.md) memuat kategori dan bobot. Terjemahan serta pemetaan kategori ada di [yan-rubric-mapping-2026-10-01.csv](yan-rubric-mapping-2026-10-01.csv). Paralel kuint/oktaf merupakan satu kategori sumber; memisahkannya untuk laporan adalah adaptasi. Indikator lama merujuk pada sebagian kategori 3 dan 5, bukan tiga kategori terpisah yang ditetapkan sumber.

Rubrik ini memiliki preseden publikasi, tetapi tidak boleh disebut instrumen Strube atau skala yang berlaku universal. Sumber belum menyediakan seluruh keputusan operasional yang diperlukan program, seperti unit penghitungan, durasi toleransi resolusi, serta penanganan semua pengecualian. Buku Laitz belum diperiksa pada latihan aslinya; rujukan latihan dalam makalah tidak membuktikan seluruh kategori rubrik diambil dari halaman tertentu buku itu.

## Dua desain utama

| Pilihan | Tugas | Keuntungan | Penyesuaian yang diperlukan |
| --- | --- | --- | --- |
| A: mengikuti tugas bas | Bas yang sama diberikan kepada semua model; model menghasilkan S–A–T | Menjaga hubungan tugas dan rubrik sumber; sopran hasil AI dapat menjadi objek pemeriksaan | Adapter bas tetap, verifikasi kendali, soal yang sesuai model, dan checkpoint dengan kemampuan tersebut |
| B: mengikuti tugas melodi | Sopran yang sama diberikan kepada semua model; model menghasilkan A–T–B | Lebih dekat dengan adapter lama dan kandidat harmonisasi melodi baru | Resolusi sopran menjadi karakteristik soal; semua kategori perlu diaudit menurut kontribusi suara hasil AI |

Kedua pilihan membaca SATB lengkap. Suara tetap menjadi konteks untuk menilai jawaban. Kejadian yang seluruh unsur relevannya berasal dari suara tetap dipisahkan dari hasil evaluasi kontribusi AI. Ini usulan adaptasi kita; jangan diatribusikan sebagai prosedur eksplisit Yan.

Jangan mencampur hasil A dan B ke satu skor yang seolah memiliki tugas dan peluang kesalahan identik. Penambahan bas tetap pada tugas sopran tetap juga mengurangi kebebasan jawaban. Hitungan mentah dan jenis kejadian yang dapat dinilai perlu diperiksa sebelum menyimpulkan pengaruh tingkat kendali.

## Model dan kelayakan yang sudah diperiksa

| Sistem | Bukti sumber | Implikasi untuk desain | Batas verifikasi |
| --- | --- | --- | --- |
| DeepBach | [Makalah](https://proceedings.mlr.press/v70/hadjeres17a/hadjeres17a.pdf), §2.3.2: pemilihan posisi/suara untuk dihasilkan | Kandidat A dan B; model SATB dengan kendali sebagian suara | Adapter lokal baru memiliki tugas sopran dan sopran+bas; adapter bas saja belum dibuat atau dijalankan |
| Coconet | [Makalah](https://archives.ismir.net/ismir2017/paper/000187.pdf), §1 dan §3: melengkapi partitur parsial | Kandidat A dan B melalui mask/masukan yang sesuai | Perilaku implementasi/checkpoint lokal dan pelestarian bas belum diuji |
| NotaGen/NotaGen-X | [Repositori resmi](https://github.com/ElectricAlexis/NotaGen): kendali periode, komponis, instrumentasi | Belum memenuhi syarat tugas soal suara tetap dalam adapter sekarang | Ketiadaan bukti pada antarmuka yang diperiksa tidak membuktikan model mustahil diadaptasi; adaptasi akan menjadi sistem baru yang harus diuji |
| DeepChoir | [Makalah ICASSP 2023](https://arxiv.org/pdf/2202.08423), §2.2; [kode dan berkas bobot](https://github.com/sander-wood/deepchoir) | Kandidat B yang memakai melodi dan akor; encoder Bi-LSTM | Bukan pengganti Transformer; tidak diasumsikan mendukung bas tetap; kendali akor harus dibedakan dari tugas melodi saja; dependensi lama belum dijalankan |
| AMT pada AI Harmonizer | [Makalah NIME 2025](https://nime.org/proceedings/2025/nime2025_84.pdf), §2.2; [kode resmi](https://github.com/mitmedialab/ai-harmonizer-nime2025); [checkpoint SATB](https://huggingface.co/mitmedialab/jsbChorales-1000) | Kandidat Transformer untuk B dengan masukan simbolik langsung | Kode/bobot tersedia menurut sumber, belum diunduh atau dijalankan. Prosedur paper membatasi timing suara pendamping mengikuti melodi; pembatasan ini bagian dari pipeline pembanding |

AI Harmonizer mencantumkan Yan sebagai referensi [24]. Bagian hasilnya berfokus pada waktu inferensi, sehingga belum memberi pemeriksaan kaidah melalui rubrik yang kita usulkan. Ini peluang pengembangan yang terlihat pada makalah tersebut, bukan bukti bahwa tidak ada penelitian lain yang pernah melakukannya. [Makalah asli](https://nime.org/proceedings/2025/nime2025_84.pdf).

Untuk kandidat AMT, periksa versi submodule dan checkpoint, pemetaan instrument ke suara, keluaran timing, pengaruh pembatasan decoding, dan kemampuan menghasilkan berkas simbolik yang dapat diperiksa. Hindari memasukkan transkripsi vokal atau sintesis suara ke pertanyaan penelitian jika objeknya musik simbolik.

## Instrumen dan penghitungan yang diusulkan

Mulai dari daftar lengkap kategori sumber. Untuk tiap kategori, tulis contoh, pengecualian, kejadian yang dihitung, serta alasan jika tidak diterapkan. Kategori yang tidak dapat diputuskan dicatat sebagai tidak dapat dinilai, bukan nol kesalahan. Daftar kategori hasil adaptasi ditetapkan sebelum data utama dikumpulkan.

Dalam skema usulan, simpan jumlah kejadian setiap kategori terlebih dahulu. Jika bobot sumber diadopsi, skor penalti dapat ditulis sebagai jumlah negatif tertimbang. Perubahan menjadi jumlah penalti positif hanya membalik arah tanda dan harus dijelaskan. Jangan menambahkan pemotongan skor ke nol atau menyebutnya persentase kepatuhan. Kesamaan bobot tidak membuktikan bahwa jumlah kesalahan, unit penghitungan, dan interpretasinya sudah sama.

Hasil utama sebaiknya mencakup profil kesalahan per kategori. Skor agregat menjadi ringkasan tambahan. Dua keluaran dapat memiliki penalti sama dengan masalah musikal berbeda. Perbandingan antaraturan juga tidak boleh menganggap setiap aturan memiliki jumlah kesempatan kejadian yang sama.

Penilaian manusia tetap dapat menghasilkan data kuantitatif: lokasi kejadian, kategori, hitungan, dan penalti. Penjelasan partitur tidak otomatis membuat desain menjadi mixed methods. Evaluasi pendengar dapat ditambahkan jika pertanyaan penelitian mencakup persepsi musikal; pelaksanaannya memerlukan desain tersendiri.

## Pemeriksaan manusia dan program

Usulan praktis adalah dua pemeriksa dengan kompetensi harmoni SATB yang relevan, bekerja independen pada sampel berkode tanpa identitas model. Jumlah dan kualifikasi ini belum diputuskan, bukan ketentuan wajib dari Yan. Pemeriksa ketiga dapat membantu menyelesaikan perbedaan jika tersedia.

Simpan penilaian awal masing-masing sebelum diskusi. Latih penggunaan pedoman pada contoh yang terpisah dari data utama. Catat alasan perbedaan, kemudian laporkan ukuran kesepakatan yang sesuai dengan data dan unit anotasinya. Korelasi tinggi belum menjamin skor sama: dua pemeriksa bisa memberi urutan identik sambil berbeda secara konsisten beberapa poin.

Program boleh menemukan kandidat lokasi paralel, jarak suara, atau persilangan. Penentuan akor, tonalitas lokal, nada non-akor, ejaan nada, dan konteks progresi memerlukan pemeriksaan lebih jauh. MIDI tidak menyimpan ejaan enharmonik seperti notasi sumber. Jangan mengubah ejaan hasil parser menjadi kebenaran musikal tanpa kebijakan yang dicatat.

Jika program hanya mengusulkan lokasi, masukkan juga pemeriksaan bagian tanpa flag untuk mencari kejadian yang terlewat. Jika seluruh hasil utama dinilai manual, ketidaklengkapan otomatisasi tidak menghilangkan hasil penelitian. Jika hasil utama dinilai otomatis, ketepatan detektor perlu dibuktikan terhadap anotasi manusia.

## Kontribusi yang masuk akal

1. Membandingkan profil kesalahan beberapa pipeline harmonisasi pada soal bersama menggunakan rubrik yang memiliki preseden publikasi. Hasil perbandingan ini menjadi kontribusi empiris; klaim kebaruannya tetap memerlukan penelusuran terkait.
2. Menguji model lebih baru yang benar-benar mendukung tugas. DeepBach dan Coconet terbit pada 2017, sehingga mengganti model Yan dengan kedua model itu tidak mendukung klaim model lebih baru.
3. Mengembangkan pedoman anotasi dan pencatatan kejadian yang membuat adaptasi rubrik dapat diperiksa ulang. Ini pengembangan metode, belum instrumen tervalidasi.
4. Menambahkan bantuan komputasional dengan analisis kesalahan terhadap penilaian manusia, jika waktu memungkinkan. Jadikan ini kontribusi tambahan agar penelitian keluaran AI tetap dapat berjalan dengan pemeriksaan manual.

Perbedaan arsitektur dapat menjadi alasan variasi pembanding. Dengan checkpoint, data latih, representasi, dan decoding yang juga berbeda, hasilnya mendukung perbandingan sistem yang diuji; atribusi sebab kepada arsitektur memerlukan desain lain.

## Hubungan dengan Strube

Pilihan paling langsung adalah menjadikan rubrik Yan sebagai acuan instrumen, lalu memakai sumber teori harmoni untuk menjelaskan kategori dan pengecualian. Jika Strube tetap dipakai, setiap hubungan harus ditunjukkan dengan edisi dan halaman yang dibaca. Kolom rujukan Strube dalam tabel pemetaan sengaja belum diisi.

Jangan mempertahankan istilah “Strube Score” untuk penalti rubrik Yan tanpa dasar baru. Jika Strube tidak lagi menentukan definisi dan cakupan instrumen, judul, rumusan masalah, variabel, teori, dan metode perlu diselaraskan. Perubahan ini merupakan keputusan metode v3; proposal historis dipertahankan.

## Rumusan yang dapat dibawa ke pembimbing

Calon pertanyaan utama: “Bagaimana profil kesalahan harmoni dan pergerakan suara pada hasil harmonisasi beberapa model AI berdasarkan adaptasi rubrik Yan dkk.?”

Untuk A, tambahkan “pada tugas harmonisasi bas yang sama”. Untuk B, tambahkan “pada tugas harmonisasi melodi sopran yang sama”. Nama model dimasukkan setelah kelayakan tugas dan checkpoint terbukti.

Objek material: partitur SATB yang dihasilkan model dari soal tertentu. Objek formal: kesalahan harmoni dan pergerakan suara menurut rubrik yang ditetapkan. Faktor pembanding utama: pipeline model/checkpoint. Hasil terukur: kejadian, hitungan tiap kategori, dan penalti agregat. Soal menjadi blok perbandingan; banyak keluaran dari satu soal tidak menambah jumlah soal independen. Pemeriksa merupakan sumber variasi pengukuran, bukan tambahan keluaran musik independen.

Jika fokusnya perbandingan model, tingkat kendali tidak perlu dipaksakan menjadi empat kondisi. Jika pengaruh kendali tetap diteliti, tetapkan intervensi yang nyata dalam masing-masing sistem dan hasil yang dapat dibandingkan. Kromatisme soal dapat menjadi pengelompokan kesulitan, tetapi perlu jumlah soal dan dasar pengelompokan yang mendukung kesimpulan tersebut.

## Urutan migrasi yang diusulkan

1. Tetapkan A atau B setelah pilot kelayakan tugas; pilih checkpoint yang sesuai, tanpa mengganti tugas untuk mengejar tiga nama model.
2. Baca 11 kategori dan contoh penilaian sumber; lengkapi lembar definisi bersama pengajar harmoni. Pisahkan kategori tidak berlaku dari kategori yang belum dapat dinilai.
3. Uji beberapa soal pendek yang berbeda pada setiap kandidat. Catat usaha yang gagal, suara yang dipertahankan, pemetaan suara, timing, dan kelayakan partitur. Jumlah pilot ditentukan untuk memeriksa fungsi, bukan sebagai ukuran sampel utama.
4. Uji pedoman anotasi secara independen; revisi dan bekukan sebelum data utama. Tetapkan soal, pengulangan, analisis, serta beban penilai berdasarkan tujuan dan sumber daya.
5. Selaraskan BAB I–III dan judul dengan desain akhir. Simpan instrumen lama serta hasilnya sebagai versi historis. Perubahan preprocessing atau aturan mewajibkan pengukuran ulang data yang terdampak.

## Jawaban sidang yang perlu disiapkan

- **Asal instrumen:** rubrik diadaptasi dari Yan dkk.; lembar anotasi dan prosedur penerapan disusun peneliti. Program bantuan merupakan implementasi peneliti. Jangan menyatakan evaluator otomatis itu milik Yan.
- **Mengapa kategori tersebut:** daftar awal mengikuti rubrik yang dipublikasikan untuk tugas pedagogis SATB. Setiap pengurangan atau perubahan dicatat menurut domain tugas, sumber teori, dan contoh, sebelum hasil utama dilihat.
- **Mengapa tidak seluruh buku harmoni:** penelitian mengukur konstruk yang dibatasi rubrik. Cakupan instrumen dan kesimpulannya dinyatakan; hasil tidak mewakili kepatuhan terhadap seluruh teori harmoni.
- **Apakah otomatis valid karena dipublikasikan:** publikasi memberi preseden dan jejak sumber; kesesuaian adaptasi, konsistensi pemeriksa, dan ketepatan program tetap perlu diperiksa pada penelitian ini.
- **Apa yang baru:** perbandingan sistem dan profil kesalahan dalam desain yang dicatat. Model lebih baru hanya klaim jika tahun, checkpoint, dan tugasnya mendukung. Kebaruan mutlak belum dibuktikan.
- **Mengapa hasil tidak menjelaskan arsitektur:** data latih dan prosedur generasi ikut berbeda. Kesimpulan mengikuti model/checkpoint/pipeline yang diuji.

## Penelusuran dan batas bukti

Rencana OpenAlex diperluas menjadi 18 query dan seluruhnya dijalankan. Semua gagal karena DNS; tidak ada rekaman yang diperoleh. Manifest: `research/outputs/openalex/20261001T094230522976Z-batch/batch_manifest.json`. Penelusuran web dan hubungan referensi sumber primer dicatat di [yan-exploration-search-2026-10-01.json](yan-exploration-search-2026-10-01.json). Ini penelusuran terarah, bukan tinjauan sistematis.

Metadata Yan diperiksa pada daftar ISMIR dan makalah asli. Metadata AI Harmonizer juga diperiksa pada [rekaman prosiding Zenodo](https://zenodo.org/records/15698966). Makalah Fang, [Bach or Mock?](https://arxiv.org/html/2006.13329v3), diperiksa sebagai alternatif evaluasi otomatis berbasis distribusi fitur; tidak diperlakukan sebagai rubrik Yan atau sebagai studi yang terbukti meneruskan rubrik tersebut. Klaim reuse rubrik dalam studi lain belum terverifikasi.

Hal yang masih harus diperoleh: edisi/halaman teori yang digunakan, pedoman kejadian dan pengecualian, keputusan tugas, hasil pilot nyata, pemeriksa yang tersedia, serta desain sampel utama. Naskah, bibliografi bersama, dan kode evaluator belum dimigrasikan dalam eksplorasi ini.
