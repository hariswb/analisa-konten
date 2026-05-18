#!/usr/bin/env python3
"""Classify all 542 articles by relevance for the report override."""
import json, collections

DATA_DIR = '/opt/data/analisa-konten/research/2026-05-18-transisi-energi-hijau/data'
with open(DATA_DIR + '/articles_list.json') as f:
    items = json.load(f)['items']

noise_kws = ['debt collector', 'penagih utang', 'fidusia', 'penggelapan', 'curanmor', 'korupsi', 'suap']
energy_kws = ['plts', 'pltsa', 'energi surya', 'panas bumi', 'geothermal', 'energi baru terbarukan',
              'transisi energi', 'energi hijau', 'karbon', 'cofiring', 'biomassa', 'plta', 'ebt',
              'spklu', 'nuklir', 'hidrogen', 'ccs', 'pembangkit listrik', 'dekarbonisasi',
              'energi bersih', 'energi terbarukan', 'baterai', 'kendaraan listrik']
entity_kws = ['pertamina', 'pln', 'prabowo', 'bahlil', 'eddy soeparno', 'airlangga']

noise_debt = 0
noise_other = 0
energy_primary = 0
energy_context = 0

for a in items:
    title = a.get('title', '')
    text = (title + ' ' + a.get('summary', '')).lower()
    is_noise = any(nk in text for nk in noise_kws)
    has_energy = any(ek in text for ek in energy_kws) or any(ek in text for ek in entity_kws)
    title_energy = any(ek in title.lower() for ek in energy_kws)

    if is_noise and not has_energy:
        if 'debt' in text:
            noise_debt += 1
        else:
            noise_other += 1
    elif has_energy:
        if title_energy:
            energy_primary += 1
        else:
            energy_context += 1
    else:
        noise_other += 1

total = len(items)
relevant = energy_primary + energy_context
print("=== CLASSIFICATION ===")
print(f"Energy (primary topic):  {energy_primary}")
print(f"Energy (context):        {energy_context}")
print(f"Noise (debt collector):  {noise_debt}")
print(f"Noise (other):           {noise_other}")
print(f"\nTotal: {total}")
print(f"Relevant: {relevant} ({relevant/total*100:.1f}%)")
print(f"Noise: {noise_debt+noise_other} ({(noise_debt+noise_other)/total*100:.1f}%)")

# Per-entity in title
print("\n=== TITLE MENTIONS PER ENTITY ===")
for ent in ['plts', 'prabowo', 'pertamina', 'pln', 'pltsa', 'ebt', 'karbon', 'bahlil', 'geothermal']:
    c = sum(1 for a in items if ent in a.get('title','').lower())
    print(f"  {ent}: {c}")

# Per-source from articles alone
source_counts = collections.Counter(a['source'] for a in items)
print("\n=== SOURCE COUNTS ===")
for s, c in source_counts.most_common():
    print(f"  {s}: {c}")

# Weekly trend
from datetime import datetime, timedelta
weekly = collections.Counter()
for a in items:
    d = a.get('published_at', '')[:10]
    if d:
        dt = datetime.strptime(d, '%Y-%m-%d')
        wk = dt - timedelta(days=dt.weekday())
        weekly[wk.strftime('%Y-%m-%d')] += 1
print("\n=== WEEKLY TREND ===")
for wk in sorted(weekly):
    print(f"  Week {wk}: {weekly[wk]}")

# Count exact PLTSA articles
pltsa_arts = [a for a in items if 'pltsa' in (a.get('title','') + ' ' + a.get('summary','')).lower()]
print(f"\nPLTSA articles: {len(pltsa_arts)}")
# Count PLTS only (excluding PLTSA)
plts_arts = [a for a in items if 'plts' in a.get('title','').lower() and 'pltsa' not in a.get('title','').lower()]
print(f"PLTS in title (not PLTSA): {len(plts_arts)}")
