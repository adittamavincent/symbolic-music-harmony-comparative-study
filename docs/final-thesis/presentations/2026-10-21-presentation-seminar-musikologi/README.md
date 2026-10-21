# 21 Oktober 2026: presentasi Seminar Musikologi 2

Materi kelas berdasarkan naskah aktif final-thesis v5, terpisah dari milestone skripsi. Presentasi memuat objek material/formal, research gap, pertanyaan dan tujuan, teori, metode/kasus/unit analisis, hipotesis kerja, instrumen/posisionalitas, serta perubahan rancangan. Jumlah materi: 9 slide termasuk sampul, tanpa slide perkembangan atau lampiran.

## Berkas yang digunakan

- [Slide PDF](2026-10-21-presentation-seminar-musikologi.pdf), format layar 16:9, tanpa footer sumber atau nomor halaman. Bookmark tiap slide tetap tersedia; rujukan ada di catatan presenter.
- [Catatan presenter](presenter-notes.md), sekitar 1.000 kata, satu paragraf singkat per slide beserta sumber. Dapat menjadi pegangan penyampaian sekitar 10–15 menit.
- [Catatan masukan kelas](masukan-kelas.md), disiapkan tanpa mengisi komentar atau persetujuan yang belum disampaikan.

## Dasar isi

Naskah v5 aktif masih BAB I–III. Revisi arah 13 Oktober memakai satu kasus Strube dengan MODEL 285 sebagai calon, sopran tetap, keputusan gerak suara kontekstual, dan perbandingan deskriptif. Dua model dan 20 percobaan per model merupakan rencana peneliti. Notasi sumber lengkap, kesepakatan lingkup, implementasi instrumen kontekstual, pilot, serta data utama masih terbuka menurut catatan proyek.

Riwayat versi berasal dari catatan perubahan dan feedback yang sudah ada. Tambahan skrip OCR pada commit 7c64d76 tanggal 21 Oktober disampaikan sebagai jejak pemrosesan teks. Objek material/formal merinci bahan dan sudut pembacaan objek yang sudah ada pada BAB III, tanpa mengubah metode penelitian.

Research gap pada slide 3 diambil dari BAB I bagian Rumusan Masalah dan BAB II bagian Posisi Penelitian, dengan batas sumber yang ditinjau. Slide 7 menambahkan usulan hipotesis kerja H1 tentang adanya penyimpangan terkonfirmasi pada keluaran masing-masing model dan H2 tentang perbedaan profil pada kasus sama, sesuai permintaan peneliti. Keduanya belum tercantum dalam naskah v5 dan belum merupakan hipotesis statistik populasi atau keputusan pembimbing. Penyelarasan naskah/protokol dan kriteria penilaian dukungan perlu dilakukan sebelum pengumpulan utama.

[Manifest sumber](source-manifest.json) menyimpan hash berkas lokal yang mendasari isi. Aset Fig. 33 dari versi presentasi sebelumnya tetap tersimpan dengan provenance; versi kelas saat ini memprioritaskan unsur rancangan penelitian.

## Edit dan bangun ulang

Sumber isi berada pada [prepare_content.py](prepare_content.py). Penyusunan slide berada pada [author.mjs](author.mjs). Sumber yang dihasilkan adalah [slides.json](slides.json); catatan presenter juga dibangkitkan dari materi yang sama. Untuk perubahan berkelanjutan, edit sumber isi agar penomoran dan catatan tetap selaras.

Jalankan dari root repositori:

```bash
bash docs/final-thesis/presentations/2026-10-21-presentation-seminar-musikologi/build.sh
```

Perintah memakai Node/Python/Artifact Tool/LibreOffice dalam runtime Codex yang terpasang di komputer ini. Jika lokasinya berubah, set SEMINAR_RUNTIME_ROOT ke folder dependencies runtime yang baru. Font desain adalah Arial. [build.mjs](build.mjs) menghasilkan PPTX perantara, LibreOffice mengonversinya menjadi PDF, lalu [publish_pdf.py](publish_pdf.py) memasang metadata dan bookmark.

PDF mengikuti kebijakan repositori yang mengabaikan berkas PDF dari Git. Sumber, catatan, dan formulir masukan tetap dapat dilacak. Bangun ulang PDF dengan perintah di atas jika berpindah checkout. Berkas perantara dan hasil pemeriksaan berada di research/outputs/seminar-2026-10-21/ yang diabaikan Git. Perintah ini hanya membangun presentasi, tanpa memasang atau menjalankan model riset.

## Sesudah kelas

Isi masukan nyata pada masukan-kelas.md, dengan pembicara, peran, nomor slide, parafrasa atau kutipan, dan tindak lanjut. Tautkan keputusan yang terkonfirmasi ke catatan bimbingan dan research-log. Perbarui PROGRESS hanya jika kesiapan penelitian benar-benar berubah. Perubahan protokol atau instrumen perlu versi dan alasan tersendiri.
