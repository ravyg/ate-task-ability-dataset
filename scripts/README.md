# Task → Ability Labeling Pipeline (economy-wide expansion)

This directory regenerates the **task → ability mappings** that power the ATE
(AI Task Exposure) dataset, extended from the original 6 SOC major groups to **all
occupations in the O*NET corpus**. It labels each O*NET task statement with the subset
of the **52 O*NET abilities** it invokes, each with a weight (1–3) and an uncertainty flag.

The method replicates the one used for the frozen published mappings in
`../data/task_ability_mapping.csv`, so new rows are consistent with the old ones.
**Nothing in the frozen file changes — this only produces NEW mappings for the
previously-missing SOC groups.**

---

## TL;DR — how to finish the run

```bash
cd scripts
python3 -m pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...          # your Anthropic API key

python3 label_chunks.py          # labels every still-pending chunk (resumable)
python3 merge_validate.py        # merges + validates -> ../data/task_ability_mapping_new_groups.csv
```

That's it. `label_chunks.py` **skips any chunk already labeled**, so you can stop and
re-run any time, and you only pay for what's left. When `merge_validate.py` prints
`ALL TASKS LABELED`, the run is complete.

---

## Current state (checked into this branch)

| | |
|---|---|
| SOC groups in scope | 15 (+ the SOC-15 pilot) |
| Chunks total | 118 |
| **Chunks already labeled** | **47** (committed under `partial_output/`) |
| **Chunks remaining** | **71  (~8,431 tasks)** |

Remaining work by group (everything else is done):

| SOC | Group | Chunks left | Tasks left |
|-----|-------|-------------|-----------|
| 25 | Education | 5 | 596 |
| 27 | Arts / Media | 7 | 806 |
| 33 | Protective Service | 5 | 522 |
| 35 | Food Prep / Serving | 3 | 319 |
| 37 | Cleaning / Grounds | 2 | 168 |
| 39 | Personal Care | 5 | 617 |
| 45 | Farming / Fishing | 2 | 220 |
| 47 | Construction | 9 | 1,141 |
| 49 | Installation / Maintenance | 8 | 1,008 |
| 51 | Production | 17 | 2,117 |
| 53 | Transportation | 8 | 917 |

> Most of the remaining groups are **manual / physical**. The spec requires their tasks
> to receive physical/psychomotor/sensory abilities (strength, dexterity, coordination,
> vision) — these occupations should end up with **low** AI-exposure, which is the key
> sanity check for the paper.

---

## What each file is

| File | Purpose |
|------|---------|
| `label_chunks.py` | Standalone labeler. Calls the Anthropic API, one request per chunk, validates against the 52 abilities, writes one CSV per chunk. **Resumable** (skips done chunks). |
| `merge_validate.py` | Concatenates all chunk CSVs, validates (52-ability check, dedup, no-skip), writes the merged new-groups CSV, and reports what's still unlabeled. |
| `LABELING_SPEC_GENERAL.md` | The exact labeling instructions + the 52-ability list + few-shot examples. This is the ground truth for *how* to label. |
| `manifest.json` | All 118 chunks: `soc`, `chunk`, `n_tasks`, input path, output path, status. |
| `chunks/socNN/chunk_XX.json` | Input task statements (from O*NET 30.2), grouped into chunks. |
| `partial_output/socNN_out/chunk_XX.csv` | Already-labeled chunks (the 47 done). Delete one to force a re-label. |
| `requirements.txt` | Just `anthropic`. |

## Output schema (one row per task–ability)

```
task_id,occupation,task_text,ability_name,weight,uncertain
```
- `ability_name` — one of the 52 exact names in the spec (no others).
- `weight` — 1 = mild, 2 = moderate, 3 = critical.
- `uncertain` — 1 if borderline, else 0.
- Typically 3–7 abilities per task (dataset mean ≈ 5.4).

## Useful flags

```bash
python3 label_chunks.py --dry-run          # list what would run, call nothing
python3 label_chunks.py --soc 51           # only Production
python3 label_chunks.py --workers 6        # more concurrency (watch rate limits)
python3 label_chunks.py --model <model-id> # pin a specific model
```

## Notes

- **Model:** defaults to Claude **Sonnet** (`claude-sonnet-4-5-20250929`) — matches the
  method used for the published mappings. Override with `--model` or `ATE_MODEL` if needed.
- **Idempotent / safe to interrupt:** kill it anytime; re-run resumes. A chunk is "done"
  purely by the existence of its output CSV.
- **No PII:** these rows are task-level ability labels only — no annotator names or
  emails. (Human-annotation/crowdsource files live elsewhere and are not touched here.)
- **Cost control:** run group-by-group with `--soc` if you want to spread it out.
- After `merge_validate.py` reports `ALL TASKS LABELED`, the new-groups CSV can be
  appended to `../data/task_ability_mapping.csv` for the full economy-wide release.
