# Persiapan BAB IV v6: Hasil dan Pembahasan

21 Oktober 2026. Dokumen kerja untuk menyiapkan BAB IV. Isi berikut menetapkan cara menyajikan hasil dari data utama; ini belum merupakan hasil penelitian dan tidak dimasukkan ke naskah sebagai bab hasil. Pendekatan dan prosedur ada di BAB III; [rancangan v6](../supervision/rancangan-v6.md) menjelaskan sumber serta alasannya.

## A. Kasus dan Korpus Harmonisasi

Uraikan identitas sumber, edisi, halaman, transkripsi lengkap serta hasil pemeriksaannya. Sajikan partitur kasus yang benar-benar digunakan, bukan sembilan nada pembuka atau fragmen OMR yang ditolak. Laporkan identitas model, paket, hash bobot dan konfigurasi efektif dari run utama. Tabel korpus memuat jumlah percobaan, keluaran layak/gagal, keluaran unik, keluaran identik dan alasan kegagalan. Angka harus dapat dihitung kembali dari attempts.csv dan berkas mentah.

Bukti yang diperlukan: sumber terbaca; case.json dengan hash dan hasil pemeriksaan sumber; run.json dengan protokol yang benar-benar dijalankan; attempts.csv; raw output; berkas SATB dan QC. Rekonsiliasi wajib: percobaan = keluaran layak + gagal/tidak layak, dengan setiap attempt_id tepat satu status akhir. Jika status menunggu masih ada, korpus belum ditutup.

## B. Kesesuaian Gerak Suara Menurut Strube

Susun pembahasan per kriteria: kuint, oktaf/unisono, tumpang tindih, jarak, persilangan, dan gerak horizontal. Pola interval tersembunyi menjadi pendamping. Untuk tiap pembahasan, hubungkan lokasi, nada awal/tujuan, interval, progresi/nada nonakor, halaman Strube, syarat atau pengecualian, keputusan, serta alternatif tafsir yang mengubah keputusan. Tampilkan cuplikan dari keluaran aktual dan beri kode yang menuju baris data.

Tabel transisi per keluaran/kriteria berkolom `output_id, rule_id, O, C, A, D, U, reviewed, R, Q`. Harus berlaku `O=C+A+D+U` dan `reviewed=O`. O=0 menghasilkan nilai tidak tersedia, bukan 0%. Tabel keadaan memuat `output_id, rule_id, pair, unique_episodes, joint_sounding_quarters, duration_C, duration_A, duration_D, duration_U`; durasi status tidak boleh melebihi waktu pasangan berbunyi bersama. Hitungan episode berstatus ganda tidak dijumlahkan sebagai episode unik. Durasi dan jumlah episode menjawab hal berbeda.

Profil horizontal memuat interval semiton, arah, langkah/lompatan diatonis jika ejaan dapat dipertanggungjawabkan, serta kelanjutan bas. Pola struktural lintas nada hias/suspensi mempunyai span_id dan tautan opportunity_id yang relevan, dengan hitungan terpisah. Tidak ada indeks penalti Strube gabungan.

## C. Pola Berulang dan Variasi Antarkeluaran

Kelompokkan pola berdasarkan kriteria, pasangan suara, letak pada melodi tetap, status dan konteks musik. Peta partitur memuat lokasi serta jumlah keluaran layak yang menunjukkan pola; nama pola tidak ditentukan hanya dari kebetulan tinggi nada yang sama. Catat definisi pengelompokan sebelum meringkas.

Tabel pola berkolom `pattern_id, rule_id, pair, score_span, context, status, output_ids, outputs_with_pattern, valid_outputs, proportion`. Setiap output_id dihitung satu kali untuk satu pola. Keluaran identik tetap dihitung menurut percobaannya, dan kontribusinya ditunjukkan agar pengulangan tidak keliru dibaca sebagai ragam pilihan. Bila diperlukan, tampilkan ringkasan tambahan hanya pada keluaran unik dengan penyebut terpisah dan tanpa menghapus ringkasan semua percobaan.

## D. Pembahasan Musikal dan Batas Temuan

Bahas pola yang berulang, variasi gerak, kejadian diterima bersyarat, penyimpangan dan ketidakpastian yang benar-benar ada. Tunjukkan alasan memilih cuplikan dan jangan memaksa kategori yang tidak muncul. Harmonisasi cetak dibaca dengan prosedur yang sama; perbedaan nada bukan ukuran kesalahan. Data Bach Doodle dapat menjadi pembanding masalah, tetapi nilai per birama dari publikasi tidak diuji langsung melawan nilai per kesempatan pada v6.

Uraikan batas representasi piano roll, ejaan inferensial, satu kasus, bobot/pengaturan, pembacaan oleh satu peneliti, dan keanggotaan kasus dalam data latih yang belum diketahui. Huron dapat membantu penjelasan teoretis; jangan menyatakan hasil persepsi, keindahan atau efektivitas belajar tanpa pengukuran tersebut. Jangan menyimpulkan mekanisme internal jaringan dari lokasi penyimpangan.

## Syarat BAB IV siap

| Syarat | Bukti yang harus tersedia | Keadaan 21 Oktober 2026 |
| --- | --- | --- |
| Kasus dan acuan terbaca | Transkripsi lengkap diperiksa terhadap sumber | Belum; MODEL 285 masih bermasalah pada bas pembuka dan akhir sopran |
| Instrumen diterapkan | Versi program/lembar keputusan cocok dengan protokol, termasuk pemeriksaan menyeluruh | Belum; instrumen 3.1 baru rencana |
| Pemeriksaan instrumen | Contoh sumber/kontra-contoh dan penjelasan batas setiap kriteria | Dua kondisi Fig. 33 saja sudah tersedia sebagai bukti terbatas; belum seluruh kriteria |
| Pilot teknis | Keluaran tersendiri, pemeriksaan mask/sopran/waktu/pemetaan | Belum tersedia |
| Data utama | Manifest dan seluruh percobaan aktual | Belum tersedia |
| Keputusan lengkap | Setiap O diperiksa, alasan/status dan sumber dapat ditelusuri | Belum tersedia |
| Hasil dapat dihitung kembali | Tabel, peta dan cuplikan terhubung ke baris data | Belum tersedia |

Langkah yang menunggu peneliti adalah memastikan sumber kasus yang dapat dibaca dan menyelesaikan pembacaan musikal serta keputusan yang menjadi tanggung jawab peneliti. Penetapan satu model mengurangi lingkup; hal itu tidak dengan sendirinya menghasilkan data yang dapat mengisi BAB IV.
