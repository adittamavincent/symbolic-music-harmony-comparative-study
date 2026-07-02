# Strube Harmonic Evaluation Framework

Proyek ini membandingkan tiga model AI generasi musik simbolik, yaitu **DeepBach** (2017), **Coconet** (2017), dan **NotaGen** (2025), menggunakan aturan harmoni fungsional Gustav Strube sebagai alat ukur.

Repositori ini sekarang dipisah jelas antara:

- pipeline eksperimen Python untuk penelitian utama,
- dokumen **fase proposal**,
- ruang khusus untuk **skripsi final** nanti.

## Struktur Repo

```text
.
├── docs/
│   ├── proposal-phase/
│   │   ├── assets/         # class, logo, bibliography
│   │   ├── proposal/       # naskah proposal
│   │   └── presentation/   # slides, notes, qna
│   └── final-thesis/       # disiapkan untuk fase skripsi final
├── experiments/            # script generasi, evaluasi, plotting
├── tests/
├── Makefile
├── run_all.py
├── setup.py
└── strube_evaluator.py
```

## Persyaratan Sistem

Pastikan software berikut sudah ada:

| Software | Versi minimum      | Cara cek |
| -------- | ------------------ | -------- |
| Git      | bebas              | `git --version` |
| Python   | 3.10               | `python3 --version` |
| uv       | bebas              | `uv --version` |
| Node.js  | 18+                | `node --version` |
| latexmk  | bebas              | `latexmk --version` |
| envsubst | bebas              | `envsubst --version` |

Install `uv` bila belum ada:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install Node.js dari [nodejs.org](https://nodejs.org). Untuk LaTeX di macOS, paling gampang pakai MacTeX.

## Setup Python

```bash
git clone <URL_REPO_KAMU>
cd <nama-folder-proyek>

uv venv .venv --python 3.10
source .venv/bin/activate
uv pip install -r requirements.txt
uv run python setup.py
```

`setup.py` akan menyiapkan dependency model ke folder `models/`, yang memang sudah di-ignore Git.

## Run Eksperimen

Jalankan full pipeline:

```bash
uv run python run_all.py
```

Command berguna lain:

```bash
# Tes awal ringan
uv run python run_all.py --samples 1

# Lihat prompt/kondisi tanpa generate
uv run python run_all.py --dry-run

# Lewati tahap generate, langsung evaluasi output yang sudah ada
uv run python run_all.py --skip-generation
```

Saat run pertama:

- DeepBach mengunduh pretrained weights,
- NotaGen mengunduh checkpoint dari Hugging Face,
- Coconet mengambil checkpoint saat model di-load.

## Build Dokumen Proposal

Semua artefak fase proposal ada di `docs/proposal-phase/`.

### 1. Isi Metadata

```bash
cp .env.example .env.local
```

Lalu isi `.env.local` dengan nama, NIM, institusi, dosen pembimbing, dan data lain.

### 2. Lihat Semua Target `make`

```bash
make help
```

### 3. Build Sesuai Kebutuhan

```bash
# Naskah proposal
make proposal

# Slide presentasi ujian proposal
make slides

# Naskah presenter berbasis slide
make notes

# Dokumen antisipasi tanya jawab
make qna

# Build semua artefak fase proposal
make proposal-phase
```

Alias lama masih didukung:

```bash
make compile   # alias make proposal
make present   # alias make slides
```

### Output PDF

PDF hasil build ada di:

- `docs/proposal-phase/proposal/main.pdf`
- `docs/proposal-phase/presentation/presentation.pdf`
- `docs/proposal-phase/presentation/presentation_notes.pdf`
- `docs/proposal-phase/presentation/qna.pdf`

### Hapus File Build

```bash
make clean
```

## Output Eksperimen

Hasil eksperimen tersimpan di `outputs/`:

```text
outputs/
├── deepbach/
├── coconet/
├── notagen/
├── MASTER_RESULTS.csv
├── SUMMARY_TABLE.csv
└── strube_evaluation_results.png
```

## Troubleshooting

| Masalah | Solusi |
| ------- | ------ |
| `uv: command not found` | Install `uv`, lalu buka terminal baru |
| `python3: command not found` | Install Python 3.10 dari python.org |
| `node: command not found` | Install Node.js dari nodejs.org |
| `latexmk: command not found` | Install distribusi LaTeX, mis. MacTeX |
| `envsubst: command not found` | Install `gettext`, lalu pastikan `envsubst` tersedia di PATH |
| `No module named 'DatasetManager'` | Jalankan `uv run python setup.py` lagi |
| Coconet `npm install` gagal | Pastikan internet stabil dan `node` terpasang |
| Generasi terlalu lama | Mulai dari `--samples 1` |
