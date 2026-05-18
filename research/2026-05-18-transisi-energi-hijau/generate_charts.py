"""Generate charts for Transisi Energi Hijau analysis (2026-03-18 to 2026-05-18)."""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

DIR = "/opt/data/analisa-konten/research/2026-05-18-transisi-energi-hijau/data"
CHARTS = "/opt/data/analisa-konten/research/2026-05-18-transisi-energi-hijau/charts"

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

POS = '#2ecc71'
NEG = '#e74c3c'
NEU = '#95a5a6'
BLUE = '#3498db'
ORANGE = '#e67e22'
DARK = '#2c3e50'

# 1. Sentiment per Source
with open(f"{DIR}/source_comparison.json") as f:
    sources = json.load(f)

sources_sorted = sorted(sources, key=lambda x: x['article_count'], reverse=True)
labels = [s['source'].replace('_', ' ').title() for s in sources_sorted]
pos = [s['sentiment_distribution']['positive'] for s in sources_sorted]
neg = [s['sentiment_distribution']['negative'] for s in sources_sorted]
neu = [s['sentiment_distribution']['neutral'] for s in sources_sorted]

fig, ax = plt.subplots(figsize=(12, 6))
y = range(len(labels))
ax.barh(y, pos, label='Positif', color=POS, alpha=0.9)
ax.barh(y, neg, label='Negatif', color=NEG, alpha=0.9, left=pos)
ax.barh(y, neu, label='Netral', color=NEU, alpha=0.9, left=[p+n for p,n in zip(pos, neg)])
ax.set_yticks(list(y))
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('Jumlah Artikel')
ax.set_title('Sentimen per Media \u2014 Transisi Energi Hijau\n(18 Mar \u2013 18 Mei 2026)', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.invert_yaxis()
for i, s in enumerate(sources_sorted):
    ax.text(s['article_count'] + 5, i, str(s['article_count']), va='center', fontsize=9, color=DARK)
plt.tight_layout()
plt.savefig(f"{CHARTS}/01_sentimen_per_media.png", dpi=150, bbox_inches='tight')
plt.close()
print("OK 01_sentimen_per_media.png")

# 2. Entity Sentiment
with open(f"{DIR}/bulk_sentiment.json") as f:
    bulk = json.load(f)

entities_sent = {k: v for k, v in bulk.items() if v.get('article_count', 0) > 0}
ent_names = list(entities_sent.keys())
ent_scores = [entities_sent[e]['average_score'] for e in ent_names]
ent_arts = [entities_sent[e]['article_count'] for e in ent_names]
colors_ent = [POS if s >= 0 else NEG for s in ent_scores]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(ent_names, ent_scores, color=colors_ent, alpha=0.85, edgecolor='white', linewidth=1.2)
ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax.set_ylabel('Rata-rata Skor Sentimen')
ax.set_title('Rata-rata Sentimen per Entitas\n(Keyword-Filtered, 18 Mar \u2013 18 Mei 2026)', fontsize=13, fontweight='bold')
for bar, art in zip(bars, ent_arts):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2,
            h + (0.5 if h >= 0 else -1.5),
            f'n={art}', ha='center', fontsize=9, fontweight='bold')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f"{CHARTS}/02_entity_sentiment.png", dpi=150, bbox_inches='tight')
plt.close()
print("OK 02_entity_sentiment.png")

# 3. Weekly Topic Trend
with open(f"{DIR}/topic_trend.json") as f:
    trend = json.load(f)

weeks = [t['date'] for t in trend]
counts = [t['article_count'] for t in trend]
week_labels = [w[-5:] for w in weeks]

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(range(len(weeks)), counts, alpha=0.3, color=BLUE)
ax.plot(range(len(weeks)), counts, '-o', color=BLUE, linewidth=2.5, markersize=8)
ax.set_xticks(range(len(weeks)))
ax.set_xticklabels(week_labels, rotation=45)
ax.set_ylabel('Jumlah Artikel')
ax.set_title('Volume Pemberitaan Transisi Energi Hijau per Minggu\n(18 Mar \u2013 18 Mei 2026)', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, c in enumerate(counts):
    ax.annotate(str(c), (i, c), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(f"{CHARTS}/03_weekly_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("OK 03_weekly_trend.png")

# 4. Positivity Ratio per Source
fig, ax = plt.subplots(figsize=(10, 5))
ratios = []
src_labels = []
for s in sources_sorted:
    t = s['sentiment_distribution']['positive'] + s['sentiment_distribution']['negative']
    if t > 0:
        ratios.append(s['sentiment_distribution']['positive'] / t * 100)
        src_labels.append(s['source'].replace('_', ' ').title())

colors_ratio = [POS if r >= 50 else NEG for r in ratios]
ax.barh(range(len(ratios)), ratios, color=colors_ratio, alpha=0.85)
ax.axvline(x=50, color='gray', linestyle='--', linewidth=1, label='50% threshold')
ax.set_yticks(range(len(ratios)))
ax.set_yticklabels(src_labels, fontsize=9)
ax.set_xlabel('Rasio Positif (%)')
ax.set_title('Rasio Positif/Negatif per Media\n(dari artikel dengan sentimen jelas)', fontsize=12, fontweight='bold')
ax.legend(loc='lower right')
ax.set_xlim(0, 100)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f"{CHARTS}/04_pos_neg_ratio.png", dpi=150, bbox_inches="tight")
plt.close()
print("OK 04_pos_neg_ratio.png")

print("\nAll charts generated!")