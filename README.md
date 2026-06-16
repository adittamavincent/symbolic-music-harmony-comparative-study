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
| Node.js  | 18 atau lebih baru | `node --version`    |

**Cara install `uv` (jika belum ada):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Setelah install, tutup dan buka ulang terminal.

**Cara install Node.js:** Unduh dari [nodejs.org](https://nodejs.org).

---

## Langkah Cepat (Quick Start)

### 1. Clone Proyek

```bash
git clone <URL_REPO_KAMU>
cd <nama-folder-proyek>
```

### 2. Buat Lingkungan Python & Install Library

```bash
uv venv .venv --python 3.10
source .venv/bin/activate
# Windows (PowerShell): .venv\Scripts\activate

uv pip install \
  music21==9.3.0 \
  numpy pandas matplotlib scipy \
  pretty_midi midiutil tqdm \
  torch transformers huggingface_hub \
  abcmidi miditoolkit
```

### 3. Setup Model Otomatis

Jalankan script setup berikut untuk mengunduh, meng-clone, dan menyiapkan file-file model (`models/deepbach`, `models/coconet`, dan `models/notagen`):

```bash
python setup.py
```

> **Catatan:** Semua model dan dependensinya disimpan dalam folder `models/` yang telah di-exclude dari Git via `.gitignore` agar tidak mengotori repository.

---

## Langkah 4 — Jalankan seluruh eksperimen

Pastikan lingkungan Python aktif (`source .venv/bin/activate`), lalu:

```bash
python run_all.py
```

Saat pertama kali dijalankan, program otomatis mengunduh resource yang belum ada:
- **DeepBach:** pretrained weights (~beberapa ratus MB) diunduh dari Dropbox.
- **NotaGen:** checkpoint (~1.5GB) diunduh dari Hugging Face.
- **Coconet:** checkpoint diambil otomatis oleh `@magenta/music` saat model di-load.

---

## Perintah lain yang berguna

```bash
# Tes cepat dengan 1 sampel saja (untuk memastikan setup benar).
python run_all.py --samples 1

# Lihat prompt yang akan digunakan tanpa menjalankan generasi apapun
python run_all.py --dry-run

# Jika output sudah ada, lewati generasi dan langsung evaluasi
python run_all.py --skip-generation
```

---

## Hasil Output

Setelah selesai, semua hasil tersimpan di folder `outputs/`:

```
outputs/
├── deepbach/         ← MIDI per kondisi
├── coconet/          ← MIDI per kondisi
├── notagen/          ← MIDI per kondisi
├── MASTER_RESULTS.csv              ← semua 120 hasil individual
├── SUMMARY_TABLE.csv               ← rata-rata per model × kondisi
└── strube_evaluation_results.png   ← grafik perbandingan
```

---

## Troubleshooting

| Masalah | Solusi |
| --- | --- |
| `uv: command not found` | Jalankan install curl di atas, lalu buka terminal baru |
| `python3: command not found` | Install Python 3.10 dari python.org |
| `node: command not found` | Install Node.js dari nodejs.org |
| `No module named 'DatasetManager'` | Pastikan kamu sudah sukses menjalankan `python setup.py` |
| Coconet `npm install` gagal | Pastikan koneksi internet stabil dan `node` terinstall, lalu coba jalankan `npm install` manual di `models/coconet` |
| Proses generasi terlalu lama | Gunakan `--samples 1` untuk tes awal |
