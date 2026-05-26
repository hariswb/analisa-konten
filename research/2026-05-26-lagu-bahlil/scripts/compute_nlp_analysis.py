#!/usr/bin/env python3
"""NLP analysis: word frequencies (unigrams, bigrams, trigrams),
vocabulary size, sentiment analysis via Tantular InSet.
Output: data/nlp_analysis.json"""

import csv, json, random
from collections import Counter
from pathlib import Path

from tantular import BagOfWords, InsetSentiment

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
CSV_PATH = DATA_DIR / 'DX_V_32ip-9_Comments.csv'
OUT_PATH = DATA_DIR / 'nlp_analysis.json'

# Load CSV
texts = []
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        t = (row.get('text') or '').strip()
        if t:
            texts.append(t)

print(f"Total text comments: {len(texts)}")

# === Bag-of-Words (unigrams, bigrams, trigrams) ===
bow = BagOfWords(min_length=1, ngram_sizes=[1, 2, 3])
term_accum = Counter()
ngram_accum = {1: Counter(), 2: Counter(), 3: Counter()}

for i, t in enumerate(texts):
    r = bow.analyze(t)
    term_accum.update(r.term_freq)
    for n, freqs in r.ngram_freq.items():
        ngram_accum[n].update(freqs)
    if (i + 1) % 5000 == 0:
        print(f"  Processed {i+1}/{len(texts)} comments...")

print(f"  Done. {len(term_accum)} unique terms.")

# Top words
top_unigrams_list = [[word, count] for word, count in term_accum.most_common(50)]

# Format bigrams/trigrams: "b o l u   k e t a n" style
def format_ngram(phrase: str) -> str:
    """Convert 'bolu ketan' to 'b o l u   k e t a n'"""
    return '   '.join(' '.join(w) for w in phrase.split())

top_bigrams_list = [[format_ngram(phrase), count] for phrase, count in ngram_accum[2].most_common(30)]
top_trigrams_list = [[format_ngram(phrase), count] for phrase, count in ngram_accum[3].most_common(20)]
vocab_size = len(term_accum)

# === Sentiment Analysis (InSet) — sample 10% (3512) ===
random.seed(42)
sample_size = 3512
sample = random.sample(texts, min(sample_size, len(texts)))

inset = InsetSentiment(use_stemmer=True)
sample_results = inset.analyze_batch(sample)

label_counts = Counter(r['label'] for r in sample_results)
total_analyzed = len(sample_results)
pos_count = label_counts.get('positive', 0)
neg_count = label_counts.get('negative', 0)
neu_count = label_counts.get('neutral', 0)
pos_pct = round(pos_count / total_analyzed * 100, 1)
neg_pct = round(neg_count / total_analyzed * 100, 1)
neu_pct = round(neu_count / total_analyzed * 100, 1)
avg_pol = round(sum(r.get('polarity', 0) or 0 for r in sample_results) / total_analyzed, 3)

# Get extreme examples
scored = list(zip(sample, sample_results))
scored_sorted = sorted(scored, key=lambda x: x[1].get('raw_score', 0))
most_neg = []
for text, res in scored_sorted[:5]:
    most_neg.append({
        'text': text,
        'score': res.get('raw_score', 0),
        'label': res.get('label', 'unknown')
    })
most_pos = []
for text, res in reversed(scored_sorted[-5:]):
    most_pos.append({
        'text': text,
        'score': res.get('raw_score', 0),
        'label': res.get('label', 'unknown')
    })

result = {
    'top_unigrams': top_unigrams_list,
    'top_bigrams': top_bigrams_list,
    'top_trigrams': top_trigrams_list,
    'vocabulary_size': vocab_size,
    'sentiment': {
        'sample_size': total_analyzed,
        'label_distribution': {
            'neutral': neu_count,
            'negative': neg_count,
            'positive': pos_count
        },
        'polarity_pos_pct': pos_pct,
        'polarity_neg_pct': neg_pct,
        'polarity_neu_pct': neu_pct,
        'avg_polarity': avg_pol,
        'most_negative_examples': most_neg,
        'most_positive_examples': most_pos
    }
}

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"nlp_analysis.json written (vocab={vocab_size}, sentiment n={total_analyzed})")