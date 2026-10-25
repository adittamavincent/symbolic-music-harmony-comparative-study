# Kandidat kontribusi teknis: stress test dengan bukti kelayakan harmonisasi

22 Oktober 2026. Peneliti kini secara eksplisit meminta titik kontribusi teknis/matematis. Rekomendasi ini memperluas arah analisis keluaran ke perancangan protokol evaluasi. Naskah, instrumen dan protokol yang berjalan belum diubah. Ini kandidat gap yang didukung alasan desain; kebaruan global belum dibuktikan.

## Pilihan yang direkomendasikan

Kembangkan **protokol stress test Coconet dengan masukan sopran yang mempunyai bukti setidaknya satu harmonisasi ATB yang memenuhi kriteria terpilih dari Strube**. Kontribusi teknis berada pada definisi kendala, konstruksi/pemeriksaan bahan uji, akuntansi ketidakpastian dan prosedur statistik. Tetap satu model AI: Coconet dengan sopran tetap.

Judul kerja: *Uji Ketahanan Harmonisasi Coconet dengan Kendala Gerak Suara Strube*.

Pertanyaan utamanya: bagaimana peluang keluaran Coconet memenuhi kriteria yang ditetapkan berubah ketika sopran mengalami perturbasi terukur, pada masukan yang diketahui mempunyai solusi dalam domain penelitian?

Ini lebih terarah daripada menjalankan banyak masukan acak dan menganggap seluruh tanda program sebagai kegagalan musikal. Bila masukan belum diketahui mempunyai solusi, tingginya penyimpangan keluaran belum menjelaskan apakah model gagal pada tugas yang sebenarnya dapat diselesaikan menurut batas tersebut. Ketiadaan bukti solusi juga tidak membuktikan masukan mustahil diharmonisasi.

## Gap dan penelitian terdahulu

| Sumber yang diperiksa | Hal yang sudah ada | Posisi calon penelitian ini |
| --- | --- | --- |
| Huang dkk. (2019), §6.3 | Evaluasi P5/P8 Coconet dan hubungan dengan karakteristik masukan; pengecualian pada korpus juga dibahas | Protokol perturbasi berpasangan dengan bukti solusi menurut kriteria yang ditetapkan dan keputusan Strube yang dapat ditelusuri |
| Dokumentasi music21 | Deteksi pola, informasi interval dan beberapa pemeriksaan kontekstual | Menggunakan fungsi yang cocok dalam spesifikasi evaluasi yang eksplisit, bukan mengklaim seluruh primitif sebagai baru |
| Strasheela dan contoh resminya | Pemodelan teori musik sebagai constraint satisfaction problem (CSP), dengan beberapa kemungkinan solusi | Memanfaatkan gagasan kendala untuk memastikan kelayakan bahan uji; tidak mengklaim CSP musik sebagai penemuan |
| MUSIB (2023), abstrak dan §1–1.1 | Benchmark infilling terstandar, metrik dan persoalan kesesuaian konteks; fokus single-monophonic, multi-monophonic seperti Coconet berada di luar cakupannya | Tugas sopran-ke-ATB serta kesesuaian terhadap kerangka normatif yang dinyatakan |
| Sprockeels dan Van Roy (2025), abstrak penerbit | Formalisasi progresi akor/modulasi dengan constraint programming, terkait proyek Harmoniser dan lapisan voicing | Batas terhadap klaim bahwa formalitas harmoni atau empat suara sendiri merupakan hal baru |
| Lafleur dkk. (2022), abstrak penerbit | Penggabungan reinforcement learning dan constraint programming untuk menghasilkan sekuens yang memperhatikan kendala | Evaluasi terhadap satu checkpoint tetap, tanpa menjadikan pengubahan/pelatihan model sebagai kebutuhan utama |

Rumusan gap yang aman: **pada sumber yang diperiksa, belum teridentifikasi protokol yang persis menguji ketahanan Coconet melalui perturbasi sopran dengan bukti kelayakan menurut operasionalisasi Strube yang dipakai di sini**. Klaim ini belum setara dengan pernyataan bahwa tidak pernah ada penelitian serupa. Teks lengkap dan metode penelitian terdekat tetap harus diperiksa sebelum klaim kebaruan masuk BAB I.

## 1. Formulasi matematis

Misalkan:

- `s` adalah sopran masukan;
- `h=(a,t,b)` adalah harmonisasi ATB;
- `B` adalah domain representasi yang dibekukan: panjang/waktu, rentang nada, pemetaan suara, ketentuan monofoni dan kemampuan masker yang cocok dengan Coconet;
- `R` adalah himpunan kriteria operasional beserta kondisi dan pengecualiannya.

Definisikan himpunan solusi:

\[
\mathcal H_R(s;B)=\{h\in B:R(s,h)=1\}.
\]

`R(s,h)=1` berarti harmonisasi telah dipastikan memenuhi seluruh kriteria yang dimasukkan ke R. Ini tidak menyatakan seluruh musik benar atau seluruh buku Strube telah diukur. Kasus dengan keputusan penting yang belum pasti tidak langsung diberi nilai 1.

Sopran masuk kelompok kelayakan terkonfirmasi bila tersedia satu harmonisasi saksi `w_s` dengan `w_s ∈ H_R(s;B)`. Menyimpan saksi membuat dasar klaim dapat diperiksa. Satu saksi cukup untuk membuktikan himpunan tersebut tidak kosong dalam model formal itu; tidak perlu menemukan semua solusi atau solusi yang paling indah.

Bukti ini bersyarat pada ketepatan R, pemeriksaan saksi dan B. Program yang menggunakan aturan salah dapat menghasilkan klaim kelayakan yang salah secara musikal. Karena itu, kesesuaian dengan sumber dan pemeriksaan ahli tetap diperlukan secara terpisah.

## 2. Cara memperoleh bahan uji

Mulai dengan pasangan SATB lengkap yang telah diperiksa terhadap R, lalu ambil soprannya. Pasangan itu boleh berasal dari sumber manusia yang hak penggunaannya jelas atau dari konstruksi berkendala. Nama Bach tidak otomatis menjamin kepatuhan terhadap R.

Buat versi perturbasi sopran dengan prosedur yang dibekukan. Setiap versi yang dipakai untuk kelompok layak harus mempunyai saksi yang sesuai versinya; saksi dari melodi awal tidak membuktikan kelayakan melodi yang sudah diubah. Saksi ATB dapat berbeda antarkondisi, sedangkan sopran pada setiap panggilan Coconet tetap sama dengan masukan kondisi tersebut.

Solver CSP adalah salah satu cara mencari saksi, tetapi tidak wajib menjadi langkah pertama. Versi yang lebih realistis untuk skripsi ialah kumpulan pasangan yang dibangun dan diverifikasi lebih dahulu. Tidak ditemukannya saksi dalam waktu pencarian bukan bukti ketidaklayakan. Jika memakai solver, pisahkan hasil SAT/ada saksi, UNSAT yang terbukti dalam spesifikasi, dan UNKNOWN/timeout.

Menerima hanya perturbasi yang mempunyai saksi dapat mengubah distribusi bahan uji. Catat seluruh usulan, penerimaan, penolakan/ketidakpastian dan cakupan per tingkat perturbasi. Kesimpulan berlaku pada distribusi konstruksi dan seleksi itu; bukan semua melodi yang mungkin.

## 3. Ukuran stress

Untuk melodi dengan ritme dan jumlah kejadian nada sama, salah satu ukuran yang dapat ditetapkan ialah proporsi posisi nada yang diganti:

\[
\epsilon(s,s')=\frac{\#\{i:p_i(s)\ne p_i(s')\}}{m},
\]

dengan `m` jumlah posisi nada yang memenuhi syarat perubahan. Posisi mana yang boleh diubah, perlakuan nada ditahan/diulang, nada pengganti, register, nada awal–akhir dan distribusi pengacakan harus dijelaskan. Ukuran ini adalah tingkat perubahan menurut prosedur penelitian, bukan ukuran universal kesulitan musikal. Besarnya lompatan dan sifat tonal lain tetap dicatat karena dapat ikut berubah.

Tidak perlu langsung sejuta masukan. Cakupan melodi dasar, tingkat perturbasi dan jumlah pengulangan dipilih menurut pertanyaan, presisi yang dituju serta biaya pemeriksaan. Dua atau tiga tingkat dapat dipertimbangkan untuk pilot; audit ini belum menetapkan jumlah final atau kecukupan sampel.

## 4. Ukuran hasil dan ketidakpastian

Untuk setiap kondisi, catat semua percobaan dan bedakan:

- `G`: keluaran teknis layak yang terkonfirmasi memenuhi R;
- `D`: keluaran teknis layak dengan sedikitnya satu penyimpangan terkonfirmasi;
- `U`: keluaran teknis layak tanpa penyimpangan terkonfirmasi tetapi masih mempunyai keputusan yang menghalangi kepastian memenuhi R;
- `F`: kegagalan teknis atau representasi, termasuk sopran yang tidak dipertahankan.

Dengan `N=G+D+U+F`, keberhasilan end-to-end terkonfirmasi adalah `G/N`. Rentang akibat keputusan yang belum selesai ialah `[G/N,(G+U)/N]` untuk N>0, jika seluruh status teknis sudah dipastikan. Rentang itu bukan interval kepercayaan dan tidak memasukkan kesalahan pengukuran yang belum diketahui.

Untuk membahas kesesuaian musikal di antara keluaran layak, gunakan penyebut `N_T=G+D+U` dan laporkan tingkat kegagalan `F/N` secara terpisah. Jangan menyebut kegagalan teknis sebagai penyimpangan musikal. Kategori pada tingkat keluaran ini merupakan agregasi dari keputusan per kriteria, bukan pengganti akuntansi kesempatan `O=C+A+D+U` pada instrumen yang sudah direncanakan.

Laporkan profil tiap kriteria beserta penyebutnya. Satu keputusan keluaran tidak memberi bobot estetis yang sama kepada setiap jenis penyimpangan; ia hanya menjawab apakah keluaran memenuhi seluruh kriteria R yang dinyatakan.

Jika memakai keputusan belum pasti, mutu evaluator harus dilaporkan bersama cakupan keputusan. Evaluator yang selalu menjawab belum pasti tidak boleh dianggap unggul hanya karena jarang membuat keputusan salah. Selective prediction/reject option sudah dikenal dalam literatur; penerapannya pada evaluator ini merupakan adaptasi, bukan temuan konsep baru. Tidak diperlukan pelatihan SelectiveNet untuk menggunakan prinsip pelaporan tersebut.

## 5. Posisi tujuh aspek Strube

Pertahankan tujuh aspek sebagai inventaris. Setiap aspek harus dipetakan ke sumber, fungsi music21 yang sesuai, syarat, pengecualian, informasi yang diperlukan dan status keterlaksanaan. Jangan memaksakan semua pernyataan pedagogis menjadi kendala keras.

Untuk pembuktian kelayakan, R hanya boleh berisi kriteria yang definisi dan keputusan penerapannya jelas. Syarat seperti sesekali atau gerak yang lebih baik dapat memerlukan anotasi ahli; jika belum bisa diputuskan, klaim kelayakan menurut kriteria itu belum tersedia. Opsi lain ialah mempersempit R secara eksplisit dan tetap melaporkan aspek lainnya sebagai profil. Bukti untuk subset tidak boleh disebut kepatuhan terhadap seluruh Strube.

Urutan sumber tetap: teks dan contoh Strube → operasionalisasi peneliti → penggunaan/penambahan fungsi → keputusan pada data. Penelitian harus bisa menunjukkan kapan program menjalankan sumber dan kapan peneliti membuat pilihan tambahan.

## 6. Bukti kontribusi yang harus dihasilkan

| Luaran | Bukti yang diperlukan |
| --- | --- |
| Spesifikasi kendala | Definisi R dan B, sumber halaman, syarat, contoh diterima/ditolak, serta ketidakpastian |
| Konstruksi bahan uji | Pasangan sopran–saksi, verifikasi tiap kondisi, prosedur perturbasi dan seluruh catatan seleksi |
| Evaluator yang dapat diperiksa | Jejak kandidat, fungsi yang dipakai, keputusan, alasan dan versi; gunakan kemampuan music21 yang sudah ada |
| Pemeriksaan evaluator | Contoh beranotasi independen yang tidak dipakai untuk menyesuaikan aturan; data pengembangan dan pemeriksaan dipisahkan menurut keluarga sumber/melodi |
| Hasil model | Profil per kriteria dan kurva keberhasilan versus perturbasi, dengan kegagalan dan keputusan U terlihat |
| Analisis statistik | Perbandingan berpasangan pada melodi dasar; pengulangan generasi bersarang; ketidakpastian estimasi dan domain generalisasi dijelaskan |

Pembanding evaluator harus memakai konfigurasi music21 yang masuk akal untuk kriteria yang sama. Jangan membuat pembanding sengaja lemah dengan mengabaikan fungsi kontekstual yang tersedia. Ketidaksesuaian terhadap satu spesifikasi Strube juga bukan bukti bahwa pustaka umum mempunyai bug.

Penilaian ahli independen diperlukan agar saksi dan label pemeriksaan tidak hanya dibenarkan oleh kode yang sama dengan pembentuknya. Pengecekan perangkat lunak dan sifat representasi tetap terpisah dari validasi musikal. Pemeriksaan invariansi yang dapat direncanakan mencakup pemecahan nada terikat tanpa mengubah makna musikal; jangan menyamakan nada berulang tanpa ikatan dengan nada ditahan. Audit ini tidak menjalankan pengujian tersebut.

## 7. Batas kontribusi dan kelayakan

Ini kontribusi matematika terapan dan metodologi komputasional: memformalkan himpunan solusi, menyertakan bukti keberadaan solusi pada bahan uji, mendefinisikan perturbasi, dan mengestimasi keberhasilan. Menulis simbol himpunan atau rumus proporsi bukan dengan sendirinya penemuan matematika baru. Nilainya harus dibuktikan melalui implementasi, mutu bahan uji dan pengetahuan empiris yang dihasilkan.

Tahap minimum tidak membutuhkan solver lengkap, model AI tambahan atau pelatihan ulang. Mulai dari bagian yang dapat diverifikasi dengan saksi. Jika tujuh aspek tidak dapat dirumuskan/diputuskan secara memadai, ruang lingkup harus dipersempit secara terbuka. Jika sumber/penilai independen tidak tersedia, kekuatan klaim validasi menurun. Jika semua perturbasi tinggi tidak memperoleh saksi, belum ada dasar mengisi kondisi itu dengan dugaan atau menyebut kegagalan Coconet.

Simpulan tentang perbedaan keberhasilan tetap pada checkpoint, pengaturan, domain representasi, kriteria dan distribusi bahan yang diuji. Ia tidak membuktikan penyebab arsitektural, keindahan musik, seluruh gaya Bach, atau jaminan bahwa model tidak pernah melihat melodi sumber.

## Sumber yang diperiksa dan penelusuran

- [Huang dkk. (2019), §6.3](https://arxiv.org/html/1907.06637v1): preseden evaluasi Coconet; masalah masukan dan pengecualian. Batas rincian checkpoint penelitian tetap mengikuti audit sebelumnya.
- [music21 voiceLeading](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html): fungsi yang sudah tersedia dan batas kesamaan dengan spesifikasi sumber.
- [Strasheela](https://strasheela.sourceforge.net/) dan [contoh resmi](https://strasheela.sourceforge.net/strasheela/doc/StrasheelaExamples.html): CSP musik, beberapa solusi dan pemodelan teori; tidak diinstal atau dijalankan, dan kompatibilitas perangkat lunak lama tidak diasumsikan.
- [MUSIB, artikel primer 2023](https://link.springer.com/article/10.1186/s13636-023-00279-6): abstrak dan §1–1.1 diperiksa, termasuk cakupan monofonik dan batas terhadap Coconet; bukan bukti bahwa seluruh ide benchmark usulan ini baru.
- [Sprockeels dan Van Roy (2025)](https://www.ijcai.org/proceedings/2025/1130): abstrak penerbit diperiksa; rincian metode lengkap belum ditelaah pada tindak lanjut ini.
- [Lafleur dkk. (2022)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2022.30): abstrak dan metadata penerbit diperiksa; tahun terbit dikoreksi terhadap salah satu rekaman OpenAlex.
- [Geifman dan El-Yaniv (2019)](https://proceedings.mlr.press/v97/geifman19a.html): abstrak penerbit untuk reject option dan risk–coverage; arsitektur SelectiveNet tidak diadopsi atau divalidasi untuk musik.

Rencana OpenAlex diperbarui sebelum dua batch lengkap dijalankan: 45 kueri pada `20261022T080359305403Z-batch` (839 karya unik), lalu 48 kueri pada `20261022T080528545198Z-batch` (865 karya unik). Beberapa kueri luas menghasilkan banyak karya tidak relevan; jumlah hasil tidak membuktikan kedalaman tinjauan atau kebaruan. Sumber penting di atas diperiksa langsung. Bibliografi naskah tidak ditambah secara otomatis.

Belum ada implementasi baru, solver, pemeriksaan instrumen, pilot atau data model yang dihasilkan pada audit ini. Dokumen ini menyiapkan pilihan kontribusi yang konkret untuk ditimbang sebelum migrasi naskah dan protokol.
