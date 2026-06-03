#!/usr/bin/env python3
"""
01_eda_dashboard.py — Pure HTML+Chart.js Dashboard
===================================================
NO matplotlib, NO seaborn, NO PNG generation.
Loads all pre-existing JSON files from data/ and builds a
single self-contained HTML dashboard with Chart.js (CDN).

Run AFTER: 01_process.py, 02_classify.py, 02b_classify_tfidf.py, 03_emosense_sample.py
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT_DATA = BASE / 'data'
CHARTS = BASE / 'charts'
CHARTS.mkdir(parents=True, exist_ok=True)

# ── Load all JSON data files ────────────────────────────────────────────
def load_json(name):
    p = OUT_DATA / name
    if p.exists():
        with open(p) as f:
            return json.load(f)
    print(f"  [WARN] {name} not found — skipping")
    return {}

meta = load_json('meta.json')
source_stats = load_json('source_stats.json')
hourly = load_json('hourly_distribution.json')
stance_dist = load_json('stance_distribution.json')
stance_by_source = load_json('stance_by_source.json')
top_terms = load_json('top_terms.json')
emoji_top = load_json('emoji_top.json')
top_commenters = load_json('top_commenters.json')
source_terms = load_json('source_terms.json')
text_lengths = load_json('text_lengths.json')
inset_summary = load_json('inset_summary.json')
inset_by_source = load_json('inset_by_source.json')
emosense_summary = load_json('emosense_summary.json')
cluster_summary = load_json('cluster_summary.json')

total = meta.get('total_comments', 0)
src_count = meta.get('source_count', 0)
unique_commenters = meta.get('unique_commenters', 0)
avg_len = meta.get('avg_comment_length', 0)

# ── Build HTML ──────────────────────────────────────────────────────────
def fmt(n):
    if isinstance(n, (int, float)):
        return f'{n:,}'
    return str(n)

# Stance colors
STANCE_COLORS = {
    'mendukung': '#2ecc71', 'mengkritik': '#e74c3c',
    'sarkasme': '#f39c12', 'faktual': '#3498db', 'lainnya': '#95a5a6',
}

SOURCE_TERMS_ACCTS = list(source_terms.keys()) if source_terms else []

# Serialize data to JSON strings
meta_json = json.dumps(meta)
source_stats_json = json.dumps(source_stats)
hourly_json = json.dumps(hourly)
stance_dist_json = json.dumps(stance_dist)
stance_by_source_json = json.dumps(stance_by_source)
top_terms_json = json.dumps(top_terms[:30] if top_terms else [])
emoji_top_json = json.dumps(emoji_top[:25] if emoji_top else [])
top_commenters_json = json.dumps(top_commenters[:25] if top_commenters else [])
source_terms_json = json.dumps(source_terms)
text_lengths_json = json.dumps(text_lengths)
inset_summary_json = json.dumps(inset_summary)
inset_by_source_json = json.dumps(inset_by_source)
emosense_summary_json = json.dumps(emosense_summary)
cluster_summary_json = json.dumps(cluster_summary)
stance_colors_json = json.dumps(STANCE_COLORS)
stance_order_json = json.dumps(['mendukung','mengkritik','sarkasme','faktual','lainnya'])

# Build the HTML template using Python string replacement (not f-string for JS)
# to avoid JSON brace escaping issues
html_template = '''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EDA Dashboard — Klarifikasi Seskab Teddy</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Inter', sans-serif; background: #0f1923; color: #e0e6ed; padding: 20px; }
  .container { max-width: 1400px; margin: 0 auto; }
  h1 { font-size: 28px; font-weight: 800; color: #fff; margin-bottom: 4px; }
  .subtitle { color: #8899aa; font-size: 14px; margin-bottom: 30px; }
  .subtitle a { color: #66b0ff; }
  .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 30px; }
  .card { background: #1a2836; border-radius: 12px; padding: 20px; border: 1px solid #2a3a4a; }
  .card .num { font-size: 32px; font-weight: 700; color: #fff; }
  .card .label { font-size: 12px; color: #8899aa; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }
  .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
  .chart-grid.one-col { grid-template-columns: 1fr; }
  .chart-card { background: #1a2836; border-radius: 12px; padding: 16px; border: 1px solid #2a3a4a; }
  .chart-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 12px; color: #c0d0e0; }
  .chart-card canvas { width: 100% !important; height: auto !important; max-height: 400px; }
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 10px 12px; background: #1f3040; color: #99aabb; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }
  td { padding: 10px 12px; border-bottom: 1px solid #223344; }
  tr:hover td { background: #1e3040; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
  .text-muted { color: #8899aa; font-size: 13px; }
  .mt-20 { margin-top: 20px; }
  .mb-20 { margin-bottom: 20px; }
  @media (max-width: 900px) { .chart-grid { grid-template-columns: 1fr; } }
  .chart-card.full { grid-column: 1 / -1; }
  .cluster-tag { display: inline-block; padding: 4px 14px; border-radius: 12px; font-size: 13px; font-weight: 600; margin-right: 6px; }
</style>
</head>
<body>
<div class="container">

<h1>&#x1F575; EDA Dashboard — Klarifikasi Seskab Teddy</h1>
<div class="subtitle">
  Analisis komentar Instagram dari 11 sumber berita terkait klarifikasi Sekretaris Kabinet Teddy Indra Wijaya
  atas kritik Dino Patti Djalal tentang kunjungan luar negeri Presiden Prabowo (1-4 Juni 2026) &middot;
  Charts rendered client-side via Chart.js
</div>

<div class="summary-grid">
  <div class="card"><div class="num">__TOTAL__</div><div class="label">Total Comments</div></div>
  <div class="card"><div class="num">__SRC_COUNT__</div><div class="label">News Sources</div></div>
  <div class="card"><div class="num">__UNIQUE__</div><div class="label">Unique Commenters</div></div>
  <div class="card"><div class="num">__AVG_LEN__</div><div class="label">Avg Comment Length (chars)</div></div>
</div>

<div id="charts">
  <!-- Charts populated by JS below -->
</div>

<!-- Source Table -->
<div class="chart-card mt-20 mb-20">
  <h3>&#x1F4CB; Source Details</h3>
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th>Account</th><th>Comments</th><th>Unique</th><th>Followers</th><th>Likes</th><th>Eng. Rate</th><th>URL</th>
      </tr></thead>
      <tbody id="source-table-body"></tbody>
    </table>
  </div>
</div>

<!-- Stance Detail Table -->
<div class="chart-card mb-20">
  <h3>&#x1F3F7; Stance Distribution Details</h3>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Category</th><th>Count</th><th>%</th><th>Keywords</th></tr></thead>
      <tbody id="stance-table-body"></tbody>
    </table>
  </div>
</div>

<!-- Cluster Summary -->
<div class="chart-card mb-20" id="cluster-section">
  <h3>&#x1F52C; TF-IDF + KMeans Clusters</h3>
  <p class="text-muted" id="cluster-meta"></p>
  <div id="cluster-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:12px;"></div>
</div>

<!-- InSet Sentiment Table -->
<div class="chart-card mb-20">
  <h3>&#x1F4CA; Sentiment Analysis (InSetSentiment)</h3>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Label</th><th>Count</th><th>Percentage</th></tr></thead>
      <tbody id="inset-table-body"></tbody>
    </table>
  </div>
  <p class="text-muted" style="margin-top:10px;" id="inset-meta"></p>
</div>

<!-- EmoSense Emotions Table -->
<div class="chart-card mb-20" id="emosense-section">
  <h3>&#x1F621; EmoSense Dominant Emotions</h3>
  <p class="text-muted" id="emosense-meta"></p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Emotion</th><th>Dominant Count</th><th>%</th><th>Avg Probability</th></tr></thead>
      <tbody id="emosense-table-body"></tbody>
    </table>
  </div>
</div>

<!-- Top Terms Table -->
<div class="chart-card mb-20">
  <h3>&#x1F3C6; Top 30 Bigrams (Tantular BagOfWords)</h3>
  <div class="table-wrap">
    <table>
      <thead><tr><th>#</th><th>Bigram</th><th>Frequency</th></tr></thead>
      <tbody id="topterms-table-body"></tbody>
    </table>
  </div>
</div>

<div class="card" style="text-align:center;margin-top:20px;">
  <p class="text-muted">
    Dibuat dengan Tantular NLP + scikit-learn &middot;
    EDA pipeline: 01_process (BoW/stance) &middot; 02_classify (InSet) &middot; 02b_classify_tfidf (KMeans) &middot; 03_emosense_sample (EmoSense) &middot;
    Charts: Chart.js (client-side)
  </p>
</div>

</div>

<script>
// ── Data embedded as JSON ──────────────────────────────────────────
const META = __META__;
const SOURCE_STATS = __SRC_STATS__;
const HOURLY = __HOURLY__;
const STANCE_DIST = __STANCE_DIST__;
const STANCE_BY_SRC = __STANCE_BY_SRC__;
const TOP_TERMS = __TOP_TERMS__;
const EMOJI_TOP = __EMOJI_TOP__;
const TOP_COMMENTERS = __TOP_COMMENTERS__;
const SOURCE_TERMS = __SRC_TERMS__;
const TEXT_LENGTHS = __TEXT_LENGTHS__;
const INSET_SUMMARY = __INSET_SUMMARY__;
const INSET_BY_SRC = __INSET_BY_SRC__;
const EMOSENSE = __EMOSENSE__;
const CLUSTER = __CLUSTER__;
const STANCE_ORDER = __STANCE_ORDER__;
const STANCE_COLORS = __STANCE_COLORS__;

// ── Derived constants ──────────────────────────────────────────────
const total = META.total_comments || 0;
const srcCount = META.source_count || 0;
const uniqueCommenters = META.unique_commenters || 0;

// ── Helpers ────────────────────────────────────────────────────────
Chart.register(ChartDataLabels);

function fmtNum(n) { return n.toLocaleString(); }

function makeCanvas(parent, id, aspect=2) {
  const div = document.createElement('div');
  div.style.cssText = `position:relative;width:100%;aspect-ratio:${aspect}`;
  const c = document.createElement('canvas');
  c.id = id;
  div.appendChild(c);
  parent.appendChild(div);
}

const chartGrid = document.getElementById('charts');

// ── CHART 1: Volume by Source ──────────────────────────────────────
const srcNames = Object.keys(SOURCE_STATS).sort((a,b) => SOURCE_STATS[b].total_comments - SOURCE_STATS[a].total_comments);
const srcVols = srcNames.map(n => SOURCE_STATS[n].total_comments);

function addChart(title, canvasId, configFn, width=1) {
  const row = document.createElement('div');
  row.className = width === 2 ? 'chart-grid one-col' : 'chart-grid';
  const card = document.createElement('div');
  card.className = 'chart-card' + (width === 2 ? ' full' : '');
  const h3 = document.createElement('h3');
  h3.textContent = title;
  card.appendChild(h3);
  makeCanvas(card, canvasId, width === 2 ? 2.5 : 2);
  row.appendChild(card);
  chartGrid.appendChild(row);
  const ctx = document.getElementById(canvasId).getContext('2d');
  configFn(ctx);
}

addChart('Volume by Source', 'chart1', (ctx) => {
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: srcNames,
      datasets: [{
        data: srcVols,
        backgroundColor: srcNames.map((_,i) => `hsl(${(i*30)%360},70%,50%)`),
        borderWidth: 0,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, datalabels: { anchor: 'end', align: 'end', color: '#c0d0e0', font: { size: 10 } } },
      scales: { x: { ticks: { color: '#8899aa' } }, y: { ticks: { color: '#c0d0e0' } } }
    }
  });
});

addChart('Engagement: Followers vs Comments', 'chart2', (ctx) => {
  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        data: srcNames.map(n => ({
          x: SOURCE_STATS[n].followers / 1e6,
          y: SOURCE_STATS[n].total_comments,
          r: Math.sqrt(SOURCE_STATS[n].unique_commenters) * 0.8,
        })),
        backgroundColor: srcNames.map((_,i) => `hsla(${(i*30)%360},70%,50%,0.7)`),
        borderColor: '#000',
        borderWidth: 0.5,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => `${srcNames[c.dataIndex]}: ${c.parsed.y.toLocaleString()} comments, ${c.parsed.x.toFixed(2)}M followers` } }
      },
      scales: {
        x: { title: { display: true, text: 'Followers (millions)', color: '#8899aa' }, ticks: { color: '#8899aa' } },
        y: { title: { display: true, text: 'Total Comments', color: '#8899aa' }, ticks: { color: '#8899aa' } }
      }
    }
  });
});

addChart('Activity by Hour (UTC)', 'chart3', (ctx) => {
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: HOURLY.map(h => h.hour.toString()),
      datasets: [{
        data: HOURLY.map(h => h.count),
        backgroundColor: HOURLY.map(h => h.count === Math.max(...HOURLY.map(x=>x.count)) ? '#e74c3c' : '#2e86ab'),
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { ticks: { color: '#8899aa' } }, y: { ticks: { color: '#8899aa' } } }
    }
  });
});

addChart('Comment Length Distribution', 'chart4', (ctx) => {
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: TEXT_LENGTHS.bins.map(b => b.bin_label),
      datasets: [{
        data: TEXT_LENGTHS.bins.map(b => b.count),
        backgroundColor: '#2e86ab',
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { ticks: { color: '#8899aa', maxTicksLimit: 12 } }, y: { ticks: { color: '#8899aa' } } }
    }
  });
});

addChart('Stance Classification (Keyword-Based)', 'chart5', (ctx) => {
  const labels = STANCE_DIST.map(d => d.category);
  const vals = STANCE_DIST.map(d => d.count);
  const colors = labels.map(l => STANCE_COLORS[l] || '#95a5a6');
  new Chart(ctx, {
    type: 'doughnut',
    data: { labels, datasets: [{ data: vals, backgroundColor: colors, borderWidth: 1, borderColor: '#1a2836' }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#c0d0e0', font: { size: 11 }, generateLabels: (c) => c.data.labels.map((l,i) => ({ text: `${l} (${fmtNum(vals[i])})` , fillStyle: colors[i], index: i })) } },
        datalabels: { color: '#fff', font: { size: 11, weight: 'bold' }, formatter: (v) => `${(v/vals.reduce((a,b)=>a+b)*100).toFixed(0)}%` }
      }
    }
  });
});

addChart('Top 30 Bigrams (Tantular BagOfWords)', 'chart6', (ctx) => {
  const terms = TOP_TERMS.slice().reverse();
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: terms.map(t => t.term),
      datasets: [{
        data: terms.map(t => t.freq),
        backgroundColor: terms.map((_,i) => `hsl(${(i*4)%360},60%,50%)`),
        borderWidth: 0,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { ticks: { color: '#8899aa' } }, y: { ticks: { color: '#c0d0e0', font: { size: 9 } } } }
    }
  });
});

addChart('Top 25 Emojis', 'chart7', (ctx) => {
  const items = EMOJI_TOP.slice().reverse();
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: items.map(e => e.emoji + ' (' + fmtNum(e.count) + ')'),
      datasets: [{
        data: items.map(e => e.count),
        backgroundColor: items.map((_,i) => `hsl(${(i*7)%360},70%,50%)`),
        borderWidth: 0,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { ticks: { color: '#8899aa' } }, y: { ticks: { color: '#c0d0e0', font: { size: 10 } } } }
    }
  });
});

addChart('Top 25 Most Active Commenters', 'chart8', (ctx) => {
  const items = TOP_COMMENTERS.slice().reverse();
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: items.map(u => u.username),
      datasets: [{
        data: items.map(u => u.count),
        backgroundColor: items.map((_,i) => `hsl(${(i*7)%360},50%,55%)`),
        borderWidth: 0,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { ticks: { color: '#8899aa' } }, y: { ticks: { color: '#c0d0e0', font: { size: 8 } } } }
    }
  });
});

// Source Terms (5 mini charts)
(function() {
  const row = document.createElement('div');
  row.className = 'chart-grid';
  const accts = Object.keys(SOURCE_TERMS).slice(0,5);
  accts.forEach((acct, ai) => {
    const card = document.createElement('div');
    card.className = 'chart-card';
    const h3 = document.createElement('h3');
    h3.textContent = `Top Terms: ${acct.slice(0,20)}`;
    h3.style.fontSize = '13px';
    card.appendChild(h3);
    const div = document.createElement('div');
    div.style.cssText = 'position:relative;width:100%;aspect-ratio:1.5';
    const c = document.createElement('canvas');
    c.id = 'chart9-' + ai;
    div.appendChild(c);
    card.appendChild(div);
    row.appendChild(card);
    setTimeout(() => {
      const ctx = document.getElementById('chart9-'+ai);
      if (!ctx) return;
      const items = (SOURCE_TERMS[acct] || []).slice(0,15).reverse();
      new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: { labels: items.map(t=>t.term), datasets: [{ data: items.map(t=>t.freq), backgroundColor: `hsl(${(ai*72)%360},60%,50%)`, borderWidth: 0 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { ticks: { color: '#c0d0e0', font: { size: 8 } } } } }
      });
    }, ai * 100);
  });
  chartGrid.appendChild(row);
})();

addChart('Total Comments vs Unique Commenters', 'chart10', (ctx) => {
  const labels = Object.keys(SOURCE_STATS);
  const totals = labels.map(l => SOURCE_STATS[l].total_comments);
  const uniques = labels.map(l => SOURCE_STATS[l].unique_commenters);
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Total Comments', data: totals, backgroundColor: '#2e86ab' },
        { label: 'Unique Commenters', data: uniques, backgroundColor: '#e67e22' }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#c0d0e0' } } },
      scales: { x: { ticks: { color: '#8899aa' } }, y: { ticks: { color: '#8899aa' } } }
    }
  });
});

addChart('Sentiment Polarity (InSetSentiment)', 'chart11', (ctx) => {
  const sd = INSET_SUMMARY.sentiment_distribution || {};
  const labels = ['Positive', 'Negative', 'Neutral'];
  const vals = [sd.positive||0, sd.negative||0, sd.neutral||0];
  const colors = ['#2ecc71','#e74c3c','#95a5a6'];
  new Chart(ctx, {
    type: 'doughnut',
    data: { labels, datasets: [{ data: vals, backgroundColor: colors, borderWidth: 1, borderColor: '#1a2836' }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#c0d0e0', font: { size: 11 }, generateLabels: (c) => labels.map((l,i) => ({ text: `${l} (${fmtNum(vals[i])})`, fillStyle: colors[i], index: i })) } },
        datalabels: { color: '#fff', font: { size: 12, weight: 'bold' }, formatter: (v) => `${(v/vals.reduce((a,b)=>a+b)*100).toFixed(0)}%` }
      }
    }
  });
});

addChart('EmoSense Dominant Emotions', 'chart12', (ctx) => {
  if (!EMOSENSE || !EMOSENSE.dominant_emotion_distribution) return;
  const entries = Object.entries(EMOSENSE.dominant_emotion_distribution).sort((a,b) => b[1] - a[1]);
  const labels = entries.map(e => e[0]);
  const vals = entries.map(e => e[1]);
  const colors = labels.map((_,i) => `hsl(${(i*40)%360},65%,55%)`);
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: vals,
        backgroundColor: colors,
        borderWidth: 0,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        datalabels: {
          anchor: 'end', align: 'end', color: '#c0d0e0', font: { size: 10 },
          formatter: (v) => `${v} (${(v/Object.values(EMOSENSE.dominant_emotion_distribution).reduce((a,b)=>a+b)*100).toFixed(0)}%)`,
        }
      },
      scales: { x: { ticks: { color: '#8899aa' } }, y: { ticks: { color: '#c0d0e0' } } }
    }
  });
});

// ── Populate Tables ───────────────────────────────────────────────

// Source table
const srcBody = document.getElementById('source-table-body');
srcNames.forEach(n => {
  const s = SOURCE_STATS[n];
  const er = s.followers > 0 ? (s.total_comments / s.followers * 100).toFixed(2) : 0;
  srcBody.innerHTML += `<tr><td><strong>${n}</strong></td><td>${fmtNum(s.total_comments)}</td><td>${fmtNum(s.unique_commenters)}</td><td>${fmtNum(s.followers)}</td><td>${fmtNum(s.likes)}</td><td>${er}%</td><td><a href="${s.url}" target="_blank" style="color:#66b0ff;font-size:12px;">link</a></td></tr>`;
});

// Stance table
const stanceBody = document.getElementById('stance-table-body');
const stanceKws = { mendukung: 'setuju, mantap, salut, presiden hebat, kerja nyata, diplomasi, investasi, triliun', mengkritik: 'kritik, bohong, ngawur, gagal, buang uang, pajak, uang rakyat, cari alasan', sarkasme: '😂🤣 wkwk, hahaha, 🤡, gas, puh sepuh, lucu, ngakak', faktual: 'berapa, data, bukti, sumber, fakta, kenapa, pertanyaan', lainnya: 'Tidak terklasifikasi' };
STANCE_DIST.forEach(d => {
  const pct = (d.count / total * 100).toFixed(1);
  const c = STANCE_COLORS[d.category] || '#888';
  stanceBody.innerHTML += `<tr><td><span class="badge" style="background:${c}22;color:${c};border:1px solid ${c}40">${d.category}</span></td><td><strong>${fmtNum(d.count)}</strong></td><td>${pct}%</td><td class="text-muted">${stanceKws[d.category]||'—'}</td></tr>`;
});

// Cluster section
const clusterSection = document.getElementById('cluster-section');
if (CLUSTER && CLUSTER.cluster_labels) {
  document.getElementById('cluster-meta').textContent = `Method: ${CLUSTER.method} / Total clustered: ${fmtNum(CLUSTER.total_clustered||0)} comments`;
  const cardsDiv = document.getElementById('cluster-cards');
  Object.entries(CLUSTER.cluster_labels).forEach(([k, label]) => {
    const size = (CLUSTER.cluster_sizes||{})[k] || 0;
    const terms = ((CLUSTER.cluster_terms||{})[k] || []).slice(0,8).map(t => t[0]).join(', ');
    const pct = (size / (CLUSTER.total_clustered||1) * 100).toFixed(1);
    const hue = (parseInt(k)*72) % 360;
    cardsDiv.innerHTML += `<div class="card" style="border-left:4px solid hsl(${hue},60%,50%)"><div style="font-size:20px;font-weight:700;color:#fff;">${label}</div><div class="text-muted">${fmtNum(size)} comments (${pct}%)</div><div style="font-size:11px;color:#8899aa;margin-top:4px;">${terms}</div></div>`;
  });
} else {
  clusterSection.style.display = 'none';
}

// InSet table
const insetBody = document.getElementById('inset-table-body');
if (INSET_SUMMARY && INSET_SUMMARY.sentiment_distribution) {
  const sd = INSET_SUMMARY.sentiment_distribution;
  const sp = INSET_SUMMARY.sentiment_percentages || {};
  const labels = ['positive','negative','neutral'];
  const labelNames = ['Positive','Negative','Neutral'];
  const colors = ['#2ecc71','#e74c3c','#95a5a6'];
  labels.forEach((l,i) => {
    insetBody.innerHTML += `<tr><td><span class="badge" style="background:${colors[i]}22;color:${colors[i]};border:1px solid ${colors[i]}40">${labelNames[i]}</span></td><td><strong>${fmtNum(sd[l]||0)}</strong></td><td>${sp[l+'_pct']||'0'}%</td></tr>`;
  });
  document.getElementById('inset-meta').innerHTML = `Avg polarity: ${INSET_SUMMARY.avg_polarity} / Pos/Neg ratio: ${INSET_SUMMARY.positive_negative_ratio}:1 / Model: InSetSentiment (Tantular NLP)`;
} else {
  document.getElementById('inset-table-body').innerHTML = '<tr><td colspan="3" class="text-muted">No InSet data available</td></tr>';
}

// EmoSense table
const emoBody = document.getElementById('emosense-table-body');
if (EMOSENSE && EMOSENSE.dominant_emotion_distribution) {
  document.getElementById('emosense-meta').textContent = `Sampled ${EMOSENSE.sample_size||0} comments stratified by stance / Model: Aardiiiiy/EmoSense-ID-Indonesian-Emotion-Classifier`;
  const entries = Object.entries(EMOSENSE.dominant_emotion_distribution).sort((a,b) => b[1] - a[1]);
  const totalEmo = entries.reduce((a, e) => a + e[1], 0);
  const avgProbs = EMOSENSE.average_probabilities || {};
  entries.forEach(([emo, cnt]) => {
    const pct = (cnt / totalEmo * 100).toFixed(1);
    const avg = (avgProbs[emo] || 0).toFixed(4);
    emoBody.innerHTML += `<tr><td><strong>${emo}</strong></td><td>${fmtNum(cnt)}</td><td>${pct}%</td><td>${avg}</td></tr>`;
  });
} else {
  document.getElementById('emosense-section').style.display = 'none';
}

// Top Terms table
const ttBody = document.getElementById('topterms-table-body');
(TOP_TERMS || []).forEach((t, i) => {
  ttBody.innerHTML += `<tr><td>${i+1}</td><td>${t.term}</td><td>${fmtNum(t.freq)}</td></tr>`;
});

</script>
</body>
</html>
'''

# Replace placeholders
html = html_template
html = html.replace('__TOTAL__', fmt(total))
html = html.replace('__SRC_COUNT__', fmt(src_count))
html = html.replace('__UNIQUE__', fmt(unique_commenters))
html = html.replace('__AVG_LEN__', f'{avg_len:.0f}')
html = html.replace('__META__', meta_json)
html = html.replace('__SRC_STATS__', source_stats_json)
html = html.replace('__HOURLY__', hourly_json)
html = html.replace('__STANCE_DIST__', stance_dist_json)
html = html.replace('__STANCE_BY_SRC__', stance_by_source_json)
html = html.replace('__TOP_TERMS__', top_terms_json)
html = html.replace('__EMOJI_TOP__', emoji_top_json)
html = html.replace('__TOP_COMMENTERS__', top_commenters_json)
html = html.replace('__SRC_TERMS__', source_terms_json)
html = html.replace('__TEXT_LENGTHS__', text_lengths_json)
html = html.replace('__INSET_SUMMARY__', inset_summary_json)
html = html.replace('__INSET_BY_SRC__', inset_by_source_json)
html = html.replace('__EMOSENSE__', emosense_summary_json)
html = html.replace('__CLUSTER__', cluster_summary_json)
html = html.replace('__STANCE_ORDER__', stance_order_json)
html = html.replace('__STANCE_COLORS__', stance_colors_json)

# ── Write dashboard file ────────────────────────────────────────────────
dashborad_path = CHARTS / 'dashboard.html'
with open(dashborad_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[✓] Dashboard written: {dashborad_path} ({dashborad_path.stat().st_size:,} bytes)")
print(f"[✓] 0 PNG files generated — all charts rendered client-side via Chart.js")
