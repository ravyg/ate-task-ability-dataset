# Human Validation of the Task→Ability Mapping

## Result (headline)

Two independent annotators — **Ravish Gupta** and **Maulik** — reviewed **all 200 audited task→ability mappings** and **endorsed 98.5% of the LLM-proposed abilities** (2,193 / 2,227), with 34 rejections. This establishes **high fidelity of the Claude-generated task→ability mapping** used in the ATES framework.

| Annotator | Tasks | LLM-proposed abilities judged | Endorsed | Rejected |
|-----------|-------|-------------------------------|----------|----------|
| Ravish Gupta | 200 | 1,078 | **97.5%** | 27 |
| Maulik | 200 | 1,149 | **99.4%** | 7 |
| **Pooled** | **200** | **2,227** | **98.5%** | **34** |

## What the number means (and its scope)

- **98.5% is a *precision* claim:** of the abilities the LLM proposed for a task, human reviewers agreed 98.5% genuinely belong. This is the basis for using the original LLM mapping in downstream ATES exposure calculations with high confidence.
- **Known coverage gap (recall):** annotators also *added* **228 abilities the LLM omitted**, concentrated in **Cognitive** (119; e.g., Mathematical Reasoning, Information Ordering, Number Facility) and hands-on **Psychomotor/Physical** abilities. The released mapping is therefore high-precision with a documented tendency to under-list; closing this gap is the subject of planned future work (see `FUTURE_WORK_prompt_refinement.md`).

## Method (brief)

- **Instrument:** the grouped-by-occupation annotation tool; annotators reviewed each LLM-proposed ability and its weight, keeping / re-weighting / removing it, and adding any missing ability, then gave an overall per-task rating.
- **Independence:** annotators worked separately and did not compare judgments.
- **Reproducibility:** `experiments/task_level_cap/compute_all.py` regenerates every number here from the raw export in `experiments/task_level_cap/data/`.
- **Data cleaning (documented, non-destructive):** one casing typo (`Problem sensitivity`→`Problem Sensitivity`) canonicalized; one out-of-taxonomy label (`Persuasion`, an O*NET *Skill*, not one of the 52 Abilities) excluded.

## Reporting note

The **98.5% validation figure is reported for the two annotators who independently reviewed the full 200-task set (Ravish Gupta, Maulik).** Additional annotators contributed to broader coverage and robustness checks and are credited below, but are not included in the headline two-rater figure.

## Acknowledgments

We thank **Maulik**, **Saket Kumar**, and **Aaryan Gupta** for their annotation work on the task→ability audit set. Their independent review made this validation possible.
