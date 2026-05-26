# Hipotesis: Apakah Lonjakan Engagement Direkayasa?

**Post:** https://www.instagram.com/reel/DX_V_32ip-9
**Akun:** @versevoxmusic
**Dataset:** 36.216 komentar, 33.666 pengguna unik, 6–26 Mei 2026
**Analisis oleh:** Hermes Agent (Tantular NLP + data forensik)

---

## Timeline Rekonstruksi

| Tanggal | Peristiwa |
|---------|-----------|
| **29 Apr** | @vokaliz_netizen (119K TikTok) mengunggah lagu "Kanda My Little Bolu Ketan" → https://www.tiktok.com/@vokaliz_netizen/video/7634163983158758664 |
| **6 Mei** | **@versevoxmusic** memposting reel di Instagram → 13M views, 36K komentar (**dataset kami**) |
| **7 Mei** | @inversi.media memposting versi sama di TikTok → https://www.tiktok.com/@inversi.media/video/7637035308005051655 |
| **6–9 Mei** | **WAVE 1:** 12.393 komentar (organic viral di Instagram Reels) |
| **10–21 Mei** | **BASELINE:** 224–388 komentar/hari (dataran rendah 14 hari) |
| **~18 Mei** | Lagu mulai beredar luas di TikTok, dipakai di berbagai video kreator |
| **20 Mei** | Bahlil Lahadalia dikabarkan menyinggung/mengakui lagu ini |
| **22–23 Mei** | **Sania Leonardo** (3,1M TikTok followers) memposting video reaksi → 2,4M+ likes |
| **22–26 Mei** | **WAVE 2:** 19.644 komentar (cascade TikTok → Instagram) |
| **24 Mei** | Media massa mulai meliput. Akun repost: satriaprabhawa, jogjastudent |
| **25 Mei** | **Pernyataan resmi Golkar:** menyebut lagu sebagai "apresiasi netizen atas kerja keras Pak Bahlil" dan mempersilakan akun afiliasi partai ikut tren |

> **Sumber:** Konversi `createTime=1777467317` dari video @vokaliz_netizen mengonfirmasi unggahan 29 Apr 12:55 UTC. Shazam & Genius mencantumkan 5–7 Mei sebagai tanggal metadata/platform, bukan unggahan asli.

---

## Tiga Hipotesis

### H₀ — Penyebaran Viral Organik Murni
Lonjakan kedua adalah propagasi meme alami melalui mekanisme social graph yang sama dengan Wave 1 — pengguna baru menemukan konten lama melalui share, tag, dan rekomendasi algoritma.

### H₁ — Perilaku Tidak Otentik Terkoordinasi (Astroturfing)
Bot farms, paid engagement services, atau komentar terorchestrasi memproduksi Wave 2 secara artifisial.

### H₂ — Viral Organik yang Diamplifikasi (Paling Konsisten)
Spark viral organik itu nyata, tetapi besarnya Wave 2 diperbesar oleh promotor strategis — reaksi kreator besar, pengakuan figur publik, atau dorongan algoritma lintas platform.

---

## Evidensi untuk H₁ (Astroturfing)

| Indikator | Data | Interpretasi |
|-----------|------|--------------|
| Wave 2 58% lebih besar dari Wave 1 | 19.644 vs 12.393 komentar pada periode lebih pendek | Tidak biasa untuk decay organik murni |
| Proporsi emoji 😭 naik +11pp | 29,2% → 40,1% | Pergeseran komposisi — Wave 2 lebih homogen emosinya |
| Referensi lirik turun | 20,3% → 14,4% | Audiens Wave 2 kurang terikat konten spesifik lagu |
| 99% pengguna Wave 2 baru | 18.281 dari 18.461 tidak ada di Wave 1 | Tidak biasa untuk post berusia 20 hari |

---

## Evidensi yang *Membantah* H₁

| Indikator | Data | Kenapa Bukan Bot |
|-----------|------|------------------|
| **0 copy-paste spam teks** | Semua duplikat eksak adalah emoji strings (😭🤣😂) | Bot farms meninggalkan signature template teks |
| **Hanya 11 burst-users** | 4+ komentar dalam 60 detik — dari 36K total | Dalam dataset bot sungguhan, jumlahnya ratusan+ |
| **24.286 istilah unik** | Dari 35.114 komentar berteks | Bot farms memiliki diversitas leksikal rendah |
| **94,8% pengguna Wave 2 baru** post sekali | 17.330 dari 18.281 | Bots biasanya post banyak atau pola terjadwal |
| **180 cross-wave returners** | Dengan narasi pribadi otentik ("takut hafal" → "udah hafal") | Tidak bisa dipalsukan di scale |
| **Sentimen netral** | Polaritas rata-rata -0,015 | Bot brigades cenderung uniform positive/negative |

---

## Verdict: H₂ — Viral Organik yang Diamplifikasi

**H₁ (astroturfing murni) ditolak.** Data tidak mendukung skenario bot/paid engagement terkoordinasi.

**H₂ diterima.** Mekanisme yang teridentifikasi:

```
                    ╔══════════════════════════╗
                    ║  @versevoxmusic (IG)     ║
                    ║  Post 6 Mei, 13M views   ║
                    ╚══════════════════════════╝
                              │
                              ▼
                    ╔══════════════════════════╗
                    ║  @vokaliz_netizen (TT)   ║
                    ║  Lagu AI, 29 Apr (119K)  ║
                    ╚══════════════════════════╝
                              │
                              ▼
              ┌───────────────────────────────┐
              │  Periode Inkubasi 10-21 Mei    │
              │  Lagu menyebar pelan di TikTok │
              └───────────────────────────────┘
                              │
                    ╔══════════════════════════╗
                    ║  Sania Leonardo (TT)     ║
                    ║  3.1M followers, 22-23   ║
                    ║  Video reaksi, 2.4M likes║
                    ╚══════════════════════════╝
                              │
                              ▼
                    ╔══════════════════════════╗
                    ║  CASCADE: TikTok → IG    ║
                    ║  Wave 2: 19.644 komentar ║
                    ╚══════════════════════════╝
```

**Audiens Wave 2 adalah pengguna TikTok nyata** yang menemukan post Instagram asli melalui reaksi Sania, lalu berkomentar secara organik. Pola mereka berbeda dari audiens Wave 1:
- Lebih banyak emoji (kultur TikTok)
- Lebih sedikit lirik (reaksi ke reaksi, bukan ke lagu langsung)
- 94,8% post sekali dan pergi (perilaku drive-by khas cross-platform)

### Dimensi Politik

Respon Golkar bukan bukti astroturfing, melainkan **narrative capture** — strategi komunikasi yang cerdas:

- Dengan segera membingkai ulang parodi sebagai "apresiasi", mereka menetralisir ujung satir
- Pernyataan bahwa akun afiliasi partai "dipersilakan ikut tren" mengisyaratkan amplifikasi strategis *setelah* gelombang organik terbentuk
- Ini bukan merekayasa engagement, tapi mengontrol narasi dari meme yang sudah hidup

---

## Investigasi Lanjutan yang Diperlukan

Untuk konfirmasi definitif, masih perlu:

- **A)** Verifikasi pernyataan Bahlil 20 Mei (sumber: referensi TikTok, perlu konfirmasi langsung)
- **B)** Cek Instagram Ad Library apakah ada promosi berbayar 22–25 Mei
- **C)** Profil 77 pengguna W2-only dengan 3+ komentar dalam 60 detik — cek apakah membentuk cluster follower yang sama
- **D)** Cross-post fingerprinting: apakah burst-user accounts (terutama @rahmaaa_b, @jsminsslana, @ems06.6 dengan 7+ komentar dalam <60 detik) juga mengomentari post politik lain di hari yang sama

---

## Sumber & Data

- Dataset: `data/DX_V_32ip-9_Comments.csv` (36.216 komentar, 36.437 baris — ~220 *newline* di field URL)
- Analisis forensik: `scripts/engineered_hypothesis.py`
- Analisis konten: `scripts/hypothesis_part2.py`
- Verdict tersimpan: `data/verdict_hypothesis_v2.json`
- Script verdict: `scripts/verdict.py`