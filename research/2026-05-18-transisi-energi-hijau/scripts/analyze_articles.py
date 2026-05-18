#!/usr/bin/env python3
"""
Analyze all 542 articles from articles_list.json.
Re-validate per-source counts, noise levels, entity mentions, and date coverage.
"""
import json, collections, sys, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
ARTICLES_PATH = os.path.join(DATA_DIR, 'articles_list.json')

with open(ARTICLES_PATH) as f:
    data = json.load(f)

items = data['items']
print(f"Loaded {len(items)} articles")

# --- Per-source counts ---
source_counts = collections.Counter()
noise_articles = []
energy_keywords = ['energi', 'plts', 'pltsa', 'plta', 'ebt', 'karbon', 'panas bumi',
                   'geothermal', 'biomassa', 'cofiring', 'nuklir', 'surya',
                   'listrik', 'emisi', 'hijau', 'batu bara', 'minyak', 'lng',
                   'ccs', 'hidrogen', 'spklu']
noise_keywords = ['debt collector', 'polisi', 'penggelapan', 'curanmor', 'kriminal',
                  'penangkapan', 'tindak pidana', 'narkoba', 'korupsi', 'suap']

for a in items:
    text = (a.get('title', '') + ' ' + a.get('summary', '')).lower()
    source_counts[a['source']] += 1
    if any(nk in text for nk in noise_keywords):
        noise_articles.append(a)

print("\n=== Source counts (from articles_list) ===")
for src, cnt in source_counts.most_common():
    print(f"  {src}: {cnt}")

# Reference from source_comparison.json
reference = {
    "kompas": 90, "cnbc_news": 85, "media_indonesia": 85, "kumparan": 57,
    "detik_berita": 45, "republika": 44, "cnn_ekonomi": 30, "detik_finance": 29,
    "cnbc_market": 20, "tirto": 17, "tempo_bisnis": 15, "liputan6_news": 14,
    "tempo_nasional": 6, "cnn_nasional": 5
}

print("\n=== Comparison vs source_comparison.json ===")
print(f"  Reference total: {sum(reference.values())}")
print(f"  Actual total:    {sum(source_counts.values())}")
any_diff = False
for src in sorted(set(list(reference.keys()) + list(source_counts.keys()))):
    ref = reference.get(src, 0)
    actual = source_counts.get(src, 0)
    if ref != actual:
        print(f"  ❌ {src}: ref={ref}, actual={actual}")
        any_diff = True
if not any_diff:
    print("  ✅ Perfect match between articles_list and source_comparison")

# Noise analysis
print(f"\n=== Noise articles (crime/irrelevant) ===")
noise_categories = collections.Counter()
for a in noise_articles:
    text = (a.get('title', '') + ' ' + a.get('summary', '')).lower()
    for nk in noise_keywords:
        if nk in text:
            noise_categories[nk] += 1
print(f"  Total noise: {len(noise_articles)} articles ({len(noise_articles)/len(items)*100:.1f}%)")
for nk, cnt in noise_categories.most_common():
    print(f"  \"{nk}\": {cnt} articles")
print("\n  Examples:")
for a in noise_articles[:8]:
    print(f"    [{a['source']}] {a['title'][:90]}")

# Entity mentions in titles
entity_in_title = collections.Counter()
entity_in_text = collections.Counter()
target_entities = ['plts', 'pltsa', 'prabowo', 'pertamina', 'pln', 'ebt', 'karbon',
                   'geothermal', 'biomassa', 'cofiring', 'plta', 'bahlil',
                   'energi surya', 'panas bumi', 'nuklir', 'hidrogen']

for a in items:
    title = a.get('title', '').lower()
    text = (title + ' ' + a.get('summary', '')).lower()
    for ent in target_entities:
        # Title-only match (more precise)
        if ent in title:
            entity_in_title[ent] += 1
        if ent in text:
            entity_in_text[ent] += 1

print(f"\n=== Entity mentions (title vs all text) ===")
print(f"  {'Entity':<20} {'Title':>8} {'All Text':>10}")
print(f"  {'-'*20} {'-'*8} {'-'*10}")
for ent in target_entities:
    print(f"  {ent:<20} {entity_in_title[ent]:>8} {entity_in_text[ent]:>10}")

# Date range
dates = [a['published_at'][:10] for a in items if a.get('published_at')]
date_counts = collections.Counter(dates)
print(f"\n=== Date range: {min(dates)} to {max(dates)} ===")
print(f"  Unique days: {len(date_counts)}")
print(f"  Top 10 busiest days:")
for d, c in date_counts.most_common(10):
    print(f"    {d}: {c} articles")

# Weekly volume (for trend verification)
from datetime import datetime
weekly = collections.Counter()
for d in dates:
    dt = datetime.strptime(d, '%Y-%m-%d')
    week_start = dt - __import__('datetime').timedelta(days=dt.weekday())
    weekly[week_start.strftime('%Y-%m-%d')] += 1

print(f"\n=== Weekly trend ===")
for wk in sorted(weekly):
    print(f"  Week of {wk}: {weekly[wk]} articles")

# PLTSA detection vs PLTS
pltsa_articles = [a for a in items if 'pltsa' in (a.get('title', '') + ' ' + a.get('summary', '')).lower()]
plt_only_articles = [a for a in items if 'plts' in a.get('title', '').lower() and 'pltsa' not in a.get('title', '').lower()]

print(f"\n=== PLTS vs PLTSA ===")
print(f"  PLTS in title (not PLTSA): {len(plt_only_articles)}")
print(f"  PLTSA mentioned:           {len(pltsa_articles)}")

# Export clean data for report generation
print(f"\n=== Exporting clean stats ===")
output = {
    'total_articles': len(items),
    'noise_count': len(noise_articles),
    'noise_pct': round(len(noise_articles)/len(items)*100, 1),
    'source_counts': dict(source_counts.most_common()),
    'entity_in_title': dict(entity_in_title.most_common()),
    'entity_in_text': dict(entity_in_text.most_common()),
    'weekly_trend': {wk: weekly[wk] for wk in sorted(weekly)},
}
stats_path = os.path.join(DATA_DIR, 'article_analysis_stats.json')
with open(stats_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"  Saved to {stats_path}")
