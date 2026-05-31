# analisa-konten

Automated Indonesian news & social media content analysis — sentiment, entities, framing, engagement forensics, and viral dynamics.

## Repo structure

```
research/
└── YYYY-MM-DD-slug/
    ├── README.md                        # Project overview
    ├── data/
    │   ├── bronze/                      # Raw data as-is from source
    │   │   └── scripts/                 # Fetch/ingestion scripts
    │   ├── silver/                      # Cleaned, parsed, validated data
    │   │   └── scripts/                 # Transform/clean scripts
    │   └── gold/                        # Aggregated, analysis-ready datasets
    │       └── scripts/                 # Aggregate / feature engineering
    ├── eda/                             # Exploratory phase — understand raw data
    │   ├── scripts/                     # EDA scripts (stats, profiling, charts)
    │   └── *.html                       # Visualizations (served via gateway :8642)
    └── analysis/                        # Answer specific research questions
        ├── RESEARCH_REPORT.md           # Final report (findings, tables, insight)
        ├── HYPOTHESIS.md                # [optional] Hypothesis framework for forensic analysis
        ├── scripts/                     # Focused analysis scripts
        └── *.html                       # Analysis visualizations (served via gateway :8642)
```

### Medallion data architecture

| Layer | What goes in | Scripts in |
|-------|-------------|------------|
| **bronze/** | Raw data from Semantik API, Instagram CSV dump, scraped HTML — never modified | `bronze/scripts/` |
| **silver/** | Parsed, validated, deduplicated — date fields converted, nulls handled, schema enforced | `silver/scripts/` |
| **gold/** | Aggregated metrics, entity-level joins, feature tables ready for analysis/visualization | `gold/scripts/` |

### Standards for new projects

| Rule | Detail |
|------|--------|
| **Self-contained** | Scripts live inside the medal/eda/analysis directory they serve — no top-level `scripts/` |
| **Reproducible** | Each medal stage has its own scripts/ to regenerate that layer from the previous one |
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

> **Note:** Previous projects used an older directory layout. New projects starting from June 2026 follow the medallion architecture above.

## Data source

- [Semantik](https://semantik.cc) — Indonesian news monitoring (sentiment, entities, framing, relations)
- [Tantular](https://github.com/hariswb/tantular) — Offline NLP for Indonesian text (BagOfWords, InSetSentiment, NER, emotion, framing)
- Instagram / TikTok API — Engagement forensics (comment CSV, timestamps, user graphs)
