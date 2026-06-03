"""
BagOfWords Analysis — Deforestasi Articles
Uses Tantular BagOfWords for n-gram frequency analysis

Usage: python3 scripts/01_bow_analysis.py
"""

import json
from collections import Counter
from pathlib import Path

from tantular.text import TextProcessor
from tantular.bow import BagOfWords

# --- Config ---
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ARTICLES_FILE = DATA_DIR / "articles_list.json"

# --- Load Data ---
with open(ARTICLES_FILE) as f:
    data = json.load(f)
items = data["items"]
print(f"Articles loaded: {len(items)}")
print("=" * 70)

# --- Preprocess (clean each doc) ---
tp = TextProcessor()
texts = []
for a in items:
    doc = f"{a['title']} {a['summary']}"
    texts.append(tp.clean(doc))

# --- Corpus BoW via compare() ---
bow = BagOfWords()
corpus = bow.compare(texts)

# --- Global top unigrams ---
print("\n🔤 TOP 30 TERMS (global frequency)")
print("-" * 50)
for term, count in corpus.top_global(30):
    print(f"  {term:20s} → {count:4d}")

# --- Per-document unigrams (aggregate by source) ---
print("\n📰 TOP 10 TERMS PER SOURCE")
print("-" * 50)
source_texts = {}
source_indices = {}
for i, a in enumerate(items):
    src = a["source"]
    if src not in source_texts:
        source_texts[src] = []
        source_indices[src] = []
    source_texts[src].append(texts[i])
    source_indices[src].append(i)

for src in sorted(source_texts.keys()):
    # Get the result objects for this source's indices
    idxs = source_indices[src]
    combined = Counter()
    for idx in idxs:
        r = corpus.results[idx]
        combined.update(r.term_freq)
    top5 = combined.most_common(10)
    print(f"  {src:20s} (n={len(idxs):2d}): {', '.join(f'{t}({c})' for t, c in top5)}")

# --- N-gram analysis: aggregate bigrams and trigrams across all docs ---
print("\n🔤 TOP 20 BIGRAMS (aggregated across all articles)")
print("-" * 50)
bigram_counter = Counter()
trigram_counter = Counter()
for r in corpus.results:
    bigram_counter.update(r.ngram_freq.get(2, {}))
    trigram_counter.update(r.ngram_freq.get(3, {}))

for phrase, count in bigram_counter.most_common(20):
    print(f"  {phrase:35s} → {count:4d}")

print("\n🔤 TOP 15 TRIGRAMS")
print("-" * 50)
for phrase, count in trigram_counter.most_common(15):
    print(f"  {phrase:45s} → {count:4d}")

# --- Document frequencies (how many articles each term appears in) ---
print("\n📊 MOST WIDELY USED TERMS (appear in most articles)")
print("-" * 50)
doc_freq_sorted = sorted(corpus.doc_freq.items(), key=lambda x: -x[1])[:20]
for term, df in doc_freq_sorted:
    pct = df / len(items) * 100
    print(f"  {term:20s} → {df:3d}/{len(items)} docs ({pct:.0f}%)")

# --- Save to JSON ---
output = {
    "global_top_terms": corpus.top_global(50),
    "doc_frequencies": sorted(corpus.doc_freq.items(), key=lambda x: -x[1])[:50],
    "bigrams": bigram_counter.most_common(30),
    "trigrams": trigram_counter.most_common(20),
    "total_articles": len(items),
}
out_path = DATA_DIR / "bow_ngrams.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\n✅ Saved n-grams to {out_path}")