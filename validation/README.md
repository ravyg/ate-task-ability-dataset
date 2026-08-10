# Validation

Human validation of the task→ability mapping.

## Headline result

Three independent annotators reviewed **all 200 audited task→ability mappings** and
**endorsed 98.9%** of the LLM-proposed abilities. See **[`RESULTS.md`](RESULTS.md)**
for the full breakdown, scope (precision vs. coverage), and method.

- `RESULTS.md` — the 200-task, three-annotator validation result (98.9% precision) and method.
- `FUTURE_WORK_prompt_refinement.md` — planned human-informed prompt-refinement study
  (separate paper; not yet run).

## Reproducibility & raw data

The raw human annotations (long-format CSV) and the reproduction script live with the
experiment code. **Raw exports contain annotator names/emails (PII) and are withheld until
the public release is de-identified.**

Pilot (100 tasks): **κ = 0.81** ("almost perfect"). The full 200-task audit is reported in
`RESULTS.md` as a precision figure (human-vs-model endorsement), with a documented coverage
gap (253 human-added abilities) addressed in the future-work plan.
