# Deforestasi Manusia — EDA Report

**Date range:** 2025-12-04 → 2026-05-31  
**Keywords:** deforestasi, illegal logging, pembalakan liar, perambahan hutan, alih fungsi hutan, konversi hutan, EUDR, konsesi hutan, izin hutan, pembukaan lahan  
**Articles:** 83 | **Sources:** 10  
**Data source:** Semantik Research API (channel: Lingkungan)

---

## Key Findings

1. **73% negative sentiment** — human-caused deforestation coverage is overwhelmingly critical, driven by law enforcement stories (illegal logging arrests) and policy critique (Anies vs Kemenhut, Megawati's "karpet merah konsesi").
2. **January 2026 peak (31 articles)** — driven by Anies' "97% deforestasi legal" claim, Kemenhut's rebuttal, and the 166,000 Ha triwulan III 2025 deforestation data release.
3. **Media Indonesia dominates (29%)** — followed by Tirto (16%) and Republika (14%). Only Tempo has net-positive sentiment (+4.50).
4. **Kemenhut is the central entity** — 8 mentions across enforcement, permit revocation, and data defense. Bulk sentiment −5.33 (negative).
5. **Two main story clusters:** (a) Law enforcement: illegal logging arrests (Gunung Ciremai, Baluran, Napabalano, Lampung) and (b) Policy debate: Anies–Kemenhut exchange, Megawati's regulatory critique, BPK findings on forest governance.
6. **EUDR appears as a minor thread** — 6 articles, mostly positive framing around trade readiness.

## Data Science

### Sentiment Distribution

| Sentiment | Count | % |
|-----------|-------|---|
| Positive | 20 | 24% |
| Neutral | 2 | 2% |
| Negative | 61 | 73% |

**Most negative source:** CNBC News (−12.00) — likely covering economic impact of policy.  
**Most positive source:** Tempo (+4.50) — only 2 articles but both positive (policy reform angle).

### Monthly Trend

| Month | Articles | Notes |
|-------|----------|-------|
| Dec 2025 | 8 | Baseline — Tirto series on illegal logging |
| **Jan 2026** | **31** | **Peak** — Anies 97% claim, Kemenhut rebuttal, PDIP critique, 166K Ha data |
| Feb 2026 | 13 | Illegal logging enforcement (Ciremai, Baluran, Napabalano) |
| Mar 2026 | 10 | Kemenhut wood pellet defense, forest governance |
| Apr 2026 | 9 | Walhi Kalsel ecological crisis, IKN deforestation, INRU permit revocation |
| May 2026 | 12 | EU trade preparation, sawit legality, monkey malaria link |

### Top Entities

| Entity | Type | Mentions |
|--------|------|----------|
| Indonesia | place | 11 |
| Aceh | place | 8 |
| Kemenhut | org | 8 |
| Sumatra | place | 6 |
| Jakarta | place | 6 |
| Pemerintah | org | 6 |
| Gakkum Kehutanan | law | 4 |
| Kuningan | place | 3 |
| Gunung Ciremai | place | 3 |
| Megawati | person | 2+2 |
| Anies | person | 2 |

### Entity Sentiment

| Entity | Avg Score | Pos | Neg | Articles |
|--------|-----------|-----|-----|----------|
| Kuningan | +4.33 | 2 | 1 | 3 |
| Aceh | −2.69 | 4 | 9 | 8 |
| Kemenhut | −5.33 | 1 | 11 | 8 |
| Sumatra | −9.00 | 2 | 5 | 6 |
| Jakarta | −18.33 | 0 | 6 | 6 |

## Text Classification

Two approaches were applied to categorize articles by thematic content:

### Approach 1: BagOfWords (Tantular)

**Top bigrams:**
| Bigram | Frequency |
|---|---|
| `pembalakan liar` | 22 |
| `pembukaan lahan` | 14 |
| `illegal logging` | 12 |
| `banjir bandang` | 7 |
| `perambahan hutan` | 6 |
| `izin hutan` | 6 |
| `krisis ekologi` | 5 |

**Top trigrams:**
- `pembalakan liar kawasan` (5)
- `dugaan pembalakan liar` (5)
- `tersangka pembalakan liar` (4)
- `izin hutan tambang` (4)
- `industri wood pellet` (3)

### Approach 2: TF-IDF + LinearSVC

**Pipeline:** TfidfVectorizer(ngram_range=1-3, max_features=5000) → LinearSVC(class_weight=balanced)

**6 categories** were defined via keyword pattern matching, then trained on 83 articles (70/30 split):

| Category | Articles | % | Precision | Recall | F1 |
|---|---|---|---|---|---|
| illegal_logging | 26 | 31% | 0.89 | 1.00 | 0.94 |
| ecological_impact | 16 | 19% | 1.00 | 0.80 | 0.89 |
| policy_politics | 11 | 13% | 0.67 | 0.50 | 0.57 |
| commodity_economy | 12 | 14% | 0.00 | 0.00 | 0.00 |
| health_disease | 4 | 5% | 1.00 | 1.00 | 1.00 |
| other | 14 | 17% | 0.25 | 0.25 | 0.25 |

**5-fold CV accuracy:** 62% ± 14% | **Test set:** 64%

**Per-source category composition:**
- **Media Indonesia** — dominant in illegal_logging (10) & commodity_economy (4)
- **Tirto** — concentrated in illegal_logging (8), investigative stance
- **Kompas** — split between commodity_economy (3) and policy_politics (3)
- **Kumparan** — mostly other (3) and ecological_impact (2), essay-style
- **Liputan6** — evenly distributed across policy, ecological, illegal logging

**Note:** Classification uses keyword-derived labels. Best-performing categories (illegal_logging, ecological_impact) have clear keyword signals; commodity_economy needs more distinctive features or human-labeled data.

## Framing Analysis

### Anies
- "97 percent deforestasi legal satgas PKH" — claimed most deforestation is legally permitted
- "Kemenhut pertanyakan klaim" — ministry pushed back

### Megawati
- "soroti regulasi karpet merah konsesi" — flagged regulatory red carpet for concessions
- "UU beri karpet merah untuk deforestasi perampasan" — legislation enables deforestation

### Kemenhut
- "166 ribu ha pada triwulan III 2025" — official data release
- "bantah tuduhan deforestasi dari industri wood pellet" — denial of wood pellet-linked deforestation
- "berupaya menurunkan angka deforestasi" — institutional framing as solution

### Key SVO Relations
- Kemenhut → bantah (denies) → tuduhan deforestasi wood pellet
- Kemenhut → catat (records) → 166 ribu Ha deforestasi
- Anies → sebut (claims) → 97% deforestasi legal
- Megawati → soroti (flags) → karpet merah konsesi

## Social Network Analysis

The NLP relations network returned sparse results for this corpus (83 articles), limiting graph analysis. Co-occurrence data shows Kemenhut co-occurs with "Indonesia," "Anies," "97 percent," and "Menhut" — confirming the policy debate cluster.

## Methodology

- **Data source:** Semantik Research API (semantik.cc)
- **Channel:** Lingkungan (keyword-filtered, not channel-level)
- **Date range:** 2025-11-01 to 2026-06-02
- **Keywords (10):** deforestasi, illegal logging, pembalakan liar, perambahan hutan, alih fungsi hutan, konversi hutan, EUDR, konsesi hutan, izin hutan, pembukaan lahan
- **Total articles after keyword filter:** 83 (vs ~2,264 channel-level)
- **API endpoints used:** source-comparison, topic-trend, sentiment/distribution, sentiment/trend, articles/search (paginated), entities/top (by group), entities/bulk-sentiment, framing/compare

### Limitations
1. **Small corpus (83 articles)** — limits statistical confidence for entity sentiment and network analysis
2. **Keyword overlap:** "izin hutan" and "konsesi hutan" may capture some non-deforestation permit news
3. **API NLP lag:** entity recognition may miss "deforestasi" as a topic entity since it's a common noun
4. **Time range:** 7 months — seasonal patterns may not be fully observable

## Directory Structure

```
research/2026-06-02-deforestasi-manusia/
├── README.md              # This file
├── requirements.txt       # Deps (matplotlib, numpy for charts)
├── run_all.sh             # Orchestrator: fetch → analyze → aggregate → visualize
├── scripts/
│   ├── 01_fetch_data.py   # Fetch all JSON from Semantik API
│   ├── 02_analyze.py      # Parse, clean, and print EDA stats
│   ├── 03_aggregate.py    # Aggregated analysis-ready data
│   └── 04_visualize.py    # Generate PNG chart images
├── data/
│   ├── articles_list.json      (83 articles, paginated)
│   ├── source_comparison.json   (10 sources)
│   ├── topic_trend.json         (weekly volume)
│   ├── sentiment_distribution.json
│   ├── sentiment_trend.json     (weekly)
│   ├── top_entities.json
│   ├── top_persons.json
│   ├── top_orgs.json
│   ├── top_gpe.json
│   ├── bulk_sentiment.json      (entity-level sentiment)
│   ├── cooccurence_*.json       (5 entities)
│   └── framing_*.json           (5 entities + compare)
└── charts/                 # PNG visualizations
    ├── source_distribution.png
    ├── monthly_trend.png
    ├── sentiment_donut.png
    ├── sentiment_trend.png
    └── sentiment_by_source.png
```