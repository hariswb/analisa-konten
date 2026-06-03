#!/usr/bin/env python3
"""
01_process.py — Process raw Instagram comments → JSON files for dashboard
======================================================================
Produces self-contained JSON files under data/ that the HTML dashboard
fetches at runtime. No matplotlib/seaborn dependency; pure data processing.
"""

import csv, json, re, os
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime, timezone

from tantular.text import TextProcessor
from tantular.bow import BagOfWords

# ── Paths ──────────────────────────────────────────────────────────────────
BASE   = Path(__file__).resolve().parent.parent
RAW    = BASE / 'data' / 'raw'
OUT    = BASE / 'data'
CHARTS = BASE / 'charts'
CHARTS.mkdir(parents=True, exist_ok=True)

# ── 1. Load meta ────────────────────────────────────────────────────────────
META = []
with open(RAW / 'meta-klarifikasi-teddy-instagram-comments.csv', 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        META.append({
            'account': row['Account'],
            'file': row['File Name'],
            'url': row['Post URL'],
            'rows': int(row['Row Count']),
            'followers': int(row['Account Follower']),
            'likes': int(row['Post Like']),
        })

# ── 2. Load all comments ──────────────────────────────────────────────────
all_comments = []
for m in META:
    with open(RAW / m['file'], 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, delimiter=';'):
            text = (row.get('text') or '').strip()
            # Parse timestamp
            ts_raw = row.get('created_at', '')
            ts = None
            try:
                ts = int(ts_raw)
            except (ValueError, TypeError):
                pass
            all_comments.append({
                'comment_id': row.get('comment_id', ''),
                'created_at_epoch': ts,
                'text': text,
                'username': row.get('username', ''),
                'source': m['account'],
            })

total = len(all_comments)
unique_users = len(set(c['username'] for c in all_comments if c['username']))
texts_with_content = [c['text'] for c in all_comments if len(c['text']) > 0]
avg_len = round(sum(len(t) for t in texts_with_content) / max(len(texts_with_content), 1), 1)

print(f"[1/6] Loaded {total:,} comments, {unique_users:,} unique users")

# ── 3. Per-source stats ─────────────────────────────────────────────────
source_stats = {}
for m in META:
    src = m['account']
    src_comments = [c for c in all_comments if c['source'] == src]
    source_stats[src] = {
        'file': m['file'],
        'url': m['url'],
        'followers': m['followers'],
        'likes': m['likes'],
        'total_comments': len(src_comments),
        'unique_commenters': len(set(c['username'] for c in src_comments if c['username'])),
    }

# ── 4. Hourly distribution ─────────────────────────────────────────────
hourly = Counter()
for c in all_comments:
    if c['created_at_epoch']:
        try:
            hour = datetime.fromtimestamp(c['created_at_epoch'], tz=timezone.utc).hour
            hourly[hour] += 1
        except (OSError, ValueError):
            pass

peak_hour = max(hourly, key=hourly.get)  # type: ignore[arg-type]
peak_count = hourly.get(peak_hour, 0)

print(f"[2/6] Hourly dist computed — peak at {peak_hour}:00 UTC ({peak_count:,})")

# ── 5. Stance classification (keyword-based) ────────────────────────────
CATEGORIES = {
    "mendukung": [
        r"setuju", r"benar", r"mantap", r"salut", r"keren", r"tepat",
        r"presiden.*hebat", r"prabowo.*terbaik", r"kerja nyata",
        r"terbukti", r"hasil nyata", r"bangga", r"good", r"respect",
        r"sepakat", r"logis", r"masuk akal", r"tugas negara",
        r"diplomasi", r"investasi", r"triliun",
    ],
    "mengkritik": [
        r"kritik", r"kritisi", r"pembohong", r"bohong", r"omong kosong",
        r"ngawur", r"ngaco", r"sampah", r"rakyat", r"miskin",
        r"tidak.*percaya", r"gagal", r"cuma.*gaya", r"pajak",
        r"buang.*uang", r"boros", r"uang rakyat", r"tega",
        r"ngapain", r"percuma", r"sinis", r"alasan", r"cari alasan",
    ],
    "sarkasme": [
        r"😭", r"😂", r"🤣", r"wkwk", r"wkwkwk", r"hahaha",
        r"b*a*e*e", r"cihuy", r"gas", r"🤡", r"top", r"cepet",
        r"puh.*", r"puh sepuh", r"emang.*bisa", r"serius.*?",
        r"asli.*?", r"lucu", r"meme", r"ngakak",
    ],
    "faktual": [
        r"berapa", r"data", r"angka", r"bukti", r"sumber",
        r"tolong.*jelaskan", r"penjelasan", r"detail",
        r"fakta", r"kenapa", r"mengapa", r"bagaimana",
        r"pertanyaan", r"tanya", r"nominal", r"total",
    ],
}


def classify_stance(text: str) -> str:
    t = text.lower()
    scores = {}
    for cat, patterns in CATEGORIES.items():
        count = sum(len(re.findall(p, t)) for p in patterns)
        if count > 0:
            scores[cat] = count
    return max(scores, key=scores.get) if scores else "lainnya"  # type: ignore[arg-type]


for c in all_comments:
    c['stance'] = classify_stance(c['text'])

stance_counts = Counter(c['stance'] for c in all_comments)
stance_by_source = defaultdict(lambda: Counter())
for c in all_comments:
    stance_by_source[c['source']][c['stance']] += 1

print(f"[3/6] Stance classified: {dict(stance_counts)}")

# ── 6. Tantular BagOfWords ─────────────────────────────────────────────
tp = TextProcessor()
bow = BagOfWords(ngram_sizes=[2])

texts_filtered = [c['text'] for c in all_comments if len(c['text']) > 3]
cleaned = [tp.clean(t) for t in texts_filtered]
corpus = bow.compare(cleaned)
global_top = corpus.top_global(50)

# Per-source BoW samples
source_texts = defaultdict(list)
for c in all_comments:
    if len(c['text']) > 3:
        source_texts[c['source']].append(c['text'])

source_bow = {}
for src, st in source_texts.items():
    s_clean = [tp.clean(t) for t in st[:300]]
    if len(s_clean) >= 3:
        try:
            source_bow[src] = bow.compare(s_clean).top_global(20)
        except Exception:
            source_bow[src] = []

print(f"[4/6] Tantular BoW: {len(global_top)} global terms extracted")

# ── 7. Emoji extraction ────────────────────────────────────────────────
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF"
    "\U00002600-\U000027BF\U00002300-\U000023FF"
    "\U0000FE00-\U0000FE0F\U00001F1E6-\U00001F1FF"
    "\U000000A9\U000000AE\U00002122\U0000203C"
    "\U00002049\U000020E3\U00002139"
    "\U00002194-\U00002199\u200D]+"
)

emoji_counts = Counter()
for c in all_comments:
    for e in EMOJI_RE.findall(c['text']):
        emoji_counts[e] += 1

print(f"[5/6] Extracted {len(emoji_counts)} unique emojis")

# ── 8. Top commenters & text length distribution ──────────────────────
user_counts = Counter(c['username'] for c in all_comments if c['username'])
top_commenters = user_counts.most_common(50)

# Text length histogram bins (0–500 chars, step 20)
lengths = [len(c['text']) for c in all_comments if c['text']]
len_bins = []
for bin_start in range(0, 500, 20):
    bin_end = bin_start + 20
    count = sum(1 for l in lengths if bin_start <= l < bin_end)
    len_bins.append({'bin_label': f'{bin_start}-{bin_end}', 'count': count})
# Tail bin for >500
len_bins.append({'bin_label': '500+', 'count': sum(1 for l in lengths if l >= 500)})

# Comment length categories
short_count = sum(1 for l in lengths if 1 <= l < 20)
medium_count = sum(1 for l in lengths if 20 <= l <= 200)
long_count = sum(1 for l in lengths if l > 200)

print(f"[6/6] Computed text distribution")

# ── 9. Write all JSON files ────────────────────────────────────────────
def write_json(filename, data):
    path = OUT / filename
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

write_json('meta.json', {
    'title': 'Klarifikasi Seskab Teddy — Instagram Comments EDA',
    'source_count': len(META),
    'total_comments': total,
    'unique_commenters': unique_users,
    'avg_comment_length': avg_len,
    'empty_comments': sum(1 for c in all_comments if not c['text']),
    'peak_hour_utc': peak_hour,
    'peak_hour_count': peak_count,
    'generated_at': '2026-06-04T00:00:00Z',
})

write_json('source_stats.json', source_stats)
write_json('hourly_distribution.json', [{'hour': h, 'count': hourly.get(h, 0)} for h in range(24)])

stance_order = ['mendukung', 'mengkritik', 'sarkasme', 'faktual', 'lainnya']
write_json('stance_distribution.json', [
    {'category': s, 'count': stance_counts.get(s, 0)} for s in stance_order
])

# Per-source stance as nested object
write_json('stance_by_source.json', {
    src: dict(stance_by_source[src]) for src in source_stats
})

write_json('top_terms.json', [
    {'term': t[0], 'freq': t[1]} for t in global_top
])

write_json('emoji_top.json', [
    {'emoji': e, 'count': c} for e, c in emoji_counts.most_common(30)
])

write_json('top_commenters.json', [
    {'username': u, 'count': c} for u, c in top_commenters
])

write_json('text_lengths.json', {
    'bins': len_bins,
    'categories': {
        'short_1_19': short_count,
        'medium_20_200': medium_count,
        'long_200_plus': long_count,
    },
    'avg_length': avg_len,
    'median_length': sorted(lengths)[len(lengths)//2] if lengths else 0,
})

# Per-source top terms (for the top 5 sources)
top5_sources = sorted(source_stats, key=lambda s: source_stats[s]['total_comments'], reverse=True)[:5]
write_json('source_terms.json', {
    src: [{'term': t[0], 'freq': t[1]} for t in source_bow.get(src, [])]
    for src in top5_sources
})

print(f"\n{'='*60}")
print(f"[✓] All JSON files written to {OUT}/")
for f in sorted(OUT.glob('*.json')):
    size = f.stat().st_size
    print(f"    {f.name:30s} {size:>8,} bytes")
print(f"{'='*60}")