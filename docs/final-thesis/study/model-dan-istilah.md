# Model dan istilah dengan bahasa sederhana

Disusun 3 Oktober 2026 untuk peneliti, diperbarui 5 Oktober 2026 untuk naskah v4. Berkas ini bahan belajar, bukan bagian naskah. Isinya menjelaskan cara kerja DeepBach dan Coconet serta istilah teknis di BAB I–III dengan perumpamaan "bayangkan kamu yang mengerjakannya". Perumpamaan membantu memahami, tetapi jangan dipakai sebagai kalimat naskah. Untuk naskah dan sidang, pakai istilah di BAB II dan BAB III.

Fakta tentang kode diambil dari catatan di awal `research/harmonization_io.py`, `research/protocol.md`, dan `records/reading-notes.csv` (dibaca dari kode sumber pada 2–4 Oktober 2026). Fakta tentang makalah diambil dari Hadjeres dkk. (2017) dan Huang dkk. (2017). Bagian 9 mencatat angka yang belum diperiksa dan karena itu jangan diucapkan.

Urutan belajar seluruh folder ada di [researcher-guide.md](researcher-guide.md). Berkas ini dibaca setelah gambaran besar di sana. Pertanyaan sidang tentang model ada di [defense-qa.md](defense-qa.md) Q20–Q24, Q41b, Q69, Q74, Q103, Q112, dan Q113, ditambah bagian 8 berkas ini.

## 1. Gambaran besar: model tidak tahu kaidah Strube

Bayangkan seorang mahasiswa yang tidak pernah membaca buku harmoni. Ia hanya menyalin ratusan chorale Bach berulang-ulang sampai punya "rasa": setelah akor ini biasanya akor itu, bas biasanya bergerak begini, alto jarang melompat jauh. Lalu ia diberi soal: melodi sopran, isi alto, tenor, dan bas.

Itulah DeepBach dan Coconet. Keduanya:

- **tidak diberi kaidah.** Tidak ada baris program yang berkata "jangan kuint sejajar". Kalau model jarang membuat kuint sejajar, itu karena Bach jarang membuatnya, jadi peluang pola itu kecil.
- **menebak dengan peluang.** Untuk setiap tempat kosong, model menghitung peluang setiap nada, misalnya G 60 persen, E 25 persen, C 10 persen. Lalu model "mengocok dadu" sesuai peluang itu. Nada berpeluang kecil kadang tetap terpilih.
- **memberi hasil berbeda setiap kali dijalankan**, karena ada pengocokan dadu. Itu sebabnya setiap melodi diharmonisasi lima kali dan hasilnya dirata-rata (BAB III, Sampel).

Konsekuensinya bagi penelitian: pertanyaannya bukan "apakah model tahu kaidah", melainkan "seberapa sering pola yang dipelajari dari Bach menghasilkan gerak yang dilarang Strube, terutama ketika soalnya bukan dari Bach".

### Kata dasar

| Istilah | Artinya | Bayangkan |
| --- | --- | --- |
| Jaringan saraf tiruan (*neural network*) | Rumus besar dengan jutaan angka yang dapat disetel | Mesin dengan jutaan kenop kecil |
| Bobot atau parameter | Angka-angka yang disetel itu | Posisi setiap kenop |
| Pelatihan (*training*) | Menyetel bobot dengan cara menebak, dibandingkan dengan jawaban Bach, lalu dikoreksi sedikit, diulang jutaan kali | Latihan soal dengan kunci jawaban; setiap salah, kebiasaanmu bergeser sedikit |
| *Deep learning* | Jaringan saraf dengan banyak lapisan | Banyak tahap pengolahan, dari pola kecil ke pola besar |
| Data latih | Contoh yang dipakai untuk pelatihan, di sini chorale Bach | Buku kumpulan chorale yang kamu salin |
| *Checkpoint* | Berkas berisi bobot hasil pelatihan | "Otak" yang sudah jadi dan disimpan. Model yang diuji selalu berarti checkpoint tertentu |
| Generasi atau *sampling* | Memakai model yang sudah terlatih untuk membuat musik baru | Mengerjakan soal ujian setelah selesai belajar |

## 2. DeepBach: kamu dengan pensil dan penghapus kecil

### Cara DeepBach "melihat" partitur

Partitur dipotong menjadi langkah seperenam belas. Pada setiap langkah, setiap suara diberi satu simbol (token):

- nama nada dengan oktaf, misalnya `G4` atau `F#3`. Ejaannya disimpan, jadi F♯ dan G♭ adalah simbol berbeda;
- `__` artinya "nada sebelumnya masih ditahan";
- `rest` untuk tanda diam.

Selain itu ada baris informasi tambahan (*metadata*): letak fermata, posisi dalam ketukan, tangga nada, dan nomor suara.

Bayangkan kertas kotak-kotak dengan empat baris (S, A, T, B). Setiap kotak berisi satu kata: `G4`, `__`, `__`, `__`, `A4`, `__`, dan seterusnya. Di bawahnya ada baris kecil yang mencatat "di sini fermata" dan "ini ketukan pertama".

Setiap suara mempunyai daftar kata sendiri (kosakata) yang hanya berisi nada yang pernah muncul pada suara itu di data latih. Melodi yang memuat nada atau ejaan di luar kosakata sopran tidak dapat dimasukkan. Itulah arti "kosakata DeepBach" di PROGRESS.md.

### Otak DeepBach

Untuk menebak satu kotak, misalnya alto pada langkah ke-37, DeepBach memakai tiga "pembaca" sekaligus:

1. **LSTM dari kiri** membaca semua suara dari awal sampai tepat sebelum langkah 37. Ia meringkas "apa yang sudah terjadi".
2. **LSTM dari kanan** membaca dari akhir mundur sampai tepat sesudah langkah 37. Ia meringkas "apa yang akan datang".
3. **Jaringan biasa** melihat suara lain pada langkah 37 itu sendiri, misalnya sopran, tenor, dan bas yang berbunyi bersamaan.

Ketiga ringkasan digabung, lalu keluar daftar peluang untuk setiap kata dalam kosakata alto. Ada empat jaringan seperti ini, satu untuk setiap suara.

Bayangkan kamu mengisi satu nada alto. Tangan kirimu menunjuk birama sebelumnya, tangan kananmu menunjuk birama sesudahnya, dan matamu melihat nada lain yang berbunyi pada ketukan itu. Dari ketiganya kamu memutuskan nada alto.

### Apa itu LSTM

RNN (*recurrent neural network*, jaringan rekuren) membaca deretan satu langkah demi satu langkah sambil membawa catatan ringkas tentang yang sudah dibaca. RNN biasa cepat lupa: catatan tentang birama jauh di belakang memudar. LSTM (*Long Short-Term Memory*) adalah RNN yang punya tiga "gerbang" untuk mengatur catatannya:

- gerbang lupa: bagian catatan mana yang dihapus;
- gerbang masuk: informasi baru mana yang ditulis;
- gerbang keluar: bagian catatan mana yang dipakai untuk langkah sekarang.

Bayangkan kamu membaca partitur birama demi birama sambil memegang kertas tempel. Ketika modulasi selesai, kamu mencoret catatan "sedang di dominan". Ketika ada fermata, kamu menulis "kadens di sini". Ketika menentukan nada berikutnya, kamu melirik catatan yang relevan saja. LSTM melakukan hal itu dengan angka.

### Cara DeepBach belajar

Ambil chorale Bach, sembunyikan satu nada, minta jaringan menebaknya dari sekelilingnya, bandingkan dengan nada asli Bach, lalu setel bobot sedikit. Ulangi untuk jutaan nada. Bayangkan latihan "tebak nada yang ditutup kertas" pada ratusan chorale.

### Cara DeepBach membuat harmonisasi: *pseudo-Gibbs sampling*

1. Sopran diisi melodi soal dan dikunci. Alto, tenor, dan bas diisi acak.
2. Pilih acak satu kotak yang tidak dikunci, misalnya tenor langkah 12.
3. Tanya jaringan tenor: dengan sekeliling seperti ini, berapa peluang setiap nada?
4. Kocok dadu sesuai peluang itu, tulis nadanya.
5. Ulangi langkah 2–4 berkali-kali. Kode resminya bawaan 500 putaran, dan setiap putaran mengganti beberapa kotak per suara sekaligus (bawaan 8).

Bayangkan kamu memulai dengan coretan asal, lalu berulang kali menunjuk satu nada secara acak, melihat sekelilingnya, dan menghapus serta menulis ulang nada itu bila ada pilihan yang lebih cocok. Lama-lama harmonisasinya "masuk akal" di setiap tempat.

**Kenapa "pseudo" (semu)?** Gibbs sampling sejati adalah metode statistik yang terbukti menghasilkan sampel dari satu distribusi peluang bersama, asalkan semua tebakan per posisi berasal dari distribusi yang sama dan konsisten. Pada DeepBach, keempat jaringan dilatih terpisah, jadi tebakan jaringan alto dan jaringan tenor tidak dijamin "sepakat" secara matematis. Karena jaminannya tidak ada, pengembangnya menyebutnya *pseudo-Gibbs*. Dalam praktik cara ini tetap menghasilkan chorale yang meyakinkan.

**Kelebihan cara ini dibanding menulis dari kiri ke kanan:** pengguna dapat mengunci kotak mana saja (batasan posisi), misalnya sopran atau kadens. Model yang hanya menulis dari kiri ke kanan tidak bisa "melihat" nada di depan yang sudah ditentukan.

## 3. Coconet: kamu dengan kertas *piano roll* dan penghapus besar

### Cara Coconet "melihat" partitur

Coconet memakai *piano roll*: kotak-kotak dengan sumbu waktu (langkah seperenam belas) dan sumbu tinggi nada (46 nada, MIDI 36–81, yaitu C2 sampai A5). Kotak diisi bila nada berbunyi. Ada empat lembar seperti ini, satu per suara. Ada juga lembar *mask* yang menandai kotak mana yang sudah diberikan dan mana yang harus diisi.

Bayangkan kertas grafik seperti layar piano di aplikasi DAW. Setiap suara punya warna sendiri, dan nada adalah garis mendatar.

Akibat penting: *piano roll* hanya mencatat "nada ini berbunyi pada langkah ini". Nada G yang ditahan dua ketukan dan dua nada G berturut-turut terlihat sama. Itu sebabnya keluaran Coconet tidak pernah mengulang nada pada alto, tenor, dan bas (defense-qa Q41b). Tidak ada ejaan nada: F♯ dan G♭ sama.

### Otak Coconet: jaringan konvolusional (CNN)

Konvolusi adalah "jendela kecil" yang digeser ke seluruh kertas. Pada setiap posisi, jendela memeriksa pola kecil, misalnya dua nada berjarak tertentu atau nada yang naik lalu turun. Jaringan Coconet menumpuk banyak lapisan seperti ini. Lapisan awal mengenali pola kecil; lapisan berikutnya menggabungkannya menjadi pola yang lebih luas.

Bayangkan kamu memeriksa partitur dengan kaca pembesar kecil yang digeser ke mana-mana. Pada putaran pertama kamu hanya mencatat interval dan langkah kecil. Pada putaran berikutnya kamu membaca catatanmu sendiri dan mulai melihat akor, lalu progresi, lalu frasa.

Coconet menebak semua kotak kosong sekaligus untuk keempat suara, bukan satu per satu.

### Cara Coconet belajar: *orderless NADE*

**NADE** (*Neural Autoregressive Distribution Estimator*) menghitung peluang satu karya utuh sebagai rangkaian tebakan berurutan: peluang nada pertama, lalu peluang nada kedua bila nada pertama sudah diketahui, dan seterusnya. Bayangkan kamu mendikte chorale nada demi nada dalam urutan yang selalu sama.

**Orderless** artinya urutannya tidak tetap. Saat pelatihan, Coconet mengambil chorale Bach, menghapus bagian acak (kadang satu suara, kadang potongan waktu, kadang kotak berserakan), lalu belajar menebak yang dihapus dari yang tersisa. Karena pola hapusannya berganti terus, model belajar mengisi bagian mana pun dari bagian mana pun.

Bayangkan gurumu setiap hari menyerahkan chorale yang sebagian dihapus dengan cara berbeda: hari ini bas hilang, besok alto dan tenor di birama 3–5, lusa hanya sopran yang tersisa. Setelah ribuan latihan, kamu bisa melengkapi chorale dari sisa apa pun. Itu sebabnya Coconet dapat menerima sopran saja lalu mengisi tiga suara lain.

### Cara Coconet membuat harmonisasi: *blocked Gibbs sampling*

1. Sopran diisi dan dikunci. Model membuat tebakan pertama untuk alto, tenor, dan bas.
2. Hapus satu blok acak dari nada alto, tenor, dan bas.
3. Isi ulang semua yang dihapus sekaligus dengan tebakan model, sambil mengocok dadu.
4. Ulangi. Mula-mula yang dihapus banyak, lalu makin sedikit (*annealing*). Magenta.js memakai bawaan 96 putaran.

Bayangkan kamu membuat sketsa kasar seluruh harmonisasi, lalu menghapus potongan besar dan menulis ulang, lalu menghapus potongan yang lebih kecil, sampai akhirnya hanya merapikan satu-dua nada.

Pengembang Coconet melaporkan bahwa cara ini menghasilkan musik yang lebih baik daripada mengisi kotak satu per satu dalam urutan tetap. Alasannya, kesalahan di awal masih bisa dihapus dan diperbaiki pada putaran berikutnya.

**Beda *blocked Gibbs* dan *pseudo-Gibbs*:** DeepBach mengganti sedikit kotak sekaligus berdasarkan sekelilingnya. Coconet mengganti satu blok yang bisa besar sekaligus, dan ukuran blok mengecil. Keduanya sama-sama "tulis, hapus sebagian, tulis ulang" berkali-kali.

## 4. Ringkasan perbedaan

| Aspek | DeepBach | Coconet |
| --- | --- | --- |
| Bentuk partitur | Token per suara per langkah, dengan ejaan nada, simbol tahan `__`, dan metadata fermata, ketukan, tangga nada | *Piano roll* per suara; tanpa ejaan, tanpa beda nada ditahan dan nada diulang |
| Jaringan | LSTM dari kiri dan dari kanan, ditambah jaringan untuk suara serentak; satu jaringan per suara | Jaringan konvolusional untuk keempat suara sekaligus |
| Cara belajar | Tebak satu nada dari sekelilingnya | Tebak bagian yang dihapus acak (*orderless NADE*) |
| Cara mengisi | *Pseudo-Gibbs*: ganti sedikit kotak berulang-ulang | *Blocked Gibbs*: hapus blok yang makin kecil, isi ulang sekaligus |
| Pengaturan bawaan | 500 putaran, *temperature* 1,0 | 96 putaran, *temperature* 0,99 |
| Batas masukan sopran | Kosakata sopran dan wilayahnya | MIDI 36–81 untuk setiap suara |
| Data latih | Chorale Bach dari korpus music21, dengan transposisi; kode resminya membagi data berurutan 85/10/5 | Versi data chorale Bach yang lain (Huang dkk. 2017, hlm. 212); pembagian data checkpoint `coconet/bach` tidak didokumentasikan |
| Implementasi yang dipakai | Kode PyTorch resmi pengembangnya, commit `6d75cb9` | Magenta.js 1.23.1, checkpoint `coconet/bach` |
| *Seed* | Setiap percobaan diberi *seed* tercatat | Magenta.js tidak menyediakan *seed*; keluaran mentah disimpan |
| Evaluasi oleh pengembang | Tebakan pendengar "*Bach or Computer*" | *Log-likelihood* dan penilaian pendengar |
| Kaitan dengan Bach Doodle | Tidak ada | Model yang dianalisis Huang dkk. 2019; checkpoint yang dipakai tidak diklaim identik dengan model produksinya (Q23) |

Tabel ini adalah lima dimensi Briot dkk. (BAB II.B.1) dalam praktik. Tujuannya sama: mengisi alto, tenor, dan bas untuk sopran yang diberikan. Representasi (baris "Bentuk partitur"), arsitektur ("Jaringan"), dan strategi ("Cara mengisi") berbeda, dan data latihnya juga berbeda. Dimensi kelima, tantangan (sifat yang diharapkan dari hasil, misalnya dapat dikendalikan), tidak dibandingkan di BAB II.

## 5. Kenapa model tetap melanggar kaidah walau belajar dari Bach

Ini penjelasan yang mungkin, bukan temuan penelitian. Penelitian ini tidak menguji penyebabnya satu per satu.

1. Model tidak diberi kaidah, hanya pola peluang.
2. Bach sendiri kadang melanggar. Huang dkk. menghitung 0,023 kuint dan 0,009 oktaf sejajar per birama pada chorale Bach.
3. Pengocokan dadu kadang memilih nada berpeluang kecil.
4. Setiap tebakan melihat sekeliling, tetapi tidak ada pemeriksa akhir yang memastikan seluruh hasil bebas kesalahan.
5. Bila melodi tidak menyerupai data latih (*out of distribution*), peluang yang dipelajari kurang cocok. Inilah gagasan Huang yang diuji ulang lewat pertanyaan 3 di v4, dengan teori pergeseran *dataset* Storkey (2008): aturan yang benar tidak berubah, tetapi model hanya mendekati aturan itu dari contoh yang pernah dilihatnya. Di v5 semua melodi berasal dari chorale Bach, dan pertanyaan 3 diganti letak pelanggaran dalam frasa, jadi gagasan ini tidak diuji lagi.
6. Bentuk partitur membatasi hasil, misalnya Coconet tidak dapat menulis nada yang diulang. Pengaruhnya diperiksa dengan analisis sensitivitas d (Q113).

## 6. Kenapa hasil tidak boleh disebut "LSTM lebih baik daripada CNN"

Bayangkan dua mahasiswa yang berbeda guru, berbeda buku kumpulan chorale, berbeda cara mencatat partitur, dan berbeda cara mengerjakan ujian. Bila nilai mereka berbeda, kamu tidak bisa menyimpulkan bahwa perbedaannya karena "jenis otak" mereka.

DeepBach dan Coconet berbeda dalam semua hal itu sekaligus: data latih, bentuk partitur, jaringan, cara belajar, cara mengisi, dan pengaturan generasi. Kesimpulan yang sah hanya: checkpoint DeepBach yang diuji lebih atau kurang patuh daripada checkpoint Coconet yang diuji, pada melodi yang diuji (BAB II.B.1, Briot dkk.; BAB III Metode Pendekatan; defense-qa Q5, Q22, dan Q103).

Sebaliknya, pada pertanyaan 3 model yang sama menerima dua kelompok melodi. Yang berubah hanya masukannya, sehingga perbedaan dapat dibaca sebagai pengaruh asal melodi pada model itu.

## 7. Kamus istilah

### Model dan pembuatan musik

| Istilah | Penjelasan sederhana |
| --- | --- |
| Model generatif | Program yang belajar dari contoh lalu membuat contoh baru yang mirip |
| Musik simbolik | Musik sebagai daftar nada, durasi, dan suara, bukan rekaman bunyi |
| Distribusi peluang | Daftar kemungkinan beserta peluangnya, misalnya G 60%, E 25%, C 10% |
| *Softmax* | Langkah terakhir jaringan yang mengubah skor mentah menjadi peluang berjumlah 100% |
| *Temperature* | Kenop keberanian. Di bawah 1 model lebih condong ke nada yang paling mungkin; di atas 1 model lebih sering memilih nada yang jarang |
| *Seed* | Angka awal pengocok dadu. *Seed* yang sama memberi kocokan yang sama, jadi hasil bisa diulang. Sampel utama memakai *seed* 20261004; uji coba memakai 41004 |
| Iterasi atau putaran | Satu kali siklus "hapus dan isi ulang" |
| Token dan kosakata | Satu simbol dan daftar semua simbol yang dikenal model |
| `OOR` | Simbol DeepBach untuk nada di luar wilayah suara. Bila muncul di keluaran, hasil dianggap gagal |
| *Mask* | Lembar penanda kotak yang diberikan dan kotak yang harus diisi |
| Batasan posisi (*positional constraint*) | Kotak yang dikunci pengguna, misalnya sopran |
| *Music inpainting* | Mengisi bagian partitur yang kosong. Harmonisasi sopran termasuk tugas ini |
| Autoregresif atau kiri ke kanan | Menulis nada berurutan dari awal sampai akhir, tanpa kembali |
| Gibbs sampling | Metode statistik: ganti satu bagian berdasarkan bagian lain, ulangi sampai stabil |
| *Annealing* | Mengurangi ukuran perubahan sedikit demi sedikit, dari kasar ke halus |
| *Log-likelihood* | Seberapa besar peluang yang diberikan model kepada chorale Bach asli yang belum pernah dilihatnya. Makin tinggi, makin model "tidak kaget" melihat musik Bach. Ukuran ini tidak memeriksa kaidah |
| *Out of distribution* | Masukan yang tidak menyerupai data latih. Bayangkan mahasiswa yang hanya belajar chorale lalu diberi soal dengan lompatan aneh |
| Data latih, validasi, evaluasi | Bagian data untuk belajar, untuk memantau saat belajar, dan untuk ujian akhir. Kode DeepBach membaginya 85/10/5 secara berurutan |
| Menghafal (*overfitting*) | Model terlalu cocok dengan data latih sehingga bagus pada yang pernah dilihat dan buruk pada yang baru. Alasan status latih setiap melodi Bach dicatat |
| Uji diskriminasi | Pendengar menebak "ini Bach atau komputer". Cara DeepBach dievaluasi |
| *Transformer* dan *attention* | Jenis jaringan yang membandingkan setiap token dengan semua token lain sekaligus. Dipakai NotaGen dan banyak model baru; tidak dipakai kedua model dalam penelitian ini |

### Data dan instrumen

| Istilah | Penjelasan sederhana |
| --- | --- |
| Nomor nada MIDI | 60 = C4. Selisih 12 = oktaf, 7 = kuint murni |
| MusicXML | Format partitur yang menyimpan ejaan nada, fermata, tangga nada, dan birama (Q41a) |
| Adapter | Penerjemah dari MusicXML ke bentuk yang dimengerti setiap model, dan sebaliknya |
| Satuan not seperenam belas (kuantisasi) | Waktu dipotong menjadi langkah seperenam belas, resolusi kedua model |
| Pemetaan suara | Memastikan nada mana milik sopran, alto, tenor, dan bas sebelum diperiksa |
| Peristiwa bunyi | Titik ketika sedikitnya satu dari dua suara yang dibandingkan memulai nada baru |
| Definisi operasional | Rumus pasti tentang apa yang dihitung. Kaidahnya dari Strube, rumusnya dari peneliti |
| music21 | Pustaka Python untuk membaca dan menganalisis partitur |
| `VoiceLeadingQuartet` | Fungsi music21 untuk memeriksa gerak empat suara. Dipakai sebagai pemeriksa silang |
| Kejadian yang ditandai | Satu tempat di partitur yang memenuhi rumus pelanggaran. Belum tentu kesalahan musikal |
| Pelanggaran per birama | Jumlah kejadian satu kaidah dibagi jumlah birama melodi masukan; birama gantung dihitung satu birama. Ukuran Y |
| Indeks penalti tertimbang | Ringkasan kelima kaidah dengan bobot rubrik Yan: 1 untuk kuint dan oktaf, 0,5 untuk tiga kaidah lain. Hanya ringkasan tambahan |
| Uji perangkat lunak, validitas, reliabilitas | Program berjalan sesuai harapan; hasilnya mengukur kaidah yang dimaksud; hasilnya sama bila diulang |
| *Preflight* | Pemeriksaan apakah setiap melodi bisa diubah ke format masukan kedua model, tanpa menjalankan model. Melodi yang ditolak dicatat tidak layak |
| Uji coba (*pilot*) | Tiga melodi Bach di luar sampel utama dan tiga melodi Strube, untuk menemukan masalah teknis. Hasilnya tidak dipakai menjawab pertanyaan |
| Kontrol kualitas | Syarat harmonisasi layak dianalisis: empat suara terpisah, satu nada per suara pada satu waktu, semua nada pada satuan seperenam belas, sopran dan panjang sama dengan melodi, setiap suara buatan model berbunyi |
| `copy_share` | Bagian langkah waktu ketika model membunyikan nada alto, tenor, dan bas yang sama persis dengan Bach pada melodi Bach. Tanda kemungkinan model menghafal (Q87) |
| `quarters` | Panjang melodi dalam ketukan seperempat, untuk menghitung pelanggaran per ketukan bila diperlukan (Q91) |

### Teori di BAB II

Penjelasan lengkap dengan perumpamaan ada di [researcher-guide.md](researcher-guide.md) bagian 2.

| Istilah | Penjelasan sederhana | Sumber |
| --- | --- | --- |
| Lima dimensi | Tujuan, representasi, arsitektur, tantangan, dan strategi sebuah sistem pembuat musik | Briot dkk. 2020, hlm. 11–13 |
| Pergeseran *dataset* | Data saat model dipakai berbeda dari data saat model dilatih | Storkey 2008 |
| Pergeseran kovariat | Hanya sebaran masukan yang berubah; hubungan masukan dan keluaran yang benar tetap sama | Storkey 2008 |
| Model gaya | Program yang meniru gaya tertentu, misalnya chorale Bach. Dinilai dengan memeriksa karya barunya lewat prosedur eksplisit | Pearce dkk. 2002 |
| *Grand theory* | Teori paling umum yang menaungi penelitian. Di sini harmoni tonal fungsional | Strube 1928, Preface dan hlm. 6 |
| Fusi nada | Unisono, oktaf, dan kuint murni cenderung terdengar menyatu | Huron 2001, hlm. 19 |
| Ko-modulasi nada | Nada yang bergerak searah cenderung terdengar menyatu | Huron 2001, hlm. 31 |
| Kedekatan nada | Telinga mengikuti satu suara lewat nada yang berdekatan | Huron 2001, hlm. 24 |
| Penyamaran minimum | Nada yang berbunyi bersama paling sedikit saling menutupi bila suara bawah berjarak lebih lebar | Huron 2001, hlm. 18 |

### Statistik

| Istilah | Penjelasan sederhana | Tanya-jawab |
| --- | --- | --- |
| Median dan rentang antarkuartil | Nilai tengah dan lebar separuh data di tengah. Tahan terhadap nilai ekstrem | — |
| Uji non-parametrik | Uji yang membandingkan urutan peringkat, bukan rata-rata, sehingga tidak perlu data normal | Q42 |
| Wilcoxon bertanda | Untuk data berpasangan: melodi yang sama, dua model | Q43, Q75 |
| Mann–Whitney | Untuk dua kelompok berbeda: melodi Bach dan melodi Strube | Q43 |
| Satu arah dan dua arah | Satu arah bila arah perbedaan sudah diperkirakan sebelum data ada | Q44 |
| Nilai *p* dan taraf 0,05 | Peluang mendapat perbedaan sebesar itu bila sebenarnya tidak ada perbedaan. Di bawah 0,05 dianggap signifikan | — |
| Koreksi Holm | Menyesuaikan batas signifikansi karena lima kaidah diuji sekaligus | Q45 |
| Ukuran efek (korelasi peringkat biserial) | Seberapa besar perbedaannya, bukan hanya ada atau tidak | Q48 |
| Analisis daya | Menghitung jumlah sampel minimum agar efek besar terdeteksi | Q25 |
| Analisis sensitivitas | Mengulang uji dengan cara hitung lain (tanpa fermata, data latih DeepBach, hanya melodi dengan lima harmonisasi layak, nada sama berurutan disatukan) untuk melihat apakah kesimpulan berubah | Q34, Q113 |
| Tidak signifikan ≠ setara | Gagal menemukan perbedaan bukan bukti kesamaan | Q46 |

## 8. Pertanyaan latihan tentang model

Pertanyaan ini melengkapi defense-qa Q20–Q24, Q41b, Q69, Q74, Q103, Q112, dan Q113.

**M1. Jelaskan DeepBach dalam satu kalimat.**
DeepBach menebak setiap nada dari nada sebelum, sesudah, dan yang berbunyi bersamaan memakai jaringan LSTM, lalu mengisi harmonisasi dengan berulang kali mengganti nada secara acak (*pseudo-Gibbs sampling*).

**M2. Jelaskan Coconet dalam satu kalimat.**
Coconet dilatih melengkapi chorale yang sebagian dihapus secara acak memakai jaringan konvolusional (*orderless NADE*), lalu mengisi harmonisasi dengan berulang kali menghapus dan mengisi ulang blok nada (*blocked Gibbs sampling*).

**M3. Apakah model diberi kaidah harmoni?**
Tidak. Keduanya hanya belajar dari chorale Bach. Kepatuhan yang terlihat berasal dari pola dalam data, bukan dari kaidah yang ditulis dalam program. Karena itu kepatuhan perlu diukur, tidak bisa diandaikan.

**M4. Kenapa satu melodi diharmonisasi lima kali?**
Kedua model memilih nada dengan pengocokan acak, sehingga melodi yang sama memberi hasil berbeda. Satu kali generasi bisa kebetulan baik atau buruk. Lima hasil dirata-rata menjadi satu nilai per melodi per model, dan tidak dihitung sebagai lima sampel (Q26).

**M5. Bagaimana model "tahu" sopran tidak boleh diubah?**
DeepBach mengunci kotak sopran sebagai batasan posisi, jadi kotak itu tidak pernah dipilih untuk diganti. Coconet menerima *mask* yang hanya menandai alto, tenor, dan bas sebagai kotak yang boleh diisi. Kontrol kualitas tetap memeriksa bahwa sopran keluaran sama dengan melodi masukan (Q41).

**M6. Apa itu *pseudo* pada *pseudo-Gibbs*?**
Gibbs sampling sejati punya jaminan matematis bila semua tebakan berasal dari satu distribusi yang konsisten. Keempat jaringan DeepBach dilatih terpisah, jadi jaminan itu tidak ada. Cara kerjanya sama, jaminannya yang tidak ada.

**M7. Apa hubungan *orderless NADE* dengan kemampuan Coconet menerima sopran saja?**
Saat belajar, Coconet melengkapi chorale yang dihapus dengan pola acak, termasuk kasus hanya satu suara yang tersisa. Karena itu model bisa mengisi bagian mana pun dari bagian mana pun, termasuk tiga suara dari sopran.

**M8. Apakah lebih banyak putaran membuat model lebih patuh?**
Belum diketahui dan tidak diuji. Penelitian ini memakai pengaturan bawaan setiap implementasi dan mencatatnya, sama untuk semua melodi (BAB III Generasi Harmonisasi). Mengubahnya berarti mengubah protokol.

**M9. Kenapa tidak menyetel *temperature* kedua model menjadi sama?**
Angka *temperature* bekerja pada model yang berbeda, sehingga angka yang sama tidak berarti tingkat keacakan yang sama. Desain memakai bawaan setiap implementasi, yaitu cara model biasanya dipakai orang. Protokol 2.1 sudah menetapkannya, tetapi persetujuan pembimbing masih ditunggu (PROGRESS.md, keputusan 5).

**M10. Kenapa *log-likelihood* tidak cukup untuk menilai harmonisasi?**
*Log-likelihood* mengukur seberapa "tidak kaget" model melihat chorale Bach asli. Ukuran itu tidak memeriksa harmonisasi yang dibuat model dan tidak menunjukkan di birama mana ada kuint sejajar.

**M11. DeepBach menyimpan ejaan nada, Coconet tidak. Apa pengaruhnya?**
Instrumen menghitung semiton, jadi ejaan tidak memengaruhi penghitungan lima kaidah (Q37). Ejaan berpengaruh pada masukan: melodi dengan ejaan di luar kosakata sopran DeepBach tidak dapat diproses dan dicatat sebagai tidak layak.

**M12. Kalau Coconet tidak bisa mengulang nada, apakah perbandingannya adil?**
Itu batas bentuk partitur Coconet. Peristiwa bunyi Coconet bisa lebih sedikit, sehingga jarak dan persilangan dapat tercatat lebih jarang. Hitungan utama tidak diubah. Analisis sensitivitas d menyatukan nada sama yang berurutan pada semua sumber (DeepBach, Coconet, dan Bach), lalu menguji ulang, jadi pengaruh batas ini bisa dilihat (Q41b, Q113).

**M13. Model lebih baru memakai *Transformer*. Kenapa tidak dipakai?**
Kriteria pemilihan model adalah menerima sopran tetap, kode dan bobot terbuka, dan dilatih pada chorale Bach. NotaGen tidak menerima melodi yang harus dipertahankan. Tujuannya menguji temuan Huang lintas model dan kaidah, bukan memeringkat model terbaru (Q20–Q21).

**M14. Bisakah dijelaskan kepada orang awam kenapa model melanggar kaidah?**
Model seperti murid yang belajar hanya dengan meniru ratusan contoh tanpa membaca aturan. Biasanya ia benar karena contohnya bagus, tetapi ia menebak, dan sesekali tebakannya salah, terutama pada soal yang tidak mirip contohnya.

## 9. Jangan diucapkan sebelum diperiksa

Angka berikut belum diperiksa di makalah atau kode dalam repositori ini. Buka sumbernya dulu bila ingin menyebutnya.

- Jumlah lapisan dan ukuran filter jaringan Coconet.
- Panjang jendela konteks LSTM DeepBach.
- Jumlah chorale latih masing-masing model dan transposisi yang dipakai.
- Jadwal *annealing* Coconet yang tepat.
- Bahwa checkpoint `coconet/bach` sama dengan model produksi Bach Doodle. Tidak didokumentasikan (Q23).
- Bahwa paket npm Magenta.js 1.23.1 yang akan dipasang sama dengan kode `master` yang dibaca. Belum dicek, karena model belum dipasang (reading-notes.csv).
