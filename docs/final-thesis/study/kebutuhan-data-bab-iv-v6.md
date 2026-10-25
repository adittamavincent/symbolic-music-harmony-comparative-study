# Data dan pekerjaan untuk BAB IV v6

Audit 21 Oktober 2026, setelah peneliti menegaskan bahwa data pendukung BAB IV perlu disiapkan dan meminta daftar yang belum tersedia. Ini mencakup sumber, model pralatih, korpus publik, instrumen, pilot, data utama dan analisis. Arahan ini tidak dicatat sebagai persetujuan akademik dari dosen.

## Yang benar-benar sudah tersedia

- Naskah BAB I–III v6, rencana BAB IV, peta kaidah Strube, dan enam templat pencatatan.
- Dua panel Fig. 33 dengan transkripsi/provenance dan pemeriksaan terbatas pada dua kondisi tumpang tindih. Ini bahan pemeriksaan instrumen, bukan keluaran model.
- Bundle kode Coconet versi 1.23.1 telah diperiksa pada tahap revisi naskah.
- Bobot publik `coconet/bach` telah diunduh pada tindak lanjut ini: manifest SHA-256 `1b84f8999523b08c7aa5086b13b2aa444a52bbc466c7b4918878bf7190cc05a4`; shard 553.436 byte, SHA-256 `b543d9ce9d924d54c1c0e88d2738830b7711326d5f49b739d35f893e31925021`. Lokasi lokal `research/models/coconet-v6/checkpoint/`. Belum dimuat atau dijalankan.
- Korpus SATB publik yang ditautkan makalah Coconet telah diunduh dari repositori penulis, commit `9a7f733ddb4ed91f48da64ac7f0f621c34aadd4d`. Berkas `Jsb16thSeparated.json` berisi 229 urutan train, 76 valid dan 77 test: total 382 urutan. Hash berkas `79294cc374f9252e95ef4b703161524c1c53dc1f712c236f00f1c1f5d54af5a7`. Ini hitungan berkas sumber, bukan pengukuran hasil penelitian.

## Pekerjaan yang belum selesai

| Bagian | Kekurangan konkret | Bukti selesai | Pelaksana/dependensi |
| --- | --- | --- | --- |
| Kasus dan acuan | MODEL 285 belum mempunyai transkripsi SATB lengkap yang terverifikasi; bas pembuka tertutup dan durasi sopran akhir belum pasti | Sumber terbaca, transkripsi lengkap, lokasi halaman, hash dan catatan pemeriksaan | Peneliti menyediakan/menemukan sumber yang jelas; asisten dapat menyiapkan transkripsi dan pemeriksaan teknis, peneliti memeriksa sumber |
| Lingkungan Coconet | Paket/dependensi belum terpasang dan bobot belum dimuat; kemampuan perangkat menjalankan konfigurasi belum dibuktikan | Paket terkunci, catatan versi/backend, pemuatan bobot dan pemeriksaan pelaksanaan | Pekerjaan teknis asisten; dapat berjalan sebelum data utama |
| Riwayat data latih | Korpus publik sudah ada, tetapi keterkaitan persisnya dengan bobot Magenta.js yang diunduh belum terbukti | Catatan sumber, split, representasi dan keterbatasan; bukti riwayat checkpoint bila tersedia | Penelusuran asisten; identitas historis yang tidak tersedia tetap dinyatakan tidak diketahui |
| Instrumen 3.1 | Kode aktif masih instrumen lama; belum ada akuntansi seluruh kesempatan, semua persilangan, episode/segmen dan keluaran keputusan v6 | Implementasi versi yang sesuai BAB III dan kontrak CSV | Pekerjaan teknis asisten dengan kaidah/keputusan musikal ditelusuri ke Strube |
| Pemeriksaan instrumen | Dua contoh overlap belum mencakup kriteria lain, kondisi batas atau kejadian yang terlewat | Contoh sumber dan kasus batas per definisi; hasil cocok/tidak cocok serta alasan dan koreksi | Asisten menyiapkan bukti teknis; peneliti memeriksa sumber dan kecukupan musikal |
| Pilot teknis | Belum ada keluaran pilot untuk memeriksa mask, sopran, waktu, rentang, pemetaan suara dan ekspor partitur | Run pilot terpisah dengan QC dan rekaman pengaturan aktual | Setelah lingkungan tersedia; pilot pada kasus utama menunggu sumber yang lengkap |
| Pembekuan prosedur | Konfigurasi, jumlah percobaan dan instrumen masih rencana tertulis | Snapshot kasus/aturan/kode/bobot/pengaturan sebelum generasi utama; keputusan akademik dicatat sesuai yang benar-benar disampaikan | Peneliti menetapkan lingkup; asisten menyimpan snapshot dan versi |
| Data utama | Belum ada 20 percobaan Coconet pada kasus terpilih | Seluruh keluaran mentah, partitur, kegagalan, hasil QC, identitas/duplikat dan manifest | Sesudah sumber, instrumen dan pilot layak serta konfigurasi aktual dibekukan |
| Keputusan musikal | Seluruh kesempatan belum dibaca dan diberi C/A/D/U, konteks dan sumber | Lembar keputusan lengkap, O=C+A+D+U, ketidakpastian dan alasan terlihat | Peneliti bertanggung jawab atas keputusan; asisten membantu pencatatan dan pemeriksaan konsistensi |
| Hasil BAB IV | Belum ada tabel/peta/cuplikannya dari data utama | Semua angka dapat dihitung kembali dan semua contoh terhubung ke keluaran serta keputusan | Sesudah data dan keputusan tersedia; [struktur BAB IV](rancangan-bab-iv-v6.md) sudah disiapkan |

## Arti data latih dalam v6

Rancangan memakai model pralatih; pelatihan ulang bukan tahap yang ditetapkan. Korpus publik berguna untuk mendeskripsikan asal dan representasi data serta menelusuri kemungkinan kemiripan kasus. Korpus itu tidak otomatis merupakan salinan persis data pelatihan bobot pilihan kita. README penulis menyebut pembagian train/valid/test, empat suara, dan hilangnya informasi fermata serta artikulasi nada ulang pada representasi ini.

Jika riwayat bobot atau keanggotaan MODEL 285 tidak dapat dipastikan, kesimpulan tetap dapat dibatasi pada evaluasi keluaran konfigurasi tersebut; jangan membuat klaim generalisasi pada melodi yang belum pernah dilihat model. Menambah atau membuat data latih sendiri tidak memulihkan riwayat bobot lama dan akan mengubah penelitian bila dipakai untuk melatih model baru.

## Urutan kerja dan bahan dari peneliti

Lingkungan model, penelusuran data, implementasi pencatatan dan pemeriksaan kondisi dapat disiapkan lebih dahulu. Pengumpulan utama pada MODEL 285 menunggu sumber yang lengkap. Bahan paling mendesak dari peneliti adalah salinan terbaca MODEL 285, terutama halaman cetak 174 dan 176; alternatifnya kasus lain dalam konteks chorale Strube yang utuh, dengan keputusan pergantian dicatat sebelum melihat hasil generasi.

Pembacaan mandiri peneliti, keputusan musikal dan keputusan dosen hanya dapat dicatat sesudah benar-benar dilakukan/disampaikan. Keberhasilan program atau ketersediaan bobot tidak menggantikannya.

## Sumber dan bukti audit

- [Makalah asli Coconet, hlm. 212](https://archives.ismir.net/ismir2017/paper/000187.pdf) menautkan kode, data dan contoh.
- [README korpus pada commit yang diambil](https://github.com/czhuang/JSB-Chorales-dataset/blob/9a7f733ddb4ed91f48da64ac7f0f621c34aadd4d/README.md).
- [Berkas JSON korpus](https://raw.githubusercontent.com/czhuang/JSB-Chorales-dataset/9a7f733ddb4ed91f48da64ac7f0f621c34aadd4d/Jsb16thSeparated.json); jumlah split dihitung langsung dari daftar pada berkas ini.
- [Manifest bobot publik](https://storage.googleapis.com/magentadata/js/checkpoints/coconet/bach/weights_manifest.json).
- Artefak lokal: `research/outputs/readiness-v6-2026-10-21/asset-audit.json`, `dataset-audit.json`, README dan daftar berkas sumber; korpus tersimpan pada `research/outputs/training-corpus-v6/9a7f733ddb4ed91f48da64ac7f0f621c34aadd4d/`.

Audit ini mengunduh sumber dan bobot serta menghitung isi korpus. Belum ada pemasangan dependensi, pemuatan model, inferensi, pilot, data utama, atau hasil gerak suara baru.
