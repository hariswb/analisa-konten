"""
TF-IDF + LinearSVC Text Classification — Deforestasi Articles
Classifies articles into thematic categories using sklearn

Labels are derived from keyword-matching on titles/summaries.
This serves as a demonstration of the full pipeline:
  preprocessing → TF-IDF vectorization → train/test split → LinearSVC → evaluation

Usage: python3 02_tfidf_classifier.py
"""

import json
import re
from collections import Counter
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    classification_report, confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.pipeline import Pipeline

# --- Config ---
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ARTICLES_FILE = DATA_DIR / "articles_list.json"

# --- Category Definitions (keyword-based labeling) ---
# Each category matches specific patterns in article titles + summaries
CATEGORIES = {
    "illegal_logging": [
        r"pembalakan liar", r"illegal logging", r"penebangan liar",
        r"perambahan hutan", r"pembukaan lahan.*ilegal", r"tersangka.*pembalakan",
        r"gakkum", r"polisi hutan", r"kayu ilegal", r"tebang liar",
        r"kasus.*pembalakan",
    ],
    "policy_politics": [
        r"izin.*dicabut", r"pencabutan.*izin", r"regulasi", r"kebijakan",
        r"karpet merah", r"konsesi", r"UU", r"diplomasi", r"EUDR",
        r"anies.*deforestasi", r"megawati", r"PDIP", r"DPR", r"alih fungsi",
        r"moratorium", r"peta jalan", r"pemerintah.*kebijakan",
        r"satgas PKH", r"97 persen",
    ],
    "ecological_impact": [
        r"banjir", r"banjir bandang", r"longsor", r"bencana.*ekologis",
        r"krisis ekologi", r"gelombang panas", r"habitat.*terancam",
        r"spesies.*kritis", r"primata.*punah", r"fragmentasi habitat",
        r"degradasi lingkungan", r"konflik satwa",
        r"kerusakan.*DAS", r"ekosistem", r"biodiversitas",
    ],
    "health_disease": [
        r"malaria", r"nipah", r"virus", r"zoonosis", r"penyakit",
        r"monkey malaria", r"nyamuk", r"epidemiolog",
    ],
    "commodity_economy": [
        r"sawit", r"wood pellet", r"mebel", r"ekspor", r"CPO",
        r"biodiesel", r"B40", r"perdagangan", r"pasar global",
        r"impor", r"ekspor", r"industri.*hutan", r"Toba Pulp",
        r"danantara", r"MIND ID", r"perhutani", r"beras.*deforestasi",
        r"singkong.*deforestasi", r"tanaman pangan",
    ],
}


def label_article(title: str, summary: str) -> str:
    """Assign the best-matching category based on keyword patterns."""
    text = f"{title} {summary}".lower()
    scores = {}
    for cat, patterns in CATEGORIES.items():
        count = 0
        for p in patterns:
            matches = re.findall(p, text)
            count += len(matches)
        if count > 0:
            scores[cat] = count

    if not scores:
        return "other"

    # Return category with most pattern matches
    return max(scores, key=scores.get)


def main():
    # --- Load Data ---
    with open(ARTICLES_FILE) as f:
        data = json.load(f)
    items = data["items"]
    print(f"Articles loaded: {len(items)}")
    print("=" * 70)

    # --- Prepare documents + labels ---
    documents = []
    labels = []
    label_counts = Counter()

    for a in items:
        doc = f"{a['title']} {a['summary']}"
        documents.append(doc)
        label = label_article(a['title'], a['summary'])
        labels.append(label)
        label_counts[label] += 1

    print("\n📊 Category Distribution (from keyword labeling)")
    print("-" * 50)
    for cat, count in label_counts.most_common():
        pct = count / len(items) * 100
        print(f"  {cat:20s}: {count:3d} ({pct:5.1f}%)")

    # --- Train/Test Split ---
    X_train, X_test, y_train, y_test = train_test_split(
        documents, labels,
        test_size=0.30,
        random_state=42,
        stratify=labels,
    )

    print(f"\n📚 Train set: {len(X_train)} articles")
    print(f"🧪 Test set:  {len(X_test)} articles")

    # --- Build Pipeline ---
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 3),     # unigrams + bigrams + trigrams
            max_df=0.85,             # ignore terms in >85% of docs (too common)
            min_df=2,                # ignore terms in <2 docs (too rare)
            max_features=5000,
            sublinear_tf=True,       # use 1 + log(tf) instead of raw tf
        )),
        ("clf", LinearSVC(
            class_weight="balanced", # handle class imbalance
            random_state=42,
            max_iter=2000,
        )),
    ])

    # --- Train ---
    print("\n🚂 Training LinearSVC with TF-IDF features...")
    pipeline.fit(X_train, y_train)

    # --- Evaluate ---
    train_acc = pipeline.score(X_train, y_train)
    test_acc = pipeline.score(X_test, y_test)
    print(f"  Train accuracy: {train_acc:.2%}")
    print(f"  Test accuracy:  {test_acc:.2%}")

    # --- Cross-validation (more robust eval on small dataset) ---
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, documents, labels, cv=cv, scoring="accuracy")
    print(f"\n🏆 5-Fold Cross-Validation Accuracy:")
    print(f"  Mean: {cv_scores.mean():.2%} ± {cv_scores.std():.2%}")
    print(f"  Per fold: {[f'{s:.2%}' for s in cv_scores]}")

    # --- Detailed Classification Report ---
    y_pred = pipeline.predict(X_test)
    print("\n📋 Classification Report (Test Set)")
    print("-" * 50)
    print(classification_report(y_test, y_pred))

    # --- Top Features Per Category (most indicative words) ---
    print("\n🔍 Top 10 Most Indicative Words Per Category")
    print("-" * 50)
    feature_names = pipeline.named_steps["tfidf"].get_feature_names_out()
    classes = pipeline.named_steps["clf"].classes_

    for i, label in enumerate(classes):
        coef = pipeline.named_steps["clf"].coef_[i]
        top_idx = coef.argsort()[-10:][::-1]
        top_features = [feature_names[j] for j in top_idx]
        print(f"\n  {label:20s}:")
        for j, feat in enumerate(top_features):
            score = coef[top_idx[j]]
            print(f"    {j+1:2d}. {feat:30s} (weight: {score:+.4f})")

    # --- Per-Source Category Breakdown ---
    print("\n📰 Category Distribution by Source")
    print("-" * 50)
    source_cats = {}
    for a in items:
        src = a["source"]
        doc = f"{a['title']} {a['summary']}"
        cat = label_article(a['title'], a['summary'])
        if src not in source_cats:
            source_cats[src] = Counter()
        source_cats[src][cat] += 1

    for src in sorted(source_cats.keys()):
        cats = source_cats[src]
        total = sum(cats.values())
        parts = [f"{c}:{n}" for c, n in cats.most_common()]
        print(f"  {src:20s} (n={total:2d}): {', '.join(parts)}")

    # --- Save Model Predictions on All Data ---
    predictions = pipeline.predict(documents)
    enriched = []
    for i, a in enumerate(items):
        enriched.append({
            "title": a["title"],
            "summary": a["summary"],
            "source": a["source"],
            "url": a["url"],
            "published_at": a["published_at"],
            "keyword_label": labels[i],
            "classifier_label": predictions[i],
        })

    out_path = DATA_DIR / "classified_articles.json"
    with open(out_path, "w") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved classified articles to {out_path}")


if __name__ == "__main__":
    main()