#!/usr/bin/env python3
"""
Analisis Framing: "Pesta Babi"
================================
Menggunakan endpoint framing dari Semantik Research API untuk menganalisis
bagaimana media yang berbeda membingkai (frame) entitas seputar film "Pesta Babi".

Meliputi:
  1. Framing per-source untuk entitas utama (pesta babi, TNI, pemerintah, yusril)
  2. Perbandingan framing antar entitas (framing/compare)
  3. Relasi SVO (subject-verb-object) untuk setiap entitas
  4. Visualisasi: heatmap framing, bar chart per-source

Dependencies: networkx, matplotlib, numpy, json (stdlib)

Cara pakai:
  python3 framing_analysis.py
"""

import json
from pathlib import Path
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

DATA_DIR = Path(__file__).parent
OUTPUT_DIR = DATA_DIR

# ─── Loading ───────────────────────────────────────────────────────
def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        print(f"[WARNING] {path} not found.")
        return None
    with open(path) as f:
        return json.load(f)


# ─── Framing Analysis ──────────────────────────────────────────────
def analyze_framing_by_source(data, entity_label):
    """Analyze framing phrases grouped by media source."""
    if not data or 'by_source' not in data:
        return None

    sources = data['by_source']
    total_by_source = {}

    for src, phrases in sources.items():
        total = sum(p['article_count'] for p in phrases)
        top = sorted(phrases, key=lambda x: x['article_count'], reverse=True)[:5]
        total_by_source[src] = {
            'total': total,
            'phrases': phrases,
            'top_phrases': top,
        }

    return total_by_source


def analyze_framing_compare(data):
    """Analyze comparative framing across entities."""
    if not data:
        return None

    result = {}
    for entity, phrases in data.items():
        total = sum(p['article_count'] for p in phrases)
        top = sorted(phrases, key=lambda x: x['article_count'], reverse=True)[:5]
        result[entity] = {
            'total': total,
            'top_phrases': top,
        }
    return result


def analyze_relations(data, entity_label):
    """Analyze SVO triples for an entity."""
    if not data or 'actions' not in data:
        return None

    actions = data['actions']
    total = data.get('total_actions', len(actions))
    role = data.get('role', 'both')

    # Group by relation type
    relation_types = Counter()
    targets = Counter()
    sources = Counter()

    for a in actions:
        relation_types[a['relation']] += a['count']
        targets[a['target_entity']] += a['count']
        sources[a['source_entity']] += a['count']

    return {
        'total_actions': total,
        'role': role,
        'relation_types': relation_types.most_common(15),
        'top_targets': targets.most_common(10),
        'top_sources': sources.most_common(10),
    }


# ─── Visualization ─────────────────────────────────────────────────
def plot_framing_heatmap(entity_data, entity_label, output_path):
    """Plot heatmap of framing phrases across sources."""
    if not entity_data:
        return

    # Collect significant phrases (mentioned in 2+ sources)
    all_phrases = {}
    for src, info in entity_data.items():
        for p in info['phrases']:
            phrase = p['framing_phrase']
            count = p['article_count']
            if phrase not in all_phrases:
                all_phrases[phrase] = {}
            all_phrases[phrase][src] = count

    # Filter to phrases appearing in 2+ sources
    multi_source = {k: v for k, v in all_phrases.items() if len(v) >= 2}
    if not multi_source:
        # Fallback: use top N phrases
        top_phrases = sorted(all_phrases.items(), key=lambda x: sum(x[1].values()), reverse=True)[:15]
        multi_source = dict(top_phrases)
    else:
        # Top 12 by total count
        top_phrases = sorted(multi_source.items(), key=lambda x: sum(x[1].values()), reverse=True)[:12]
        multi_source = dict(top_phrases)

    if not multi_source:
        return

    sources = sorted(entity_data.keys())
    phrases = list(multi_source.keys())

    # Build matrix
    matrix = np.zeros((len(phrases), len(sources)))
    for i, phrase in enumerate(phrases):
        for j, src in enumerate(sources):
            matrix[i, j] = multi_source[phrase].get(src, 0)

    # Plot
    fig, ax = plt.subplots(figsize=(14, max(6, len(phrases) * 0.5)))
    fig.patch.set_facecolor("#fafafa")

    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Article count", fontsize=9)

    # Labels
    ax.set_xticks(range(len(sources)))
    ax.set_xticklabels(sources, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(phrases)))
    ax.set_yticklabels(phrases, fontsize=7)

    ax.set_title(f"Framing Heatmap: '{entity_label}' — Cross-Source Comparison", fontsize=12, fontweight="bold")

    # Annotate cells
    for i in range(len(phrases)):
        for j in range(len(sources)):
            val = matrix[i, j]
            if val > 0:
                ax.text(j, i, int(val), ha="center", va="center", fontsize=7,
                        color="white" if val > matrix.max() * 0.6 else "black")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[✓] Framing heatmap saved: {output_path}")


def plot_source_framing_bars(entity_data, entity_label, output_path):
    """Bar chart: top framing phrases per source."""
    if not entity_data:
        return

    # Get top 3 phrases per source
    source_data = []
    for src, info in sorted(entity_data.items(), key=lambda x: x[1]['total'], reverse=True):
        top = info['top_phrases'][:3]
        for p in top:
            source_data.append({
                'source': src,
                'phrase': p['framing_phrase'],
                'count': p['article_count'],
            })
        source_data.append({'source': src, 'phrase': '───', 'count': 0})  # separator

    if not source_data:
        return

    fig, ax = plt.subplots(figsize=(12, max(5, len(source_data) * 0.35)))
    fig.patch.set_facecolor("#fafafa")

    # Use distinct colors for each source
    unique_sources = list(dict.fromkeys(d['source'] for d in source_data if d['phrase'] != '───'))
    colors = plt.cm.Set2(np.linspace(0, 1, len(unique_sources)))
    source_colors = {}
    for src, c in zip(unique_sources, colors):
        source_colors[src] = c

    y_pos = range(len(source_data))
    bars = []
    labels = []

    for i, item in enumerate(source_data):
        labels.append(f"{item['source']}: {item['phrase']}")
        if item['count'] > 0:
            bar = ax.barh(i, item['count'], color=source_colors[item['source']],
                          edgecolor="#333", linewidth=0.3, height=0.7)
            bars.append(bar)
        else:
            # Separator
            ax.barh(i, 0, color="none")
            ax.axhline(i - 0.5, color="#ccc", linewidth=0.5)

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=6.5)
    ax.invert_yaxis()
    ax.set_xlabel("Article count")
    ax.set_title(f"Top Framing Phrases per Source: '{entity_label}'", fontsize=12, fontweight="bold")

    # Legend
    legend_patches = [mpatches.Patch(color=source_colors[s], label=s) for s in unique_sources]
    ax.legend(handles=legend_patches, fontsize=7, loc="lower right")

    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[✓] Source framing bars saved: {output_path}")


def plot_compare_bars(compare_data, output_path):
    """Stacked bar chart comparing framing across entities."""
    if not compare_data:
        return

    # Get top phrases for each entity
    entities = list(compare_data.keys())
    all_top = {}
    for entity, info in compare_data.items():
        for p in info['top_phrases']:
            key = p['framing_phrase'][:50]  # truncate long phrases
            if key not in all_top:
                all_top[key] = {}
            all_top[key][entity] = p['article_count']

    # Keep phrases with at least 2 mentions total
    all_top = {k: v for k, v in all_top.items() if sum(v.values()) >= 2}
    if not all_top:
        return

    # Sort by total mentions
    sorted_phrases = sorted(all_top.items(), key=lambda x: sum(x[1].values()), reverse=True)[:12]

    fig, ax = plt.subplots(figsize=(12, max(5, len(sorted_phrases) * 0.5)))
    fig.patch.set_facecolor("#fafafa")

    y_pos = range(len(sorted_phrases))
    entity_colors = plt.cm.Set1(np.linspace(0, 1, len(entities)))

    # Stacked horizontal bar
    for i, (phrase, entity_counts) in enumerate(sorted_phrases):
        left = 0
        for j, entity in enumerate(entities):
            count = entity_counts.get(entity, 0)
            if count > 0:
                ax.barh(i, count, left=left, color=entity_colors[j],
                        edgecolor="#333", linewidth=0.3, height=0.7)
                left += count

    ax.set_yticks(range(len(sorted_phrases)))
    ax.set_yticklabels([p for p, _ in sorted_phrases], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("Article count")
    ax.set_title("Perbandingan Framing Antar Entitas", fontsize=12, fontweight="bold")

    legend_patches = [mpatches.Patch(color=entity_colors[i], label=e) for i, e in enumerate(entities)]
    ax.legend(handles=legend_patches, fontsize=8, loc="lower right")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[✓] Compare chart saved: {output_path}")


# ─── Report ─────────────────────────────────────────────────────────
def print_framing_report(framing_results, compare_data, relations):
    """Print structured framing analysis report."""
    lines = []
    sep = "=" * 60
    lines.append(sep)
    lines.append("  ANALISIS FRAMING: PESTA BABI")
    lines.append(f"  Data dari Semantik Research API — framing + relations")
    lines.append(sep)
    lines.append("")

    # ── Framing by source ──
    for entity_label, (entity_data, source_data) in framing_results.items():
        if not source_data:
            continue
        lines.append(f"[1] FRAMING: '{entity_label}' per Media")
        lines.append("-" * 50)
        for src, info in sorted(source_data.items(), key=lambda x: x[1]['total'], reverse=True):
            lines.append(f"  [{src}] — {info['total']} total framing phrases")
            for p in info['top_phrases'][:4]:
                lines.append(f"    • \"{p['framing_phrase']}\" (×{p['article_count']})")
        lines.append("")

    # ── Comparison ──
    if compare_data:
        lines.append("[2] PERBANDINGAN FRAMING ANTAR ENTITAS")
        lines.append("-" * 50)
        for entity, info in compare_data.items():
            lines.append(f"  {entity} ({info['total']} total):")
            for p in info['top_phrases'][:5]:
                lines.append(f"    • \"{p['framing_phrase']}\" (×{p['article_count']})")
        lines.append("")

    # ── Relations ──
    if relations:
        lines.append("[3] RELASI SVO (SUBJECT-VERB-OBJECT)")
        lines.append("-" * 50)
        for entity_label, rel in relations.items():
            if not rel:
                continue
            lines.append(f"  {entity_label} — {rel['total_actions']} actions:")
            lines.append(f"  Top relations:")
            for source, count in rel['top_sources'][:4]:
                lines.append(f"    {source} (×{count})")
            for rel_type, count in rel['relation_types'][:4]:
                lines.append(f"    —[{rel_type}]→ (×{count})")
            for target, count in rel['top_targets'][:4]:
                lines.append(f"    → {target} (×{count})")
            lines.append("")

    lines.append(sep)
    lines.append("  SELESAI. Visualisasi ada di direktori ini.")
    lines.append(sep)

    print("\n".join(lines))

    report_path = OUTPUT_DIR / "framing_report.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\n[✓] Framing report saved: {report_path}")


# ─── Main ───────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  FRAMING ANALYSIS: Pesta Babi")
    print("=" * 60)

    # 1. Load framing by-source
    entities_by_source = {
        'pesta babi': ('framing_pesta_by_source.json', 'Pesta Babi'),
        'tni': ('framing_tni_by_source.json', 'TNI'),
        'pemerintah': ('framing_pemerintah_by_source.json', 'Pemerintah'),
        'yusril': ('framing_yusril_by_source.json', 'Yusril'),
    }

    framing_results = {}
    all_source_data = {}

    print("\n[○] Loading framing by-source...")
    for key, (fname, label) in entities_by_source.items():
        raw = load_json(fname)
        if not raw:
            print(f"  [✗] {label}: no data")
            continue
        result = analyze_framing_by_source(raw, label)
        if result:
            all_source_data[key] = (label, result)
            total = sum(v['total'] for v in result.values())
            print(f"  [✓] {label}: {len(result)} sources, {total} total framing phrases")
            framing_results[label] = (raw, result)
        else:
            print(f"  [✗] {label}: empty")

    # 2. Load framing compare
    print("\n[○] Loading framing/compare...")
    raw_compare = load_json('framing_compare.json')
    compare_data = analyze_framing_compare(raw_compare)
    if compare_data:
        for entity, info in compare_data.items():
            print(f"  [✓] {entity}: {info['total']} total phrases")
        print()

    # 3. Load relations
    relation_files = {
        'TNI': 'rel_tni.json',
        'Pemerintah': 'rel_pemerintah.json',
        'Pesta Babi': 'rel_pesta.json',
        'Papua': 'rel_papua.json',
    }
    relations = {}
    print("[○] Loading relations...")
    for label, fname in relation_files.items():
        raw = load_json(fname)
        if raw:
            rel = analyze_relations(raw, label)
            if rel:
                relations[label] = rel
                print(f"  [✓] {label}: {rel['total_actions']} actions")

    # 4. Generate visualizations
    print("\n[○] Generating framing visualizations...")
    for key, (label, source_data) in all_source_data.items():
        plot_framing_heatmap(
            source_data, label,
            OUTPUT_DIR / f"framing_heatmap_{key}.png"
        )
        plot_source_framing_bars(
            source_data, label,
            OUTPUT_DIR / f"framing_bars_{key}.png"
        )

    if compare_data:
        plot_compare_bars(compare_data, OUTPUT_DIR / "framing_compare_stacked.png")

    # 5. Print report
    print("\n[○] Generating framing report...")
    print_framing_report(framing_results, compare_data, relations)

    print("\n[✓] All done!")


if __name__ == "__main__":
    main()