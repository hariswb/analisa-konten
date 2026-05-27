#!/usr/bin/env python3
"""Compute daily comment counts and daily emoji occurrence counts.
Output: data/daily_emoji.json"""

import csv, json
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
CSV_PATH = DATA_DIR / 'DX_V_32ip-9_Comments.csv'
OUT_PATH = DATA_DIR / 'daily_emoji.json'


def is_emoji(ch: str) -> bool:
    cp = ord(ch)
    return (
        (0x1F300 <= cp <= 0x1F9FF) or  # Misc Symbols, Emoticons, Supplemental
        (0x1FA00 <= cp <= 0x1FAFF) or  # Chess, Symbols Extended
        (0x2600 <= cp <= 0x27BF) or    # Misc Symbols, Dingbats
        (0x2300 <= cp <= 0x23FF) or    # Misc Technical
        (0xFE00 <= cp <= 0xFE0F) or    # Variation Selectors
        cp == 0x200D or                # ZWJ
        (0x1F1E6 <= cp <= 0x1F1FF) or  # Regional Indicators (flags)
        cp in (0x00A9, 0x00AE, 0x2122,
               0x203C, 0x2049,
               0x20E3,
               0x2139, 0x2194, 0x2195, 0x2196, 0x2197, 0x2198, 0x2199,
               0x21A9, 0x21AA, 0x231A, 0x231B, 0x2328, 0x23CF,
               0x23E9, 0x23EA, 0x23EB, 0x23EC, 0x23ED, 0x23EE, 0x23EF,
               0x23F0, 0x23F1, 0x23F2, 0x23F3, 0x23F8, 0x23F9, 0x23FA,
               0x24C2, 0x25AA, 0x25AB, 0x25B6, 0x25C0, 0x25FB, 0x25FC,
               0x25FD, 0x25FE, 0x2600, 0x2601, 0x2602, 0x2603, 0x2604,
               0x260E, 0x2611, 0x2614, 0x2615, 0x2618, 0x261D, 0x2620,
               0x2622, 0x2623, 0x2626, 0x262A, 0x262E, 0x262F, 0x2638,
               0x2639, 0x263A, 0x2640, 0x2642, 0x2648, 0x2649, 0x264A,
               0x264B, 0x264C, 0x264D, 0x264E, 0x264F, 0x2650, 0x2651,
               0x2652, 0x2653, 0x265F, 0x2660, 0x2663, 0x2665, 0x2666,
               0x2668, 0x267B, 0x267E, 0x267F, 0x2692, 0x2694, 0x2695,
               0x2696, 0x2697, 0x2699, 0x269B, 0x269C, 0x26A0, 0x26A1,
               0x26AA, 0x26AB, 0x26B0, 0x26B1, 0x26BD, 0x26BE, 0x26C4,
               0x26C5, 0x26C8, 0x26CE, 0x26CF, 0x26D1, 0x26D3, 0x26D4,
               0x26E9, 0x26EA, 0x26F0, 0x26F1, 0x26F2, 0x26F3, 0x26F4,
               0x26F5, 0x26F7, 0x26F8, 0x26F9, 0x26FA, 0x26FD, 0x2702,
               0x2705, 0x2708, 0x2709, 0x270A, 0x270B, 0x270C, 0x270D,
               0x270F, 0x2712, 0x2714, 0x2716, 0x271D, 0x2721, 0x2728,
               0x2733, 0x2734, 0x2744, 0x2747, 0x274C, 0x274E, 0x2753,
               0x2754, 0x2755, 0x2757, 0x2763, 0x2764, 0x2795, 0x2796,
               0x2797, 0x27A1, 0x27B0, 0x27BF, 0x2934, 0x2935, 0x2B05,
               0x2B06, 0x2B07, 0x2B1B, 0x2B1C, 0x2B50, 0x2B55, 0x3030,
               0x303D, 0x3297, 0x3299)
    )


comments = []
null_ts = 0
outlier_ts = 0

with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        ts_raw = (row.get('created_at') or '').strip()
        text = (row.get('text') or '')
        if not ts_raw:
            null_ts += 1
            continue
        try:
            ts = int(ts_raw)
            if ts < 1451606400 or ts > 1893456000:  # 2016-2030 bounds
                outlier_ts += 1
                continue
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            date_str = dt.strftime('%Y-%m-%d')
            # Extract emojis from text
            emojis = [ch for ch in text if is_emoji(ch)]
            comments.append({
                'date': date_str,
                'emojis': emojis
            })
        except (ValueError, TypeError):
            outlier_ts += 1

valid = len(comments)

# --- Daily comment counts ---
daily_comment_counts = Counter()
for c in comments:
    daily_comment_counts[c['date']] += 1

# --- Daily emoji counts ---
daily_emoji_counts = defaultdict(Counter)
for c in comments:
    for em in c['emojis']:
        daily_emoji_counts[c['date']][em] += 1

# Sort by date
sorted_dates = sorted(daily_comment_counts.keys())

# Build structured output
daily = {}
for date in sorted_dates:
    emoji_counter = daily_emoji_counts[date]
    total_emoji = sum(emoji_counter.values())
    daily[date] = {
        'comments': daily_comment_counts[date],
        'total_emoji': total_emoji,
        'emoji_breakdown': {
            ch: cnt
            for ch, cnt in emoji_counter.most_common()
        }
    }

# --- Emoji running totals (all days) ---
all_emoji_counter = Counter()
for c in comments:
    for em in c['emojis']:
        all_emoji_counter[em] += 1

# Top 10 emoji overall
top_emoji_overall = [
    {'emoji': ch, 'emoji_code': f'U+{ord(ch):04X}', 'count': cnt, 'pct': round(cnt / sum(all_emoji_counter.values()) * 100, 1)}
    for ch, cnt in all_emoji_counter.most_common(10)
]

# --- Wave summaries ---
wave1_dates = [f'2026-05-{d:02d}' for d in range(6, 10)]
wave2_dates = [f'2026-05-{d:02d}' for d in range(22, 27)]

def sum_wave(date_list, field):
    if field == 'comments':
        return sum(daily_comment_counts.get(d, 0) for d in date_list)
    elif field == 'emoji':
        return sum(sum(daily_emoji_counts.get(d, Counter()).values()) for d in date_list)

# Count total emoji appearances per wave (not just unique types)
w1_emoji_total = sum(sum(daily_emoji_counts.get(d, Counter()).values()) for d in wave1_dates)
w2_emoji_total = sum(sum(daily_emoji_counts.get(d, Counter()).values()) for d in wave2_dates)

result = {
    'meta': {
        'total_comments': valid + null_ts + outlier_ts,
        'null_timestamps': null_ts,
        'outlier_timestamps': outlier_ts,
        'valid_comments_analyzed': valid,
        'date_range': f'{sorted_dates[0]} to {sorted_dates[-1]}',
        'data_file': 'DX_V_32ip-9_Comments.csv'
    },
    'daily': daily,
    'top_emoji_overall': top_emoji_overall,
    'summary': {
        'total_comments': sum(daily_comment_counts.values()),
        'total_emoji_occurrences': sum(all_emoji_counter.values()),
        'unique_emoji_types': len(all_emoji_counter),
        'percent_comments_with_emoji': round(
            sum(1 for c in comments if c['emojis']) / valid * 100, 1
        )
    },
    'wave_1': {
        'period': '2026-05-06 to 2026-05-09',
        'comments': sum(daily_comment_counts.get(d, 0) for d in wave1_dates),
        'emoji_occurrences': w1_emoji_total
    },
    'wave_2': {
        'period': '2026-05-22 to 2026-05-26',
        'comments': sum(daily_comment_counts.get(d, 0) for d in wave2_dates),
        'emoji_occurrences': w2_emoji_total
    }
}

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"daily_emoji.json written ({valid} valid comments, {sum(all_emoji_counter.values())} emoji occurrences)")