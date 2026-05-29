#!/usr/bin/env python3
"""Bag-of-words (unigrams + bigrams) split by wave.

Wave 1: 2026-05-06 to 2026-05-09
Wave 2: 2026-05-22 to 2026-05-26

Output: data/wave_bow.json
"""

import csv, json
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

from tantular import BagOfWords

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "DX_V_32ip-9_Comments.csv"
OUT_PATH = DATA_DIR / "wave_bow.json"

WIB = timezone(timedelta(hours=7))

WAVE_1_START = datetime(2026, 5, 6, tzinfo=WIB)
WAVE_1_END   = datetime(2026, 5, 9, 23, 59, 59, tzinfo=WIB)
WAVE_2_START = datetime(2026, 5, 22, tzinfo=WIB)
WAVE_2_END   = datetime(2026, 5, 26, 23, 59, 59, tzinfo=WIB)

w1_texts, w2_texts = [], []

with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        t = (row.get("text") or "").strip()
        ts_raw = (row.get("created_at") or "").strip()
        if not t or not ts_raw:
            continue
        try:
            ts = datetime.fromtimestamp(int(ts_raw), tz=WIB)
        except (ValueError, OSError):
            continue

        if WAVE_1_START <= ts <= WAVE_1_END:
            w1_texts.append(t)
        elif WAVE_2_START <= ts <= WAVE_2_END:
            w2_texts.append(t)

print(f"Wave 1: {len(w1_texts):,} comments | Wave 2: {len(w2_texts):,} comments")

bow = BagOfWords(min_length=1, ngram_sizes=[1, 2])

def compute_bow(texts: list[str], label: str) -> dict:
    unigrams: Counter = Counter()
    bigrams: Counter = Counter()
    for i, t in enumerate(texts):
        r = bow.analyze(t)
        unigrams.update(r.term_freq)
        bigrams.update(r.ngram_freq.get(2, {}))
        if (i + 1) % 5000 == 0:
            print(f"  [{label}] {i+1}/{len(texts)}...")
    print(f"  [{label}] done. {len(unigrams):,} unique unigrams, {len(bigrams):,} unique bigrams.")
    return {
        "total_comments": len(texts),
        "top_unigrams": [[w, c] for w, c in unigrams.most_common(50)],
        "top_bigrams":  [[p, c] for p, c in bigrams.most_common(30)],
        "vocab_size": len(unigrams),
    }

result = {
    "meta": {
        "wave_1_period": "2026-05-06 to 2026-05-09",
        "wave_2_period": "2026-05-22 to 2026-05-26",
    },
    "wave_1": compute_bow(w1_texts, "wave_1"),
    "wave_2": compute_bow(w2_texts, "wave_2"),
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"wave_bow.json written → {OUT_PATH}")
