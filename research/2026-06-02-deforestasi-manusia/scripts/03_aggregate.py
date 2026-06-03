"""Silver → Gold: Aggregated analysis-ready data.

Usage: python 03_aggregate.py
Output: ../../gold/data/*.json
"""

import json, os
from collections import Counter

SILVER = os.path.join(os.path.dirname(__file__), "..", "data")
GOLD = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(GOLD, exist_ok=True)

def load(name):
    with open(os.path.join(SILVER, name)) as f:
        return json.load(f)

def save(name, data):
    path = os.path.join(GOLD, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  -> data/{name}")

arts = load("articles_clean.json").get("items", [])
sources = load("sources_clean.json").get("sources", [])
trend = load("sentiment_trend_clean.json")
monthly = load("monthly_agg.json")
sent_dist = load("sentiment_distribution_clean.json")

# ── Summary dashboard ──────────────────────────────────────
total = len(arts)
neg_pct = sent_dist["negative"] / max(sent_dist["total"], 1) * 100
pos_pct = sent_dist["positive"] / max(sent_dist["total"], 1) * 100

save("summary.json", {
    "total_articles": total,
    "total_sources": len(sources),
    "date_range": {
        "from": arts[0]["date"] if arts else None,
        "to": arts[-1]["date"] if arts else None,
    },
    "sentiment": {
        "positive": sent_dist["positive"],
        "negative": sent_dist["negative"],
        "neutral": sent_dist["neutral"],
        "positive_pct": round(pos_pct, 1),
        "negative_pct": round(neg_pct, 1),
    },
    "dominant_source": max(sources, key=lambda s: s["article_count"])["source"],
    "peak_month": max(monthly, key=lambda m: m["article_count"])["month"],
})

# ── Source ranking ─────────────────────────────────────────
save("source_ranking.json", sorted(sources, key=lambda s: s["article_count"], reverse=True))

# ── Monthly with sentiment ─────────────────────────────────
agg_monthly = []
for m_rec in monthly:
    m = m_rec["month"]
    m_arts = [a for a in arts if a["month"] == m]
    save(f"articles_{m.replace('-', '_')}.json", m_arts)

print(f"\n✅ Gold layer — {total} articles aggregated across {len(monthly)} months")