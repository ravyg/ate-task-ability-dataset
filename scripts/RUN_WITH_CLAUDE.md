# How to finish the labeling with Claude Code (no API key)

This run is done **inside Claude Code**, using your Claude plan credits — the same way
the first 47 chunks were labeled. There is **no API key and no `pip install`**. Claude
itself reads each chunk + the spec and writes the label CSVs, using its **Sonnet** model.

## Steps

1. Open a terminal in the `scripts/` folder of this repo.
2. Start Claude Code:  `claude`
3. Paste the prompt below.

Claude will label the remaining 71 chunks (~8,431 tasks) and skip the 47 already done.

---

## Prompt to paste into Claude Code

```
You are finishing a task→ability labeling job for an academic dataset. Work entirely
inside Claude Code using your own Sonnet model — do NOT use any Anthropic API key, and
do NOT write a script that calls an API. You do the labeling yourself (or via subagents),
exactly as a human-quality annotator would.

Setup:
- Read `LABELING_SPEC_GENERAL.md` — it defines the 52 allowed abilities, the weighting
  (1/2/3), the uncertain flag, and how to handle manual/physical vs cognitive tasks.
- Read `manifest.json` — it lists all 118 chunks (soc, chunk, input path, output path).
- A chunk is ALREADY DONE if its output CSV exists under `partial_output/`. There are 47
  done; skip those. The remaining ~71 are your work.

For each remaining chunk (its output CSV does NOT yet exist):
1. Read the input file `chunks/socNN/chunk_XX.json` (a JSON array of tasks).
2. For EVERY task, choose the abilities it genuinely invokes — typically 3–7 — each with
   a weight (1=mild, 2=moderate, 3=critical) and uncertain (0/1). Use ONLY the 52 exact
   ability names from the spec. Manual/physical tasks MUST get physical/psychomotor/sensory
   abilities (strength, dexterity, coordination, vision); cognitive/clerical tasks stay
   cognitive. Do not under-label physical work.
3. Write the output CSV to `partial_output/socNN_out/chunk_XX.csv` with header
   `task_id,occupation,task_text,ability_name,weight,uncertain` — one row per (task,
   ability). Preserve task_id/occupation/task_text exactly; CSV-quote fields with commas.
4. Verify before moving on: every input task_id appears, all ability names are in the
   52-list, weights are 1–3.

Use Sonnet. Spawn parallel subagents (one per chunk) — run up to 10 chunks concurrently
at a time, and as each finishes start the next, until all remaining chunks are done. Keep
every subagent on Sonnet, not Opus or Haiku. Process the manual/physical groups (SOC 33,
35, 37, 39, 45, 47, 49, 51, 53) with the same care as the cognitive ones.

When all 118 chunks have output CSVs, run:  python3 merge_validate.py
and show me its summary. I want to see "ALL TASKS LABELED", 0 invalid abilities, and the
mean abilities/task. Report progress as you go so I can confirm it is working.
```

---

## What you'll see confirming it works

- Claude reports each chunk as it finishes: e.g. *"soc51 chunk 00 → 130 tasks, 812 rows."*
- New CSVs appear under `partial_output/socNN_out/`.
- At the end, `merge_validate.py` prints `ALL TASKS LABELED`, `Invalid ability names: 0`,
  and a mean of ~5–6 abilities/task.

## Notes

- **Resumable:** if you stop and restart, Claude skips every chunk that already has a CSV,
  so you only ever do the unfinished ones. To force a redo, delete that chunk's CSV.
- **Model:** must stay on **Sonnet** to match the method used for the frozen mappings and
  the 47 chunks already done.
- **Frozen data untouched:** this only creates NEW mappings for the missing SOC groups.
  `../data/task_ability_mapping.csv` is never modified.
