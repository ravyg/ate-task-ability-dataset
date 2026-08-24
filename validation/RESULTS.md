# Human Validation of the Task→Ability Mapping

## Result (headline)

The task→ability labels were produced by a large language model (**Claude Sonnet**)
against the O\*NET taxonomy (see [`docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)). To
validate them, **three annotators** independently re-annotated the 200-task audit
sample. Two covered all 200 tasks; the third covered 187.

Across the three, **93.9% of LLM-proposed abilities were kept at the weight the
model assigned**, and **99.1% were kept in some form**, counting abilities that were
retained but re-weighted. **30 were rejected** outright.

| Metric | Value |
|--------|-------|
| Annotators | 3 |
| Tasks reviewed | 200, 200 and 187 |
| LLM-proposed abilities judged | 3,159 |
| Kept at the model's weight | **2,966 (93.9%)** |
| Kept but re-weighted | 163 (5.2%) |
| Kept in some form | **3,129 (99.1%)** |
| Rejected | 30 (0.9%) |
| Abilities added by annotators | 219 |

Figures are recomputed from the raw annotations under the cleaning rules in
`compute_all.py`, which keeps one authoritative session per annotator and discards
superseded sessions.

## Which number to quote

**Two definitions are in circulation and they differ by five points.** State which
one you mean.

- **93.9%** counts only abilities kept at the model's own weight. This is the
  stricter reading and the one to use when the claim is that the model's output is
  correct as produced.
- **99.1%** also counts abilities the annotator kept but re-weighted. Use this when
  the claim is about whether the ability belongs to the task at all, setting aside
  how important it is.

Both are precision claims about what the model proposed. Neither says anything about
what it missed.

## Per-annotator breakdown

Review depth varied substantially, so the pooled rate is worth reading alongside the
individual columns rather than on its own.

| Annotator | Tasks | Proposals | Kept at weight | Re-weighted | Rejected | Added | Edits per task |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 200 | 1,079 | 991 (91.8%) | 61 | 27 | 163 | 1.25 |
| 2 | 200 | 1,079 | 993 (92.0%) | 83 | 3 | 55 | 0.70 |
| 3 | 187 | 1,001 | 982 (98.1%) | 19 | 0 | 1 | 0.11 |

The third annotator used a form that pre-filled the model's answer, and their edit
volume is roughly a tenth of the first annotator's. A high keep rate from a reviewer
who rarely edits is weaker evidence than the same rate from one who edits often, so
the pooled figure is somewhat flattered by that column. The reliability analysis in
`ate-framework-experiments/task_level_cap/` carries the full diagnostics.

## Inter-rater agreement

Raw Cohen's κ is near zero or slightly negative for every pair, which is the
expected artifact when one category holds 91 to 97 percent of the mass. PABAK is the
appropriate statistic here.

| Pair | Presence PABAK | Weight κ |
|---|---:|---:|
| Annotator 1 × 2 | 0.640 | 0.792 |
| Annotator 1 × 3 | 0.694 | 0.886 |
| Annotator 2 × 3 | 0.899 | 0.859 |

Across all three simultaneously, Krippendorff's α is **0.391** on presence and
**0.847** on the ordinal weight scale. The presence figure sits below the 0.667
tentative threshold, which follows directly from the differing edit volumes above.

## Known coverage gap (recall)

Annotators added **219 abilities the model omitted**, concentrated in Cognitive
(Mathematical Reasoning, Information Ordering, Number Facility) and in hands-on
Psychomotor and Physical abilities. The released mapping is high precision with a
documented tendency to under-list. Closing that gap is future work, see
[`FUTURE_WORK_prompt_refinement.md`](FUTURE_WORK_prompt_refinement.md).

## Method (brief)

- **Instrument:** a structured intake form (grouped by occupation); each annotator reviewed every LLM-proposed ability and its weight, keeping / re-weighting / removing it, and adding any missing ability, then gave an overall per-task rating.
- **Independence:** each annotator worked alone through their own form and could not see any other annotator's entries; the individual responses were compiled only afterward from the shared response sheet. No annotation was influenced by another annotator's judgment.
- **Reproducibility:** `experiments/task_level_cap/compute_all.py` regenerates every number here from the raw export in `experiments/task_level_cap/data/`.
- **Data cleaning (documented, applied to the released files).** A small set of LLM-generated label/weight artifacts, where an uncertainty `?` had leaked into a value string, were canonicalized so that `ability_name` contains exactly the **52 O\*NET abilities**: (a) a trailing `?` stripped from 45 ability labels (e.g. `Mathematical Reasoning?`→`Mathematical Reasoning`), with those rows marked `uncertain=1`; (b) one casing typo (`Problem sensitivity`→`Problem Sensitivity`) canonicalized; (c) one out-of-taxonomy label (`Persuasion`, an O\*NET *Skill*, not one of the 52 Abilities) removed. In `audit_sample_200.csv`, 33 weights recorded as `1?` were corrected to `1` and flagged `uncertain=1`. Net effect on the main dataset: 95,331→**95,330 rows**, 65→**52 distinct abilities**; no annotator verdict changed.

## Scope note

The headline figures pool three annotators (Ravish Gupta, Saket Kumar, Maulik). Two reviewed all 200 audit tasks; the third reviewed 187. A fourth annotator, **Aaryan Gupta**, reviewed a partial set (64 tasks) as an additional robustness check and is not included in the headline figures.

## Acknowledgments

We thank **Saket Kumar**, **Maulik**, and **Aaryan Gupta** for their independent expert annotation of the validation sample.
