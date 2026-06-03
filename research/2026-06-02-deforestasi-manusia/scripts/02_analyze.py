"""Parse and analyze raw deforestation news data.

Usage: python 02_analyze.py
Reads from: ../data/ (the flat data dir)
"""

import json, os, sys
from collections import Counter
from datetime import datetime

BRONZE = os.path.join(os.path.dirname(__file__), "..", "data")
SILVER = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(SILVER, exist_ok=True)

def load(name):
    with open(os.path.join(BRONZE, name)) as f:
        return json.load(f)

def save(name, data):
    path = os.path.join(SILVER, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  -> data/{name}")

# ── Clean articles list ────────────────────────────────────
raw_arts = load("articles_list.json")
items = raw_arts.get("items", [])

cleaned_articles = []
for a in items:
    cleaned_articles.append({
        "id": a.get("id"),
        "title": a.get("title", "").strip(),
        "summary": a.get("summary", "").strip(),
        "source": a.get("source", ""),
        "published_at": a.get("published_at", ""),
        "date": a.get("published_at", "")[:10],
        "month": a.get("published_at", "")[:7],
        "url": a.get("url", ""),
    })

cleaned_articles.sort(key=lambda x: x["published_at"])

save("articles_clean.json", {
    "total": len(cleaned_articles),
    "items": cleaned_articles,
})

# ── Clean source comparison ─────────────────────────────────
sc = load("source_comparison.json")
cleaned_sources = []
for s in sc:
    sd = s.get("sentiment_distribution", {})
    cleaned_sources.append({
        "source": s["source"],
        "article_count": s["article_count"],
        "avg_sentiment_score": s.get("avg_sentiment_score", 0),
        "sentiment": {
            "positive": sd.get("positive", 0),
            "neutral": sd.get("neutral", 0),
            "negative": sd.get("negative", 0),
        },
        "top_entities": s.get("top_entities", []),
    })

save("sources_clean.json", {
    "total_sources": len(cleaned_sources),
    "total_articles": sum(s["article_count"] for s in cleaned_sources),
    "sources": cleaned_sources,
})

# ── Clean sentiment trend ──────────────────────────────────
st = load("sentiment_trend.json")
cleaned_trend = [{
    "week": w["date"],
    "positive": w.get("positive", 0),
    "neutral": w.get("neutral", 0),
    "negative": w.get("negative", 0),
    "total": w.get("positive", 0) + w.get("neutral", 0) + w.get("negative", 0),
} for w in st]

save("sentiment_trend_clean.json", cleaned_trend)

# ── Monthly aggregation ────────────────────────────────────
monthly = Counter()
for a in cleaned_articles:
    monthly[a["month"]] += 1

monthly_agg = [{"month": m, "article_count": c} for m, c in sorted(monthly.items())]
save("monthly_agg.json", monthly_agg)

# ── Entity cleanup ─────────────────────────────────────────
for entity_file in ["top_entities.json", "top_persons.json", "top_orgs.json", "top_gpe.json"]:
    ents = load(entity_file)
    src_type = entity_file.replace("top_", "").replace(".json", "")
    cleaned = [{
        "name": e["word"],
        "group": e.get("entity_group", ""),
        "mention_count": e["mention_count"],
    } for e in ents]
    save(f"entities_{src_type}_clean.json", cleaned)

# ── Sentiment distribution clean ───────────────────────────
sd = load("sentiment_distribution.json")
save("sentiment_distribution_clean.json", {
    "positive": sd.get("positive", 0),
    "neutral": sd.get("neutral", 0),
    "negative": sd.get("negative", 0),
    "total": sd.get("total", 0),
})

print(f"\n✅ Silver layer — {len(cleaned_articles)} articles cleaned")