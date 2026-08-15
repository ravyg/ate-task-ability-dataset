# Human Validation of the Task→Ability Mapping

## Result (headline)

The task→ability labels were produced by a large language model (**Claude Sonnet**)
against the O\*NET taxonomy (see [`docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)). To
validate them, **three independent annotators** each reviewed **all 200 audited
task→ability mappings**. Across the three, **98.9% of the LLM-proposed abilities were
endorsed** (3,334 / 3,370), with 36 rejections. This establishes **high fidelity of the
Claude-generated task→ability mapping** used in the ATES framework.

| Metric | Value |
|--------|-------|
| Independent annotators | 3 |
| Tasks reviewed (each annotator) | 200 |
| LLM-proposed abilities judged (total) | 3,370 |
| Endorsed | **3,334 (98.9%)** |
| Rejected | 36 |

## What the number means (and its scope)

- **98.9% is a *precision* claim:** of the abilities the LLM proposed for a task, human reviewers agreed 98.9% genuinely belong. This is the basis for using the original LLM mapping in downstream ATES exposure calculations with high confidence.
- **"Endorsed"** counts abilities the reviewer kept as belonging to the task (including abilities kept but re-weighted); **"Rejected"** counts abilities marked as not belonging.
- **Known coverage gap (recall):** annotators also *added* **253 abilities the LLM omitted**, concentrated in **Cognitive** (e.g., Mathematical Reasoning, Information Ordering, Number Facility) and hands-on **Psychomotor/Physical** abilities. The released mapping is therefore high-precision with a documented tendency to under-list; closing this gap is the subject of planned future work (see `FUTURE_WORK_prompt_refinement.md`).

## Method (brief)

- **Instrument:** a structured intake form (grouped by occupation); each annotator reviewed every LLM-proposed ability and its weight, keeping / re-weighting / removing it, and adding any missing ability, then gave an overall per-task rating.
- **Independence:** each annotator worked alone through their own form and could not see any other annotator's entries; the individual responses were compiled only afterward from the shared response sheet. No annotation was influenced by another annotator's judgment.
- **Reproducibility:** `experiments/task_level_cap/compute_all.py` regenerates every number here from the raw export in `experiments/task_level_cap/data/`.
- **Data cleaning (documented, applied to the released files).** A small set of LLM-generated label/weight artifacts, where an uncertainty `?` had leaked into a value string, were canonicalized so that `ability_name` contains exactly the **52 O\*NET abilities**: (a) a trailing `?` stripped from 45 ability labels (e.g. `Mathematical Reasoning?`→`Mathematical Reasoning`), with those rows marked `uncertain=1`; (b) one casing typo (`Problem sensitivity`→`Problem Sensitivity`) canonicalized; (c) one out-of-taxonomy label (`Persuasion`, an O\*NET *Skill*, not one of the 52 Abilities) removed. In `audit_sample_200.csv`, 33 weights recorded as `1?` were corrected to `1` and flagged `uncertain=1`. Net effect on the main dataset: 95,331→**95,330 rows**, 65→**52 distinct abilities**; no annotator verdict changed.

## Scope note

The headline **98.9%** figure is the pooled result of the three annotators (Ravish Gupta, Saket Kumar, Maulik) who each independently reviewed the full 200-task set. A fourth annotator, **Aaryan Gupta**, reviewed a partial set (115 tasks) as an additional robustness check and is not included in the headline figure.

## Acknowledgments

We thank **Saket Kumar**, **Maulik**, and **Aaryan Gupta** for their independent expert annotation of the validation sample.
