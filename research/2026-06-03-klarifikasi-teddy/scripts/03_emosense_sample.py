#!/usr/bin/env python3
"""
03_emosense_sample.py — Run EmoSense-ID on a small stratified sample
====================================================================
Output: data/emosense_summary.json + data/emosense_sample.jsonl + data/stance_emotion_profiles.json
"""

import csv, json, re, sys, random
from collections import Counter, defaultdict
from pathlib import Path

from tantular.emotion import EmotionClassifier

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / 'data' / 'raw'
OUT = BASE / 'data'
random.seed(42)

# ── Quick label function (same as 02_classify) ──────────────────────────
CATEGORIES = {
    "mendukung": [
        r"setuju|benar|mantap|salut|keren|tepat|bangga|good|respect|sepakat|logis|masuk akal",
        r"presiden.*hebat|prabowo.*terbaik|kerja nyata|hasil nyata|tugas negara",
        r"diplomasi|investasi|triliun",
    ],
    "mengkritik": [
        r"kritik|kritisi|pembohong|bohong|omong kosong|ngawur|ngaco|sampah|gagal|tega",
        r"cuma.*gaya|buang.*uang|boros|uang rakyat|pajak|ngapain|percuma|sinis",
        r"alasan|cari alasan|tidak.*percaya",
    ],
    "sarkasme": [
        r"😂|🤣|😭", r"wkwk|hahaha", r"🤡", r"puh.*sepuh|gas|cihuy|lucu|ngakak",
        r"b*a*e*e|emang.*bisa|serius.*?|asli.*?",
    ],
    "faktual": [
        r"berapa|data|angka|bukti|sumber|fakta|kenapa|mengapa|bagaimana|pertanyaan|tanya",
        r"tolong.*jelaskan|penjelasan|detail|nominal|total",
    ],
}

def label_stance(text: str) -> str:
    t = text.lower()
    scores = {}
    for cat, patterns in CATEGORIES.items():
        count = sum(len(re.findall(p, t)) for p in patterns)
        if count > 0:
            scores[cat] = count
    return max(scores, key=scores.get, default="lainnya")  # type: ignore[arg-type]

# ── Load texts ─────────────────────────────────────────────────────────
META = []
with open(RAW / 'meta-klarifikasi-teddy-instagram-comments.csv', 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        META.append({'account': row['Account'], 'file': row['File Name']})

texts, labels = [], []
for m in META:
    with open(RAW / m['file'], 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, delimiter=';'):
            text = (row.get('text') or '').strip()
            if text:
                texts.append(text)
                labels.append(label_stance(text))

print(f"[LOAD] {len(texts):,} texts with labels")

# ── Stratified sample (small) ─────────────────────────────────────────
SAMPLE = 300
classes = sorted(set(labels))
sample_idx = []
for cat in classes:
    idxs = [i for i, l in enumerate(labels) if l == cat]
    n = max(1, int(SAMPLE * len(idxs) / len(labels)))
    sample_idx.extend(random.sample(idxs, min(n, len(idxs))))
if len(sample_idx) > SAMPLE:
    sample_idx = random.sample(sample_idx, SAMPLE)

sample_idx.sort()
print(f"[SAMPLE] {len(sample_idx)} comments:")
for cat in classes:
    print(f"          {cat}: {sum(1 for i in sample_idx if labels[i]==cat)}")

# ── Run EmoSense ──────────────────────────────────────────────────────
print("[EMO] Loading EmoSense-ID model...", flush=True)
ec = EmotionClassifier()
print("       Model loaded. Running batch classification...", flush=True)

sample_texts = [texts[i] for i in sample_idx]
BATCH = 64
results = []
for i in range(0, len(sample_texts), BATCH):
    batch = sample_texts[i:i+BATCH]
    try:
        results.extend(ec.classify_batch(batch))
    except Exception:
        for t in batch:
            try:
                results.append(ec.classify(t))
            except Exception:
                results.append({})
    print(f"       {min(i+BATCH, len(sample_texts))}/{len(sample_texts)}", flush=True)

# ── Aggregate ──────────────────────────────────────────────────────────
emotion_accum = defaultdict(list)
for r in results:
    for label, prob in r.items():
        emotion_accum[label].append(prob)

emotion_avg = {l: round(sum(v)/len(v), 4) for l, v in emotion_accum.items()}
print(f"[AGG] Avg emotion probabilities:")
for l, v in sorted(emotion_avg.items(), key=lambda x: -x[1]):
    print(f"       {l}: {v:.4f}")

# ── Per-stance emotion profiles ───────────────────────────────────────
stance_emo = {}
for cat in classes:
    cat_i = [j for j, i in enumerate(sample_idx) if labels[i] == cat]
    cat_emos = defaultdict(list)
    for j in cat_i:
        for label, prob in results[j].items():
            cat_emos[label].append(prob)
    if cat_emos:
        stance_emo[cat] = {
            l: round(sum(v)/len(v), 4)
            for l, v in sorted(cat_emos.items(), key=lambda x: -sum(x[1])/len(x[1]))
        }

# ── Dominant emotion per comment (for distribution) ────────────────────
dominant_emo = Counter()
for r in results:
    if r:
        dominant_emo[max(r, key=r.get)] += 1

# ── Save ───────────────────────────────────────────────────────────────
def wj(name, data):
    with open(OUT / name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

wj('emosense_summary.json', {
    'model': 'Aardiiiiy/EmoSense-ID-Indonesian-Emotion-Classifier',
    'sample_size': len(sample_idx),
    'method': 'stratified_sample',
    'emotion_labels': sorted(emotion_avg.keys()),
    'average_probabilities': dict(sorted(emotion_avg.items(), key=lambda x: -x[1])),
    'dominant_emotion_distribution': dict(dominant_emo.most_common()),
})

wj('stance_emotion_profiles.json', stance_emo)

# Sample results as JSONL
with open(OUT / 'emosense_sample.jsonl', 'w', encoding='utf-8') as f:
    for idx, r in zip(sample_idx, results):
        f.write(json.dumps({
            'comment_index': idx,
            'text': texts[idx][:200],
            'stance_keyword': labels[idx],
            'dominant_emotion': max(r, key=r.get) if r else 'unknown',
            'emotion_scores': r,
        }, ensure_ascii=False) + '\n')

print(f"\n[OK] Files written:")
for f in sorted(OUT.glob('emosense_*.json')) + sorted(OUT.glob('emosense_*.jsonl')) + sorted(OUT.glob('stance_emotion_*')):
    print(f"     {f.name:40s} {f.stat().st_size:>8,} bytes")