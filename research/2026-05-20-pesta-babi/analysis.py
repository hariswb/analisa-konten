#!/usr/bin/env python3
"""
Analisis Jaringan & Sentimen: "Pesta Babi"
============================================
Menggunakan data dari Semantik Research API untuk menganalisis
cakupan media, jaringan co-occurrence entitas, dan sentimen
seputar film dokumenter "Pesta Babi".

Dependencies: networkx, matplotlib, numpy, json (stdlib)

Cara pakai:
  python3 analysis.py

Pastikan SEMANTIK_RESEARCH_API_KEY ter-set jika ingin fetch ulang data.
"""

import json
import os
import sys
from pathlib import Path

import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# ─── Konfigurasi ────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent
OUTPUT_DIR = DATA_DIR

TOPIC = "pesta babi"
DATE_FROM = "2026-03-20"  # 2 bulan sebelum 2026-05-20
DATE_TO = "2026-05-20"

# ─── Warna entity group ─────────────────────────────────────────────
GROUP_COLORS = {
    "PER": "#e74c3c",   # People — merah
    "ORG": "#3498db",   # Organisasi — biru
    "NOR": "#2ecc71",   # Norma/Institusi — hijau
    "GPE": "#f39c12",   # Geopolitical — oranye
    "EVT": "#9b59b6",   # Event — ungu
    "LOC": "#1abc9c",   # Location — teal
    "CRD": "#95a5a6",   # Cardinal — abu-abu
}

DEFAULT_COLOR = "#95a5a6"

# ─── Load Data ──────────────────────────────────────────────────────
def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        print(f"[WARNING] {path} not found. Skipping.")
        return None
    with open(path) as f:
        return json.load(f)


def load_cooccurence():
    d = load_json("cooccurence_data.json")
    if not d:
        return [], []
    return d.get("nodes", []), d.get("edges", [])


def load_sentiment_trend():
    return load_json("sentiment_trend.json") or []


def load_top_entities():
    return load_json("top_entities.json") or []


def load_source_comparison():
    return load_json("source_comparison.json") or []


# ─── Network Analysis ───────────────────────────────────────────────
def build_network(nodes, edges):
    """Build a weighted undirected graph from co-occurrence data."""
    G = nx.Graph()

    node_attrs = {}
    for n in nodes:
        name = n["name"]
        G.add_node(name)
        node_attrs[name] = {
            "entity_group": n.get("entity_group", "UNK"),
            "mention_count": n.get("mention_count", 0),
        }
    nx.set_node_attributes(G, node_attrs)

    for e in edges:
        G.add_edge(e["source"], e["target"], weight=e.get("weight", 1))

    return G


def network_metrics(G):
    """Compute network metrics for the co-occurrence graph."""
    results = {}

    # 1. Basic stats
    results["nodes"] = G.number_of_nodes()
    results["edges"] = G.number_of_edges()
    results["density"] = nx.density(G)
    results["is_connected"] = nx.is_connected(G)

    # 2. Connected components
    components = list(nx.connected_components(G))
    results["components"] = len(components)
    if components:
        largest = max(components, key=len)
        results["largest_component_size"] = len(largest)

    # 3. Degree centrality (top 10)
    deg_centrality = nx.degree_centrality(G)
    top_deg = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    results["top_degree_centrality"] = [
        {"entity": name, "centrality": round(val, 4)}
        for name, val in top_deg
    ]

    # 4. Weighted degree (top 10) — total co-occurrence weight
    weighted_deg = dict(G.degree(weight="weight"))
    top_wdeg = sorted(weighted_deg.items(), key=lambda x: x[1], reverse=True)[:10]
    results["top_weighted_degree"] = [
        {"entity": name, "total_weight": val}
        for name, val in top_wdeg
    ]

    # 5. Betweenness centrality (top 10)
    if G.number_of_nodes() > 1:
        betweenness = nx.betweenness_centrality(G)
        top_bet = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
        results["top_betweenness"] = [
            {"entity": name, "centrality": round(val, 4)}
            for name, val in top_bet
        ]

    # 6. Clustering coefficient per node (top 10)
    clustering = nx.clustering(G)
    top_clust = sorted(clustering.items(), key=lambda x: x[1], reverse=True)[:10]
    results["top_clustering"] = [
        {"entity": name, "clustering": round(val, 4)}
        for name, val in top_clust
    ]

    # 7. Communities (greedy modularity)
    try:
        from networkx.algorithms.community import greedy_modularity_communities
        communities = list(greedy_modularity_communities(G, weight="weight"))
        results["communities"] = len(communities)
        results["community_sizes"] = [len(c) for c in communities]
        results["community_labels"] = [
            sorted(list(c)) for c in communities
        ]
    except Exception:
        results["communities"] = 0

    # 8. Assortativity by entity_group
    try:
        group_map = {n: G.nodes[n].get("entity_group", "UNK") for n in G.nodes()}
        results["assortativity"] = round(nx.attribute_assortativity_coefficient(G, "entity_group"), 4)
    except Exception:
        results["assortativity"] = None

    return results


# ─── Visualization ──────────────────────────────────────────────────
def visualize_network(G, metrics, output_path):
    """Generate a network visualization with node size/color by importance."""
    fig, ax = plt.subplots(1, 1, figsize=(16, 14))
    fig.patch.set_facecolor("#fafafa")

    # Layout
    pos = nx.spring_layout(G, k=1.2, iterations=50, seed=42)

    # Node sizes by mention_count (scaled)
    mention_counts = nx.get_node_attributes(G, "mention_count")
    sizes = [(mention_counts.get(n, 1) ** 0.7) * 80 for n in G.nodes()]
    sizes = [max(s, 100) for s in sizes]

    # Node colors by entity_group
    group_map = nx.get_node_attributes(G, "entity_group")
    colors = [GROUP_COLORS.get(group_map.get(n, ""), DEFAULT_COLOR) for n in G.nodes()]

    # Edge widths by weight
    edge_weights = [G.edges[e]["weight"] for e in G.edges()]
    max_w = max(edge_weights) if edge_weights else 1
    edge_widths = [1 + 3 * (w / max_w) for w in edge_weights]

    # Edge alpha
    edge_alphas = [0.2 + 0.5 * (w / max_w) for w in edge_weights]

    # Draw edges
    for i, (u, v) in enumerate(G.edges()):
        ax.annotate(
            "", xy=pos[v], xytext=pos[u],
            arrowprops=dict(
                arrowstyle="-",
                color="#888888",
                alpha=edge_alphas[i],
                lw=edge_widths[i],
            ),
        )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_size=sizes,
        node_color=colors,
        edgecolors="#333",
        linewidths=0.5,
        alpha=0.9,
    )

    # Labels — only for top nodes by mention count
    top_nodes = set(
        n for n, _ in sorted(
            mention_counts.items(), key=lambda x: x[1], reverse=True
        )[:20]
    )
    labels = {n: n for n in G.nodes() if n in top_nodes}
    nx.draw_networkx_labels(
        G, pos, labels=labels, ax=ax,
        font_size=8,
        font_family="sans-serif",
        font_weight="bold",
    )

    # Legend for entity groups
    from matplotlib.patches import Patch
    legend_elements = []
    seen_groups = set(group_map.values())
    for group, color in GROUP_COLORS.items():
        if group in seen_groups:
            legend_elements.append(
                Patch(facecolor=color, edgecolor="#333", label={
                    "PER": "Person (Individu)",
                    "ORG": "Organisasi",
                    "NOR": "Institusi/Norma",
                    "GPE": "Lokasi Geopolitik",
                    "EVT": "Acara/Topik",
                    "LOC": "Lokasi",
                    "CRD": "Lainnya",
                }.get(group, group))
            )
    ax.legend(handles=legend_elements, loc="upper right", fontsize=9,
              framealpha=0.9, edgecolor="#ccc")

    # Title
    ax.set_title(
        "Jaringan Co-occurrence: Pesta Babi\n"
        f"{G.number_of_nodes()} entitas, {G.number_of_edges()} hubungan",
        fontsize=14, fontweight="bold", pad=15
    )
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[✓] Network visualization saved: {output_path}")


def visualize_sentiment(sentiment_trend, source_comp, output_dir):
    """Generate sentiment charts."""
    # ── Trend line chart ──
    if sentiment_trend:
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("#fafafa")

        dates = [s["date"] for s in sentiment_trend]
        x = range(len(dates))
        ax.plot(x, [s.get("positive", 0) for s in sentiment_trend],
                color="#2ecc71", marker="o", label="Positif", linewidth=2)
        ax.plot(x, [s.get("negative", 0) for s in sentiment_trend],
                color="#e74c3c", marker="o", label="Negatif", linewidth=2)
        ax.plot(x, [s.get("neutral", 0) for s in sentiment_trend],
                color="#95a5a6", marker="o", label="Netral", linewidth=2)

        ax.set_xticks(x)
        ax.set_xticklabels(dates, rotation=30, ha="right", fontsize=8)
        ax.set_title("Tren Sentimen (Mingguan)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Jumlah Artikel")
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        trend_path = output_dir / "sentiment_trend.png"
        plt.savefig(trend_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[✓] Sentiment trend saved: {trend_path}")

    # ── Source comparison bar chart ──
    if source_comp:
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#fafafa")

        sources = [s["source"] for s in source_comp]
        article_counts = [s["article_count"] for s in source_comp]
        colors = ["#2ecc71" if s["avg_sentiment_score"] >= 0 else "#e74c3c"
                  for s in source_comp]
        bars = ax.barh(range(len(sources)), article_counts, color=colors, edgecolor="#333", linewidth=0.5)

        ax.set_yticks(range(len(sources)))
        ax.set_yticklabels(sources, fontsize=9)
        ax.set_xlabel("Jumlah Artikel")
        ax.set_title("Liputan per Media", fontsize=12, fontweight="bold")

        # Add labels
        for i, (bar, s) in enumerate(zip(bars, source_comp)):
            score = s["avg_sentiment_score"]
            label = f"{article_counts[i]} ({score:+.1f})"
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    label, va="center", fontsize=8)

        from matplotlib.patches import Patch
        ax.legend(handles=[
            Patch(facecolor="#2ecc71", label="Rata-rata positif"),
            Patch(facecolor="#e74c3c", label="Rata-rata negatif"),
        ], fontsize=8, loc="lower right")

        ax.set_xlim(0, max(article_counts) * 1.3)
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        source_path = output_dir / "source_comparison.png"
        plt.savefig(source_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[✓] Source comparison saved: {source_path}")


# ─── Report ─────────────────────────────────────────────────────────
def print_report(metrics, source_comp, sentiment_trend, top_entities):
    """Print structured analysis report."""
    report = []
    report.append("=" * 60)
    report.append("ANALISIS: PESTA BABI")
    report.append(f"Periode: {DATE_FROM} s.d. {DATE_TO}")
    report.append("=" * 60)

    # ── 1. Network metrics ──
    report.append("\n[1] METRIK JARINGAN CO-OCCURRENCE")
    report.append("-" * 40)
    report.append(f"  Total nodes (entitas):   {metrics['nodes']}")
    report.append(f"  Total edges (hubungan):  {metrics['edges']}")
    report.append(f"  Density jaringan:        {metrics['density']:.4f}")
    report.append(f"  Terhubung:               {metrics['is_connected']}")
    report.append(f"  Komponen terhubung:      {metrics['components']}")
    report.append(f"  Komponen terbesar:       {metrics['largest_component_size']} nodes")

    if metrics["assortativity"] is not None:
        report.append(f"  Assortativity (group):   {metrics['assortativity']:+.4f}")

    if metrics.get("communities"):
        report.append(f"  Komunitas (modularity):  {metrics['communities']} kelompok")
        for i, size in enumerate(metrics["community_sizes"]):
            labels = metrics["community_labels"][i]
            report.append(f"    Kelompok {i+1}: {size} entitas: {', '.join(labels[:5])}{'...' if size > 5 else ''}")

    # ── 2. Centrality ──
    report.append("\n[2] ENTITAS PALING SENTRAL (Degree Centrality)")
    report.append("-" * 40)
    for item in metrics["top_degree_centrality"]:
        report.append(f"  {item['entity']:30s} centrality={item['centrality']:.4f}")

    report.append("\n[3] ENTITAS DENGAN BOBOT HUBUNGAN TERBESAR")
    report.append("-" * 40)
    for item in metrics["top_weighted_degree"]:
        report.append(f"  {item['entity']:30s} total_weight={item['total_weight']}")

    report.append("\n[4] ENTITAS PENGHUBUNG (Betweenness Centrality)")
    report.append("-" * 40)
    for item in metrics.get("top_betweenness", []):
        report.append(f"  {item['entity']:30s} betweenness={item['centrality']:.4f}")

    # ── 3. Top entities ──
    report.append("\n[5] TOP ENTITAS (dari API)")
    report.append("-" * 40)
    for e in top_entities[:15]:
        sources = ", ".join(e.get("top_sources", [])[:3])
        report.append(f"  {e['word']:30s} ({e['entity_group']:3s}) — {e['mention_count']:3d} sebutan  [{sources}]")

    # ── 4. Source comparison ──
    report.append("\n[6] LIPUTAN PER MEDIA (sentiment score)")
    report.append("-" * 40)
    total_articles = sum(s["article_count"] for s in source_comp)
    report.append(f"  Total artikel: {total_articles}")
    for s in source_comp:
        dist = s["sentiment_distribution"]
        report.append(
            f"  {s['source']:20s} | {s['article_count']:3d} artikel "
            f"| score={s['avg_sentiment_score']:+.2f} "
            f"| [+]={dist.get('positive',0)} [-]={dist.get('negative',0)} "
            f"|/[o]={dist.get('neutral',0)}"
        )

    # ── 5. Sentiment ──
    report.append("\n[7] TREN SENTIMEN (Mingguan)")
    report.append("-" * 40)
    for s in sentiment_trend:
        report.append(f"  {s['date']} | [+]={s.get('positive',0)} [-]={s.get('negative',0)} |/[o]={s.get('neutral',0)}")

    report.append("\n" + "=" * 60)
    report.append("SELESAI. Data dan visualisasi tersimpan di direktori ini.")
    report.append("=" * 60)

    print("\n".join(report))

    # Save report to file
    report_path = OUTPUT_DIR / "report.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(report))
    print(f"\n[✓] Report saved: {report_path}")


# ─── Main ───────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  ANALISIS PESTA BABI — Co-occurrence Network & Sentimen")
    print("=" * 60)

    # Load data
    print("\n[○] Loading data...")
    nodes, edges = load_cooccurence()
    if not nodes:
        print("[✗] No co-occurrence data found. Exiting.")
        return

    sentiment_trend = load_sentiment_trend()
    top_entities = load_top_entities()
    source_comp = load_source_comparison()

    print(f"  Co-occurrence: {len(nodes)} nodes, {len(edges)} edges")
    print(f"  Sentiment trend: {len(sentiment_trend)} weeks")
    print(f"  Top entities: {len(top_entities)}")
    print(f"  Source comparison: {len(source_comp)} media")

    # Build network
    print("\n[○] Building network graph...")
    G = build_network(nodes, edges)

    # Compute metrics
    print("[○] Computing network metrics...")
    metrics = network_metrics(G)

    # Visualize
    print("\n[○] Generating visualizations...")
    visualize_network(G, metrics, OUTPUT_DIR / "network_cooccurence.png")
    visualize_sentiment(sentiment_trend, source_comp, OUTPUT_DIR)

    # Report
    print("\n[○] Generating report...")
    print_report(metrics, source_comp, sentiment_trend, top_entities)

    print("\n[✓] All done!")


if __name__ == "__main__":
    main()
