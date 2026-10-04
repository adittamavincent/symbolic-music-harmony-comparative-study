# Melodi latihan Strube yang diketik

Folder ini berisi satu berkas teks untuk setiap kandidat melodi latihan dalam buku Strube (1928), hlm. 11–80. Daftar kandidat berasal dari `../strube-exercise-inventory.csv` (71 baris dengan `given_voice = soprano` dan `eligible = candidate`). Berkas dibuat kosong oleh `make melody-templates`; isinya diketik peneliti dari cetakan.

Berkas teks ini adalah data penelitian. Scan buku tetap berada di folder `references/` yang tidak masuk Git.

## Cara mengetik

Buka berkas, misalnya `strube1928-ex012.txt`, lalu isi kolom yang kosong:

```text
kode: strube1928-ex012
sumber: Strube 1928, hlm. 17, latihan 12 (PDF hlm. 23)
kunci: 1
mode: major
birama: 4/4
anakan: 0
nada: G4:1 A4:1 B4:1 C5:1 | B4:2 A4:2 | G4:4!
```

Contoh di atas hanya menunjukkan format; nadanya bukan isi latihan 12.

| Kolom | Isi |
| --- | --- |
| `kunci` | Jumlah kres (positif) atau mol (negatif) pada tanda kunci. Tanpa tanda kunci: `0`. Dua mol: `-2`. |
| `mode` | `major` atau `minor`, menurut tangga nada latihan. |
| `birama` | Tanda birama seperti tercetak, misalnya `4/4`, `3/4`, `6/8`. Tanda C ditulis `4/4`. |
| `anakan` | Panjang birama gantung (*anacrusis*) dalam ketukan seperempat. Tanpa birama gantung: `0`. Satu ketukan seperempat: `1`. Satu seperdelapan: `0.5`. |
| `nada` | Nada demi nada, dipisahkan spasi; garis birama ditulis `|`. |

Setiap nada ditulis `NADA:DURASI`.

- `NADA`: huruf, tanda alterasi bila tercetak, lalu oktaf. C4 adalah C tengah, C5 satu oktaf di atasnya. Tanda alterasi: `#` kres, `##` kres ganda, `b` mol, `bb` mol ganda, `n` pugar. Nada tanpa tanda alterasi otomatis mengikuti tanda kunci, dan tanda alterasi yang tercetak berlaku sampai garis birama untuk huruf dan oktaf yang sama, seperti membaca partitur.
- `DURASI` dalam ketukan seperempat: `4` not penuh, `2` not setengah, `1` not seperempat, `0.5` not seperdelapan, `0.25` not seperenam belas, `3` not setengah bertitik, `1.5` not seperempat bertitik.
- Tanda diam: `r:DURASI`.
- Fermata: tambahkan `!` setelah durasi, misalnya `G4:2!`.
- Ikatan (*tie*): tambahkan `~` setelah durasi nada pertama, misalnya `D5:2~ | D5:1`. Nada berikutnya harus sama.

Setiap birama penuh harus berjumlah sesuai tanda birama. Birama pertama harus sama dengan `anakan` bila `anakan` bukan 0. Birama terakhir boleh lebih pendek.

## Memeriksa hasil ketikan

Dari root repositori:

```bash
make melodies
```

Perintah ini membaca semua berkas, membuat MusicXML di `research/outputs/melodies/strube/`, dan menulis status setiap latihan di `research/outputs/melodies/manifest.csv`. Kesalahan format ditampilkan dengan nomor birama dan nomor nadanya. Kolom kunci, mode, birama, panjang, nilai terpendek, dan fermata pada inventaris diisi otomatis dari ketikan yang lolos.

Setelah lolos, bandingkan kembali dengan cetakan: buka berkas MusicXML di MuseScore, cocokkan nada demi nada, lalu isi kolom `typed_by` dan `checked_against_print_date` pada inventaris. Latihan 67 dan 68 dibaca dari terjemahan 2015 (hlm. 58) karena hlm. 48 hilang dari scan 1928; cocokkan dengan buku cetak 1928 bila tersedia.
