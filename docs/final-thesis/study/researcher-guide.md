# Panduan peneliti untuk revisi v5

Diperbarui 13 Oktober 2026. Ini bahan belajar dan langkah kerja, di luar naskah. [Panduan 9 Oktober](researcher-guide-2026-10-09.md) menyimpan desain 40 melodi/zona fermata sebagai riwayat; angka, uji, dan perintah pengumpulan di sana tidak dipakai untuk kasus yang sekarang direncanakan.

Mulai belajar dengan [panduan belajar v5](panduan-belajar-v5.md), lalu kerjakan [24 latihan bimbingan](latihan-bimbingan-v5.md). Keduanya tersedia dalam satu PDF melalui make learn-v5; berkas ini tetap menjadi panduan langkah kerja.

## Penelitianmu dalam dua menit

Kamu ingin tahu bagaimana AI menyusun alto, tenor, dan bas ketika soprannya sudah diberikan. Pedoman yang kamu pelajari adalah Strube. Karena Strube memberi aturan bertahap, kamu memeriksa gerak suara beserta kondisi dan pengecualiannya. DeepBach dan Coconet belajar pola chorale Bach dari data; keluaran keduanya dapat diperiksa dengan Strube meskipun buku itu tidak terbukti menjadi bahan latih.

Satu melodi dari bab chorale dipakai untuk kedua model. MODEL 285 menjadi calon karena buku mencetak harmonisasi empat suara. Harmonisasi itu memberi contoh pilihan dalam sumber, bukan satu jawaban yang harus disalin. Rencananya 20 percobaan per model. Satu melodi dengan 40 percobaan tetap satu kasus; pengulangan memperlihatkan variasi jawaban untuk masukan yang sama.

Program mencatat pola dan membantu mencari kejadian. Kamu membaca partitur serta menentukan apakah suatu gerak menyimpang, diterima dengan syarat, atau belum cukup jelas untuk diputuskan. Gerak horizontal suara juga masuk pembahasan: langkah, lompatan, arah, dan kelanjutan bas. Fermata tetap dapat membantu memahami kadens dan metadata, tetapi tidak menjadi pertanyaan perbandingan tersendiri.

Dua pertanyaanmu adalah bagaimana keluaran sesuai dengan kaidah Strube setelah syaratnya dibaca, dan bagaimana profil kedua sistem berbeda pada kasus yang sama. Jawabannya berupa peta kejadian, contoh partitur, alasan musikal, dan ringkasan per kriteria. Kesimpulan dibatasi pada kasus dan konfigurasi yang benar-benar diuji.

## Yang perlu kamu lakukan sekarang

1. **Baca BAB I–III dan tandai bagian yang belum kamu pahami.** Mulai dari dua pertanyaan, lalu [peta kaidah](peta-kaidah-gerak-suara-strube.md). Untuk tiap kaidah, baca halaman Strube yang disebut, contoh, dan pengecualiannya.
2. **Cari salinan notasi yang lebih jelas.** Yang paling dibutuhkan adalah MODEL 285, halaman cetak 174–176: bas awal yang tertutup cap dan durasi akhir sopran. Bisa melalui buku perpustakaan atau sumber cetak pembimbing. Foto/scan perlu memperlihatkan paranada dan tanda lengkap. Jika sumber tetap tidak dapat dipastikan, gunakan kasus chorale lain yang utuh sebelum data utama diambil.
3. **Bawa naskah dan lembar arah ke Bu Yoni lalu Pak Gathut.** [Handout bimbingan](../supervision/bimbingan-arah-v5.md) memuat butir yang perlu disepakati: satu kasus, satu atau dua model, kriteria/pengecualian, jumlah percobaan, metode deskriptif dan kebutuhan hipotesis menurut prodi. G07 menyarankan kasus kecil dan mempertimbangkan satu model; dua model belum disetujui. Catat keputusan dan tanggal sebenarnya.
4. **Periksa transkripsi serta sumber inti sendiri.** Mulai dari dua panel Fig. 33, kemudian MODEL setelah sumbernya cukup jelas. Isi kolom researcher_read_status dalam [reading-notes.csv](../records/reading-notes.csv) hanya sesudah benar-benar membaca.
5. **Setelah arah, kasus dan kriteria jelas, minta implementasi protokol serta pilot.** Pipeline yang tersedia masih menjalankan desain lama 3.0; protokol kasus 4.0 belum dipasang di pipeline. Keluaran uji coba dipisahkan. Data utama, BAB hasil, dan BAB kesimpulan dikerjakan sesudah prosedur dibekukan.

Langkah 1–4 dapat kamu kerjakan sambil menunggu jadwal bimbingan. Kasus dan instrumen belum dibekukan, sehingga generasi besar sekarang belum menyelesaikan masalah sumber dan keputusan musik.

## Arti teori yang dipakai

| Teori | Tugasnya pada skripsi |
| --- | --- |
| Strube | Kerangka harmoni dan penulisan empat suara, kaidah, tahap, contoh, syarat dan pengecualian yang dipakai menilai kejadian |
| Briot, Hadjeres, Pachet | Menjelaskan perbedaan tujuan, representasi, arsitektur, tantangan dan strategi model; membatasi klaim penyebab perbedaan |
| Pearce, Meredith, Wiggins | Menjelaskan perlunya evaluasi sesuai tujuan; kaidah gerak suara hanya satu aspek musik |
| Huron | Membantu menjelaskan keterpisahan suara secara teori; penelitianmu tidak mengukur persepsi pendengar |
| Flyvbjerg; Lazic | Mendukung alasan kasus kontekstual dan pembedaan kasus, keluaran, serta kejadian; penerapannya pada musik adalah penalaran penelitian ini |

Fungsi akor berarti peran seperti tonika, subdominan, dominan, dan tujuan resolusi nada. Strube menjelaskannya pada Preface dan halaman 6. Istilah itu membantu membaca gerak suara; judul grand theory tidak menambah variabel baru. Susunan kerangka umum → kaidah → definisi operasional dibuat peneliti.

## Bacaan inti dengan tugas singkat

| Bacaan | Baca dan tulis |
| --- | --- |
| Strube, Preface; hlm. 6–13, 20, 23, 34–35, 45, 83, 96, 109, 174–176 | Satu kaidah, syaratnya, contoh, dan halaman pengecualian; cocokkan istilah terjemahan yang tersedia |
| Hadjeres et al. 2017, [DeepBach](https://proceedings.mlr.press/v70/hadjeres17a.html), §2 | Data asli 352 → 2.503, representasi, kendali sopran, sampling; bedakan makalah asli dan bobot PyTorch yang akan diuji |
| Huang et al. 2017, [Counterpoint by Convolution](https://archives.ismir.net/ismir2017/paper/000187.pdf), §3 dan §6 | Piano roll, data chorale, pelengkapan partitur dan batas representasi |
| Huang et al. 2019, Bach Doodle §6.3 hlm. 798; Yan et al. 2018 §4 dan rubrik | Bedakan hitungan kandidat, keputusan penilai, bobot sumber dan adaptasi penelitianmu |
| [Flyvbjerg 2006](https://arxiv.org/abs/1304.1186); [Lazic 2010](https://link.springer.com/article/10.1186/1471-2202-11-5) | Mengapa satu kasus dapat dibaca mendalam; mengapa 40 keluaran bukan 40 melodi |
| Briot et al. hlm. 11–13; Pearce et al. 2002; Huron 2001 hlm. 2–5, 18–37 | Satu kalimat tentang peran setiap teori dan batas bukti yang diberikannya |

Untuk istilah model, gunakan [model-dan-istilah.md](model-dan-istilah.md). Bahan tanya-jawab lama dalam defense-qa.md dan persiapan-pembimbing-1.md perlu dibaca menurut tanggal/desainnya; rumus, hipotesis zona dan jumlah sampel lama bukan metode kasus saat ini.

## Yang sudah ada dan yang masih terbuka

BAB I–III, judul dan abstrak sudah mengikuti arah kasus. Peta 14 keluarga kaidah, syarat dan pengecualian tersedia; dua panel Fig. 33 mempunyai MusicXML dan provenance. Hasil 0/1 overlap pada dua panel hanya bukti kondisi itu, bukan validasi semua kaidah. Teks kedua scan sudah di-OCR seluruh halaman PDF; notasi MODEL belum lengkap.

Persetujuan pembimbing, salinan jelas MODEL, pemeriksaan mandiri peneliti, implementasi instrumen kontekstual, pilot, dan data utama masih terbuka. [PROGRESS.md](../PROGRESS.md) mencatat kemajuan saat ini; [protocol.md](../../../research/protocol.md) memisahkan protokol kasus 4.0 tertulis dari pipeline 3.0 lama.

## Catatan yang perlu kamu simpan

Sesudah membaca, isi sumber, halaman, klaim yang didukung, batasnya, dan keputusan desain dalam reading-notes.csv. Sesudah bimbingan, catat siapa mengatakan apa dan kapan di feedback.md. Sesudah sesi riset, isi apa yang dilakukan, ditemukan, diubah, dan harus diselesaikan pada research-log.md. Pemeriksaan asisten, bacaanmu, persetujuan dosen dan hasil model adalah empat bukti berbeda.
