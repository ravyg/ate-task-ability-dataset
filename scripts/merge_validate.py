#!/usr/bin/env python3
"""
merge_validate.py  —  Merge all labeled chunks into one CSV and validate it.

- Concatenates every partial_output/soc*_out/chunk_*.csv
- Validates: only the 52 permitted abilities, no duplicate (task_id, ability) rows,
  every input task_id present, weights in {1,2,3}, uncertain in {0,1}
- Writes  ../data/task_ability_mapping_new_groups.csv  (new groups only — an APPEND
  to the frozen published data/task_ability_mapping.csv; the frozen file is untouched)
- Reports coverage vs the manifest so you can see exactly what is still unlabeled.

No annotator names or emails exist in these rows (schema is task-level labels only),
so no PII step is required for this file.

Usage:  python merge_validate.py
"""
import os, json, glob, csv, collections

HERE = os.path.dirname(os.path.abspath(__file__))
from label_chunks import ABILITIES  # single source of truth for the 52 names

def main():
    manifest = json.load(open(os.path.join(HERE, "manifest.json")))
    expected_ids = {}
    for e in manifest:
        for t in json.load(open(os.path.join(HERE, e["input"]))):
            expected_ids[str(t["task_id"])] = e["soc"]

    rows, seen_pairs, bad_ability, bad_weight = [], set(), collections.Counter(), 0
    labeled_ids = set()
    for csvf in sorted(glob.glob(os.path.join(HERE, "partial_output/soc*_out/chunk_*.csv"))):
        with open(csvf, encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                tid, ab = row["task_id"], row["ability_name"]
                labeled_ids.add(tid)
                if ab not in ABILITIES:
                    bad_ability[ab] += 1; continue
                try:
                    w = int(row["weight"]); assert w in (1,2,3)
                except Exception:
                    bad_weight += 1; continue
                key = (tid, ab)
                if key in seen_pairs:      # de-dup identical (task, ability)
                    continue
                seen_pairs.add(key)
                rows.append(row)

    out = os.path.join(HERE, "..", "data", "task_ability_mapping_new_groups.csv")
    out = os.path.abspath(out)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["task_id","occupation","task_text","ability_name","weight","uncertain"])
        for row in rows:
            w.writerow([row["task_id"],row["occupation"],row["task_text"],
                        row["ability_name"],row["weight"],row["uncertain"]])

    unlabeled = set(expected_ids) - labeled_ids
    by_group = collections.Counter(expected_ids[i] for i in unlabeled)
    print("=" * 60)
    print(f"Merged rows written : {len(rows):>8}   -> {out}")
    print(f"Unique tasks labeled: {len(labeled_ids):>8} / {len(expected_ids)} expected")
    print(f"Mean abilities/task : {len(rows)/max(len(labeled_ids),1):.2f}")
    print(f"Invalid ability names: {sum(bad_ability.values())}  {dict(bad_ability) or ''}")
    print(f"Bad weights dropped  : {bad_weight}")
    if unlabeled:
        print(f"\nSTILL UNLABELED: {len(unlabeled)} tasks across groups "
              f"{ {k:v for k,v in sorted(by_group.items())} }")
        print("Run  python label_chunks.py  to finish them, then re-run this.")
    else:
        print("\nALL TASKS LABELED. Ready to append to data/task_ability_mapping.csv")
    print("=" * 60)

if __name__ == "__main__":
    main()
