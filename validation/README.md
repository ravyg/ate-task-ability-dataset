# Validation

Human validation of the task→ability mapping.

- `human_annotations.csv` — exported responses from the crowdsource form
  (tidy long format; one row per human judgment). **Add this once annotation
  is complete** (export the Responses tab of the Google Sheet as CSV).
- `kappa_results.md` — Cohen's κ (inter-rater + human-vs-model) and agreement tables.
- `compute_kappa.py` — script to reproduce the agreement numbers from the CSV.

Pilot (100 tasks): **κ = 0.81** ("almost perfect"). Full 200-task audit results
to be added once co-author annotation completes.
