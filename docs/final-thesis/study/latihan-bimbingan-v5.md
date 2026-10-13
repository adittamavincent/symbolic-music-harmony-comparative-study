# Latihan bimbingan v5

Gunakan setelah membaca panduan belajar dan naskah. Jawab pertanyaan berikut dengan bahasamu sendiri sebelum membuka jawaban pegangan. Jika belum mengetahui jawaban yang memerlukan sumber atau persetujuan, sebutkan apa yang perlu diperiksa.

## Pertanyaan

1. Apa objek penelitianmu dan apa yang dihasilkan oleh AI?
2. Apa dua pertanyaan penelitian v5?
3. Mengapa Strube digunakan sebagai pedoman?
4. Apa arti fungsi akor dan bagaimana kaitannya dengan gerak suara?
5. Apa grand theory yang kamu gunakan? Apakah Strube membagi teorinya dalam tiga tingkat itu?
6. Mengapa aturan Strube perlu dibaca menurut tahap dan kondisi?
7. Apa perbedaan MODEL 285 dengan EXERCISES 286?
8. Mengapa MODEL 285 menjadi calon kasus? Apakah sudah siap menjadi masukan lengkap?
9. Apakah keluaran yang berbeda dari harmonisasi cetak berarti salah?
10. Apa hubungan data DeepBach/Coconet dengan Strube?
11. Apakah kasus tersebut pasti belum pernah dilihat model?
12. Apa perbedaan model, implementasi dan checkpoint?
13. Apakah LSTM berarti DeepBach hanya menulis musik dari kiri ke kanan?
14. Mengapa pengulangan generasi diperlukan? Mengapa direncanakan 20 per model?
15. Apakah satu melodi dengan 40 percobaan berarti 40 sampel melodi?
16. Mengapa kamu mempertahankan dua model, dan apa status pilihan itu di depan pembimbing?
17. Mengapa tanda program belum langsung menjadi penyimpangan terkonfirmasi?
18. Jelaskan perbedaan tumpang tindih dan persilangan melalui Fig. 33.
19. Mengapa contoh good pertama diterima dan avoid dihindari?
20. Apa yang kamu lakukan ketika fungsi atau ejaan nada belum jelas?
21. Bagaimana mencatat jarak yang berlangsung terus, dan mengapa tidak menghitung setiap langkah sebagai kesalahan baru?
22. Bagaimana menyajikan tiga penyimpangan dan dua keputusan belum pasti dari 60 kesempatan?
23. Bagaimana membedakan uji kode, validasi, pilot dan data utama?
24. Apa kontribusi penelitian, batas kesimpulan dan manfaat bagi pengajar?

## Jawaban pegangan

1. Objeknya gerak suara pada harmonisasi simbolik. Sopran diberikan; AI mengisi alto, tenor dan bas. Hubungan suara yang dihasilkan dengan sopran juga diperiksa.

2. Pertama, bagaimana kesesuaian terhadap Strube sesudah kondisi dan pengecualiannya dibaca. Kedua, bagaimana perbedaan profil kedua sistem pada kasus yang sama, termasuk lokasi berulang dan pilihan terhadap acuan.

3. Strube adalah pedoman pembelajaran harmoni yang dipelajari peneliti dan menyediakan kaidah empat suara serta konteksnya. Pemakaiannya dijelaskan melalui halaman, contoh, tahap dan syarat.

4. Fungsi adalah peran akor dalam hubungan tonal, seperti tonika, subdominan dan dominan. Fungsi membantu menentukan peran suatu nada dan tujuan geraknya. Dasarnya Preface dan hlm. 6.

5. Kerangka umumnya teori harmoni Strube tentang fungsi akor dan penulisan empat suara. Hubungan kerangka umum, kaidah dan definisi operasional disusun peneliti untuk penelitian ini.

6. Kelonggaran diberikan pada keadaan tertentu. Contohnya kuint IV-II pada hlm. 45 dan persilangan suara bawah dalam chorale pada hlm. 174. Keadaan itu harus cocok dengan kejadian yang dinilai.

7. MODEL memuat contoh harmonisasi SATB pada hlm. 174-176. EXERCISES sesudahnya memuat soal melodi. Tidak ditemukan kunci tiap latihan dalam scan yang ditinjau; MODEL bukan kunci seluruh latihan.

8. Ada sopran dan pilihan harmonisasi cetak dalam satu konteks yang bisa ditelusuri. Sumber masih perlu diperjelas pada bas awal yang tertutup cap dan durasi akhir sopran, lalu transkripsi lengkap diperiksa.

9. Perbedaan nada merupakan pilihan lain yang perlu dinilai dengan kriteria yang sama. Acuan memberi contoh keputusan dalam sumber, tanpa menjadi satu jawaban yang wajib disalin.

10. Keduanya belajar chorale Bach dan dapat diberi tugas sopran tetap dalam empat suara. Itu hubungan domain dan tugas. Kesamaan tersebut tidak membuktikan model mempelajari buku Strube atau memenuhi semua kaidahnya.

11. Belum diketahui. Keanggotaan kasus dalam data checkpoint belum diperiksa. Saya membatasi klaim pada keluaran kasus yang diuji, tanpa mengklaim generalisasi ke melodi yang pasti baru.

12. Model menyebut sistem atau rancangan; implementasi adalah kode yang menjalankannya; checkpoint adalah bobot hasil pelatihan. Ketiganya perlu dicatat untuk mengetahui konfigurasi yang menghasilkan keluaran.

13. Komponen LSTM dipakai untuk membaca konteks. Pseudo-Gibbs sampling memperbarui nada berdasarkan konteks itu; generasinya tidak dijelaskan sebagai penulisan satu arah saja.

14. Pengulangan memperlihatkan variasi jawaban pada masukan tetap. Angka 20 adalah rencana beban pembacaan partitur dan masih perlu ditetapkan setelah pemeriksaan teknis serta kesepakatan; bukan hasil power analysis.

15. Ada satu kasus melodi dan 40 percobaan. Banyak kejadian di dalam keluaran juga tidak otomatis menjadi melodi independen. Setiap tingkat dilaporkan dengan jumlahnya sendiri.

16. Dua model memungkinkan perbandingan profil pada tugas sama. Ini pilihan peneliti. G07 menyarankan kasus kecil dan mempertimbangkan satu model; persetujuan pembimbing atas dua model belum tercatat.

17. Program mengenali bentuk pola. Keputusan memerlukan kaidah yang berlaku serta pengecualiannya. Kandidat dapat diterima, menyimpang, atau belum dapat diputuskan.

18. Persilangan membandingkan urutan nada pada saat sama. Tumpang tindih membandingkan nada sekarang dengan nada sebelumnya pada suara tetangga. Pada avoid, tenor tetap di atas bas pada tujuan tetapi sudah turun melewati posisi bas sebelumnya.

19. Pada good pertama, tenor F#3 ke G3 melangkah saat bas D3 ke G3 menumpang tindih. Pada avoid, tenor B3 ke F#3 dan bas G3 ke D3 sama-sama melompat. Uraian dan label hlm. 12-13 menjadi dasarnya.

20. Saya mencatat inferensi atau alternatif dan memakai status belum dapat diputuskan bila dasar belum cukup. Angka belum pasti tetap dilaporkan dan tidak diperlakukan sebagai nol.

21. Saya mencatat episode berkesinambungan pada pasangan dan kondisi sama, beserta durasinya dalam satuan not seperempat. Perubahan posisi waktu di dalam keadaan yang sama tidak otomatis membuat episode baru.

22. Untuk angka ilustrasi itu, R = 3/60 = 5 persen dan Q = 2/60 sekitar 3,33 persen. Pembilang/penyebut serta ketidakpastian tetap tampak. Ini bukan hasil data utama.

23. Uji kode memeriksa perilaku sesuai definisi. Validasi memeriksa kecukupan penilaian musikal. Pilot memeriksa kelayakan teknis sebelum pembekuan. Data utama menjawab pertanyaan melalui prosedur yang sudah ditetapkan.

24. Kontribusinya uraian gerak suara pada keluaran AI beserta pola, lokasi dan keputusan. Kesimpulan dibatasi pada kasus/checkpoint/pengaturan. Pengajar mendapat bahan pemeriksaan; penelitian tidak mengukur peningkatan hasil belajar atau persepsi pendengar.

## Latihan yang perlu dikerjakan di kertas

1. Gambar kembali posisi tenor-bas sebelum dan sesudah pada kedua panel Fig. 33. Tandai nada sebelumnya yang dilampaui. Sebutkan langkah atau lompatan tiap suara.
2. Buat satu catatan kaidah: halaman, bunyi aturan dengan bahasamu, tahap, syarat, pengecualian, dan contoh. Pilih tumpang tindih atau persilangan terlebih dahulu.
3. Ulangi ilustrasi rasio pada panduan tanpa melihat hasilnya. Jelaskan mengapa penyebut frekuensi keluaran layak berbeda dari jumlah seluruh percobaan.
4. Tulis tiga kalimat untuk membedakan suatu temuan sumber, keputusan peneliti dan hasil yang benar-benar diukur. Pakai contoh yang sudah ada; jangan mengisi hasil AI yang belum dikumpulkan.
5. Pilih dua pertanyaan yang belum lancar dijawab. Catat apakah kekurangannya ada pada pemahaman, akses sumber, atau keputusan yang harus dibawa ke pembimbing.

## Yang dibawa ke bimbingan

Bawa naskah, lembar arah, peta kaidah dan catatan sumber yang sudah dibaca. Jelaskan pilihan satu kasus serta dua model sebagai rencana, lalu minta keputusan tentang lingkup, jumlah percobaan, kriteria dan bentuk metode/hipotesis yang diminta prodi. Catat jawaban serta tanggal sebenarnya dalam feedback.md.

Gunakan [panduan belajar](panduan-belajar-v5.md) untuk memeriksa dasar jawaban dan [panduan peneliti](researcher-guide.md) untuk langkah kerja yang masih diperlukan.
