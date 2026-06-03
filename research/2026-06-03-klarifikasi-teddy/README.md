# Klarifikasi Seskab Teddy — Instagram Comments EDA

**Topic:** Instagram comment analysis of 11 news sources covering Sekretaris Kabinet Teddy Indra Wijaya's clarification regarding Dino Patti Djalal's criticism of President Prabowo's foreign visits.

**Timeline:** 1–4 June 2026
**Corpus:** 15,424 comments from 11 Instagram news accounts

## Pipeline Architecture (Independent Metrics)

Each metric lives in its own script — **no conflation**. Scripts can be run independently in any order.

| Script | Metric | Method | Output Files | Independent? |
|--------|--------|--------|-------------|:---:|
| `01_process.py` | **BoW + EDA** | Tantular BagOfWords (bigrams-only), keyword-based stance, emoji extraction | `meta.json`, `source_stats.json`, `hourly_distribution.json`, `stance_distribution.json`, `stance_by_source.json`, `top_terms.json`, `emoji_top.json`, `top_commenters.json`, `text_lengths.json`, `source_terms.json` | ✅ |
| `02_classify.py` | **Sentiment** | InSetSentiment (Tantular) — polarity on all comments | `inset_summary.json`, `inset_by_source.json`, `inset_results.jsonl` | ✅ |
| `02b_classify_tfidf.py` | **Clusters** | TF-IDF + SVD(50) + KMeans — unsupervised | `cluster_summary.json`, `cluster_by_source.json`, `cluster_results.jsonl` | ✅ |
| `03_emosense_sample.py` | **Emotions** | EmoSense-ID — 298 stratified sample, dominant emotion per comment | `emosense_summary.json`, `emosense_sample.jsonl`, `stance_emotion_profiles.json` | ✅ |
| `01_eda_dashboard.py` | **Dashboard** | Loads all JSONs, generates `dashboard.html` with Chart.js | `charts/dashboard.html` | ✅ (reads JSONs only) |

**Key principle:** Stance (keyword-based), sentiment (InSet), clustering (TF-IDF + KMeans), and emotions (EmoSense) are kept strictly separate. No script trains on another script's output. No supervised labeling on ad-hoc categories.

## Dashboard

The dashboard is a self-contained HTML page with Chart.js (CDN). No PNG files. All charts render client-side from JSON data files.

```bash
cd charts/
python3 -m http.server 8642
# → http://localhost:8642/dashboard.html
```

## Data Files

| File | Source | Description |
|------|--------|-------------|
| `data/raw/*.csv` | — | Raw Instagram comment CSVs (11 posts) |
| `data/raw/meta-*.csv` | — | Source metadata: accounts, URLs, follower counts |
| `data/*.json` | Various | Analysis outputs — see pipeline table above |

## Cluster Labels (TF-IDF + KMeans)

| Cluster | Label | Comments | Description |
|---------|-------|:--------:|-------------|
| 0 | skeptis | 488 | Skeptical comments about believing Teddy |
| 1 | mengkritik | 803 | APBN/qurban spending criticism |
| 2 | umum | 12,161 | Large generic cluster |
| 3 | sarkasme | 46 | Tagging/reply chains |
| 4 | mendukung | 1,238 | Supportive references to Teddy/Prabowo/Dino |

## InSetSentiment Results

| Polarity | Count | % |
|----------|:-----:|:-:|
| Positive | 3,832 | 24.8% |
| Negative | 5,176 | 33.6% |
| Neutral | 6,416 | 41.6% |
| **Avg polarity** | −0.09 | |
| **Pos/Neg ratio** | 0.74:1 | |

## EmoSense Dominant Emotions (298 sampled)

| Emotion | Count | % |
|---------|:-----:|:-:|
| anger | 74 | 25% |
| joy | 51 | 17% |
| disgust | 35 | 12% |
| trust | 34 | 11% |
| sadness | 29 | 10% |
| surprise | 29 | 10% |
| anticipation | 27 | 9% |
| fear | 19 | 6% |

## Project Structure

```
research/2026-06-03-klarifikasi-teddy/
├── README.md                     # This file
├── data/
│   ├── raw/                      # Raw CSV files from Instagram
│   ├── *.json                    # Analysis outputs
│   └── *.jsonl                   # Per-comment results (cluster, inset, emosense)
├── scripts/
│   ├── 01_process.py             # EDA + BoW (bigrams) + keyword stance
│   ├── 02_classify.py            # InSetSentiment (standalone)
│   ├── 02b_classify_tfidf.py     # TF-IDF + KMeans clustering (unsupervised)
│   ├── 03_emosense_sample.py     # EmoSense emotion sampling
│   └── 01_eda_dashboard.py       # Dashboard generator (loads JSON → Chart.js HTML)
└── charts/
    └── dashboard.html            # Self-contained dashboard (no PNGs)
```
