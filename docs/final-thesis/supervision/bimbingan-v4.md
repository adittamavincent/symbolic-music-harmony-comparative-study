# Ringkasan untuk bimbingan: naskah v4

Disusun 4 Oktober 2026 untuk dibawa bersama PDF `Skripsi_v4_23104810131_Vincent.pdf` (BAB I–III). Rinciannya ada di [perubahan-v3-ke-v4.md](perubahan-v3-ke-v4.md) dan `research/protocol.md`.

## Yang berubah dari v3

- **Landasan teori disusun ulang dengan teori bernama ahli**, masing-masing untuk satu pertanyaan penelitian:

| Teori | Dipakai untuk |
| --- | --- |
| Briot, Hadjeres, dan Pachet (2020), lima dimensi model generatif musik | Menafsirkan perbedaan DeepBach dan Coconet (pertanyaan 2) |
| Storkey (2008), pergeseran dataset; Huang dkk. (2019) | Menafsirkan pengaruh asal melodi (pertanyaan 3) |
| Pearce, Meredith, dan Wiggins (2002), evaluasi model gaya musik | Menempatkan pengukuran kaidah sebagai evaluasi musik hasil AI dan membatasi kesimpulan (pertanyaan 1) |
| Strube (1928), kaidah gerak suara dan fungsi akor | Definisi lima kaidah dan pengecualiannya |
| Huron (2001), alasan perseptual kaidah gerak suara | Arti musikal setiap jenis pelanggaran |

- **Tinjauan pustaka** membahas setiap studi utama secara utuh (judul, cara, temuan, hubungan), ditutup tabel perbandingan delapan studi. Dua studi baru: Leemhuis dkk. (2020) dan Choi dkk. (2023).
- **Rumusan masalah** satu paragraf, diikuti tiga pertanyaan.
- **Semua sitasi diperiksa** ke sumber aslinya; dua nama penulis yang salah diperbaiki, sumber yang hanya didaftar dihapus.
- **Metode** dirinci: pengaturan model, *seed*, kontrol kualitas, empat analisis kepekaan.

## Desain singkat (tidak berubah)

Melodi yang sama diberikan kepada DeepBach dan Coconet. Asal melodi: sopran *chorale* Bach dan latihan melodi Strube. Lima kaidah dihitung otomatis per birama dengan music21, tanpa penilai manusia. X1 model, X2 asal melodi, Y pelanggaran per birama. Uji Wilcoxon (model) dan Mann–Whitney (asal melodi), koreksi Holm.

## Kesiapan eksperimen

- Program generasi, evaluasi, dan analisis sudah lengkap dan diuji dengan model palsu; model belum dijalankan.
- Kerangka sampel Bach: 318 melodi layak dari 350 berkas korpus music21.
- Yang masih perlu dikerjakan peneliti: mengetik 71 melodi latihan Strube (templat sudah tersedia), mengetik contoh cetak Strube untuk uji instrumen, lalu uji coba pada tiga melodi per kelompok.

## Pertanyaan untuk Bapak

1. Apakah susunan landasan teori (teori tentang objek: Briot, Storkey, Pearce; teori tentang fokus: Strube, Huron) sudah sesuai harapan?
2. Apakah desain tanpa penilai manusia, judul, dan tiga pertanyaan penelitian dapat disetujui?
3. Apakah terjemahan Bapak, *Teori dan Penggunaan Akor* (2015, jilid I), sebaiknya ikut dikutip di samping edisi 1928? Tiga kalimat berbeda antara kedua edisi (jarak sopran–alto, syarat gerak melangkah pada tumpang tindih, bas di atas tenor); rinciannya di `study/persiapan-pembimbing-1.md`.
4. Apakah Strube dipakai sebagai buku ajar mata kuliah harmoni di program studi?
5. Bagaimana aturan program studi tentang pengungkapan penggunaan alat bantu AI dalam penelitian dan penulisan?
6. Setelah uji coba, apakah protokol dapat dibekukan untuk pengumpulan data utama?

## Sesudah pertemuan

Pertemuan dengan Pak Gathut tercatat sebagai G01–G15 di [feedback.md](feedback.md) (transkrip diserahkan 6 Oktober 2026). Beliau menyarankan lingkup dibatasi menjadi studi kasus dalam konteks *chorale* Strube. Pertanyaan 1–6 di atas tidak tampak dibahas dalam transkrip; yang masih relevan dipindahkan ke [rencana-v5.md](rencana-v5.md) bagian 8.
