#!/usr/bin/env python3
"""
label_chunks.py  —  Standalone task -> ability labeler for the ATE dataset.

Labels O*NET task statements with the subset of the 52 O*NET abilities each task
invokes (name + weight 1/2/3 + uncertain flag), replicating the method used for
the frozen published mappings. Output is one CSV per chunk under partial_output/.

RESUME BY DESIGN: a chunk whose output CSV already exists is SKIPPED. So you can
stop and re-run anytime; only unlabeled chunks are processed. Safe to run in
parallel across machines as long as they don't share the same output dir.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install -r requirements.txt
    python label_chunks.py                 # label every pending chunk
    python label_chunks.py --soc 51        # only one SOC group
    python label_chunks.py --workers 6     # concurrency (default 4)
    python label_chunks.py --model claude-sonnet-4-5-20250929   # pin a model
    python label_chunks.py --dry-run       # show what WOULD run, call nothing

When done, run:  python merge_validate.py
"""
import os, sys, json, csv, glob, argparse, time, re
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_PATH = os.path.join(HERE, "LABELING_SPEC_GENERAL.md")
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"  # Sonnet — matches the published dataset method

# The 52 O*NET abilities. The model may ONLY use these exact strings.
ABILITIES = {
    # Cognitive (21)
    "Category Flexibility","Deductive Reasoning","Flexibility of Closure","Fluency of Ideas",
    "Inductive Reasoning","Information Ordering","Mathematical Reasoning","Memorization",
    "Number Facility","Oral Comprehension","Oral Expression","Originality","Perceptual Speed",
    "Problem Sensitivity","Selective Attention","Spatial Orientation","Speed of Closure",
    "Time Sharing","Visualization","Written Comprehension","Written Expression",
    # Psychomotor (10)
    "Arm-Hand Steadiness","Control Precision","Finger Dexterity","Manual Dexterity",
    "Multilimb Coordination","Rate Control","Reaction Time","Response Orientation",
    "Speed of Limb Movement","Wrist-Finger Speed",
    # Physical (9)
    "Dynamic Flexibility","Dynamic Strength","Explosive Strength","Extent Flexibility",
    "Gross Body Coordination","Gross Body Equilibrium","Stamina","Static Strength","Trunk Strength",
    # Sensory (12)
    "Auditory Attention","Depth Perception","Far Vision","Glare Sensitivity","Hearing Sensitivity",
    "Near Vision","Night Vision","Peripheral Vision","Sound Localization","Speech Clarity",
    "Speech Recognition","Visual Color Discrimination",
}

def load_spec():
    with open(SPEC_PATH, encoding="utf-8") as f:
        return f.read()

SYSTEM = (
    "You are an expert O*NET occupational analyst labeling tasks with the human abilities "
    "they require, for an academic dataset. You follow the provided spec exactly and use ONLY "
    "the 52 permitted ability names."
)

def build_user_prompt(spec, tasks):
    task_block = "\n".join(
        f'{t["task_id"]}\t{t["occupation"]}\t{t["task_text"]}' for t in tasks
    )
    return f"""{spec}

---
Label EVERY task below. For each task choose the abilities it genuinely invokes
(typically 3-7; range 1-12), each with weight (1=mild, 2=moderate, 3=critical) and
uncertain (0/1). Manual/physical tasks MUST receive the physical/psychomotor/sensory
abilities they require; do not under-label physical work. Cognitive/clerical tasks stay cognitive.

Return ONLY a JSON array, no prose. Each element:
  {{"task_id":"<id>","abilities":[{{"name":"<one of the 52>","weight":1-3,"uncertain":0|1}}, ...]}}
Every input task_id must appear exactly once. Use ONLY the 52 exact ability names.

TASKS (tab-separated: task_id, occupation, task_text):
{task_block}
"""

def extract_json(text):
    """Pull the JSON array out of the model response, tolerating code fences/prose."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("no JSON array found in response")
    return json.loads(text[start:end+1])

def label_chunk(client, model, spec, entry, max_retries=4):
    with open(entry["input"], encoding="utf-8") as f:
        tasks = json.load(f)
    by_id = {str(t["task_id"]): t for t in tasks}
    prompt = build_user_prompt(spec, tasks)

    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.messages.create(
                model=model, max_tokens=16000, system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            parsed = extract_json("".join(b.text for b in resp.content if b.type == "text"))
            # ---- validate ----
            seen, bad = set(), set()
            rows = []
            for item in parsed:
                tid = str(item["task_id"])
                if tid not in by_id:
                    continue
                seen.add(tid)
                for ab in item.get("abilities", []):
                    name = ab["name"].strip()
                    if name not in ABILITIES:
                        bad.add(name); continue
                    w = int(ab.get("weight", 2)); w = 1 if w < 1 else 3 if w > 3 else w
                    unc = 1 if int(ab.get("uncertain", 0)) else 0
                    t = by_id[tid]
                    rows.append((tid, t["occupation"], t["task_text"], name, w, unc))
            missing = set(by_id) - seen
            if bad:
                raise ValueError(f"invalid ability names: {sorted(bad)[:5]}")
            if missing:
                raise ValueError(f"{len(missing)} tasks unlabeled (e.g. {sorted(missing)[:3]})")
            # ---- write ----
            os.makedirs(os.path.dirname(entry["output"]), exist_ok=True)
            with open(entry["output"], "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["task_id", "occupation", "task_text", "ability_name", "weight", "uncertain"])
                w.writerows(rows)
            return (entry, len(by_id), len(rows), round(len(rows)/max(len(by_id),1), 2), None)
        except Exception as e:
            last_err = e
            time.sleep(min(2 ** attempt, 20))
    return (entry, 0, 0, 0, str(last_err))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--soc", help="only this SOC group, e.g. 51")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--model", default=os.environ.get("ATE_MODEL", DEFAULT_MODEL))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = json.load(open(os.path.join(HERE, "manifest.json")))
    pending = [e for e in manifest
               if not os.path.exists(os.path.join(HERE, e["output"]))
               and (not args.soc or e["soc"] == args.soc)]
    # normalize paths to absolute
    for e in pending:
        e["input"] = os.path.join(HERE, e["input"])
        e["output"] = os.path.join(HERE, e["output"])

    total_tasks = sum(e["n_tasks"] for e in pending)
    print(f"Pending chunks: {len(pending)}  |  tasks: {total_tasks}  |  model: {args.model}")
    if args.dry_run:
        for e in pending:
            print(f"  would label soc{e['soc']} chunk {e['chunk']:02d}  ({e['n_tasks']} tasks)")
        return
    if not pending:
        print("Nothing pending. Run:  python merge_validate.py")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ERROR: set ANTHROPIC_API_KEY in your environment first.")
    from anthropic import Anthropic
    client = Anthropic()
    spec = load_spec()

    ok = fail = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(label_chunk, client, args.model, spec, e): e for e in pending}
        for fut in as_completed(futs):
            entry, ntasks, nrows, mean, err = fut.result()
            if err:
                fail += 1
                print(f"  FAIL soc{entry['soc']} c{entry['chunk']:02d}: {err}")
            else:
                ok += 1
                print(f"  ok   soc{entry['soc']} c{entry['chunk']:02d}: {ntasks} tasks -> {nrows} rows (mean {mean})")
    print(f"\nDone. labeled {ok} chunks, {fail} failed.")
    print("Re-run to retry any failures (finished chunks are skipped). Then: python merge_validate.py")

if __name__ == "__main__":
    main()
