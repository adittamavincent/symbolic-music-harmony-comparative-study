# Paket audit 3 Oktober 2026

Paket ini dibuat terpisah dari naskah karena peneliti menyatakan chat lain masih mengedit Bab I–III. Usulan belum diterapkan ke bab, bibliografi, protokol, atau instrumen oleh audit ini.

| Berkas | Isi |
| --- | --- |
| [AUDIT.md](AUDIT.md) | 39 temuan dengan prioritas, bukti, akibat, dan tindakan |
| [usulan-revisi-bab-1-3.md](usulan-revisi-bab-1-3.md) | Paragraf pengganti dan keputusan metode yang perlu diselaraskan |
| [simulasi-sidang.md](simulasi-sidang.md) | 72 pertanyaan, susulan, 16 cabang hasil/kegagalan, sembilan alternatif metode, dan tiga latihan dialog |
| [citation-checks.csv](citation-checks.csv) | Inventaris 50 kunci sitasi aktif dan satu kandidat, status pemeriksaan, serta batas dukungan |
| [citation-inventory.json](citation-inventory.json) | Waktu dan hash berkas ketika inventaris sitasi diperiksa |
| [probes.py](probes.py) | Lima skenario sintetis untuk menunjukkan perilaku program tanpa mengubah instrumen |
| [probe-results.json](probe-results.json) | Hasil probe, versi music21, dan hash instrumen |
| [baseline.json](baseline.json) | Identitas berkas pada snapshot awal laporan |

Mulai dari tabel prioritas dalam AUDIT.md, kemudian baca usulan revisi yang merujuk ID temuan. Gunakan simulasi sidang setelah keputusan metode sesuai dengan naskah dan pekerjaan sebenarnya. Jawaban yang mengakui bukti belum tersedia harus diperbarui hanya setelah bukti itu ada.

Pencarian literatur memakai rencana `research/literature/openalex_queries.json` yang diperbarui pada audit ini. Seluruh 21 kueri berjalan dan menghasilkan 532 rekaman unik di `research/outputs/openalex/20261003T070513511032Z-batch/`. Hasil tersebut belum merupakan 532 sumber yang dibaca atau disaring penuh; bibliografi bersama tidak ditambah otomatis.

Pemeriksaan mengikuti `docs/final-thesis/eval.md`: klaim dibedakan dari keputusan peneliti, pekerjaan rencana dibedakan dari hasil, angka menyebut sumber dan penyebut, serta usulan menyertakan penjelasan perubahan. Tidak ada kesimpulan data utama yang dibuat.
