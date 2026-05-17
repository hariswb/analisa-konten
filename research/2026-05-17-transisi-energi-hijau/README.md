# Transisi Energi Hijau di Indonesia

**Periode:** 17 April – 17 Mei 2026  
**Sumber:** Semantik API (keyword-filtered)  
**Kata kunci:** transisi energi, energi hijau, EBT, energi baru terbarukan, energi surya, geothermal, PLTS, PLTA, biomassa, cofiring, CCS, karbon

---

## Ringkasan

Dari 310 artikel yang membahas transisi energi hijau (12 keyword, 14 media), **Pertamina** tetap mendominasi (307 sebutan) tapi framing-nya seputar BBM, bukan hijau. **PLTS** adalah entitas paling relevan untuk energi terbarukan (39 sebutan, sentimen +1.79). **PLN** mendapat sentimen negatif (−1.03) karena pemadaman listrik Jakarta. **EBT** dan **Karbon** masih sangat minim pemberitaan (2-3 sebutan).

> **Catatan scope:** Volume dan sumber berasal dari endpoint keyword-filtered. Data entitas (sentimen, timeline, ko-okurensi) menggunakan endpoint entity-level — mencakup semua artikel yang menyebut entitas tersebut, bukan hanya dari keyword filter.

---

## 1. Volume & Sumber

310 artikel dari 14 media nasional.

- Kompas: 56
- CNBC News: 48
- Kumparan: 42
- Detik Berita: 29
- Media Indonesia: 21
- Liputan6 News: 17
- CNBC Market: 17
- Detik Finance: 16
- Tirto: 15
- CNN Ekonomi: 14
- CNN Nasional: 13
- Republika: 10
- Detik Health: 7
- Suara: 5

## 2. Sentimen Entitas

| Entitas | Positif | Negatif | Rata-rata | Artikel |
|---------|:---:|:---:|:---:|:---:|
| Pertamina | 277 | 132 | +2.76 | 307 |
| PLN | 71 | 93 | −1.03 | 113 |
| Prabowo | 1,707 | 1,138 | +1.45 | 2,109 |
| Bahlil | 191 | 130 | +2.14 | 231 |
| Nikel | 28 | 17 | +1.06 | 49 |
| PLTS | 33 | 20 | +1.79 | 39 |
| EBT | 2 | 0 | +16.0 | 2 |
| Karbon | 2 | 1 | +1.67 | 3 |

## 3. Temuan Kunci

1. **Volume naik dengan keyword yang lebih luas** — dari 72 (4 keyword) menjadi 310 (12 keyword).

2. **Pertamina mendominasi tapi tidak hijau** — 307 sebutan, sentimen +2.76. Framing-nya tetap seputar BBM, LPG, dan harga.

3. **PLTS adalah entitas paling relevan** — 39 sebutan, sentimen +1.79. Satu-satunya entitas yang benar-benar terkait langsung dengan energi terbarukan.

4. **PLN negatif karena krisis** — sentimen −1.03, framing didominasi pemadaman listrik Jakarta.

5. **EBT dan Karbon sangat minim** — masing-masing 2-3 sebutan. Topik ini belum masuk pemberitaan mainstream.

6. **Nikel ambigu** — terkait batu bara dan ekstraksi, bukan hanya baterai EV.

## 4. Keterbatasan API

- Endpoint entity-level tidak mendukung filter `topic_keywords`. Data entitas mencakup semua artikel lintas topik.
- `articles/search` dibatasi 50 hasil.
- `framing/{word}/by-source` untuk Pertamina mengembalikan JSON corrupt (embedded newlines).

## Data

- `data/source_comparison.json` — per-media breakdown (keyword-filtered)
- `data/topic_trend.json` — volume mingguan
- `data/articles_search.json` — sample 50 artikel
- `data/{entitas}_sentiment.json` — sentimen per entitas
- `data/{entitas}_timeline.json` — sebutan harian
- `data/{entitas}_cooccurrence.json` — ko-okurensi
- `data/{entitas}_framing.json` — framing per sumber

---

*Dibuat dengan Semantik API + Jupyter Notebook. 17 Apr – 17 Mei 2026.*
