# O*NET Task → Ability Mapping Dataset

A fine-grained mapping from **4,577 O\*NET work tasks** to the **52 O\*NET human abilities**
each task requires, with a graded importance weight per (task, ability) pair.

This dataset supports task-level analysis of human ability requirements — enabling
research on automation exposure, skill demand, and human–AI task allocation at the
**task** level rather than the coarser occupation level.

> Built as the empirical foundation for the **ATES** (Agentic Task Exposure Score)
> framework. The mapping is independently useful for labor-economics and
> AI-exposure research even without the ATES model.

---

## What's here

| File | Description |
|------|-------------|
| `data/task_ability_mapping.csv` | **Main dataset** — 24,796 (task, ability) rows over 4,577 tasks |
| `data/abilities_reference.csv` | The 52 O\*NET abilities and their category |
| `data/audit_sample_200.csv` | 200-task stratified validation sample (human re-annotation) |
| `validation/` | Human annotations + inter-rater agreement (Cohen's κ) |
| `crowdsource/` | The web form used to collect human validation labels |
| `docs/METHODOLOGY.md` | How the mapping was built and validated |
| `docs/SCHEMA.md` | Column-by-column schema |

---

## Main dataset schema

`data/task_ability_mapping.csv` — one row per (task, ability) requirement:

| Column | Type | Description |
|--------|------|-------------|
| `task_id` | int | O\*NET task identifier |
| `occupation` | string | O\*NET occupation title the task belongs to |
| `task_text` | string | Full task statement |
| `ability_name` | string | One of the 52 O\*NET abilities |
| `weight` | int | Importance: **1** = mild, **2** = moderate, **3** = critical |
| `uncertain` | 0/1 | 1 if the annotation was flagged low-confidence |

**Coverage:** 4,577 tasks · 24,796 mappings · avg 5.4 abilities/task.
**Weight distribution:** 1 → 12.9% · 2 → 63.5% · 3 → 23.7%.
**Uncertain:** 869 rows (3.5%) across 687 tasks.

---

## How it was built (short version)

1. **LLM pass** — each task labeled with its required abilities + weights against the
   52-ability O\*NET taxonomy, cross-checked against the O\*NET GWA (Generalized Work
   Activities) chain baseline.
2. **Human validation** — a 200-task stratified sample (all uncertain-flagged tasks +
   random draw, seed 42) was independently re-annotated by domain experts.
3. **Agreement** — inter-rater and human-vs-model agreement reported as Cohen's κ in
   `validation/` (pilot κ = 0.81, "almost perfect").

Full protocol: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

---

## Source & license

- **Source taxonomy:** [O\*NET 30.2](https://www.onetcenter.org/database.html)
  (U.S. Department of Labor, public domain).
- **This dataset:** licensed **CC-BY-4.0** — free to use with attribution.

## Citation

If you use this dataset, please cite the accompanying paper. Copy-paste in your
preferred style:

**APA**
```
Gupta, R., & Kumar, S. (2026). Agentic AI and Occupational Displacement: A Multi-Regional Task Exposure Analysis of Emerging Labor Market Disruption. arXiv preprint arXiv:2604.00186.
```

**MLA**
```
Gupta, Ravish, and Saket Kumar. "Agentic AI and Occupational Displacement: A Multi-Regional Task Exposure Analysis of Emerging Labor Market Disruption." arXiv preprint arXiv:2604.00186 (2026).
```

**Chicago**
```
Gupta, Ravish, and Saket Kumar. "Agentic AI and Occupational Displacement: A Multi-Regional Task Exposure Analysis of Emerging Labor Market Disruption." arXiv preprint arXiv:2604.00186 (2026).
```

**Harvard**
```
Gupta, R. and Kumar, S., 2026. Agentic AI and Occupational Displacement: A Multi-Regional Task Exposure Analysis of Emerging Labor Market Disruption. arXiv preprint arXiv:2604.00186.
```

**Vancouver**
```
Gupta R, Kumar S. Agentic AI and Occupational Displacement: A Multi-Regional Task Exposure Analysis of Emerging Labor Market Disruption. arXiv preprint arXiv:2604.00186. 2026 Mar 31.
```

**BibTeX**
```bibtex
@article{gupta2026agentic,
  title   = {Agentic AI and Occupational Displacement: A Multi-Regional Task Exposure Analysis of Emerging Labor Market Disruption},
  author  = {Gupta, Ravish and Kumar, Saket},
  journal = {arXiv preprint arXiv:2604.00186},
  year    = {2026}
}
```

To cite the **dataset** specifically, see `CITATION.cff`.

## Acknowledgements

**Special thanks to our annotators** *(TBD — names to be added on publication)*, whose
independent expert re-annotation of the validation sample made the quality assessment
(Cohen's κ) of this dataset possible. Their careful judgments on task→ability
requirements are the backbone of its reliability.

<!-- TBD: add annotator names/affiliations once validation completes, e.g.
- Ravish Gupta
- Saket ...
- Maulik ...
- Akriti ...
-->

### 🙋 Want your name here? Become an annotator

This dataset gets better with more human eyes — and we credit every contributor.
If you'd like to help validate task→ability labels (it takes ~15 minutes, no special
background needed) **your name will be listed in the Acknowledgements of this dataset
and its accompanying paper.**

It's a simple, citable way to contribute to open research on AI and the future of work —
something concrete to point to on your CV, LinkedIn, or Google Scholar.

👉 **Interested? Reach out:** [ravishgupta.me/#contact](https://ravishgupta.me/index.html#contact)

Tell us roughly how many tasks you'd like to annotate and we'll send you a link.
Every verified contributor is acknowledged by name (or kept anonymous on request).

## Related

- **Paper:** Gupta & Kumar (2026), *Agentic AI and Occupational Displacement*, arXiv:2604.00186.
- **ATES framework** — the model this dataset was built for *(link on paper release)*.
