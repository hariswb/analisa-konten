#!/usr/bin/env python3
"""Fetch deforestation news data from Semantik API → bronze layer.

Usage: python 01_fetch_data.py
Output: ../data/*.json
"""

import json, os, subprocess, sys, time

BASE = "https://semantik.cc"
KW = "deforestasi,illegal+logging,pembalakan+liar,perambahan+hutan,alih+fungsi+hutan,konversi+hutan,EUDR,konsesi+hutan,izin+hutan,pembukaan+lahan"
DATES = "date_from=2025-11-01&date_to=2026-06-02"
TOKEN = os.environ.get("SEMANTIK_RESEARCH_API_KEY", "")
if not TOKEN:
    print("ERROR: SEMANTIK_RESEARCH_API_KEY not set")
    sys.exit(1)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def curl(url, label=""):
    print(f"  Fetching {label or url[:60]}...", end=" ", flush=True)
    r = subprocess.run(
        ["curl", "-s", url, "-H", f"Authorization: Bearer {TOKEN}"],
        capture_output=True, text=True, timeout=120)
    data = json.loads(r.stdout)
    count_str = ""
    if isinstance(data, list) and data:
        if "article_count" in data[0]:
            count_str = f" ({sum(s['article_count'] for s in data)} arts)"
        elif "word" in data[0]:
            count_str = f" ({len(data)} items)"
    elif isinstance(data, dict) and "items" in data:
        count_str = f" ({len(data['items'])} items)"
    print(f"OK{count_str}")
    return data

def save(name, data):
    path = os.path.join(DATA_DIR, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  -> bronze/data/{name}")

# 1. Aggregated endpoints
save("source_comparison.json", curl(
    f"{BASE}/api/aggregated/source-comparison?topic_keywords={KW}&{DATES}", "source_comparison"))
save("topic_trend.json", curl(
    f"{BASE}/api/aggregated/topic-trend?keywords={KW}&{DATES}&interval=weekly", "topic_trend"))
save("sentiment_distribution.json", curl(
    f"{BASE}/api/sentiment/distribution?topic_keywords={KW}&{DATES}", "sentiment_distribution"))
save("sentiment_trend.json", curl(
    f"{BASE}/api/sentiment/trend?topic_keywords={KW}&{DATES}&interval=weekly", "sentiment_trend"))

# 2. Paginate all articles
all_items = []
offset = 0
while True:
    data = curl(f"{BASE}/api/articles/search?keywords={KW}&{DATES}&limit=50&offset={offset}", f"articles offset={offset}")
    items = data.get("items", [])
    if not items:
        break
    all_items.extend(items)
    offset += 50
    time.sleep(0.3)
save("articles_list.json", {"total": len(all_items), "items": all_items})
print(f"  Total articles fetched: {len(all_items)}")

# 3. Top entities
save("top_entities.json", curl(
    f"{BASE}/api/entities/top?topic_keywords={KW}&{DATES}&limit=30", "top_entities"))
save("top_persons.json", curl(
    f"{BASE}/api/entities/top?entity_group=PER&topic_keywords={KW}&{DATES}&limit=10", "top_persons"))
save("top_orgs.json", curl(
    f"{BASE}/api/entities/top?entity_group=ORG&topic_keywords={KW}&{DATES}&limit=10", "top_orgs"))
save("top_gpe.json", curl(
    f"{BASE}/api/entities/top?entity_group=GPE&topic_keywords={KW}&{DATES}&limit=10", "top_gpe"))

# 4. Bulk sentiment
key_ents = ["deforestasi", "illegal+logging", "kemenhut", "konsesi", "hutan",
            "aceh", "sumatra", "papua", "jakarta", "kuningan",
            "megawati", "anies", "prabowo"]
save("bulk_sentiment.json", curl(
    f"{BASE}/api/entities/bulk-sentiment?entities={','.join(key_ents)}&topic_keywords={KW}&{DATES}", "bulk_sentiment"))

# 5. Co-occurrence per entity
for ent in ["deforestasi", "illegal+logging", "kemenhut", "konsesi", "hutan"]:
    name = f"cooccurence_{ent.replace('+','_')}.json"
    data = curl(f"{BASE}/api/entities/{ent}/cooccurrence?topic_keywords={KW}&{DATES}&limit=15", f"cooccurrence {ent}")
    save(name, data)
    time.sleep(1)

# 6. Framing per entity
for ent in ["deforestasi", "illegal+logging", "kemenhut", "hutan", "konsesi"]:
    name = f"framing_{ent.replace('+','_')}.json"
    data = curl(f"{BASE}/api/framing/{ent}?topic_keywords={KW}&{DATES}&limit=10", f"framing {ent}")
    save(name, data)
    time.sleep(1)

# 7. Framing compare
save("framing_compare.json", curl(
    f"{BASE}/api/framing/compare?entities=deforestasi,kemenhut,anies,megawati&topic_keywords={KW}&{DATES}", "framing_compare"))

print("\n✅ Bronze layer complete — all raw data saved")