# analisa-konten

Automated Indonesian news content analysis — sentiment, entities, relations, and framing across 7 monitored topics.

## Topics covered

| Topic | Coverage |
|-------|----------|
| **Legislasi** | RUU, legislation, judicial review |
| **Demokrasi** | Digital rights, press freedom, criminalization |
| **Lingkungan** | Energy transition, mining, deforestation |
| **Ekonomi** | Budget, taxes, inflation, poverty |
| **Pasar Modal** | Stocks, fintech, crypto, banking |
| **Hukum** | Courts, constitutional court, verdicts |
| **Keamanan** | TNI/Polri, terrorism, defense |

## Repo structure

```
research/
├── 2026-05-20-pesta-babi/  # Co-occurrence network & sentiment analysis
└── YYYY-MM-DD-topic-slug/
    ├── analysis.py          # Reproducible Python analysis script
    ├── report.txt           # Structured text report
    ├── network_cooccurence.png
    ├── sentiment_trend.png
    ├── source_comparison.png
    ├── all_articles.json    # Full article metadata (89 articles)
    └── data/                # Source data from API
```

## Data source

All analysis is powered by [Semantik](https://semantik.cc) — an Indonesian news monitoring platform that tracks and processes articles from national media outlets.