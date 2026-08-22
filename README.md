# O*NET Task → Ability Mapping Dataset

A fine-grained mapping from **18,796 O\*NET work tasks** — the full O\*NET task corpus,
spanning **all 23 SOC major groups (economy-wide)** — to the **52 O\*NET human abilities**
each task requires, with a graded importance weight per (task, ability) pair.

This dataset supports task-level analysis of human ability requirements — enabling
research on automation exposure, skill demand, and human–AI task allocation at the
**task** level rather than the coarser occupation level.

> Built as the empirical foundation for the **ATES** (Agentic Task Exposure Score)
> framework. The mapping is independently useful for labor-economics and
> AI-exposure research even without the ATES model.

**Get it:** [🤗 Hugging Face](https://huggingface.co/datasets/ravishgupta/ate-task-ability-dataset) · [Zenodo (archival DOI)](https://doi.org/10.5281/zenodo.21989176) · [GitHub source](https://github.com/ravyg/ate-task-ability-dataset)

Load it programmatically from Hugging Face:

```python
from datasets import load_dataset

ds = load_dataset("ravishgupta/ate-task-ability-dataset")            # full mapping
audit = load_dataset("ravishgupta/ate-task-ability-dataset", "audit_sample")
```

> ⭐ **Find this useful?** Please **clone it and give the repo a star** — it takes one
> click, helps others discover the dataset, and lets us gauge interest to keep it
> maintained and expanded. If you use it in your work, a [citation](#citation) is the
> best thanks of all. 🙏

> ### ✅ Status: labels released · human validation **complete**
> The full task→ability mapping (**18,796 tasks — economy-wide, all 23 SOC major
> groups**) is **available today**. Labels were produced by a large language model
> (**Claude Sonnet**) against the O\*NET taxonomy, using one consistent method across
> all groups. **Independent human validation is complete:** three annotators each
> re-annotated all **200 audit-sample tasks** and **endorsed 98.9%** of the
> LLM-proposed abilities (3,334 / 3,370, 36 rejections). The validation sample was
> drawn from the initial six-group release; the expanded groups were labeled by the
> identical Sonnet method. Full breakdown, method, and scope in
> [`validation/`](validation/).

---

## What's here

| File | Description |
|------|-------------|
| `data/task_ability_mapping.csv` | **Main dataset** — 95,330 (task, ability) rows over 18,796 tasks |
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

**Coverage:** 18,796 tasks · 95,330 mappings · avg 5.07 abilities/task.
**Weight distribution:** 1 → 22.4% · 2 → 57.1% · 3 → 20.5%.
**Uncertain:** 1,521 rows (1.6%) across 1,232 tasks.

---

## How it was built (short version)

1. **LLM pass** — each task labeled with its required abilities + weights against the
   52-ability O\*NET taxonomy (model: **Claude Sonnet**), cross-checked against the
   O\*NET GWA (Generalized Work Activities) chain baseline.
2. **Human validation** *(complete)* — a 200-task stratified sample (all
   uncertain-flagged tasks + random draw, seed 42) was independently re-annotated by
   **three annotators**, each reviewing all 200 tasks.
3. **Agreement** — human-vs-model endorsement reached **98.9%** (3,334 / 3,370
   LLM-proposed abilities endorsed across the three annotators); a **pilot of 100 tasks
   reached κ = 0.81** ("almost perfect"). Full results in [`validation/`](validation/).

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

### Citing the dataset

The dataset is archived on Zenodo with a DOI (concept DOI, always resolves to the latest version):

**DOI:** [10.5281/zenodo.21989176](https://doi.org/10.5281/zenodo.21989176)

```bibtex
@misc{gupta2026onetdataset,
  author    = {Gupta, Ravish and Kumar, Saket},
  title     = {{O*NET} Task-to-Ability Mapping Dataset},
  year      = {2026},
  publisher = {Zenodo},
  version   = {2.0.0},
  doi       = {10.5281/zenodo.21989176},
  url       = {https://doi.org/10.5281/zenodo.21989176}
}
```

See also `CITATION.cff`.

## Acknowledgements

**Special thanks to our annotators — Ravish Gupta, Saket Kumar, Maulik, and Aaryan
Gupta** — whose independent expert re-annotation of the 200-task validation sample made
the quality assessment of this dataset possible. Their careful judgments on task→ability
requirements are the backbone of its reliability.

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

- **Hugging Face:** [ravishgupta/ate-task-ability-dataset](https://huggingface.co/datasets/ravishgupta/ate-task-ability-dataset) — load with `datasets.load_dataset(...)`.
- **Zenodo:** [10.5281/zenodo.21989176](https://doi.org/10.5281/zenodo.21989176) — archival record + citation DOI.
- **Paper:** Gupta & Kumar (2026), *Agentic AI and Occupational Displacement*, arXiv:2604.00186.
- **ATES framework** — the model this dataset was built for *(link on paper release)*.

---

⭐ **If this dataset helped your work, please [star the repo](https://github.com/ravyg/ate-task-ability-dataset) and cite the paper.** It's the simplest way to support open research and keep this dataset growing. Thank you!
