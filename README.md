# analisa-konten

Automated Indonesian news & social media content analysis — sentiment, entities, framing, engagement forensics, and viral dynamics.

## Repo structure

```
research/
└── YYYY-MM-DD-slug/
    ├── README.md                        # Project overview
    ├── data/
    │   ├── raw/                         # Raw data as-is from source (CSV, JSON, scraped HTML)
    │   │   └── scripts/                 # Fetch/ingestion scripts
    │   └── processed/                   # Cleaned, parsed, aggregated data
    │       └── scripts/                 # Transform/aggregate scripts
    ├── charts/                          # Visualizations (served via gateway :8642)
    │   └── dashboard.html
    └── scripts/                         # EDA + analysis scripts at root
```

### Flat project structure

All scripts live at the research dir root under `scripts/`. Data goes flat in `data/` — `raw/` for untouched original files, `processed/` for output. Charts in `charts/` at root.

### Standards for new projects

| Rule | Detail |
|------|--------|
| **Self-contained** | Scripts live inside the `scripts/` directory |
| **No venv** | Single `requirements.txt` at project root |
| **Deterministic** | Seeded random — identical output on re-run |
| **English** | Everything (README, reports, docstrings) |
| **No GitHub Pages** | Visualizations served via gateway API on port 8642 |

## Research projects

| Project | Focus | Source |
|---------|-------|--------|
| [Transisi Energi Hijau](research/2026-05-18-transisi-energi-hijau/) | Green energy news coverage (542 articles, 14 outlets) | Semantik API |
| [Andrie Yunus Preliminary](research/2026-05-19-andrie-yunus-preliminary/) | Early framing exploration of Andrie Yunus | Semantik API |
| [Pesta Babi](research/2026-05-20-pesta-babi/) | Controversial documentary coverage (88 articles) | Semantik API |
| [Lagu Bahlil](research/2026-05-26-lagu-bahlil/) | Viral Instagram Reel — 36K comments, 2 waves | Instagram API + Tantular NLP |
| [Klarifikasi Teddy](research/2026-06-03-klarifikasi-teddy/) | Instagram comments on Seskab Teddy's clarification — 15K comments, 11 sources | Instagram + Tantular + scikit-learn |

> **Note:** Previous projects used an older directory layout. New projects starting from June 2026 follow the flat structure above.

## Data source

- [Semantik](https://semantik.cc) — Indonesian news monitoring (sentiment, entities, framing, relations)
- [Tantular](https://github.com/hariswb/tantular) — Offline NLP for Indonesian text (BagOfWords, InSetSentiment, NER, emotion, framing)
- Instagram / TikTok API — Engagement forensics (comment CSV, timestamps, user graphs)
