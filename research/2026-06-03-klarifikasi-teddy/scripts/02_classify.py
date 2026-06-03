#!/usr/bin/env python3
"""
02_classify.py — InSetSentiment polarity (standalone)
=====================================================
NO stance labels, NO TF-IDF, NO EmoSense — fully independent.
Runs InSetSentiment on every non-empty comment and outputs
per-comment results + summary statistics.

Outputs:
  data/inset_results.jsonl        — per-comment sentiment
  data/inset_summary.json         — distribution + averages
  data/inset_by_source.json       — per-source sentiment breakdown
"""

import csv, json
from collections import Counter, defaultdict
from pathlib import Path

from tantular.sentiment import InsetSentiment

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / 'data' / 'raw'
OUT = BASE / 'data'

# ── Load data ───────────────────────────────────────────────────────────
META = []
with open(RAW / 'meta-klarifikasi-teddy-instagram-comments.csv', 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        META.append({'account': row['Account'], 'file': row['File Name']})

all_comments = []
for m in META:
    with open(RAW / m['file'], 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, delimiter=';'):
            text = (row.get('text') or '').strip()
            all_comments.append({
                'comment_id': row.get('comment_id', ''),
                'text': text,
                'source': m['account'],
            })

total = len(all_comments)
print(f"[DATA] {total:,} comments loaded")

# ── InSetSentiment ──────────────────────────────────────────────────────
print("[INSET] Running InSetSentiment polarity on all comments...")
inset = InsetSentiment()

sentiment_dist = Counter()
polarity_values = []
raw_scores = []

for c in all_comments:
    if c['text']:
        try:
            result = inset.analyze(c['text'])
            c['inset_label'] = result.get('label', 'neutral')
            c['inset_polarity'] = result.get('polarity', 0.0)
            c['inset_raw_score'] = result.get('raw_score', 0)
        except Exception:
            c['inset_label'] = 'neutral'
            c['inset_polarity'] = 0.0
            c['inset_raw_score'] = 0
    else:
        c['inset_label'] = 'neutral'
        c['inset_polarity'] = 0.0
        c['inset_raw_score'] = 0

    sentiment_dist[c['inset_label']] += 1
    polarity_values.append(c['inset_polarity'])
    raw_scores.append(abs(c['inset_raw_score']))

positive_n = sentiment_dist.get('positive', 0)
negative_n = sentiment_dist.get('negative', 0)
neutral_n = sentiment_dist.get('neutral', 0)
total_classified = positive_n + negative_n + neutral_n

avg_polarity = round(sum(polarity_values) / max(len(polarity_values), 1), 4)
sentiment_ratio = round(positive_n / max(negative_n, 1), 2)

print(f"        Positive: {positive_n:,} ({positive_n/max(total_classified,1)*100:.1f}%)")
print(f"        Negative: {negative_n:,} ({negative_n/max(total_classified,1)*100:.1f}%)")
print(f"        Neutral:  {neutral_n:,} ({neutral_n/max(total_classified,1)*100:.1f}%)")
print(f"        Avg polarity: {avg_polarity} | Pos/Neg ratio: {sentiment_ratio}")

# ── Per-source sentiment ───────────────────────────────────────────────
src_sentiment = defaultdict(lambda: Counter())
for c in all_comments:
    if c['text']:
        src_sentiment[c['source']][c['inset_label']] += 1

# ── Save ────────────────────────────────────────────────────────────────
def wj(name, data):
    with open(OUT / name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

wj('inset_summary.json', {
    'model': 'InSetSentiment (Tantular)',
    'total_comments': total,
    'total_classified': total_classified,
    'sentiment_distribution': {
        'positive': positive_n,
        'negative': negative_n,
        'neutral': neutral_n,
    },
    'sentiment_percentages': {
        'positive_pct': round(positive_n / max(total_classified, 1) * 100, 1),
        'negative_pct': round(negative_n / max(total_classified, 1) * 100, 1),
        'neutral_pct': round(neutral_n / max(total_classified, 1) * 100, 1),
    },
    'avg_polarity': avg_polarity,
    'positive_negative_ratio': sentiment_ratio,
    'avg_abs_raw_score': round(sum(raw_scores) / max(len(raw_scores), 1), 2),
})

wj('inset_by_source.json', {
    src: dict(src_sentiment[src]) for src in sorted(src_sentiment)
})

# JSONL per comment
with open(OUT / 'inset_results.jsonl', 'w', encoding='utf-8') as f:
    for c in all_comments:
        f.write(json.dumps({
            'comment_id': c['comment_id'],
            'source': c['source'],
            'text': c['text'][:200],
            'inset_label': c['inset_label'],
            'inset_polarity': c['inset_polarity'],
            'inset_raw_score': c['inset_raw_score'],
        }, ensure_ascii=False) + '\n')

print(f"\n{'='*60}")
print("[✓] InSetSentiment complete!")
for f in sorted(OUT.glob('inset_*.json')) + sorted(OUT.glob('inset_*.jsonl')):
    print(f"    {f.name:35s} {f.stat().st_size:>8,} bytes")
print(f"{'='*60}")