# Methodology

How the O\*NET task→ability mapping was constructed and validated.

## 1. Source data

- **O\*NET 30.2** (U.S. Department of Labor): task statements, occupations, and the
  52-ability taxonomy (`Abilities.txt`).
- The **52 abilities** span four families: cognitive, psychomotor, physical, and
  sensory (see `data/abilities_reference.csv`).
- A **GWA (Generalized Work Activities) chain baseline** was used as a sanity anchor:
  O\*NET already links occupations→abilities and tasks→GWAs, giving a coarse prior
  for which abilities a task's occupation tends to require.

## 2. Labeling pass

Each of the 18,796 task statements (the full O\*NET corpus, 22 SOC major groups) was labeled with:
- the subset of the 52 abilities the task **requires**, and
- an importance **weight**: 1 (mild), 2 (moderate), 3 (critical).

Labels were produced by a large language model (Claude Sonnet) prompted with the
task text, its occupation, the full 52-ability taxonomy with O\*NET definitions, and
the GWA baseline prior. Low-confidence judgments were explicitly flagged
(`uncertain = 1`) rather than dropped, so reviewers can prioritize them.

Tasks were processed in chunks; all chunks were merged, de-duplicated, and sorted
by numeric `task_id` into `data/task_ability_mapping.csv`. The initial release covered
six SOC major groups (4,577 tasks); the dataset was subsequently extended to the full
O\*NET corpus (18,796 tasks, 22 SOC major groups) using the identical Sonnet method
— a pure append that left the original rows unchanged. The regeneration pipeline is in
[`scripts/`](../scripts/).

## 3. Validation

### Sample
A **200-task stratified sample** (`data/audit_sample_200.csv`) was drawn:
- **all** uncertain-flagged tasks in the sample window, plus
- a random draw to reach 200 (seed = 42) for representativeness.

### Human re-annotation
Domain experts independently re-annotated the sample using a purpose-built web form
(`crowdsource/`). For each task they marked every model-assigned ability as
agree / wrong-weight / wrong, and could add missed abilities. Each judgment is stored
fully attributed (annotator, timestamp, session) in a tidy long format so aggregation
decisions (whose labels, majority vote, union of additions) are deferred, not baked in.

### Agreement metric
**Cohen's κ** quantifies agreement beyond chance:

    κ = (Po − Pe) / (1 − Pe)

where Po is observed agreement and Pe is chance agreement. A pilot of 100 tasks
reached **κ = 0.81** ("almost perfect"). Full audit results are in `validation/`.

## 4. Known limitations

- Weights are ordinal (1–3), not calibrated cardinal magnitudes.
- Ability requirements are derived from task *text*; context not in the statement
  (tools, setting) is not modeled.
- 1.6% of rows are `uncertain`-flagged; treat those with care or filter them out.
- SOC-55 (Military Specific Occupations) is not covered. O\*NET lists 19 military
  occupations; none appear here.
- Coverage is the U.S. O\*NET taxonomy; cross-country transfer is untested here.
