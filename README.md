# analisa-konten

Static artifacts from automated Indonesian news content analysis using [Semantik](https://semantik.cc).

## Pipeline

```
Research Question + Topics
       ↓
 Semantik API ──→ Data extraction (entities, sentiment, relations, framing)
       ↓
 Hermes Agent ──→ Analysis & charting
       ↓
 Markdown artifact ──→ Published to this repo
       ↓
 Claude Design ──→ Instagram slides
```

Each research cycle:

1. **Data pull** — Query Semantik API: articles, entities, sentiment trends, actor relations, framing analysis, co-occurrence networks
2. **Analysis** — Three layers:
   - **Data Science** — sentiment distributions, topic trends, entity frequency
   - **Social Network** — entity co-occurrence graphs, actor-action networks
   - **Content Analysis** — framing comparison across sources, SVO triples
3. **Artifact** — Markdown with inline charts + raw data tables, published to `research/YYYY-MM-DD-topic-slug/`
4. **Deliver** — Raw markdown passed to Claude Design for Instagram slide production

## Structure

```
research/
├── YYYY-MM-DD-topic-slug/
│   ├── README.md          # Full analysis report
│   ├── charts/            # Generated chart images
│   └── data/              # Raw JSON/CSV from API
└── index.md               # Index of all research artifacts
```

## Channels

Semantik monitors 7 Indonesian news channels by keyword-tracked daily:

| Channel | Keywords |
|---------|----------|
| Legislasi | RUU, legislation, judicial review |
| Demokrasi | Digital rights, press freedom, criminalization |
| Lingkungan | Energy transition, mining, deforestation |
| Ekonomi | Budget, taxes, inflation, poverty |
| Pasar Modal | Stocks, fintech, crypto, banking |
| Hukum | Courts, constitutional court, verdicts |
| Keamanan | TNI/Polri, terrorism, defense |