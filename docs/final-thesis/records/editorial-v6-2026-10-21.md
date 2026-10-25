# Revisi dan pemeriksaan v6, 21 Oktober 2026

Revisi dilakukan atas permintaan peneliti setelah laporan masukan kelas Pak Galih. Naskah v5 tetap pada tag thesis/v5; v6 adalah perubahan working tree, belum dikomit atau ditag. Tidak ada perubahan pada sumber proposal.

## Perubahan substansial

1. BAB I: objek menjadi satu model Coconet; gap dan pertanyaan kedua beralih dari perbedaan sistem ke pola antarkeluaran pada satu kasus. Angka tren pendidikan Indonesia di pembuka dihapus karena tidak diperlukan untuk membangun persoalan gerak suara; manfaat pembelajaran tetap dibatasi pada bahan pemeriksaan.
2. BAB II: alasan pemilihan mengikuti tugas SATB/sopran tetap dan persoalan paralel dalam publikasi Coconet. DeepBach tetap penelitian terdahulu. Peran Strube, model generatif, tujuan evaluasi, dan Huron dipertahankan dengan batasnya. Kueri discovery tidak diklaim sebagai bukti isi; klaim penelusuran Garuda/Google Scholar yang tidak ditelusuri pada revisi ini tidak digunakan sebagai dasar gap baru.
3. BAB III: pendekatan eksplisit kualitatif dalam studi kasus evaluatif. Yin dan Maxwell diperiksa pada teks penerbit. Angka mendukung keputusan partitur; hipotesis statistik dan variabel perlakuan tidak dibuat untuk memenuhi label. Tidak ada klaim bahwa pembacaan manual saja membuat penelitian kualitatif.
4. Definisi pencarian, kesempatan, empat status keputusan dan pemeriksaan menyeluruh diperjelas. Penyebut hanya dilaporkan setelah semua kesempatan diperiksa. Episode fisik dan segmen keputusan dibedakan; rentang struktural tidak dipindahkan ke penyebut transisi langsung. Ini perubahan rencana instrumen dari 3.0 menjadi 3.1, ditulis pada protokol 5.0 tanpa mengaku sudah diimplementasikan.
5. Judul serta dua abstrak diubah sebatas lingkup/metode baru. Berkas cover, pengajuan, pengesahan, pernyataan, motto, persembahan dan kata pengantar tidak diubah; judul tercetak mengikuti metadata. Tidak ada pemberitahuan draft atau status proyek di dalam naskah.
6. Format BAB IV dan kontrak pencatatan disiapkan di dokumen kerja. Bab hasil tidak diisi dari contoh instrumen, korpus Bach historis, atau angka rekaan.
7. Bibliografi diratakan kiri pada lingkungannya agar URL sumber tidak direnggangkan secara ekstrem oleh pengaturan justification naskah. Badan naskah tetap mengikuti kelas yang ada.

## Pemeriksaan editorial

Kedua skill lokal, peta adaptasi StoryScope, alur paragraf dan dua eval.md digunakan. Pemeriksaan mencakup tujuan paragraf, kontinuitas objek/pertanyaan/metode, atribusi sumber dan keputusan peneliti, kejelasan penyebut, batas inferensi, istilah konsisten, serta penghapusan klaim hasil yang tidak didukung. Definisi, contoh musikal, pengecualian, dan batas yang dibutuhkan tetap dipertahankan. Pemeriksaan ini bukan deteksi kepengarangan atau validasi instrumen.

Bukti sumber yang baru diperiksa mencakup Coconet 2017/2019, dokumentasi resmi dan bundle paket 1.23.1, Yin bab 1, Maxwell bagian yang relevan, serta Cuthbert/Ariza hlm. 637–638. Sumber pendukung lain mempertahankan dukungan yang tercatat pada reading-notes.csv; tidak semua buku/artikel dibaca ulang secara penuh pada revisi ini. Pembacaan mandiri peneliti belum dicatat.

## Pemeriksaan artefak

`make thesis` berhasil membangun PDF v6, 60 halaman. Semua halaman ditinjau melalui lima contact sheet; abstrak, metode, tabel kriteria, rumus, tabel alur jawaban dan bibliografi diperiksa pada render lebih besar. Bibliografi dirender ulang setelah perbaikan alignment. Pemeriksaan teks tidak menemukan glyph null/replacement, penanda ??, atau sitasi tak terdefinisi; seluruh 33 kunci sitasi ditemukan dalam bibliografi. Tidak ada kata di luar batas halaman pada pemeriksaan koordinat.

`git diff --check` dan pemeriksaan tautan lokal dokumen baru dilakukan. Bukti PDF, hash, ekstraksi, render, pemeriksaan koordinat dan sumber berada di `research/outputs/writing-v6-2026-10-21/` serta `research/outputs/source-verification-v6-2026-10-21/`. PDF kerja dan salinan pengiriman dibandingkan byte-for-byte.

Tidak ada software test, instalasi model, pilot, generasi, validasi instrumen keseluruhan, penilaian utama, pengukuran pendengar, atau persetujuan pembimbing yang diklaim dari keberhasilan kompilasi. Kebutuhan sumber kasus dan data utama masih membatasi kesiapan BAB IV.
