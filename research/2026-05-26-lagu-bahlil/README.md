# Lagu Bahlil — Analisis Komentar Instagram

**Post:** https://www.instagram.com/p/DX_V_32ip-9/
**Tanggal posting:** 6 Mei 2026
**Metrik publik:** 13M views, 36k komentar
**Konteks:** Reel berisi lagu AI-generated tentang Bahlil Lahadalia (Menteri Energi, Ketum Golkar). Lagu bergaya parodi/komedi dengan lirik absurd & nada ceria.

## Data

**Sumber:** Instagram API → `data/DX_V_32ip-9_Comments.csv`
**Jumlah:** 36,216 komentar dari 33,666 pengguna unik
**Periode:** 6–26 Mei 2026 (3 minggu)

## Temuan Eksplorasi

### Ringkasan

| Metrik | Nilai |
|--------|-------|
| Total komentar | 36,216 |
| Pengguna unik | 33,666 |
| Komentar dengan teks | 35,114 (97%) |
| Komentar kosong/emoji-only | 1,102 (3%) |
| Rata-rata panjang teks | 29.1 karakter |
| Komentar mengandung emoji | 26,988 (74.5%) |
| Total kemunculan emoji | 64,980 |

### Distribusi Panjang Komentar

Sebagian besar komentar sangat pendek, konsisten dengan komentar organik di Reels:

| Panjang | Jumlah | % |
|---------|--------|---|
| 1–10 karakter | 8,555 | 23.6% |
| 11–30 karakter | 13,509 | 37.3% |
| 31–50 karakter | 8,798 | 24.3% |
| 51–100 karakter | 4,731 | 13.1% |
| 101–200 karakter | 580 | 1.6% |
| 200+ karakter | 43 | 0.1% |

### Timeline (Komentar per Hari)

Dua gelombang utama:

| Tanggal | Komentar | Keterangan |
|---------|----------|------------|
| 6 Mei | 1,668 | Hari posting — awal viral |
| 7 Mei | **7,427** | Puncak gelombang pertama |
| 8–9 Mei | 2,302 → 996 | Menurun |
| 10–21 Mei | 224–388/hari | Dataran rendah (2 minggu) |
| **22 Mei** | **2,564** | **Gelombang kedua mulai** |
| **23 Mei** | **7,762** | **Puncak baru (tertinggi)** |
| 24 Mei | 4,819 | Masih tinggi |
| 25 Mei | 3,711 | Mulai turun |
| 26 Mei | 788 | Partial (hari ini) |

**Pola:** Dua puncak terpisah ~2 minggu — kemungkinan repost/re-share atau embel-embel politik baru yang memicu ulang.

### Aktivitas per Jam (UTC)

Distribusi cukup merata (06:00–17:00 WIB), puncak di jam 01:00–04:00 UTC = 08:00–11:00 WIB (pagi hari Indonesia):

| Jam UTC | Komentar | % |
|---------|----------|---|
| 01:00 (08:00 WIB) | 2,532 | 7.0% |
| 02:00 (09:00 WIB) | 2,517 | 6.9% |
| 03:00 (10:00 WIB) | 2,462 | 6.8% |
| 04:00 (11:00 WIB) | 2,321 | 6.4% |
| 00:00 (07:00 WIB) | 2,234 | 6.2% |

### Emoji

**74.5% komentar mengandung emoji.** Dominasi luar biasa dari 3 emoji:

| Emoji | Kode | Jumlah |
|-------|------|--------|
| 😭 | U+1F62D (Loudly Crying Face) | **23,791** |
| 🤣 | U+1F923 (Rolling on the Floor Laughing) | **20,297** |
| 😂 | U+1F602 (Face with Tears of Joy) | **12,155** |
| 🔥 | U+1F525 (Fire) | 1,682 |
| 😍 | U+1F60D (Heart Eyes) | 834 |
| 👏 | U+1F44F (Clapping Hands) | 823 |
| 😢 | U+1F622 (Crying Face) | 563 |
| ❤ | U+2764 (Red Heart) | 472 |

😭 (23,791) + 🤣 (20,297) + 😂 (12,155) = **56,243 dari 64,980 total** — ini ~86.5% dari semua emoji. Pola emoji ini menunjukkan reaksi **terhibur tapi juga "cringe"** — khas parodi politik yang absurd.

### Top Mentions

| Akun | Disebut |
|------|---------|
| @bahlillahadalia | 426 kali |
| @\_mfr\_18 | 221 |
| @eghgmlr222 | 166 |
| @mom.stefi | 60 |
| @sanialeonardo | 54 |
| @ngga.jo | 53 |
| @kartikasari_lubis | 51 |
| @melangkahdaritimur.id | 50 |
| @ariusav | 45 |
| @afifazizah | 44 |

Tag ke akun Bahlil sendiri (426) menunjukkan sebagian komentar menandai figur publik ini langsung. Akun-akun lain kemungkinan teman yang di-tag untuk "liat ini lucu" — pola viral organik.

## Analisis NLP (dengan Tantular)

### Word Frequency (Top Unigram)

| Kata | Frekuensi |
|------|-----------|
| lagu | 2,794 |
| bolu | 2,555 |
| ketan | 2,441 |
| lagunya | 2,095 |
| my | 2,081 |
| hafal | 2,024 |
| little | 1,884 |
| takut | 1,450 |
| enak | 1,262 |
| bahlil | 1,203 |
| banget | 1,144 |
| hapal | 1,127 |
| terngiang | 967 |
| kanda | 764 |
| mbg | 591 |
| ganteng | 613 |

### Top Bigrams

| Bigram | Frekuensi |
|--------|-----------|
| bolu ketan | 2,322 |
| my little | 1,703 |
| little bolu | 1,554 |
| terngiang ngiang | 510 |
| mas bahlil | 354 |
| takut banget | 334 |
| bahlil ganteng | 311 |
| takut hafal | 303 |
| cilok pentol | 255 |
| pentol kecap | 234 |

### Top Trigrams

| Trigram | Frekuensi |
|---------|-----------|
| little bolu ketan | 1,449 |
| my little bolu | 1,407 |
| mas bahlil ganteng | 257 |
| mbg mas bahlil | 215 |
| cilok pentol kecap | 174 |
| my little cilok | 165 |

**Interpretasi lirik:** Lagu ini adalah parodi dari "My Little Bolu Ketan" — sebuah lagu populer Indonesia. Lirik yang dikomentari paling sering: "my little bolu ketan", "mas bahlil ganteng", "cilok pentol kecap", "terngiang-ngiang", "takut hafal", "harta tahta kakanda", "buah yang manis". Ini adalah lirik absurd/komedi yang melekat di kepala orang.

### Sentimen (InSet Lexicon — sample 3,512 komentar)

| Label | % |
|-------|---|
| Neutral | 54.1% |
| Negative | 23.3% |
| Positive | 22.6% |

**Rata-rata polaritas:** -0.007 (netral)

Polaritas hampir sempurna netral — sedikit lebih ke negatif tapi sangat tipis. Ini masuk akal untuk komentar komedi: kebanyakan orang bereaksi dengan emoji/lucu (neutral), sebagian kecil mengkritik (negative — "fitnah", "bahaya", "dijadikan olokan"), dan sebagian kecil memuji kreativitas (positive).

**Contoh negatif (skor rendah):**
- "Bahaya ini gx mau hapal gak mauu..dengerin nya geli tp kesel itu Gimaaaaaanaaa.." (−20)
- "🤣🤣🤣🤣 fitnah itu lbh kejam dri pembunuhan loh..." (−14)
- "Kenapa sih dia jd olokan org indo bapak ini serius nanya 🙄🙄" (−13)

**Contoh positif (skor tinggi):**
- "enak di denger ni lagu nya.. pinter kreatif emank yg buat ni lagu 😍" (+12)
- "Paduka Yang Mulia, Raja Diraja Maharaja, Sultan Maha Sultan Camerad... sehat selalu Kanda MBG" (+15)
- "Ya Allah Gusti Nu Aguuung...terngiang ngiang ya Allah....Rakyat selucu ini bertarung dengan Buahlil😭😭😂😂😂" (+15)

### Vocabulary

**24,253** istilah unik dari 35,114 komentar berteks — kosakata sangat beragam untuk komentar media sosial.

### Emoji per Hari (Timeline)

Data lengkap di `data/hourly_counts.json`. Visualisasi: `timeline_emoji.html`

| Tanggal | Total | 😭 | 🤣 | 😂 |
|---------|------:|------:|------:|------:|
| 6 Mei | 1,591 | 458 | 420 | 1,274 |
| 7 Mei | 7,192 | 4,199 | 4,937 | 2,901 |
| 8 Mei | 2,242 | 1,371 | 1,509 | 829 |
| 9 Mei | 960 | 631 | 538 | 369 |
| 10–21 Mei | 274–560 | 166–319 | 147–346 | 61–161 |
| 22 Mei | 2,474 | 2,072 | 1,189 | 862 |
| 23 Mei | 7,512 | 5,705 | 4,530 | 2,432 |
| 24 Mei | 4,688 | 3,478 | 2,352 | 1,250 |
| 25 Mei | 3,631 | 2,716 | 1,834 | 777 |

Pola:  **😭** semakin dominan di Wave 2 secara proporsional.

## Analisis Pengguna Kembali

**2,049 pengguna (6.1% dari 33,666)** mengomentari lebih dari sekali, menyumbang **4,572 komentar tambahan**.

### Jarak Komentar 1 → 2

| Metrik | Nilai |
|--------|-------|
| Median | 79 menit |
| Mean | ~52 jam (terdistorsi outlier antar-gelombang) |
| P25 | 1.2 menit |
| P75 | 22.9 jam |

**Distribusi jarak:**
| Rentang | Jumlah | % |
|---------|--------|---|
| ≤1 jam | 1,000 | 48.8% |
| ≤6 jam | 1,237 | 60.4% |
| ≤24 jam | 1,545 | 75.4% |
| ≤1 minggu | 1,800 | 87.8% |
| >1 minggu | 249 | 12.2% |

### Pola Gap Dominan

1. **Tag → reply chain (gap 1–5 menit):** Pola terbanyak — User A men-tag teman, teman membalas dalam hitungan menit. Ini mendorong 48.8% ke ≤1 jam.

2. **Same-minute dual comment (gap 0–2 menit):** Pengguna memposting 2 komentar berturut-turut — biasanya tag ke akun berbeda di komentar terpisah, atau balas diri sendiri.

3. **Cross-wave returning (gap 12–19 hari):** 179 pengguna yang berkomentar di Wave 1 (6–9 Mei) kembali di Wave 2 (22–26 Mei). Median gap: 16 hari.

### Cross-Wave Returning — Analisis Mendalam

**179 pengguna** kembali setelah jeda 12–19 hari (median 16). Temuan kualitatif:

#### Self-Updating Narrative
Tema paling menarik: pengguna berkomentar tentang kekhawatiran/ramalan di Wave 1, lalu kembali di Wave 2 untuk mengonfirmasi bahwa ramalan itu terjadi. Ini seperti *arc cerita mini* yang terentang antar gelombang.

| Pengguna | Wave 1 (6–9 Mei) | Wave 2 (22–26 Mei) |
|----------|-----------------|-------------------|
| @lina_putrie | "Curiga bentar lagi anakku apal 😭" | "dan anakku sudah hafal 😭" |
| @yourembernight | "TAKUT HAPALLLLL😭😭😭😭😭" | "dannn skrg aku udah hapal😭😭😭😭" |
| @otak_random12 | "TAKUT BANGET APAL😭😭😭😭" | "wes apal aku😭😭😭" |
| @nrulishaaaahr_ | "gamau balik ah takut hafal liriknya 😭" | "asem anjr jadi hafal lagunya" |
| @amaliaa_fp | "Gak usah viral viral dong takut anakku 5th apalll" | "waah gawat kan !! aku aja iyaa diem diem nyanyiin ini 😭" |
| @citrus_nobillis | "Bahaya nnti terngiang²" | "kak skrg tambah viral😭" |

#### Persistent Tag Chains
Pasangan pengguna yang saling tag di Wave 1 dan Wave 2, dengan jeda persis 18 hari. Ini menunjukkan konten ini dibagikan dalam jaringan pertemanan yang sama dan tetap relevan berminggu-minggu kemudian.

> @elsasilvyanaaaa__ (8 Mei): "@dndutt.be dinda dicari kakanda buahlil nih wkwkwk"  
> @dndutt.be (8 Mei 7 menit kemudian): "@elsasilvyanaaaa__ takutttt 😫"  
> *(18 hari kemudian — 26 Mei)*  
> @elsasilvyanaaaa__: "@dndutt.be cilok pentol kecap dindaa, emng kau ngenjok dio kecap kebanyakan ndaa"  
> @dndutt.be: "@elsasilvyanaaaa__ jadi hapal lirik depan😭"

#### Wave 2 sebagai "Ini Masih Viral!" Moment
Beberapa pengguna kembali bukan untuk menambah komentar baru, tapi untuk mereaksi bahwa konten ini masih bertahan:

- **@citrus_nobillis**: "Bahaya nnti terngiang²" → "kak skrg tambah viral😭"
- **@hm.almubarok**: "Pak😭 @bahlillahadalia" → "tapi enak lho lagunya"
- **@fahira_nafa**: Kekhawatiran anak hafal → tag teman bagaimana ini masih viral

#### Insight

Keberadaan 179 cross-wave returners (0.5% dari total pengguna) mengonfirmasi bahwa konten ini memiliki **retensi organik yang langka** — tidak seperti kebanyakan viral satu-gelombang yang mati dalam 2–3 hari. Fakta bahwa orang-orang kembali berminggu-minggu kemudian untuk *update* atau *re-tag* menunjukkan bahwa lagu ini menjadi semacam **meme yang hidup di ekosistem pertemanan**, bukan sekadar tontonan sekali lewat.

## Catatan Data

- File CSV asli: 22.4 MB, 36,437 baris (header + 36,436 komentar). Angka sedikit beda dengan 36k yang tertera di Instagram — kemungkinan karena komentar terhapus atau filter API.
- 15 baris memiliki timestamp tidak valid (sebelum posting atau tahun 4401).
- 1 baris timestamp tahun 4401 M — kemungkinan bug scraping dibuang.
- Delimiter CSV: `;`, encoding: UTF-8 BOM.
- `created_at` adalah Unix timestamp (detik sejak epoch).

## Tools

Analisis menggunakan [Tantular](https://github.com/hariswb/tantular) — NLP toolkit for Indonesian text:
- `BagOfWords`: frekuensi kata, n-gram
- `InsetSentiment`: lexicon-based sentiment (offline, tanpa download model)
- Modul lain yang tersedia: NER, emotion classification, entity resolution, co-occurrence network, framing extraction