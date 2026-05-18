# Transisi Energi Hijau di Indonesia

**Periode:** 17 April – 18 Mei 2026  
**Sumber:** Semantik API (12 keyword-filtered + entity-level dengan `topic_keywords`)  
**Kata kunci:** transisi energi, energi hijau, EBT, energi baru terbarukan, energi surya, geothermal, PLTS, PLTA, biomassa, cofiring, CCS, karbon

> **Pembaruan penting:** Semua data entitas (sentimen, timeline, ko-okurensi, framing) sekarang menggunakan `topic_keywords` — hanya artikel dalam topik transisi energi hijau, bukan seluruh artikel lintas topik. Laporan sebelumnya tanpa filter ini sehingga angka entitas tercampur dengan artikel di luar topik.

---

## Ringkasan

Dari 310 artikel tentang transisi energi hijau (12 keyword, 14 media), **PLTS** adalah entitas energi terbarukan paling dominan dengan 39 sebutan (sentimen +1.79, 17 hari berbeda). **PLN** mendapat sentimen positif (+2.31) karena framing-nya seputar cofiring biomassa dan PLTS, bukan pemadaman. **Pertamina** hanya 9 sebutan dalam konteks hijau (turun drastis dari 307 tanpa filter) — framing seputar bioetanol dan LanzaTech.

| Entitas | Artikel (topic-filtered) | Sentimen | Perubahan dari laporan lama |
|---------|:-----------------------:|:--------:|:--------------------------:|
| PLTS | 39 | +1.79 | Sama (39→39) ✅ |
| PLN | 19 | +2.31 | 113→19, −1.03→+2.31 🔄 |
| Prabowo | 12 | +3.20 | 2.109→12 | 🔄 |
| Pertamina | 9 | +1.07 | 307→9 🔄 |
| Karbon | 3 | +1.67 | Sama (3→3) ✅ |
| EBT | 2 | +16.00 | Sama (2→2) ✅ |
| Bahlil | 2 | −2.00 | 231→2 🔄 |
| Nikel | 1 | +8.00 | 49→1 🔄 |

---

## 1. Volume & Sumber

310 artikel dari 14 media nasional.

- Kompas: 56
- CNBC News: 48
- Media Indonesia: 47
- Kumparan: 32
- Republika: 25
- Detik Berita: 23
- Detik Finance: 17
- CNN Ekonomi: 17
- CNBC Market: 12
- Tempo Bisnis: 11
- Tirto: 9
- Liputan6 News: 8
- CNN Nasional: 3
- Tempo Nasional: 2

## 2. Temuan Kunci

1. **PLTS adalah entitas energi hijau paling dominan** — 39 sebutan, sentimen +1.79, 17 hari berbeda. Framing: PLTS atap, PLTS Mentari Nusantara I (1.225 MW), target 100 GW, ekspansi Bangladesh. Satu-satunya entitas yang sepenuhnya relevan dengan transisi energi.

2. **Pertamina: dari 307 ke 9 dengan topic filter** — tanpa filter, data mencakup semua artikel Pertamina (BBM, LPG). Dengan filter, Pertamina dalam konteks hijau hanya 9 artikel (bioetanol Lampung, minyak jelantah, LanzaTech).

3. **PLN positif (+2.31) setelah topic filter** — laporan lama sentimen PLN −1.03 karena tercampur artikel pemadaman Jakarta. Dengan filter topik, framing PLN: cofiring biomassa, PLTS Mentari Nusantara, smart building.

4. **Prabowo 12 artikel dalam konteks energi** (dari 2.109 tanpa filter) — framing terkait PLTS 100 GW dan target energi hijau.

5. **EBT dan Karbon masih minim** — 2-3 artikel. Carbon trading belum masuk pemberitaan mainstream. Ko-okurensi karbon dengan Bank Mandiri dan IDX menunjukkan fokus bursa karbon.

6. **Nikel hanya 1 artikel dalam konteks hijau** — meskipun penting untuk baterai EV, pemberitaan nikel lebih banyak terkait ekstraksi.

## 3. Perubahan Metodologi

✅ **Semua endpoint entity-level sekarang mendukung `topic_keywords`** — data entitas benar-benar spesifik pada topik transisi energi hijau.

❌ Laporan sebelumnya (17 Mei) menggunakan entity-level **tanpa filter topik**, sehingga data entitas tercampur dengan artikel di luar topik.

Dampak: angka sebenarnya 5–20× lebih kecil dari yang dilaporkan sebelumnya. Ini bukan penurunan volume, melainkan koreksi akurasi.

## 4. Keterbatasan

- `articles/search` dibatasi 50 hasil
- Keyword matching masih menghasilkan noise (entity "debt collector" dan "polisi" muncul karena artikel mengandung kata-kata yang cocok secara kebetulan)
- `framing/{word}/by-source` untuk beberapa entitas masih berpotensi corrupt JSON

## Data

- `data/source_comparison.json` — per-media breakdown (keyword-filtered)
- `data/topic_trend.json` — volume mingguan
- `data/articles_search.json` — sample 50 artikel
- `data/{entitas}_sentiment.json` — sentimen per entitas (topic-filtered)
- `data/{entitas}_timeline.json` — sebutan harian (topic-filtered)
- `data/{entitas}_cooccurrence.json` — ko-okurensi (topic-filtered)
- `data/{entitas}_framing.json` — framing per sumber (topic-filtered)

## Notebook

[transisi-energi-hijau-2026.ipynb](transisi-energi-hijau-2026.ipynb) — Jupyter notebook dengan analisis lengkap dan visualisasi.

---

*Dibuat dengan Semantik API + Jupyter Notebook. 17 Apr – 18 Mei 2026. Dataset update: Semua entity-level endpoints menggunakan `topic_keywords` untuk akurasi topik.*
