#!/usr/bin/env bash
set -euo pipefail

# Reproduce all Lagi Bahlil research outputs from scratch.
# Run from the project root (research/2026-05-26-lagu-bahlil/).
#
# Prerequisites: Python 3.13+, pip, git
#   pip install --user git+https://github.com/hariswb/tantular.git

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Computing basic stats ==="
python3 scripts/compute_basic_stats.py

echo "=== Computing hourly counts ==="
python3 scripts/compute_hourly_counts.py

echo "=== Computing NLP analysis (BagOfWords + InSet sentiment) ==="
python3 scripts/compute_nlp_analysis.py

echo "=== Testing engineered hypothesis ==="
python3 scripts/engineered_hypothesis.py

echo "=== Testing hypothesis part 2 ==="
python3 scripts/hypothesis_part2.py

echo "=== Generating verdict ==="
python3 scripts/verdict.py

echo "=== Computing daily emoji counts ==="
python3 scripts/compute_daily_emoji.py

echo "=== Generating timeline visualizations ==="
python3 scripts/compute_timeline.py

echo ""
echo "=== DONE ==="
echo "Output JSONs:"
ls -lh data/*.json
echo ""
echo "Output HTMLs:"
ls -lh *.html