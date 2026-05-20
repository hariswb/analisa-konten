#!/usr/bin/env python3
"""
Analysis of "Pesta Babi" documentary coverage in Indonesian news media.
Uses Semantik Research API data to produce charts and structured report.

Reproducible — run from the research directory:
  cd research/2026-05-20-pesta-babi
  python3 scripts/analysis.py

Requires: pip install matplotlib networkx numpy
Data files expected in ./data/
"""

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import networkx as nx
import numpy as np

# ── Configuration ──────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CHARTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Color scheme — dark theme, Indonesia-inspired palette
BG_COLOR = "#1a1a2e"
TEXT_COLOR = "#e0e0e0"
COLORS = {
    "positive": "#4caf50",
    "negative": "#f44336",
    "neutral": "#9e9e9e",
    "tempo_nasional": "#e91e63",
    "kompas": "#2196f3",
    "tirto": "#9c27b0",
    "cnn_nasional": "#ff9800",
    "media_indonesia": "#00bcd4",
    "detik_berita": "#4caf50",
    "republika": "#795548",
    "liputan6_news": "#ff5722",
    "kumparan": "#607d8b",
}
SOURCE_LABELS = {
    "tempo_nasional": "Tempo",
    "kompas": "Kompas",
    "tirto": "Tirto",
    "cnn_nasional": "CNN Indonesia",
    "media_indonesia": "Media Indonesia",
    "detik_berita": "Detik",
    "republika": "Republika",
    "liputan6_news": "Liputan6",
    "kumparan": "Kumparan",
}

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": "#16213e",
    "axes.edgecolor": "#444",
    "axes.labelcolor": TEXT_COLOR,
    "axes.titlecolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "legend.facecolor": "#16213e",
    "legend.edgecolor": "#444",
    "legend.labelcolor": TEXT_COLOR,
    "font.size": 11,
    "figure.dpi": 150,
})


def load_json(name):
    path = os.path.join(DATA_DIR, name)
    with open(path) as f:
        return json.load(f)


# ── 1. Source Comparison Bar Chart ──────────────────────────────────
def chart_source_comparison(sc_data):
    """Bar chart of article count by source, colored by avg sentiment."""
    sc_data.sort(key=lambda x: x["article_count"], reverse=True)
    sources = [SOURCE_LABELS.get(s["source"], s["source"]) for s in sc_data]
    counts = [s["article_count"] for s in sc_data]
    sentiments = [s.get("avg_sentiment_score", 0) for s in sc_data]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(range(len(sources)), counts, height=0.7)

    # Color by sentiment: red (negative) → grey (neutral) → green (positive)
    for bar, sent in zip(bars, sentiments):
        if sent > 2:
            bar.set_color("#4caf50")
        elif sent < -2:
            bar.set_color("#f44336")
        else:
            bar.set_color("#9e9e9e")
        bar.set_alpha(0.85)

    ax.set_yticks(range(len(sources)))
    ax.set_yticklabels(sources)
    ax.set_xlabel("Article Count")
    ax.set_title("Articles by Source (colored by avg sentiment)")
    for bar, count, sent in zip(bars, counts, sentiments):
        label = f"{count} ({sent:+.1f})"
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                label, va="center", fontsize=9, color=TEXT_COLOR)

    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "source_comparison.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── 2. Sentiment Distribution ──────────────────────────────────────
def chart_sentiment_pie(sent_data):
    """Pie chart of positive/negative/neutral split."""
    labels = []
    sizes = []
    colors_list = []
    for key in ["positive", "negative", "neutral"]:
        if sent_data.get(key, 0) > 0:
            labels.append(key.title())
            sizes.append(sent_data[key])
            colors_list.append(COLORS[key])

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%",
        colors=colors_list, startangle=90,
        textprops={"color": TEXT_COLOR, "fontsize": 12},
        wedgeprops={"linewidth": 1, "edgecolor": BG_COLOR},
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title(
        f"Sentiment Distribution (n={sent_data['total']})",
        fontsize=14, pad=20,
    )
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "sentiment_pie.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── 3. Sentiment Trend Over Time ───────────────────────────────────
def chart_sentiment_trend(trend_data):
    """Line chart of sentiment (pos/neg/neu) over time."""
    dates = []
    pos, neg, neu = [], [], []
    for point in trend_data:
        dates.append(datetime.strptime(point["date"], "%Y-%m-%d"))
        pos.append(point.get("positive", 0))
        neg.append(point.get("negative", 0))
        neu.append(point.get("neutral", 0))

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(dates, neg, 0, alpha=0.3, color=COLORS["negative"], label="Negative")
    ax.fill_between(dates, pos, 0, alpha=0.3, color=COLORS["positive"], label="Positive")
    ax.plot(dates, neg, color=COLORS["negative"], linewidth=2, marker="o", markersize=4)
    ax.plot(dates, pos, color=COLORS["positive"], linewidth=2, marker="o", markersize=4)
    ax.axhline(0, color="#555", linewidth=0.5)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    ax.set_xlabel("Date")
    ax.set_ylabel("Article Count")
    ax.set_title("Daily Sentiment Trend")
    ax.legend()
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "sentiment_trend.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── 4. Topic Trend ─────────────────────────────────────────────────
def chart_topic_trend(topic_data):
    """Weekly article count trend."""
    weeks = []
    counts = []
    for point in topic_data:
        weeks.append(point["date"])
        counts.append(point["article_count"])

    fig, ax = plt.subplots(figsize=(10, 4))
    x = range(len(weeks))
    bars = ax.bar(x, counts, color="#e91e63", alpha=0.85, width=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(weeks)
    ax.set_xlabel("Week Starting")
    ax.set_ylabel("Article Count")
    ax.set_title("Weekly Article Volume")
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(count), ha="center", fontsize=10, color=TEXT_COLOR)
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "topic_trend.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── 5. Entity Frequency ────────────────────────────────────────────
def chart_entity_frequency(entities_data, top_n=15):
    """Top N entities bar chart."""
    entities = sorted(entities_data, key=lambda x: x["mention_count"], reverse=True)[:top_n]

    names = [e["word"] for e in entities]
    counts = [e["mention_count"] for e in entities]
    groups = [e["entity_group"] for e in entities]

    # Color by entity group
    group_colors = {
        "PER": "#4caf50",
        "ORG": "#2196f3",
        "GPE": "#ff9800",
        "NOR": "#e91e63",
        "EVT": "#9c27b0",
        "LAW": "#00bcd4",
    }
    bar_colors = [group_colors.get(g, "#9e9e9e") for g in groups]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(range(len(names)), counts, color=bar_colors, alpha=0.85)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel("Mention Count")
    ax.set_title("Top Entities in Pesta Babi Coverage")
    ax.invert_yaxis()

    # Legend for entity groups
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#e91e63", label="NOR (Organization/Institution)"),
        Patch(facecolor="#9c27b0", label="EVT (Event)"),
        Patch(facecolor="#4caf50", label="PER (Person)"),
        Patch(facecolor="#ff9800", label="GPE (Location)"),
        Patch(facecolor="#2196f3", label="ORG (Organization)"),
    ]
    ax.legend(handles=legend_elements, fontsize=8, loc="lower right")

    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", fontsize=9, color=TEXT_COLOR)

    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "entity_frequency.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── 6. Network Co-occurrence Graph ─────────────────────────────────
def chart_network_cooccurrence(net_data):
    """Social network graph of entity co-occurrence."""
    G = nx.Graph()
    nodes = net_data.get("nodes", [])
    edges = net_data.get("edges", [])

    if not nodes:
        print("  ⚠ No nodes in network data, skipping")
        return None

    for n in nodes:
        G.add_node(n["name"], entity_group=n.get("entity_group", "?"),
                   mention_count=n.get("mention_count", 1))

    for e in edges:
        G.add_edge(e["source"], e["target"], weight=e.get("weight", 1))

    if len(G.nodes) < 2:
        print("  ⚠ Too few nodes, skipping network chart")
        return None

    # Layout
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

    fig, ax = plt.subplots(figsize=(14, 10))

    # Node sizes
    mention_counts = [G.nodes[n].get("mention_count", 1) for n in G.nodes]
    node_sizes = [max(200, m**0.7 * 150) for m in mention_counts]

    # Node colors by entity group
    group_cmap = {
        "PER": "#4caf50",
        "ORG": "#2196f3",
        "GPE": "#ff9800",
        "NOR": "#e91e63",
        "EVT": "#9c27b0",
        "LAW": "#00bcd4",
    }
    node_colors = [group_cmap.get(G.nodes[n].get("entity_group", ""), "#9e9e9e")
                   for n in G.nodes]

    # Edge widths
    edge_weights = [G.edges[e].get("weight", 1) for e in G.edges]
    edge_widths = [max(0.3, w * 0.5) for w in edge_weights]

    nx.draw_networkx_edges(G, pos, alpha=0.3, width=edge_widths,
                           edge_color="#888", ax=ax)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors,
                           alpha=0.85, ax=ax, edgecolors="#333", linewidths=1)

    # Labels for top nodes only
    top_nodes = sorted(G.nodes, key=lambda n: G.nodes[n].get("mention_count", 0),
                       reverse=True)[:12]
    label_dict = {n: n for n in top_nodes}
    nx.draw_networkx_labels(G, pos, labels=label_dict, font_size=9,
                            font_color=TEXT_COLOR, ax=ax)

    ax.set_title("Entity Co-occurrence Network (Pesta Babi Coverage)",
                 fontsize=14, pad=20)
    ax.axis("off")

    # Stats annotation
    stats = (
        f"Nodes: {len(G.nodes)} | Edges: {len(G.edges)} | "
        f"Density: {nx.density(G):.3f}"
    )
    ax.text(0.02, 0.02, stats, transform=ax.transAxes, fontsize=9,
            color=TEXT_COLOR, alpha=0.7,
            bbox=dict(boxstyle="round,pad=0.3", fc="#16213e", ec="#444", alpha=0.8))

    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "network_cooccurence.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── 7. Framing Heatmap ─────────────────────────────────────────────
def chart_framing_heatmap(framing_data_dict):
    """Heatmap: framing_phrase × entity (source), colored by article_count."""
    if not framing_data_dict or all(
        isinstance(v, list) and len(v) == 0 for v in framing_data_dict.values()
    ):
        print("  ⚠ No framing data, skipping heatmap")
        return None

    # Build matrix: entity_name → framing_phrase → article_count
    all_frames = set()
    matrix = defaultdict(lambda: defaultdict(int))

    for entity_name, frames in framing_data_dict.items():
        for f in frames:
            phrase = f["framing_phrase"][:60]
            all_frames.add(phrase)
            matrix[entity_name][phrase] = f["article_count"]

    if not all_frames:
        print("  ⚠ No framing data, skipping heatmap")
        return None

    # Rank frames by total mentions across all entities
    frame_totals = defaultdict(int)
    for phrase in all_frames:
        for entity_name in framing_data_dict:
            frame_totals[phrase] += matrix[entity_name][phrase]
    top_frames = sorted(frame_totals, key=frame_totals.get, reverse=True)[:10]

    entities_list = sorted(k for k in framing_data_dict
                           if any(matrix[k][f] > 0 for f in top_frames))

    if not top_frames or not entities_list:
        print("  ⚠ No data in framing matrix, skipping")
        return None

    data = np.zeros((len(top_frames), len(entities_list)))
    for i, frame in enumerate(top_frames):
        for j, entity in enumerate(entities_list):
            data[i, j] = matrix[entity][frame]

    if data.max() == 0:
        print("  ⚠ Empty framing matrix, skipping")
        return None

    fig, ax = plt.subplots(figsize=(10, max(5, len(top_frames) * 0.5)))
    im = ax.imshow(data, aspect="auto", cmap="YlOrRd", interpolation="nearest")

    ax.set_xticks(range(len(entities_list)))
    ax.set_xticklabels(entities_list, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(top_frames)))
    ax.set_yticklabels(top_frames, fontsize=8)

    # Annotate cells
    for i in range(len(top_frames)):
        for j in range(len(entities_list)):
            if data[i, j] > 0:
                ax.text(j, i, int(data[i, j]), ha="center", va="center",
                        fontsize=8, color="white" if data[i, j] > data.max() / 2 else "black")

    ax.set_title("Framing Heatmap: Entity × Framing Phrase",
                 fontsize=14, pad=20)
    fig.colorbar(im, ax=ax, label="Article Count")
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "framing_heatmap.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── 8. Bulk Sentiment by Entity ────────────────────────────────────
def chart_bulk_sentiment(bulk_data):
    """Grouped bar: positive/negative for each entity."""
    entities = sorted(bulk_data.keys(),
                      key=lambda e: bulk_data[e]["article_count"],
                      reverse=True)

    names = [e[:20] for e in entities]
    pos_vals = [bulk_data[e]["positive"] for e in entities]
    neg_vals = [bulk_data[e]["negative"] for e in entities]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(names))
    width = 0.35

    bars_pos = ax.bar(x - width / 2, pos_vals, width, label="Positive",
                      color=COLORS["positive"], alpha=0.85)
    bars_neg = ax.bar(x + width / 2, neg_vals, width, label="Negative",
                      color=COLORS["negative"], alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Article Count")
    ax.set_title("Entity Sentiment Comparison")
    ax.legend()
    fig.tight_layout()
    path = os.path.join(CHARTS_DIR, "bulk_sentiment.png")
    fig.savefig(path, dpi=150, facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  → {path}")
    return path


# ── Report Printer ─────────────────────────────────────────────────
def print_report(sc_data, sent_data, trend_data, topic_data, entities_data,
                 net_data, bulk_data, framing_compare, all_articles):
    """Print structured report to stdout."""
    lines = []
    lines.append("=" * 60)
    lines.append("PESTA BABI — News Content Analysis Report")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    # Data Science
    lines.append("\n## DATA SCIENCE ANALYTICS\n")
    lines.append(f"Total Articles: {sent_data['total']}")
    lines.append(f"Sentiment: {sent_data['positive']} positive, "
                 f"{sent_data['negative']} negative, {sent_data['neutral']} neutral")
    lines.append(f"Sentiment Ratio: "
                 f"{sent_data['positive']/max(sent_data['total'],1)*100:.0f}% pos / "
                 f"{sent_data['negative']/max(sent_data['total'],1)*100:.0f}% neg")

    lines.append(f"\nSources ({len(sc_data)}):")
    for s in sorted(sc_data, key=lambda x: -x["article_count"]):
        lines.append(f"  {SOURCE_LABELS.get(s['source'], s['source']):20s} "
                     f"{s['article_count']:3d} articles  avg_sent={s.get('avg_sentiment_score',0):+.2f}")

    lines.append(f"\nTopic Trend:")
    for point in topic_data:
        lines.append(f"  {point['date']}: {point['article_count']} articles")

    lines.append(f"\nSentiment Trend:")
    for point in trend_data:
        lines.append(f"  {point['date']}: +{point.get('positive',0)}/-{point.get('negative',0)}")

    # Entities
    lines.append(f"\n## TOP ENTITIES\n")
    for e in sorted(entities_data, key=lambda x: -x["mention_count"])[:15]:
        lines.append(f"  {e['word']:25s} ({e['entity_group']:3s})  {e['mention_count']:3d} mentions")

    # Social Network
    lines.append(f"\n## SOCIAL NETWORK ANALYSIS\n")
    nodes = net_data.get("nodes", [])
    edges = net_data.get("edges", [])
    lines.append(f"Network: {len(nodes)} nodes, {len(edges)} edges, "
                 f"density={len(edges)/max(len(nodes)*(len(nodes)-1)/2,1):.4f}")
    top_nodes = sorted(nodes, key=lambda n: n["mention_count"], reverse=True)[:10]
    lines.append("Central nodes:")
    for n in top_nodes:
        lines.append(f"  {n['name']:25s} ({n['entity_group']:3s})  {n['mention_count']:3d}")

    # Framing
    lines.append(f"\n## FRAMING ANALYSIS\n")
    for entity_name, frames in sorted(framing_compare.items()):
        lines.append(f"\n  {entity_name}:")
        for f in frames[:5]:
            lines.append(f"    • {f['framing_phrase'][:70]}: {f['article_count']}")

    # Relations
    lines.append(f"\n## ACTOR RELATIONS (SVO)\n")
    rel_files = [f for f in os.listdir(DATA_DIR) if f.startswith("rel_")]
    for rf in sorted(rel_files):
        with open(os.path.join(DATA_DIR, rf)) as f:
            d = json.load(f)
        actions = d.get("actions", [])
        if actions:
            entity = d.get("source_entity", rf)
            lines.append(f"\n  {entity}:")
            for a in actions[:5]:
                lines.append(f"    {a['source_entity']} --[{a['relation']}]--> "
                             f"{a['target_entity']} (x{a['count']})")

    # Key Findings
    lines.append(f"\n## KEY FINDINGS\n")
    print("\n".join(lines))

    # Return structured data for README
    total_pos = sent_data["positive"]
    total_neg = sent_data["negative"]
    total = sent_data["total"]
    neg_pct = total_neg / max(total, 1) * 100
    pos_pct = total_pos / max(total, 1) * 100
    return {
        "total_articles": total,
        "neg_pct": neg_pct,
        "pos_pct": pos_pct,
        "sources_count": len(sc_data),
        "top_source": max(sc_data, key=lambda x: x["article_count"])["source"],
        "top_source_label": SOURCE_LABELS.get(max(sc_data, key=lambda x: x["article_count"])["source"], "?"),
        "peak_week": max(topic_data, key=lambda x: x["article_count"])["date"],
        "peak_count": max(topic_data, key=lambda x: x["article_count"])["article_count"],
        "top_entities": sorted(entities_data, key=lambda x: -x["mention_count"])[:10],
        "node_count": len(nodes),
        "edge_count": len(edges),
    }


# ── Main ───────────────────────────────────────────────────────────
def main():
    print("Loading data...")
    sc_data = load_json("source_comparison.json")
    sent_data = load_json("sentiment_distribution.json")
    trend_data = load_json("sentiment_trend.json")
    topic_data = load_json("topic_trend.json")
    entities_data = load_json("top_entities.json")
    net_data = load_json("network_cooccurrence.json")
    bulk_data = load_json("bulk_sentiment.json")
    framing_compare = load_json("framing_compare.json")
    all_articles = load_json("all_articles.json")

    print("\n=== Generating Charts ===\n")
    chart_source_comparison(sc_data)
    chart_sentiment_pie(sent_data)
    chart_sentiment_trend(trend_data)
    chart_topic_trend(topic_data)
    chart_entity_frequency(entities_data)
    chart_network_cooccurrence(net_data)
    chart_bulk_sentiment(bulk_data)
    chart_framing_heatmap(framing_compare)

    print("\n=== Report ===\n")
    stats = print_report(sc_data, sent_data, trend_data, topic_data,
                         entities_data, net_data, bulk_data,
                         framing_compare, all_articles)

    # Save stats for README generation
    stats_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report_stats.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"\nStats saved to {stats_path}")
    print("\n✅ All charts generated in ./charts/")


if __name__ == "__main__":
    main()