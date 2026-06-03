#!/usr/bin/env bash
# Reproduce everything for deforestation human-caused research
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo " DEFORESTASI MANUSIA — Full Pipeline"
echo "========================================"

echo ""
echo "=== Phase 1: Fetch data ==="
python3 scripts/01_fetch_data.py

echo ""
echo "=== Phase 2: Analyze ==="
python3 scripts/02_analyze.py

echo ""
echo "=== Phase 3: Aggregate ==="
python3 scripts/03_aggregate.py

echo ""
echo "=== Phase 4: Visualize ==="
python3 scripts/04_visualize.py

echo ""
echo "=== Phase 5: Text Classification (BoW) ==="
uv run python3 scripts/01_bow_analysis.py

echo ""
echo "=== Phase 6: Text Classification (TF-IDF + LinearSVC) ==="
uv run python3 scripts/02_tfidf_classifier.py

echo ""
echo "✅ Pipeline complete"