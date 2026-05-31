# analisa-konten

Automated Indonesian news & social media content analysis — sentiment, entities, framing, engagement forensics, and viral dynamics.

## Repo structure

```
research/                    # Each project is a dated, self-contained directory
└── YYYY-MM-DD-topic-slug/
    ├── README.md            # Temuan & interpretasi (Bahasa Indonesia)
    ├── HYPOTHESIS.md        # [opsional] Framework hipotesis untuk analisis forensik
    ├── requirements.txt     # Dependencies pin
    ├── run_all.sh           # Orchestrator — reproduce semua output dari scratch
    ├── scripts/             # Script Python — dipisah per fungsi, dinomori urut pipeline
    ├── data/                # Output JSON/CSV — generated oleh scripts/
    └── charts/              # [opsional] Static chart images untuk README

docs/                        # GitHub Pages — HTML explorer & data dashboard
└── *.html                   # Output HTML untuk publikasi
```

### Standar project baru

| Aturan | Keterangan |
|--------|------------|
| **Reproducible** | Setiap project wajib punya `run_all.sh` + `requirements.txt` |
| **Scripts only** | Semua kode di `scripts/`, tidak ada script di root project |
| **No .venv** | Gunakan `requirements.txt`, jangan commit virtual environment |
| **HTML → docs/** | Output visual untuk GitHub Pages simpan langsung di `docs/` root repo |
| **Deterministik** | Script harus seeded (random seed tetap) — output identik tiap run |
| **Bahasa** | README di project → Indonesia. Docstring di script → English |
| **Pipeline numerik** | Script dinomori urut (01_, 02_, dst) sesuai alur pipeline |
| **Forensik** | Analisis hipotesis-driven tambahkan `HYPOTHESIS.md` |

## Research projects

| Project | Fokus | Data source |
|---------|-------|-------------|
| [Transisi Energi Hijau](research/2026-05-18-transisi-energi-hijau/) | Pemberitaan green energy (542 artikel, 14 media) | Semantik API |
| [Andrie Yunus Preliminary](research/2026-05-19-andrie-yunus-preliminary/) | Eksplorasi awal framing Andrie Yunus | Semantik API |
| [Pesta Babi](research/2026-05-20-pesta-babi/) | Liputan dokumenter kontroversial (88 artikel) | Semantik API |
| [Lagu Bahlil](research/2026-05-26-lagu-bahlil/) | Viral Instagram Reel — 36K komentar, 2 gelombang | Instagram API + Tantular NLP |

## Data source

- [Semantik](https://semantik.cc) — Indonesian news monitoring platform (sentiment, entities, framing, relations)
- [Tantular](https://github.com/hariswb/tantular) — Offline NLP toolkit for Indonesian text (BagOfWords, InSetSentiment, NER, emotion, framing)
- Instagram / TikTok API — Engagement forensics (comment CSV, timestamps, user graphs)
