#!/usr/bin/env python3
"""Extract per-entity articles from full 542 dataset for report quality check."""
import json, collections, os

DATA_DIR = '/opt/data/analisa-konten/research/2026-05-18-transisi-energi-hijau/data'
with open(os.path.join(DATA_DIR, 'articles_list.json')) as f:
    data = json.load(f)
items = data['items']

keywords = {
    'PLTS': ['plts'],
    'PLTSA': ['pltsa'],
    'Prabowo': ['prabowo', 'presiden'],
    'Pertamina': ['pertamina', 'pge'],
    'PLN': ['pln'],
    'EBT': ['ebt', 'energi baru terbarukan'],
    'Karbon': ['karbon'],
    'Bahlil': ['bahlil'],
    'Geothermal': ['geothermal', 'panas bumi'],
    'Biomassa': ['biomassa'],
    'PLTA': ['plta']
}

entity_articles = {e: [] for e in keywords}
for a in items:
    title = a.get('title', '').lower()
    summary = a.get('summary', '').lower()
    for ent_name, kws in keywords.items():
        for kw in kws:
            if kw in title or kw in summary:
                entity_articles[ent_name].append(a)
                break

# Print per-entity
for ent_name in ['PLTS', 'PLTSA', 'Prabowo', 'Pertamina', 'PLN', 'EBT', 'Karbon']:
    arts = entity_articles[ent_name]
    # PLTS filter
    if ent_name == 'PLTS':
        arts = [a for a in arts if 'pltsa' not in (a.get('title','') + ' ' + a.get('summary','')).lower()]
    
    print(f"\n{'='*70}")
    print(f"{ent_name}: {len(arts)} articles")
    print(f"{'='*70}")
    sources = collections.Counter(a['source'] for a in arts)
    print(f"  Sources: {dict(sources.most_common(8))}")
    for a in arts[:5]:
        d = a.get('published_at','')[:10]
        s = a['source']
        t = a['title'][:100]
        su = a.get('summary','')[:120]
        print(f"  [{d}] [{s}] {t}")
        print(f"    {su}")
        print()

# Cross-reference with bulk_sentiment
with open(os.path.join(DATA_DIR, 'bulk_sentiment.json')) as f:
    bulk = json.load(f)

print(f"\n{'='*70}")
print("CROSS-REFERENCE: text-mentions vs bulk_sentiment.article_count")
print(f"{'='*70}")
cross = {
    'PLTS': ('plts', 'PLTS'),
    'PLTSA': ('pltsa', 'PLTSA'),
    'Prabowo': ('prabowo', 'Prabowo'),
    'Pertamina': ('pertamina', 'Pertamina'),
    'PLN': ('pln', 'PLN'),
    'EBT': ('ebt', 'EBT'),
    'Karbon': ('karbon', 'Karbon'),
}
for label, (bulk_key, ent_label) in cross.items():
    arts = entity_articles[label]
    if label == 'PLTS':
        arts = [a for a in arts if 'pltsa' not in (a.get('title','') + ' ' + a.get('summary','')).lower()]
    mention = len(arts)
    bc = bulk.get(bulk_key, {}).get('article_count', 'N/A')
    print(f"  {label:<10} text-mentions: {mention:<4} | bulk_sentiment count: {bc}")
