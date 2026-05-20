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
└── YYYY-MM-DD-topic-slug/
    ├── README.md       # Analysis report
    ├── charts/         # Generated charts
    └── data/           # Source data
```

## Data source

All analysis is powered by [Semantik](https://semantik.cc) — an Indonesian news monitoring platform that tracks and processes articles from national media outlets.