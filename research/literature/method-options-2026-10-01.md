# Pilihan pengukuran harmonisasi AI

Tanggal penelusuran: 1 Oktober 2026. Catatan diskusi dan sumber, belum merupakan protokol final atau perubahan instrumen. Naskah, kode evaluator, dan bibliografi tidak diubah oleh catatan ini.

## Arah yang dinyatakan peneliti

Peneliti ingin menilai bagian yang dihasilkan AI ketika sebagian suara diberikan sebagai soal. Sopran sebagai masukan adalah contoh yang dibahas, belum keputusan akhir untuk semua kondisi/model. Ketersediaan kendali harus diperiksa pada implementasi masing-masing model.

Usulan pengukuran: suara tetap tetap dibaca sebagai konteks. Pemeriksaan relasional yang melibatkan suara hasil generasi dan suara tetap dapat menjadi hasil evaluasi. Kejadian yang seluruh unsur relevannya berasal dari masukan tetap dicatat sebagai karakteristik soal, bukan kontribusi generasi. Ini usulan adaptasi peneliti, bukan aturan yang diklaim telah ditetapkan oleh sumber di bawah.

## Penelusuran

- Rencana OpenAlex ditambah dengan q12–q14 untuk suara tetap, rubrik harmonisasi, dan evaluasi tonal berbasis kaidah.
- Seluruh 14 query dijalankan melalui `uv run research/scripts/openalex_search.py --batch`. Semua gagal karena DNS; tidak ada rekaman OpenAlex yang berhasil diperoleh. Manifest kegagalan: `research/outputs/openalex/20261001T092917710683Z-batch/batch_manifest.json`.
- Penelusuran web tambahan: `chorale harmonization evaluation generated voices fixed soprano voice leading rule violations`; `automatic harmonization evaluation rule based evaluation leading tone resolution chorale`; `Ebcioglu CHORAL 1988 expert system harmonizing four part chorales 350 rules`; `Part-invariant Model Harmonization Yan Lustig 2018 pdf`.
- Sumber penting diperiksa pada teks asli, bukan disimpulkan dari judul atau hitungan sitasi. Penelusuran ini terarah, bukan tinjauan sistematis atau bukti ketiadaan penelitian lain.

## Sumber dan batas dukungannya

### Hadjeres, Pachet, dan Nielsen (2017), DeepBach

[Makalah PMLR](https://proceedings.mlr.press/v70/hadjeres17a/hadjeres17a.pdf), §2.3.2 dan §3.1: sopran dapat ditetapkan sementara alto, tenor, dan bas dihasilkan. Pada evaluasi mereka, sopran sama antar-model. Ini mendukung tugas harmonisasi dengan masukan tetap, bukan rumus skor kaidah penelitian ini.

### Yan, Lustig, VanderStel, dan Duan (2018)

[Makalah ISMIR](https://labsites.rochester.edu/air/publications/Yan2018partInvariant.pdf), §4.2, hlm. 208–209: evaluasi harmonisasi bas melibatkan pemeriksaan partitur oleh tiga mahasiswa doktoral teori musik dan tim pendengar terpisah. Penilai tidak mengetahui sumber keluaran. Ini preseden pengukuran berbasis rubrik dengan pemeriksa manusia, bukan evaluator otomatis Strube.

[Rubrik pelengkap](https://labsites.rochester.edu/air/projects/model0.md): 11 kategori, termasuk gerak paralel, resolusi, penggandaan nada, jarak suara, voice crossing, dan voice overlap. Resolusi nada penuntun dibatasi pada sopran; pada tugas evaluasi mereka bas adalah masukan. Rubrik ini kandidat adaptasi. Tidak boleh disebut rubrik Strube atau dianggap membenarkan tiga indikator lama secara otomatis.

### Chong dan Ding, eContact! 16.2

[Teks asli](https://www.econtact.ca/16_2/chong-ding_representation.html), bagian Modelling Tonal Harmony, Input Data, dan A Case for Declarative Rules: representasi dan kaidah dirancang mengikuti tujuan pedagogis. Masukan berupa angka Romawi membatasi masalah penentuan kunci dan nada non-akor. Mendukung pembatasan domain yang dijelaskan; tidak menyediakan instrumen MIDI SATB siap pakai untuk penelitian ini.

## Opsi yang dibawa ke pembimbing

1. Pemeriksaan manual dengan adaptasi rubrik terpublikasi. Dokumentasikan kategori yang dipakai, sumber musikal, konteks, pengecualian, dan kesepakatan pemeriksa.
2. Pemeriksaan gabungan: program menandai kandidat kejadian; manusia memeriksa status musikal. Ukur kesalahan program sebelum otomatisasi lebih luas.
3. Pemeriksaan otomatis terbatas pada kaidah terpilih. Cakupan klaim harus mengikuti indikator yang benar-benar didefinisikan dan divalidasi.

Rekomendasi diskusi: mulai dari opsi 1 atau 2 untuk menilai kebutuhan instrumen; jangan menetapkan jumlah indikator berdasarkan kode yang sudah ada. Keputusan adaptasi dan jumlah kaidah masih menunggu pembacaan Strube dan pembahasan dengan pembimbing/pengajar harmoni.

## Pseudocode

BAB III menjelaskan masukan, suara tetap/hasil generasi, definisi kejadian, konteks, pengecualian, dan penyebut. Pseudocode rinci dapat ditempatkan pada lampiran dengan versi instrumen dan rujukan kode. Pseudocode yang dirancang peneliti harus diatribusikan sebagai rancangan tersebut; adaptasi algoritma orang lain harus menyebut sumber dan perubahan.

Skema keputusan awal, belum algoritma tervalidasi:

```text
Masukan: soal, keluaran, identitas suara tetap, spesifikasi kaidah
Periksa apakah keluaran mempertahankan bagian soal; catat kegagalannya
Untuk setiap kejadian yang sesuai domain suatu kaidah:
    Jika seluruh unsur yang dinilai berasal dari soal, catat pada kelompok masukan
    Selain itu, periksa menggunakan konteks lengkap dan pengecualian yang ditetapkan
    Jika konteks belum dapat diputuskan, catat sebagai belum dapat dinilai
    Simpan lokasi, suara yang terlibat, alasan, dan status pemeriksaan
Ringkas setiap kaidah menggunakan penyebut yang telah dijustifikasi
```

Pada masukan sopran tetap, resolusi sopran sendiri tidak menjadi hasil generasi utama. Relasi S–A, S–T, dan S–B tetap relevan. Pada masukan S dan B tetap, relasi S–B dicatat sebagai masukan; S–A, S–T, A–T, A–B, dan T–B melibatkan bagian yang dihasilkan. Penggantian indikator resolusi sopran ke suara lain memerlukan dasar musikal baru, bukan perubahan nama otomatis.

Penelitian baru tidak perlu memiliki pendahulu identik untuk dapat dilakukan. Rujukan mendukung konsep, memperjelas perbedaan dari penelitian terdahulu, dan membantu memilih metode. Pilihan baru harus dijustifikasi dan diperiksa; keberadaan penelitian terdahulu tidak otomatis memvalidasi adaptasi.
