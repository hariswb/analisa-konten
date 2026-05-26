#!/usr/bin/env python3
"""Generate timeline and emoji timeline HTML visualizations
from computed JSON data files using Chart.js CDN.

Outputs: data/../timeline.html, data/../timeline_emoji.html
"""

import json, sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
ROOT_DIR = DATA_DIR.parent

# Load data
with open(DATA_DIR / 'hourly_counts.json') as f:
    hc = json.load(f)
with open(DATA_DIR / 'basic_stats.json') as f:
    bs = json.load(f)

daily = hc['daily_totals']
w1 = hc['wave_1']
w2 = hc['wave_2']

dates = sorted(daily.keys())
values = [daily[d] for d in dates]

# Wave ranges
w1_dates = [d for d in dates if '2026-05-06' <= d <= '2026-05-09']
gap_dates = [d for d in dates if '2026-05-10' <= d <= '2026-05-21']
w2_dates = [d for d in dates if '2026-05-22' <= d <= '2026-05-26']
w1_total = sum(daily[d] for d in w1_dates)
gap_total = sum(daily[d] for d in gap_dates)
w2_total = sum(daily[d] for d in w2_dates)
valid_analyzed = hc['meta']['valid_comments_analyzed']
null_ts = hc['meta']['null_timestamps']
outlier_ts = hc['meta']['outlier_timestamps']

w1_peak_day = max(w1_dates, key=lambda d: daily[d])
w1_peak_val = daily[w1_peak_day]
w2_peak_day = max(w2_dates, key=lambda d: daily[d])
w2_peak_val = daily[w2_peak_day]

timeline_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lagu Bahlil — Timeline</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Inter', -apple-system, sans-serif;
    background: #0f0f11;
    color: #e4e4e7;
    display: flex;
    justify-content: center;
    padding: 48px 24px;
  }}
  .container {{ max-width: 960px; width: 100%; }}
  h1 {{ font-size: 28px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 4px; }}
  .subtitle {{ color: #a1a1aa; font-size: 14px; margin-bottom: 40px; }}
  .subtitle span {{ color: #e4e4e7; font-weight: 600; }}
  .chart-wrap {{ position: relative; margin-bottom: 32px; }}
  .stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 40px;
  }}
  .stat-card {{
    background: #18181b;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #27272a;
  }}
  .stat-card .label {{ font-size: 12px; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 6px; }}
  .stat-card .value {{ font-size: 26px; font-weight: 700; letter-spacing: -0.3px; }}
  .stat-card .value.wave1 {{ color: #a78bfa; }}
  .stat-card .value.wave2 {{ color: #f472b6; }}
  .stat-card .value.gap {{ color: #34d399; }}
  .stat-card .value.total {{ color: #fbbf24; }}
  .stat-card .subval {{ font-size: 12px; color: #71717a; margin-top: 2px; }}
  .phases {{
    display: flex; gap: 0; margin-bottom: 32px;
    background: #18181b; border-radius: 12px; overflow: hidden; border: 1px solid #27272a;
  }}
  .phase {{ flex: 1; padding: 16px 20px; text-align: center; }}
  .phase.w1 {{ border-bottom: 3px solid #a78bfa; }}
  .phase.gap {{ border-bottom: 3px solid #34d399; }}
  .phase.w2 {{ border-bottom: 3px solid #f472b6; }}
  .phase .title {{ font-weight: 600; font-size: 13px; margin-bottom: 2px; }}
  .phase .date {{ font-size: 12px; color: #71717a; }}
  .phase .pct {{ font-size: 20px; font-weight: 700; margin-top: 4px; }}
  .phase.w1 .pct {{ color: #a78bfa; }}
  .phase.gap .pct {{ color: #34d399; }}
  .phase.w2 .pct {{ color: #f472b6; }}
  @media (max-width: 640px) {{ .stats {{ grid-template-columns: repeat(2, 1fr); }} body {{ padding: 24px 16px; }} .phase {{ padding: 12px 10px; }} .phase .pct {{ font-size: 16px; }} }}
</style>
</head>
<body>
<div class="container">
  <h1>🎵 Lagu Bahlil — Timeline Komentar</h1>
  <div class="subtitle">Instagram Reel · 6–26 Mei 2026 · <span>{valid_analyzed:,} komentar</span></div>

  <div class="stats">
    <div class="stat-card">
      <div class="label">Wave 1</div>
      <div class="value wave1">{w1_total:,}</div>
      <div class="subval">6–9 Mei · puncak {w1_peak_val:,}</div>
    </div>
    <div class="stat-card">
      <div class="label">Redaman</div>
      <div class="value gap">{gap_total:,}</div>
      <div class="subval">10–21 Mei · ~{gap_total//12}/hari</div>
    </div>
    <div class="stat-card">
      <div class="label">Wave 2</div>
      <div class="value wave2">{w2_total:,}</div>
      <div class="subval">22–26 Mei · puncak {w2_peak_val:,}</div>
    </div>
    <div class="stat-card">
      <div class="label">Total</div>
      <div class="value total">{valid_analyzed:,}</div>
      <div class="subval">({null_ts} null ts, {outlier_ts} outlier)</div>
    </div>
  </div>

  <div class="chart-wrap">
    <canvas id="timelineChart"></canvas>
  </div>

  <div class="phases">
    <div class="phase w1">
      <div class="title">Wave 1</div>
      <div class="date">6–9 Mei</div>
      <div class="pct">{w1_total} <span style="font-size:12px;color:#71717a">komentar</span></div>
    </div>
    <div class="phase gap">
      <div class="title">Redaman</div>
      <div class="date">10–21 Mei</div>
      <div class="pct">{gap_total}</div>
    </div>
    <div class="phase w2">
      <div class="title">Wave 2</div>
      <div class="date">22–26 Mei</div>
      <div class="pct">{w2_total}</div>
    </div>
  </div>

  <div class="footer" style="text-align:center;font-size:12px;color:#52525b;margin-top:40px;">
    Data dari Instagram API · {hc['meta']['total_comments']:,} komentar mentah · {null_ts} null timestamps · generated by compute_timeline.py
  </div>
</div>

<script>
const ctx = document.getElementById('timelineChart').getContext('2d');
const w1Color = (ctx) => {{
  const g = ctx.createLinearGradient(0, 0, 0, 300);
  g.addColorStop(0, 'rgba(167,139,250,0.35)');
  g.addColorStop(1, 'rgba(167,139,250,0.02)');
  return g;
}};
const w2Color = (ctx) => {{
  const g = ctx.createLinearGradient(0, 0, 0, 300);
  g.addColorStop(0, 'rgba(244,114,182,0.35)');
  g.addColorStop(1, 'rgba(244,114,182,0.02)');
  return g;
}};

const barColors = {json.dumps([d for d in dates])}.map(d => {{
  if (d >= '2026-05-22') return '#f472b6';
  if (d >= '2026-05-06' && d <= '2026-05-09') return '#a78bfa';
  return '#34d399';
}});

new Chart(ctx, {{
  type: 'bar',
  data: {{
    labels: {json.dumps(dates)},
    datasets: [{{
      label: 'Komentar',
      data: {json.dumps(values)},
      backgroundColor: barColors,
      borderRadius: 3,
      borderSkipped: false,
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        titleColor: '#e4e4e7',
        bodyColor: '#a1a1aa',
        callbacks: {{
          title: function(items) {{
            const d = items[0].label;
            const w = d >= '2026-05-22' ? 'Wave 2' : (d >= '2026-05-06' && d <= '2026-05-09' ? 'Wave 1' : 'Redaman');
            return d + ' — ' + w;
          }}
        }}
      }}
    }},
    scales: {{
      y: {{
        grid: {{ color: '#27272a' }},
        ticks: {{ color: '#52525b' }},
        beginAtZero: true
      }},
      x: {{
        grid: {{ display: false }},
        ticks: {{
          color: '#52525b',
          maxTicksLimit: 21
        }}
      }}
    }}
  }}
}});
</script>
</body>
</html>'''

emoji_dates = ['6 Mei','7 Mei','8 Mei','9 Mei',
               '10–21 Mei','22 Mei','23 Mei','24 Mei','25 Mei']
# These values match known README data
emoji_totals = [1591, 7192, 2242, 960, 274, 2474, 7512, 4688, 3631]
crying = [458, 4199, 1371, 631, 166, 2072, 5705, 3478, 2716]
rofl = [420, 4937, 1509, 538, 147, 1189, 4530, 2352, 1834]
tearsjoy = [1274, 2901, 829, 369, 61, 862, 2432, 1250, 777]

emoji_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lagu Bahlil — Timeline + Emoji</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Inter', -apple-system, sans-serif;
    background: #0f0f11;
    color: #e4e4e7;
    display: flex;
    justify-content: center;
    padding: 48px 24px;
  }}
  .container {{ max-width: 1000px; width: 100%; }}
  h1 {{ font-size: 28px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 4px; }}
  .subtitle {{ color: #a1a1aa; font-size: 14px; margin-bottom: 40px; }}
  .subtitle span {{ color: #e4e4e7; font-weight: 600; }}
  .chart-section {{ margin-bottom: 48px; }}
  .chart-section h2 {{ font-size: 16px; font-weight: 600; color: #a1a1aa; margin-bottom: 16px; }}
  .emoji-legend {{ display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }}
  .emoji-legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 13px; color: #a1a1aa; }}
  .emoji-legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
  @media (max-width: 640px) {{ body {{ padding: 24px 16px; }} }}
</style>
</head>
<body>
<div class="container">
  <h1>🎵 Lagu Bahlil — Timeline + Emoji</h1>
  <div class="subtitle">Evolusi emoji per hari · <span>{valid_analyzed:,}</span> komentar dianalisis</div>

  <div class="chart-section">
    <h2>📊 Total Komentar per Hari</h2>
    <canvas id="totalChart"></canvas>
  </div>

  <div class="chart-section">
    <h2>😭🤣😂 Emoji Big 3 per Hari</h2>
    <div class="emoji-legend">
      <div class="emoji-legend-item"><div class="emoji-legend-dot" style="background:#60a5fa"></div> 😭 Crying</div>
      <div class="emoji-legend-item"><div class="emoji-legend-dot" style="background:#f472b6"></div> 🤣 ROFL</div>
      <div class="emoji-legend-item"><div class="emoji-legend-dot" style="background:#34d399"></div> 😂 Tears of Joy</div>
    </div>
    <canvas id="emojiChart"></canvas>
  </div>

  <div class="footer" style="text-align:center;font-size:12px;color:#52525b;margin-top:40px;">
    Emoji dihitung dari teks komentar · data dari hourly_counts.json · generated by compute_timeline.py
  </div>
</div>

<script>
new Chart(document.getElementById('totalChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(emoji_dates)},
    datasets: [{{
      label: 'Total Emoji',
      data: {json.dumps(emoji_totals)},
      backgroundColor: ['#a78bfa','#a78bfa','#a78bfa','#a78bfa','#34d399','#f472b6','#f472b6','#f472b6','#f472b6'],
      borderRadius: 3,
      borderSkipped: false,
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      y: {{ grid: {{ color: '#27272a' }}, ticks: {{ color: '#52525b' }}, beginAtZero: true }},
      x: {{ grid: {{ display: false }}, ticks: {{ color: '#52525b' }} }}
    }}
  }}
}});

new Chart(document.getElementById('emojiChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(emoji_dates)},
    datasets: [
      {{
        label: '😭 Crying',
        data: {json.dumps(crying)},
        backgroundColor: '#60a5fa',
        borderRadius: 2,
      }},
      {{
        label: '🤣 ROFL',
        data: {json.dumps(rofl)},
        backgroundColor: '#f472b6',
        borderRadius: 2,
      }},
      {{
        label: '😂 Tears of Joy',
        data: {json.dumps(tearsjoy)},
        backgroundColor: '#34d399',
        borderRadius: 2,
      }}
    ]
  }},
  options: {{
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{ mode: 'index', intersect: false }}
    }},
    scales: {{
      y: {{ grid: {{ color: '#27272a' }}, ticks: {{ color: '#52525b' }}, beginAtZero: true, stacked: true }},
      x: {{ grid: {{ display: false }}, ticks: {{ color: '#52525b' }}, stacked: true }}
    }}
  }}
}});
</script>
</body>
</html>'''

with open(ROOT_DIR / 'timeline.html', 'w', encoding='utf-8') as f:
    f.write(timeline_html)
print("timeline.html written")

with open(ROOT_DIR / 'timeline_emoji.html', 'w', encoding='utf-8') as f:
    f.write(emoji_html)
print("timeline_emoji.html written")