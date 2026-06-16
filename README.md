# Strube Harmonic Evaluation Framework

Proyek ini membandingkan tiga model AI generasi musik simbolik —
**DeepBach** (2017), **Coconet** (2019), dan **NotaGen** (2025) —
menggunakan aturan harmoni fungsional dari teori Gustav Strube sebagai alat ukur.

Proyek ini adalah bagian dari penelitian skripsi S1 ${PROGRAM_STUDY}.

---

## Apa yang dilakukan proyek ini?

Setiap model AI diminta menghasilkan musik paduan suara 4 suara (SATB)
dalam empat kondisi berbeda — dari tanpa batasan hingga diberi banyak petunjuk.
Hasilnya dianalisis secara otomatis: seberapa banyak pelanggaran *parallel fifths*,
*parallel octaves*, dan *leading tone* yang dihasilkan?
Skor akhir mencerminkan kepatuhan terhadap prinsip harmoni fungsional Strube.

---

## Persyaratan Sistem

Sebelum mulai, pastikan semua software berikut sudah terinstal:

| Software | Versi minimum | Cara cek di terminal    |
|----------|---------------|--------------------------|
| Git      | apa saja      | `git --version`          |
| Python   | 3.10          | `python3 --version`      |
| uv       | apa saja      | `uv --version`           |
| Node.js  | 18 atau lebih baru | `node --version`     |

**Cara install `uv` (jika belum ada):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Setelah install, tutup dan buka ulang terminal.

**Cara install Node.js:** Unduh dari [nodejs.org] — versi **20 LTS** paling cepat untuk Coconet. Node versi lebih baru tetap bisa jalan, tetapi Coconet memakai backend JavaScript yang lebih lambat.

---

## Langkah 1 — Clone proyek ke komputermu

Buka terminal, lalu jalankan:

```bash
git clone <URL_REPO_KAMU>
cd <nama-folder-proyek>
git submodule update --init --recursive
```

> `git submodule update` mengunduh kode DeepBach, Coconet, dan NotaGen
> secara otomatis. Proses ini membutuhkan koneksi internet dan bisa
> memakan waktu beberapa menit.
>

---

## Langkah 2 — Buat lingkungan Python

```bash
uv venv .venv --python 3.10
source .venv/bin/activate
```

> **Windows (PowerShell):** ganti baris kedua dengan `.venv\Scripts\activate`
>

Lalu install semua library yang dibutuhkan:

```bash
uv pip install \
  music21==9.3.0 \
  numpy pandas matplotlib scipy \
  pretty_midi midiutil tqdm \
  torch transformers huggingface_hub
```

Verifikasi berhasil:

```bash
python -c "import music21; print('OK:', music21.__version__)"
```

---

## Langkah 3 — Setup Coconet (Node.js)

Coconet menggunakan JavaScript. Ini perlu dilakukan sekali saja:

```bash
cd models/coconet
npm install
cd ../..
```

> Jika `npm install` gagal pada Node versi baru karena `@tensorflow/tfjs-node`,
> lanjutkan saja. Dependency native itu opsional; program otomatis memakai
> fallback JavaScript.
>

---

## Langkah 4 — Jalankan seluruh eksperimen

Pastikan lingkungan Python aktif (`source .venv/bin/activate`), lalu:

```bash
python run_all.py
```

Saat pertama kali dijalankan, program otomatis mengunduh resource yang belum ada:

- DeepBach pretrained model/cache, jika belum tersedia.
- NotaGen-X checkpoint ke `models/notagen/gradio/weights_notagenx_p_size_16_p_length_1024_p_layers_20_h_size_1280.pth`, jika belum tersedia.
- Coconet checkpoint diambil otomatis oleh Magenta saat model di-load.

Ini akan menjalankan empat tahap secara berurutan:

1. ✅ **Face validity test** — membuktikan evaluator bekerja benar sebelum eksperimen
2. 🎵 **Generasi** — 120 file MIDI total (10 sampel × 4 kondisi × 3 model)
3. 📊 **Evaluasi Strube** — analisis harmoni semua file MIDI
4. 📈 **Visualisasi** — membuat grafik perbandingan ketiga model

> ⏱ Proses ini memakan waktu **30–90 menit** tergantung hardware.
> Kamu bisa biarkan berjalan di background.
>

---

## Perintah lain yang berguna

```bash
# Tes cepat dengan 1 sampel saja (untuk memastikan setup benar).
# Tetap mengunduh checkpoint otomatis jika belum ada.
python run_all.py --samples 1

# Lihat prompt yang akan digunakan tanpa menjalankan generasi apapun
python run_all.py --dry-run

# Jika output sudah ada, lewati generasi dan langsung evaluasi
python run_all.py --skip-generation

# Jalankan ketiga model secara paralel (hanya jika RAM ≥ 32 GB)
python run_all.py --parallel-models
```

---

## Hasil Output

Setelah selesai, semua hasil tersimpan di folder `outputs/`:

```
outputs/
├── deepbach/
│   ├── A_neutral/    ← 10 file .mid
│   ├── B_key/
│   ├── C_satb/
│   └── D_full/
├── coconet/          ← struktur yang sama
├── notagen/          ← struktur yang sama
├── MASTER_RESULTS.csv              ← semua 120 hasil individual
├── SUMMARY_TABLE.csv               ← rata-rata per model × kondisi
└── strube_evaluation_results.png   ← grafik perbandingan
```

Buka `SUMMARY_TABLE.csv` di Excel atau Google Sheets untuk melihat
ringkasan perbandingan ketiga model.

---

## Desain Eksperimen: Empat Kondisi

Definisi lengkap ada di `experiments/strube_conditions.json`.

| Kondisi | Deskripsi |
| --- | --- |
| A_neutral | Tanpa batasan — model bebas berkreasi |
| B_key | Diberi konteks kunci/periode tanpa seed melodi |
| C_satb | Sopran dikunci, model mengisi Alto/Tenor/Bass |
| D_full | Sopran + Bass dikunci, model mengisi A/T |

**Catatan metodologis:** Setiap kondisi menggunakan *equivalent conditioning level*,
bukan prompt string yang identik. DeepBach dikontrol via tensor constraint,
Coconet via note seed injection, NotaGen via metadata teks — sesuai interface
native masing-masing model. Ini adalah standar yang dipakai dalam penelitian
evaluasi komparatif MIR (Hadjeres et al. 2017, Huang et al. 2019).

---

## Evaluasi Manual (Opsional)

```bash
source .venv/bin/activate

# Evaluasi satu file MIDI
python strube_evaluator.py outputs/deepbach/A_neutral/deepbach_neutral_01.mid

# Evaluasi seluruh folder
python strube_evaluator.py outputs/deepbach/A_neutral/

# Jalankan face validity test saja
python tests/test_strube_validity.py
```

---

## Troubleshooting

| Masalah | Solusi |
| --- | --- |
| `uv: command not found` | Jalankan install curl di atas, lalu buka terminal baru |
| `python3: command not found` | Install Python 3.10 dari python.org |
| `node: command not found` | Install Node.js dari nodejs.org (pilih versi 20 LTS) |
| `git submodule` gagal | Pastikan koneksi internet aktif, ulangi perintah |
| `import music21` gagal | Jalankan `uv pip install music21==9.3.0` lagi |
| Coconet `npm install` gagal pada `@tensorflow/tfjs-node` | Bisa diabaikan pada Node baru; fallback JavaScript dipakai otomatis. Untuk lebih cepat, pakai Node 20 lalu ulangi `npm install` |
| NotaGen checkpoint belum ada | Jalankan `python run_all.py`; program mengunduh otomatis ke `models/notagen/gradio/` |
| Output MIDI hanya 1 track | File tetap dievaluasi dan di-flag di CSV — ini data valid |
| Proses generasi terlalu lama | Gunakan `--samples 1` untuk tes awal |

---

## Struktur File Proyek

```
.
├── run_all.py                    ← ENTRYPOINT UTAMA (jalankan ini)
├── strube_evaluator.py           ← logika evaluasi Strube
├── Makefile                      ← otomasi templating & kompilasi LaTeX
├── experiments/
│   ├── strube_conditions.json   ← definisi kondisi A–D untuk semua model
│   └── scripts/
│       ├── run_experiment.py    ← dispatcher generasi
│       ├── run_deepbach.py      ← adapter DeepBach
│       ├── run_coconet.py       ← adapter Coconet
│       ├── run_notagen.py       ← adapter NotaGen
│       ├── run_evaluation.py    ← batch evaluator
│       └── plot_results.py      ← visualisasi
├── tests/
│   └── test_strube_validity.py  ← face validity tests
├── models/
│   ├── deepbach/                ← git submodule
│   ├── coconet/                 ← git submodule
│   └── notagen/                 ← git submodule
└── outputs/                     ← dibuat otomatis saat eksperimen berjalan
```

---

## Referensi

- Hadjeres, G., Pachet, F., & Nielsen, F. (2017). DeepBach: a Steerable Model for Bach Chorales Generation. *ICML 2017*.
- Huang, C. Z. A., et al. (2019). Counterpoint by Convolution. *ICLR 2019*.
- Sheng, Z., et al. (2025). NotaGen: Advancing Musicality in Symbolic Music Generation. *arXiv 2025*.
- Strube, G. (1928). *The Theory and Use of Chords*. Oliver Ditson Company.
