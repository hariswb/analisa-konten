#!/usr/bin/env python3
"""
02b_classify_tfidf.py — Unsupervised TF-IDF + KMeans clustering
===============================================================
NO stance labels, NO InSet, NO EmoSense — fully independent.
Clusters comments by lexical similarity, then we inspect each
cluster's top terms and sample comments to assign human-readable
labels. Pure unsupervised approach.

Outputs:
  data/cluster_results.jsonl       — per-comment cluster assignment
  data/cluster_summary.json        — cluster centroids, top terms, samples, labels
  data/cluster_by_source.json      — cluster distribution per source
"""

import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
import numpy as np

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / 'data' / 'raw'
OUT = BASE / 'data'
N_CLUSTERS = 5
SAMPLE_PER_CLUSTER = 12
random_state = np.random.RandomState(42)

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
train_texts = [c['text'] for c in all_comments if c['text']]
print(f"[DATA] {total:,} comments loaded, {len(train_texts):,} non-empty")

# ── TF-IDF + SVD + KMeans ──────────────────────────────────────────────
print("[TFIDF] Vectorizing...")
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 3), max_df=0.85, min_df=3,
        max_features=5000, sublinear_tf=True,
    )),
    ("svd", TruncatedSVD(n_components=50, random_state=42)),
    ("kmeans", KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init="auto")),
])

labels = pipeline.fit_predict(train_texts)

# Also get distances to centroids for confidence scoring
svd_out = pipeline.named_steps["svd"].transform(
    pipeline.named_steps["tfidf"].transform(train_texts)
)
distances = pipeline.named_steps["kmeans"].transform(svd_out)  # (n_samples, n_clusters)
min_distances = distances.min(axis=1)  # distance to assigned centroid

cluster_counts = Counter(labels)
print(f"[KMEANS] Clusters: {dict(cluster_counts)}")

# ── Get top terms per cluster via centroid analysis ────────────────────
feature_names = pipeline.named_steps["tfidf"].get_feature_names_out()
# Project centroids back to TF-IDF space
# centroids are in SVD space (50-d). To get term importances, we use the
# SVD components to estimate centroid direction in TF-IDF space.
centroids_svd = pipeline.named_steps["kmeans"].cluster_centers_  # (5, 50)
svd_components = pipeline.named_steps["svd"].components_  # (50, n_features_tfidf)
# Approx centroids in TF-IDF space
centroids_tfidf = centroids_svd @ svd_components  # (5, n_features)

cluster_terms = {}
for k in range(N_CLUSTERS):
    centroid = centroids_tfidf[k]
    top_idx = centroid.argsort()[-25:][::-1]
    terms = [(feature_names[i], round(centroid[i], 4)) for i in top_idx]
    cluster_terms[int(k)] = terms

# ── Sample comments from each cluster ──────────────────────────────────
cluster_indices = defaultdict(list)
for idx, lbl in enumerate(labels):
    cluster_indices[int(lbl)].append(idx)

cluster_samples = {}
for k in sorted(cluster_indices.keys()):
    indices = cluster_indices[k]
    # Deterministic sampling using sorted indices
    step = max(1, len(indices) // SAMPLE_PER_CLUSTER)
    sampled = sorted(indices)[::step][:SAMPLE_PER_CLUSTER]
    cluster_samples[int(k)] = [
        {'index': int(i), 'text': train_texts[i][:250]}
        for i in sampled
    ]

# ── Assign human-readable labels based on inspection ────────────────────
print("\n[INSPECT] Cluster content — assigning labels based on top terms & samples:\n")

cluster_labels = {}
for k in sorted(cluster_terms.keys()):
    terms = cluster_terms[k]
    samples = cluster_samples[k]

    print(f"── Cluster {k} ({cluster_counts[k]:,} comments) ──")
    print(f"  Top terms: {', '.join(t[0] for t in terms[:12])}")
    print(f"  Sample comments:")
    for s in samples[:5]:
        print(f"    [{s['index']}] {s['text'][:120]}")
    print()

# ── Assign labels based on term analysis ───────────────────────────────
    # We inspect top terms and sample comments programmatically to label clusters
    for k in range(N_CLUSTERS):
        top_terms_list = [t[0] for t in cluster_terms[k]]

        # Heuristic label assignment based on observed content patterns
        supportive_keywords = {'setuju', 'benar', 'mantap', 'salut', 'keren', 'bangga',
                               'good', 'respect', 'sepakat', 'kerja', 'nyata', 'presiden',
                               'prabowo', 'hebat', 'terbaik', 'diplomasi', 'investasi',
                               'cerdas', 'bermanfaat', 'top', 'mantab'}
        critical_keywords = {'kritik', 'bohong', 'pembohong', 'gagal', 'sampah', 'ngawur',
                             'ngaco', 'bodoh', 'rakyat', 'miskin', 'pajak', 'uang',
                             'boros', 'percuma', 'alasan', 'sinis', 'apbn', 'kurban',
                             'qurban', 'anggaran'}
        sarcasm_keywords = {'wkwk', 'hahaha', 'lucu', 'ngakak', 'meme', 'gas', 'cihuy',
                            '😭', '😂', '🤣', '🤡', 'top', 'puh', 'ngakak', 'wakakaka'}
        factual_keywords = {'berapa', 'data', 'angka', 'bukti', 'sumber', 'fakta',
                            'kenapa', 'mengapa', 'bagaimana', 'pertanyaan', 'tanya',
                            'penjelasan', 'detail', 'nominal', 'total', 'dino', 'bulan',
                            'tahun', '2014', 'diplomatik', 'kemenlu'}
        skeptical_keywords = {'percaya', 'gak percaya', 'ga percaya', 'tidak percaya',
                              'gk percaya', 'kalian percaya', 'lebih percaya'}

        supportive_score = sum(1 for t in top_terms_list if any(kw in t for kw in supportive_keywords))
        critical_score = sum(1 for t in top_terms_list if any(kw in t for kw in critical_keywords))
        sarcasm_score = sum(1 for t in top_terms_list if any(kw in t for kw in sarcasm_keywords))
        factual_score = sum(1 for t in top_terms_list if any(kw in t for kw in factual_keywords))
        skeptical_score = sum(1 for t in top_terms_list if any(kw in t for kw in skeptical_keywords))

        scores = {
            'mendukung': supportive_score,
            'mengkritik': critical_score,
            'sarkasme': sarcasm_score,
            'faktual': factual_score,
            'skeptis': skeptical_score,
        }
        best = max(scores, key=scores.get)
        best_score = scores[best]

        if best_score >= 2:
            cluster_labels[k] = best
        elif best_score == 1 and cluster_counts[k] < 200:
            # Small clusters with weak signal — label as reply/spam
            cluster_labels[k] = 'tagging'
        else:
            cluster_labels[k] = 'umum'

        print(f"  → Cluster {k} labeled as: [{cluster_labels[k]}] "
              f"(mendukung={supportive_score}, mengkritik={critical_score}, "
              f"sarkasme={sarcasm_score}, faktual={factual_score}, "
              f"skeptis={skeptical_score})")

# ── Map to comments ─────────────────────────────────────────────────────
pred_idx = 0
for c in all_comments:
    if c['text']:
        c['cluster_id'] = int(labels[pred_idx])
        c['cluster_label'] = cluster_labels[int(labels[pred_idx])]
        c['cluster_distance'] = round(float(min_distances[pred_idx]), 4)
        pred_idx += 1
    else:
        c['cluster_id'] = -1
        c['cluster_label'] = 'empty'
        c['cluster_distance'] = 0.0

# Per-source cluster distribution
src_cluster = defaultdict(lambda: Counter())
for c in all_comments:
    if c['text']:
        src_cluster[c['source']][c['cluster_label']] += 1

# ── Save ────────────────────────────────────────────────────────────────
def wj(name, data):
    with open(OUT / name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

wj('cluster_summary.json', {
    'method': 'TF-IDF + SVD(50) + KMeans',
    'n_clusters': N_CLUSTERS,
    'total_clustered': len(train_texts),
    'cluster_labels': {str(k): cluster_labels[k] for k in sorted(cluster_labels)},
    'cluster_sizes': {str(k): cluster_counts[k] for k in sorted(cluster_counts)},
    'cluster_terms': {str(k): cluster_terms[k][:15] for k in sorted(cluster_terms)},
    'cluster_samples': {str(k): cluster_samples[k][:6] for k in sorted(cluster_samples)},
    'tfidf_params': {'ngram_range': '(1,3)', 'max_df': 0.85, 'min_df': 3, 'max_features': 5000},
})

wj('cluster_by_source.json', {src: dict(src_cluster[src]) for src in sorted(src_cluster)})

# JSONL per comment
with open(OUT / 'cluster_results.jsonl', 'w', encoding='utf-8') as f:
    for c in all_comments:
        f.write(json.dumps({
            'comment_id': c['comment_id'],
            'source': c['source'],
            'text': c['text'][:200],
            'cluster_id': c['cluster_id'],
            'cluster_label': c['cluster_label'],
            'cluster_distance': c['cluster_distance'],
        }, ensure_ascii=False) + '\n')

print(f"\n{'='*60}")
print("[✓] Unsupervised TF-IDF + KMeans complete!")
for f in sorted(OUT.glob('cluster_*.json')) + sorted(OUT.glob('cluster_*.jsonl')):
    print(f"    {f.name:35s} {f.stat().st_size:>8,} bytes")
print(f"{'='*60}")