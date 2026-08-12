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

The labeling is done **inside Claude Code** on your Claude plan credits — the same system
that produced the first 47 chunks. **No API key, no `pip install` for labeling.**

1. `cd scripts` and start Claude Code: `claude`
2. Paste the prompt in **[`RUN_WITH_CLAUDE.md`](RUN_WITH_CLAUDE.md)**. Claude labels the
   remaining chunks with its **Sonnet** model, skipping the 47 already done.
3. When labeling finishes, validate:
   ```bash
   python3 merge_validate.py     # merges + validates -> ../data/task_ability_mapping_new_groups.csv
   ```

That's it. The run **skips any chunk already labeled**, so you can stop and restart any
time and only do what's left. When `merge_validate.py` prints `ALL TASKS LABELED`, you're done.

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
| `RUN_WITH_CLAUDE.md` | **Start here.** The Claude Code prompt to paste to finish the run (Sonnet, your plan credits, no API key). |
| `merge_validate.py` | Concatenates all chunk CSVs, validates (52-ability check, dedup, no-skip), writes the merged new-groups CSV, and reports what's still unlabeled. |
| `LABELING_SPEC_GENERAL.md` | The exact labeling instructions + the 52-ability list + few-shot examples. This is the ground truth for *how* to label. |
| `manifest.json` | All 118 chunks: `soc`, `chunk`, `n_tasks`, input path, output path, status. |
| `chunks/socNN/chunk_XX.json` | Input task statements (from O*NET 30.2), grouped into chunks. |
| `partial_output/socNN_out/chunk_XX.csv` | Already-labeled chunks (the 47 done). Delete one to force a re-label. |

## Output schema (one row per task–ability)

```
task_id,occupation,task_text,ability_name,weight,uncertain
```
- `ability_name` — one of the 52 exact names in the spec (no others).
- `weight` — 1 = mild, 2 = moderate, 3 = critical.
- `uncertain` — 1 if borderline, else 0.
- Typically 3–7 abilities per task (dataset mean ≈ 5.4).

## Notes

- **Model:** must stay on Claude **Sonnet** — matches the method used for the published
  mappings and the 47 chunks already done. (The prompt in `RUN_WITH_CLAUDE.md` says so.)
- **Idempotent / safe to interrupt:** stop anytime; restart resumes. A chunk is "done"
  purely by the existence of its output CSV. To force a redo, delete that CSV.
- **Cost control:** you can tell Claude to do one SOC group at a time to spread it out.
- **No PII:** these rows are task-level ability labels only — no annotator names or
  emails. (Human-annotation/crowdsource files live elsewhere and are not touched here.)
- After `merge_validate.py` reports `ALL TASKS LABELED`, the new-groups CSV can be
  appended to `../data/task_ability_mapping.csv` for the full economy-wide release.
