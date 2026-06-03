"""Generate EDA chart images for deforestation news.

Usage: python 04_visualize.py
Output: ../charts/*.png
"""

import json, os
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHARTS, exist_ok=True)

def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)

# Dark theme
BG = "#1a1a2e"
FG = "#e0e0e0"
GRID = "#2a2a4e"
plt.style.use("dark_background")
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.edgecolor": "#404060", "axes.labelcolor": FG,
    "axes.titlecolor": "#ffffff", "xtick.color": FG,
    "ytick.color": FG, "grid.color": GRID, "grid.alpha": 0.3,
    "legend.facecolor": "#222244", "legend.edgecolor": "#404060",
    "legend.labelcolor": FG, "text.color": FG,
})

sc = load("source_comparison.json")
arts = load("articles_list.json").get("items", [])

# ── 1. Source Distribution Bar ─────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
names = [s["source"].replace("_", " ").title() for s in sorted(sc, key=lambda x: x["article_count"])]
counts = [s["article_count"] for s in sorted(sc, key=lambda x: x["article_count"])]
colors = plt.cm.RdYlGn_r([max(0, min(1, (s.get("avg_sentiment_score", 0) + 12) / 24)) for s in sorted(sc, key=lambda x: x["article_count"])])
bars = ax.barh(names, counts, color=colors, edgecolor="#404060", linewidth=0.5)
ax.set_xlabel("Articles")
ax.set_title("Source Distribution - Deforestasi Manusia", fontsize=14, fontweight="bold")
for bar, c in zip(bars, counts):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, str(c), va="center", fontsize=9, color=FG)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "source_distribution.png"), dpi=150)
plt.close()
print("✅ source_distribution.png")

# ── 2. Monthly Trend ──────────────────────────────────────
monthly = Counter()
for a in arts:
    monthly[a["published_at"][:7]] += 1
fig, ax = plt.subplots(figsize=(10, 4.5))
months = sorted(monthly)
counts_m = [monthly[m] for m in months]
x = range(len(months))
ax.plot(x, counts_m, color="#4fc3f7", linewidth=2.5, marker="o", markersize=8, markerfacecolor="#81d4fa", markeredgecolor="#0288d1")
ax.fill_between(x, counts_m, alpha=0.15, color="#4fc3f7")
for i, c in enumerate(counts_m):
    ax.annotate(str(c), (i, c), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=9, color="#b0bec5")
ax.set_xticks(x)
ax.set_xticklabels([m.replace("2026-", "") for m in months], rotation=30, ha="right")
ax.set_ylabel("Articles")
ax.set_title("Monthly Article Volume - Deforestasi Manusia", fontsize=14, fontweight="bold")
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "monthly_trend.png"), dpi=150)
plt.close()
print("✅ monthly_trend.png")

# ── 3. Sentiment Donut ────────────────────────────────────
sd = load("sentiment_distribution.json")
fig, ax = plt.subplots(figsize=(6, 5))
sizes = [sd["positive"], sd["neutral"], sd["negative"]]
colors_pie = ["#66bb6a", "#ffee58", "#ef5350"]
wedges, texts, autotexts = ax.pie(sizes, explode=(0.02, 0.02, 0.05),
    labels=["Positive", "Neutral", "Negative"], autopct="%1.0f%%",
    colors=colors_pie, startangle=90, pctdistance=0.78,
    textprops={"color": FG, "fontsize": 11})
for at in autotexts:
    at.set_fontsize(12); at.set_fontweight("bold")
ax.set_title("Sentiment Distribution", fontsize=14, fontweight="bold", pad=15)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "sentiment_donut.png"), dpi=150)
plt.close()
print("✅ sentiment_donut.png")

# ── 4. Weekly Sentiment Trend ─────────────────────────────
st = load("sentiment_trend.json")
fig, ax = plt.subplots(figsize=(12, 4.5))
weeks = [w["date"] for w in st]
pos = [w["positive"] for w in st]
neg = [w["negative"] for w in st]
neu = [w["neutral"] for w in st]
x = range(len(weeks))
visible_ix = list(range(0, len(weeks), 3))
ax.stackplot(x, pos, neu, neg, labels=["Positive", "Neutral", "Negative"],
    colors=["#66bb6a", "#ffee58", "#ef5350"], alpha=0.8)
ax.set_xticks(visible_ix)
ax.set_xticklabels([weeks[i] for i in visible_ix], rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Articles")
ax.set_title("Weekly Sentiment Trend", fontsize=14, fontweight="bold")
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "sentiment_trend.png"), dpi=150)
plt.close()
print("✅ sentiment_trend.png")

# ── 5. Sentiment by Source ──────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
src_sorted = sorted(sc, key=lambda s: s["article_count"], reverse=True)
names_ss = [s["source"].replace("_", " ").title() for s in src_sorted]
x_ss = range(len(names_ss))
width = 0.3
pos_ss = [s.get("sentiment_distribution", {}).get("positive", 0) for s in src_sorted]
neg_ss = [s.get("sentiment_distribution", {}).get("negative", 0) for s in src_sorted]
neu_ss = [s.get("sentiment_distribution", {}).get("neutral", 0) for s in src_sorted]
ax.bar([i - width for i in x_ss], pos_ss, width, label="Positive", color="#66bb6a", edgecolor="#404060", linewidth=0.3)
ax.bar(x_ss, neg_ss, width, label="Negative", color="#ef5350", edgecolor="#404060", linewidth=0.3)
ax.bar([i + width for i in x_ss], neu_ss, width, label="Neutral", color="#ffee58", edgecolor="#404060", linewidth=0.3)
ax.set_xticks(x_ss)
ax.set_xticklabels(names_ss, rotation=45, ha="right", fontsize=9)
ax.set_ylabel("Articles")
ax.set_title("Sentiment by Source", fontsize=14, fontweight="bold")
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "sentiment_by_source.png"), dpi=150)
plt.close()
print("✅ sentiment_by_source.png")

print(f"\n✅ 5 charts saved to charts/")