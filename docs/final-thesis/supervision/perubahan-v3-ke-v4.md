# Perubahan dari naskah v3 ke naskah v4

Disusun 4 Oktober 2026. Naskah v3 dikunci sebagai tag `thesis/v3` (3 Oktober 2026). Dokumen ini menjelaskan apa yang berubah di v4, mengapa, dan dasarnya.

## Asal revisi

v4 tidak berasal dari masukan dosen baru. Dasarnya ada tiga:

- **Review teman (P01–P17):** pembacaan v3 oleh Manda, teman satu angkatan, dalam panggilan 4 Oktober 2026. Catatannya ada di [review-teman-2026-10-04.md](review-teman-2026-10-04.md). Manda bukan dosen; catatan ini tidak boleh disebut sebagai permintaan dosen. Hal yang Manda sampaikan atas nama orang lain (Prof. Andre, Bu Suryati) adalah laporan tidak langsung.
- **Audit 3 Oktober 2026 (A01–A39):** temuan dalam [../records/audit-2026-10-03/AUDIT.md](../records/audit-2026-10-03/AUDIT.md) yang belum ditangani di v3.
- **Tindak lanjut peneliti:** keputusan yang diambil agar eksperimen siap dijalankan.

Masukan dosen F01–F12 dari Seminar Musikologi 2 tetap dipenuhi; tidak ada yang dibatalkan.

## Ringkasan perubahan naskah

| Bagian | Naskah v3 | Naskah v4 | Dasar |
| --- | --- | --- | --- |
| Tanda baca | Banyak titik dua di tengah paragraf | Titik dua hanya sebelum daftar | Review teman P01 |
| Istilah asing | Sebagian tidak dimiringkan, termasuk *checkpoint* di abstrak | Dimiringkan secara konsisten dan diperiksa dengan skrip | P02 |
| Kata kunci | ... Musik Simbolik | ... Asal Melodi (variabel judul) | P03 |
| Sitasi | 50 kunci; banyak hanya dicek dari abstrak; dua nama penulis salah | 38 kunci; semua dicek ke Crossref/OpenAlex dan teks lengkap atau abstraknya; halaman ditambahkan bila teks lengkap tersedia; 20 sumber yang hanya didaftar dihapus; 8 sumber baru | P04, P10; audit A33–A35 |
| I.A Latar Belakang | "Rancangan jaringan komputasi … dijelaskan pada Bab II"; "dipilih dengan tiga syarat"; "berkorelasi dengan umpan balik positif" | Penjelasan singkat cara model mengisi suara; lima kaidah disebut langsung; bahasa disederhanakan; satu sumber Indonesia (Ridhwan dan Wisnugraha, 2026) | P05–P07, P14; audit A36 |
| I.B Rumusan Masalah | Dua paragraf | Satu paragraf diikuti daftar pertanyaan; definisi *checkpoint* dan batas arsitektur pindah ke III.A | P08; masukan dosen F03 tetap dipenuhi |
| I.F Sistematika Penulisan | Uraian BAB I–V | Dihapus; template departemen tidak memintanya | Keputusan peneliti 2026-10-04 setelah review teman (uraian per bab terasa seperti buku; lihat P14) |
| Rujukan antarbagian | "dibahas pada subbab berikut", "diuraikan di bawah", "pada akhir subbab ini" | Dihapus; rujukan ke tabel dan gambar tetap | Keputusan peneliti mengikuti P14 |
| Kata kunci abstrak | Baris kata kunci menjorok | Tanpa indentasi | Keputusan peneliti |
| II.A Tinjauan Pustaka | Subbab tema dengan rangkaian sitasi satu kalimat; "Posisi Penelitian" muncul tanpa pengantar | Setiap studi utama dibahas dengan judul, cara, temuan, dan hubungannya; setiap tema ditutup sintesis; tabel perbandingan delapan studi; bagian "Rangkuman dan Posisi Penelitian" | P09–P11; template departemen; audit A32 |
| II.A studi baru | — | Leemhuis et al. (2020): uji dengar ahli tetapi pelanggaran gerak suara tetap ada. Choi et al. (2023): menekan gerak paralel memengaruhi ciri lain | Riset literatur; audit A33 |
| II.B Landasan Teori | Grand/middle/applied theory; subbab "Musik simbolik, model generatif, distribusi data latih" tanpa nama ahli | Teori bernama ahli, masing-masing untuk satu pertanyaan: Briot et al. (2020) untuk model; Storkey (2008) untuk pergeseran dataset; Pearce et al. (2002) untuk evaluasi musik hasil AI; Strube (1928) untuk kaidah; Huron (2001) untuk alasan perseptual kaidah; Kerangka Berpikir dengan gambar | P12; template departemen (teori tentang objek dan fokus); contoh skripsi kuantitatif Prodi Musik 2026 yang memuat kerangka berpikir |
| Grand theory | Dirujuk ke Schoenberg (1954) tanpa halaman yang terverifikasi | Dirujuk ke pernyataan Strube sendiri tentang fungsi akor (Preface; hlm. 6) | Masukan dosen F08/F12 tetap dijawab; sumber yang dapat dicek |
| Keterangan budaya | Harrison dan Pearce tentang konsonansi | Huron (2001, hlm. 2, 4): kaidah gerak suara sebagai konvensi sejarah tertentu | Sumber yang langsung membahas gerak suara |
| Gaya bahasa BAB I–III | Kaku: "X karena itu Y" di tengah kalimat, "merupakan", frasa benda ("kelulusan uji", "penerapan konsep … merupakan"), pola "dua hal. Pertama, … Kedua, …" | Sekitar 50 kalimat dilonggarkan; beberapa kalimat diawali keterangan atau dibalik susunannya; istilah, sitasi, angka, hipotesis, dan rumus tetap; abstrak tidak diubah | P06; keputusan peneliti 5 Oktober 2026 |
| Istilah BAB I–III dan abstrak | "laju pelanggaran (per birama)"; "bilangan acak awal", "suhu pengambilan sampel", "fungsi kerugian", "dilatih awal"; "analisis kepekaan", "penganotasi", "kisi seperenam belas", "penandaan", "alat pengarah"; *dataset* tegak | "pelanggaran per birama"; *seed*, *temperature*, *loss function*, *pre-training*; "analisis sensitivitas", "anotator", "satuan not seperenam belas", "kejadian yang ditandai", "alat untuk mengarahkan model"; *dataset* miring. Istilah musik tetap, karena sudah sejalan dengan terjemahan Strube oleh Pak Gathut (2015). Abstrak Indonesia dan Inggris diubah bersamaan ("violations per measure") | P02, P06; keputusan peneliti 5 Oktober 2026 |
| III.A | Kalimat "deskriptif, komparatif, asosiatif kausal" | Dihapus; penjelasan langsung tentang tiap pertanyaan | P13; audit A01 |
| III.B Populasi dan sampel | "371 chorale Bach" | 371 nomor Riemenschneider = 350 berkas berbeda; 23 tidak layak, 9 mengulang melodi lain, kerangka sampel 318 melodi; penanganan melodi ganda | Temuan saat membangun kerangka sampel; audit A20 |
| III.B Data latih DeepBach | Status dicatat dari kode | Dihitung ulang program; sah hanya bila jumlah contoh sama dengan data yang disertakan bersama bobot | Audit A21 |
| III.C Generasi | "Pengaturan bawaan, misalnya iterasi" | Angka pengaturan, sumber, versi terkunci, *seed* DeepBach, Coconet tanpa *seed*, log percobaan, uji coba terpisah | Tindak lanjut peneliti; audit A22–A24 |
| III.C Instrumen | Fermata: "gerak dari nada berfermata ke peristiwa berikutnya" | Rumusan sesuai kode: gerak yang berawal selama nada berfermata; penghitungan tambahan kedua: nada sama berurutan disatukan | Audit A05, A06; keputusan 7 di PROGRESS |
| III.C Validitas | Pemeriksaan silang dan angka Huang tanpa batas klaim | Dinyatakan sebagai pemeriksaan dasar dan pemeriksaan kewajaran; penandaan jarak = kejadian di atas ambang | Audit A04, A08, A28 |
| III.C Kontrol kualitas | Empat suara, monofonik, sopran identik, kisi | Ditambah panjang keluaran dan setiap suara memuat nada | Audit A07 |
| III.D Analisis | Tiga analisis kepekaan | Empat (ditambah representasi bunyi bersama); arah ukuran efek, nol, keluarga Holm dinyatakan | Audit A10–A12, A31 |

## Perubahan riset (di luar naskah)

- Protokol versi 2.1 (`research/protocol.md`, `research/experiments/protocol_v2.json`): pengaturan model dikunci, *seed*, kontrol kualitas, analisis kepekaan keempat, aturan melodi ganda, set uji coba.
- Pipeline lengkap siap dijalankan tanpa menjalankan model: format ketik melodi Strube dan 71 templatnya, kerangka melodi Bach, pemeriksaan masukan, pengambilan sampel ber-*seed*, generasi (DeepBach dan Coconet), evaluasi, analisis statistik, tabel LaTeX untuk BAB IV, grafik, contoh partitur, cek kelengkapan. `make dry-run-v2` menjalankan seluruh rantai dengan model palsu.
- Lingkungan Python dipindah ke 3.12 karena SciPy 1.15 untuk Python 3.10 tidak dapat dimuat di macOS versi sekarang.

## Yang tidak berubah

Judul, tiga pertanyaan penelitian, variabel, hipotesis, lima kaidah, instrumen versi 2.0, sampel minimal 30 melodi per kelompok, dan desain tanpa penilai manusia. Halaman judul, pengesahan, dan kata pengantar tidak diubah.
