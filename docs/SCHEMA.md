# Schema

## `data/task_ability_mapping.csv` (main dataset)

One row per (task, ability) requirement. 95,330 rows.

| Column | Type | Notes |
|--------|------|-------|
| `task_id` | int | O\*NET task identifier. 18,796 distinct values. |
| `occupation` | string | O\*NET occupation title the task belongs to. |
| `task_text` | string | Full O\*NET task statement. |
| `ability_name` | string | One of the 52 O\*NET abilities (see `abilities_reference.csv`). |
| `weight` | int (1–3) | 1 = mild, 2 = moderate, 3 = critical requirement. |
| `uncertain` | int (0/1) | 1 = annotation flagged low-confidence. |

A `task_id` appears in as many rows as it has required abilities (avg 5.07).

## `data/abilities_reference.csv`

| Column | Type | Notes |
|--------|------|-------|
| `ability_name` | string | Canonical O\*NET ability name. |
| `category` | string | cognitive · psychomotor · physical · sensory. |

52 rows.

## `data/audit_sample_200.csv` (validation sample)

| Column | Type | Notes |
|--------|------|-------|
| `task_id` | int | Task in the 200-task audit sample. |
| `occupation` | string | Occupation title. |
| `task_text` | string | Task statement. |
| `ability_name` | string | Model-assigned ability. |
| `weight` | int/str | Model-assigned weight (may carry a `?` uncertainty marker). |
| `uncertain` | 0/1 | Whether this row was uncertainty-flagged. |

## `validation/human_annotations.csv` (collected labels)

Tidy long format — one row per human judgment:

| Column | Notes |
|--------|-------|
| `timestamp` | Submission time. |
| `annotator` / `annotator_email` | Who labeled it. |
| `session_id` | Stable per-annotator id (enables per-rater filtering). |
| `task_id` / `occupation` / `task_text` | The task judged. |
| `ability_name` | Ability being judged. |
| `llm_weight` | Model's original weight. |
| `human_judgment` | agree / wrong-weight / wrong. |
| `corrected_weight` | Human's corrected weight (if any). |
| `is_addition` | 1 if the human added an ability the model missed. |
| `overall_task_rating` | Overall 👍/👌/👎 for the task. |
| `comment` | Free-text note. |

## Known inconsistency between the two released files

`data/audit_sample_200.csv` and `data/task_ability_mapping.csv` agree on every
`weight`, `occupation` and `task_text` across all 1,078 shared (task, ability) pairs,
but they disagree on `uncertain` for **213 rows over 46 tasks**. The disagreement is
one-way: the audit file marks 1 where the mapping marks 0, never the reverse. Totals
over those 200 tasks are 291 flagged rows in the audit file against 78 in the mapping.

The documented cleanup accounts for 33 of these, where a weight recorded as `1?` was
corrected to `1` and flagged. The remaining 180 predate it and are unexplained.

Treat `task_ability_mapping.csv` as authoritative for the released mapping. If you are
filtering on `uncertain`, filter against that file rather than the audit sample.

