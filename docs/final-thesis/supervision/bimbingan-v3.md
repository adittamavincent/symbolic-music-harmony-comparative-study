# Ringkasan untuk bimbingan: naskah v3

Disusun 2 Oktober 2026 untuk dibawa bersama PDF BAB I–III. Satu halaman; rinciannya ada di `research/protocol.md`.

## Apa yang berubah dari proposal v2

| Proposal v2 | Naskah v3 | Alasan |
| --- | --- | --- |
| DeepBach, Coconet, NotaGen | DeepBach dan Coconet | NotaGen hanya menerima petunjuk periode, komponis, dan instrumentasi; tidak bisa diberi melodi yang harus dipertahankan |
| Empat tingkat kendali A–D | Asal melodi: sopran chorale Bach vs latihan melodi Strube | Tingkat kendali tidak setara antar-model (kondisi C dan D NotaGen identik) dan tidak berasal dari penelitian terdahulu |
| Tiga kaidah (kuint, oktaf, nada penuntun) | Lima kaidah dari rubrik Yan dkk. (2018), dirumuskan menurut Strube | Pemilihan kaidah kini mengikuti syarat tertulis; nada penuntun di sopran tidak dihasilkan model |
| Strube Score (rumus buatan sendiri) | Laju pelanggaran per birama, ditambah indeks berbobot rubrik Yan | Satuan per birama dipakai Huang dkk. (2019); bobot dari rubrik terbitan |

## Desain singkat

Penelitian ini melanjutkan analisis Bach Doodle (Huang dkk., 2019), yang menemukan bahwa kuint dan oktaf sejajar pada Coconet meningkat ketika melodi pengguna tidak menyerupai data latih. Di sini melodi yang sama diberikan kepada DeepBach dan Coconet. Melodinya berasal dari dua sumber: sopran chorale Bach dan latihan melodi Strube. Pelanggaran dihitung otomatis dengan music21, tanpa penilai manusia.

- **X1:** model. **X2:** asal melodi. **Y:** laju pelanggaran per birama untuk lima kaidah.
- **Uji:** Wilcoxon untuk perbandingan model (data berpasangan), Mann–Whitney untuk pengaruh asal melodi, koreksi Holm.
- **Sampel:** minimal 30 melodi per kelompok (analisis daya). Buku Strube hlm. 11–80 memuat 71 latihan melodi (latihan 67–68 dibaca dari terjemahan 2015 hlm. 58 karena hlm. 48 hilang dari scan 1928). Tiap melodi diharmonisasi lima kali per model, lalu dirata-rata.

## Dasar Strube (edisi 1928)

| Kaidah | Halaman | Rumusan yang dipakai |
| --- | --- | --- |
| Kuint sejajar | 9, 12 | Dilarang dalam penulisan ketat; gerak berlawanan tidak dihitung (hlm. 9) |
| Oktaf/unisono sejajar | 9, 12 | Sama; unisono termasuk |
| Jarak suara atas | 20 | S–A dan A–T lebih dari satu oktaf |
| Persilangan | 174 | Hanya yang melewati sopran; persilangan lain dibolehkan Strube |
| Tumpang tindih | 12–13 | Dihitung bila tidak ada suara yang bergerak melangkah |

## Yang sudah dikerjakan

- BAB I–III, judul, dan abstrak disesuaikan dengan desain ini.
- Instrumen versi 2 sudah dibuat dan diuji. Pada 345 dari 371 chorale Bach yang memenuhi syarat, hasilnya sama dengan fungsi music21 untuk persilangan dan tumpang tindih. Perbedaan untuk paralel hanya pada kasus gerak berlawanan, yang dibolehkan Strube. Laju Bach jauh di bawah laju Coconet yang dilaporkan Huang dkk.
- Inventaris latihan Strube 1–118 selesai.
- Format bersama untuk kedua model sudah dibuat: melodi masuk dan harmonisasi keluar sebagai MusicXML, dengan penerjemah tersendiri untuk DeepBach dan Coconet. Model belum dijalankan; pilot menunggu persetujuan desain.

## Pertanyaan untuk pembimbing

1. Apakah desain tanpa penilai manusia, judul baru, dan tiga pertanyaan penelitian dapat disetujui?
2. Apakah edisi 1928 tepat sebagai rujukan, atau terjemahan Indonesia 2015 (jilid I, terjemahan Bapak) sebaiknya ikut dikutip? Jilid I tidak memuat kaidah persilangan (1928 hlm. 174). Tiga kalimat berbeda antara kedua edisi: jarak sopran–alto, syarat gerak melangkah pada tumpang tindih, dan bas di atas tenor (rincian di `study/persiapan-pembimbing-1.md`).
3. Apakah Strube buku ajar mata kuliah harmoni di program studi? (Untuk alasan pemilihan sumber.)
4. Bagaimana aturan program studi tentang pengungkapan penggunaan alat bantu AI dalam penelitian dan penulisan?
5. Apakah format halaman depan sudah sesuai pedoman 2026?
