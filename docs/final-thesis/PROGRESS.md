# V6: kesiapan skripsi

Diperbarui 22 Oktober 2026. Peneliti meminta v6 memakai satu model setelah melaporkan masukan Pak Galih di Seminar Musikologi 2. Naskah BAB I–III direvisi untuk Coconet dan pendekatan kualitatif dalam studi kasus evaluatif, dengan hitungan deskriptif pendukung. Target BAB I–IV belum terpenuhi karena data utama belum tersedia. Tag `thesis/v5` tetap dipertahankan; v6 belum ditag atau dikomit.

## Audit arah, 22 Oktober

Tindak lanjut permintaan kontribusi teknis/matematis: [kandidat stress test dengan bukti kelayakan](supervision/kontribusi-teknis-stress-test-2026-10-22.md) merumuskan himpunan solusi, harmonisasi saksi per sopran, perturbasi dan ukuran keberhasilan/ketidakpastian. Ini usulan eksperimen komputasional dengan validasi instrumen, belum migrasi naskah/protokol. Klaim kebaruan global belum terbukti; pemrograman kendala musik dan benchmark infilling sudah mempunyai preseden. Tidak ada solver atau data baru dihasilkan.

Peneliti meminta pemilihan arah menurut alasan ilmiah dan kelayakan. [Audit Strube, NotaGen dan music21](supervision/arah-evaluasi-strube-2026-10-22.md) merekomendasikan tetap satu Coconet untuk sopran tetap, cakupan beberapa masukan yang dipilih menurut kondisi musikal, dan kontribusi utama berupa analisis keluaran beserta anotasi keputusan kontekstual. MODEL 285 tidak disarankan menjadi satu-satunya jalan karena sumber belum lengkap. Jumlah masukan/percobaan baru belum ditetapkan. Usulan ini belum dimigrasikan ke naskah atau protokol.

Sumber primer memperlihatkan music21 sudah mempunyai overlap, crossing dan hidden intervals selain P5/P8; klaim kebaruan berupa tujuh detektor yang sebelumnya tidak ada tidak didukung. Ekstensi khusus tetap mungkin, dengan menggunakan primitif yang ada. NotaGen-X tersedia di repositori resmi tetapi belum dibuktikan dapat menjaga sopran masukan atau menghasilkan SATB pada tugas penelitian. Tidak ada instalasi, pilot, generasi, atau pengujian perangkat lunak dalam audit ini. Batch 41 kueri OpenAlex selesai dengan 791 karya unik; reading-notes dan audit menyimpan dukungan serta batasnya.

## Keputusan dan hasil revisi

**Tindak lanjut audit metode:** peneliti menanyakan kembali variabel, hipotesis, dan kesalahan dalam penelitian kuantitatif. [Audit kuantitatif v6](supervision/audit-kuantitatif-v6.md) mengoreksi alasan pemilihan kualitatif yang terlalu cepat dan merekomendasikan kuantitatif deskriptif dalam studi kasus evaluatif. Dokumen itu berisi variabel hasil, calon hipotesis deskriptif, batas H0/H1 inferensial, serta kebijakan kegagalan dan ketidakpastian. Naskah/PDF saat ini masih memuat pendekatan kualitatif; penyelarasan ke rekomendasi kuantitatif belum dilakukan. Daftar di bawah mencatat isi revisi awal, bukan keputusan bahwa metode tersebut sudah final.

- Model: Coconet, dipilih karena kesinambungan masalah gerak sejajar pada publikasi Bach Doodle dan tugas pelengkapan SATB dengan sopran tetap. DeepBach tetap penelitian terdahulu. Perbandingan arsitektur dihapus dari tujuan.
- Judul: Evaluasi Musik Hasil AI Coconet Berdasarkan Kaidah Gerak Suara Strube dalam Harmonisasi Chorale (13 kata).
- Dua pertanyaan: kesesuaian kontekstual menurut Strube; pola gerak yang berulang dan bervariasi antarkeluaran Coconet.
- Pendekatan: kualitatif; desain studi kasus evaluatif; analisis partitur deduktif menurut sumber; angka untuk mendukung pola. Alasan dan batas Yin/Maxwell sudah dijelaskan. Variabel perlakuan dan H0/H1 populasi tidak digunakan.
- Satu chorale; MODEL 285 masih calon. Bas pembuka dan durasi sopran akhir memerlukan sumber yang jelas sebelum input/acuan lengkap dapat dibekukan. Identitas sebagai karya asli Bach belum dibuktikan.
- Rencana 20 percobaan Coconet tetap keputusan beban kerja peneliti, bukan persetujuan dosen atau perhitungan daya/kejenuhan.
- Instrumen disusun peneliti: peta sumber, pembaca music21, pencari kandidat, dan lembar keputusan. music21 tidak otomatis menerapkan Strube. Setiap kesempatan yang dihitung harus diperiksa; pemeriksaan sampel tanpa tanda pada v5 diganti dengan cakupan menyeluruh.
- Akuntansi keputusan O=C+A+D+U; D/O dan U/O memakai kesempatan sama dan hanya diringkas setelah seluruh O diperiksa. Episode fisik jarak/persilangan dibedakan dari segmen status dan durasi. Gerak horizontal dan rentang struktural tetap dijelaskan.
- Protokol tertulis 5.0 dan instrumen 3.1 masih rencana. Program bawaan tetap protokol historis 3.0 / instrumen 2.0; belum mengimplementasikan v6.

Penjelasan lengkap dan sumber: [rancangan v6](supervision/rancangan-v6.md). Penyiapan hasil: [rancangan BAB IV](study/rancangan-bab-iv-v6.md). [Templat data](../../research/experiments/v6/README.md) berisi kontrak dan header tanpa hasil rekaan.

## Kesiapan per bagian

| Bagian | Keadaan | Bukti atau kebutuhan |
| --- | --- | --- |
| BAB I | Direvisi ke satu model | Masalah, dua pertanyaan, tujuan dan manfaat selaras |
| BAB II | Direvisi ke Coconet dan peran sumber | Strube, teori pendukung, alasan model, posisi pertanyaan/hipotesis |
| BAB III | Rencana analisis ditulis rinci | Pendekatan, unit, data, kategori, pemeriksaan penuh, penyebut dan bentuk jawaban; pelaksanaan belum terbukti |
| BAB IV | Struktur dan kontrak data disiapkan di dokumen kerja; hasil belum dapat ditulis | Belum ada data utama yang sah untuk mengisi bab |
| Sumber kasus | Belum lengkap | MODEL 285 belum dapat dibekukan |
| Pemeriksaan instrumen | Bukti terbatas dua kondisi Fig. 33 | Belum mewakili seluruh kriteria/konteks |
| Implementasi instrumen 3.1 | Belum ada | Termasuk episode/segmen dan akuntansi seluruh kesempatan |
| Bobot dan korpus publik | Bobot coconet/bach serta korpus SATB publik telah diunduh | Belum ada pemuatan/inferensi; 382 urutan pada korpus bukan bukti identitas seluruh data latih checkpoint |
| Lingkungan model | Paket/dependensi Coconet belum terpasang | Unduhan bobot belum membuktikan model dapat dijalankan |
| Pilot dan data utama | Belum ada | Uji program/korpus Bach historis bukan data Coconet v6 |
| Persetujuan akademik | Belum dicatat atas rancangan lengkap | Masukan satu model dari Pak Galih tidak merupakan persetujuan seluruh pembimbing |
| Pemeriksaan naskah/PDF | Kompilasi dan tinjauan 60 halaman selesai | 33 kunci sitasi tersedia, tanpa penanda ??/glyph rusak/kata di luar halaman; rincian di catatan editorial |

## Urutan penyelesaian penelitian

1. Periksa [rancangan v6](supervision/rancangan-v6.md), khususnya alasan metode dan penggunaan angka. Bawa poin yang memerlukan keputusan prodi/pembimbing, termasuk format final BAB IV.
2. Pastikan kasus dan transkripsi lengkap terhadap sumber. Gunakan salinan lebih jelas atau pilih kasus lain pada konteks sama sebelum melihat keluaran model.
3. Lakukan pembacaan sumber oleh peneliti dan catat di reading-notes.csv. Pemeriksaan asisten tidak menggantikan pembacaan mandiri.
4. Implementasikan instrumen/protokol yang cocok dengan v6 dan periksa kondisi yang diukur; lakukan pilot tersendiri sesudahnya. Bekukan konfigurasi aktual dan jumlah percobaan sebelum pengumpulan utama.
5. Kumpulkan data utama, catat semua percobaan dan kegagalan, selesaikan keputusan partitur, lalu tulis BAB IV dari bukti tersebut. Kesiapan hasil baru dapat dinyatakan pada tahap ini.

## Penelusuran dan preservasi

Rencana OpenAlex diperbarui sebelum seluruh 33 kueri dijalankan. Manifest batch `20261021T054123948242Z-batch` menyimpan 731 karya unik. Kueri metodologi tidak selalu menemukan karya sasaran; sumber dipastikan langsung pada penerbit, bukan dari judul atau sitasi tertinggi. Yin (sampel bab resmi), Maxwell (PDF penerbit melalui web), dokumentasi resmi Coconet dan kode distribusi paket 1.23.1 diperiksa. Dukungan dan keterbatasan ada di [reading-notes.csv](records/reading-notes.csv).

Naskah proposal dan tag v3/v4/v5 dipertahankan. Hasil, protokol dan program lama tetap historis; tidak diganti dengan pengukuran v6. Model setup, pilot, generasi dan penilaian utama belum dijalankan dalam revisi ini.

## Bukti pemeriksaan revisi

`make thesis` menghasilkan `scratch/Skripsi_v6_23104810131_Vincent.pdf` (60 halaman). Seluruh halaman ditinjau pada contact sheet, dengan pemeriksaan detail pada abstrak, metode, tabel, rumus dan bibliografi. [Catatan editorial](records/editorial-v6-2026-10-21.md) menjelaskan perubahan, sumber yang diperiksa, serta batasnya. `git diff --check`, resolusi 33 kunci sitasi, tautan lokal dokumen baru, glyph dan koordinat halaman diperiksa. Salinan pengiriman dibandingkan dengan PDF kerja. Ini pemeriksaan naskah, bukan validasi instrumen atau bukti data penelitian.

## Tindak lanjut kesiapan BAB IV

Peneliti meminta seluruh data pendukung disiapkan dan kekurangannya dijelaskan. [Inventaris kebutuhan](study/kebutuhan-data-bab-iv-v6.md) mencatat pekerjaan, bukti selesai dan dependensinya. Pada tindak lanjut 21 Oktober, bobot publik coconet/bach diunduh dan di-hash; korpus SATB publik penulis diambil dari commit tetap dan memuat 229 train, 76 valid, 77 test. Ini korpus rujukan publik, belum bukti riwayat pelatihan persis checkpoint Magenta.js. Tidak ada pemuatan model atau generasi pada tindak lanjut audit ini. Sumber kasus, instrumen, pilot, data utama dan keputusan partitur masih diperlukan.
