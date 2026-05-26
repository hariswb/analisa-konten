#!/usr/bin/env python3
"""Compute hourly and daily comment counts.
Output: data/hourly_counts.json"""

import csv, json
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
CSV_PATH = DATA_DIR / 'DX_V_32ip-9_Comments.csv'
OUT_PATH = DATA_DIR / 'hourly_counts.json'

comments = []
null_ts = 0
outlier_ts = 0

with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        ts_raw = (row.get('created_at') or '').strip()
        if not ts_raw:
            null_ts += 1
            continue
        try:
            ts = int(ts_raw)
            if ts < 1451606400 or ts > 1893456000:  # 2016-2030 bounds
                outlier_ts += 1
                continue
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            comments.append({
                'ts': ts,
                'dt': dt,
                'date': dt.strftime('%Y-%m-%d'),
                'hour_wib': (dt.hour + 7) % 24
            })
        except (ValueError, TypeError):
            outlier_ts += 1

valid = len(comments)

# Daily totals
daily = Counter()
for c in comments:
    daily[c['date']] += 1
daily_totals = dict(sorted(daily.items()))

# Wave definitions
wave1_range = ('2026-05-06', '2026-05-09')
wave2_range = ('2026-05-22', '2026-05-26')
wave1_dates_range = [f'2026-05-{d:02d}' for d in range(6, 10)]
wave2_dates_range = [f'2026-05-{d:02d}' for d in range(22, 27)]

# Hourly by wave (WIB)
w1_hourly = Counter()
w2_hourly = Counter()
all_hourly = Counter()
for c in comments:
    all_hourly[c['hour_wib']] += 1
    if wave1_range[0] <= c['date'] <= wave1_range[1]:
        w1_hourly[c['hour_wib']] += 1
    if wave2_range[0] <= c['date'] <= wave2_range[1]:
        w2_hourly[c['hour_wib']] += 1

hourly_by_wave = {
    'wave_1': {f"{h:02d}": w1_hourly[h] for h in range(24)},
    'wave_2': {f"{h:02d}": w2_hourly[h] for h in range(24)}
}
hourly_all_wib = {f"{h:02d}": all_hourly[h] for h in range(24)}

# Find peak hours
w1_peak_h = max(range(24), key=lambda h: w1_hourly[h])
w2_peak_h = max(range(24), key=lambda h: w2_hourly[h])
w1_total = sum(w1_hourly[h] for h in range(24))
w2_total = sum(w2_hourly[h] for h in range(24))

result = {
    'meta': {
        'total_comments': valid + null_ts + outlier_ts,
        'null_timestamps': null_ts,
        'outlier_timestamps': outlier_ts,
        'valid_comments_analyzed': valid,
        'timezone': 'UTC (stored), WIB (UTC+7 for display)',
        'date_range': '2026-05-06 to 2026-05-26',
        'data_file': 'DX_V_32ip-9_Comments.csv'
    },
    'daily_totals': daily_totals,
    'wave_1': {
        'period': f'{wave1_range[0]} to {wave1_range[1]}',
        'total_comments': w1_total,
        'peak_day': f'{max(wave1_dates_range, key=lambda d: daily_totals.get(d, 0))} ({max(daily_totals.get(d, 0) for d in wave1_dates_range)} comments)',
        'peak_hour_wib': f'{w1_peak_h:02d}:00 WIB ({w1_hourly[w1_peak_h]} comments)',
        'peak_hour_utc': f'{(w1_peak_h - 7) % 24:02d}:00 UTC'
    },
    'wave_2': {
        'period': f'{wave2_range[0]} to {wave2_range[1]}',
        'total_comments': w2_total,
        'peak_day': f'{max(wave2_dates_range, key=lambda d: daily_totals.get(d, 0))} ({max(daily_totals.get(d, 0) for d in wave2_dates_range)} comments)',
        'peak_hour_wib': f'{w2_peak_h:02d}:00 WIB ({w2_hourly[w2_peak_h]} comments)',
        'peak_hour_utc': f'{(w2_peak_h - 7) % 24:02d}:00 UTC'
    },
    'hourly_by_wave_wib': hourly_by_wave,
    'hourly_all_wib': hourly_all_wib
}

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"hourly_counts.json written ({valid} valid, {null_ts} null, {outlier_ts} outlier)")