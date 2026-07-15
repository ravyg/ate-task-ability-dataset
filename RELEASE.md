# Release Checklist

The steps to take this dataset from **private / pre-submission** to a **public,
permanently-archived, citable release** — to run once, when the paper is ready.

> ⚠️ **Do NOT run this before you're ready.** Making the repo public and minting a
> Zenodo DOI are effectively **irreversible** (a DOI cannot be deleted). Because of
> the paper's **blind-review** considerations, keep everything private until the
> paper is submitted/accepted and de-anonymized.

---

## Phase 0 — Pre-flight (data must be final)

- [ ] Annotation drive complete (co-authors + any volunteers).
- [ ] `validation/human_annotations.csv` exported from the Google Sheet and committed.
- [ ] `validation/kappa_results.md` computed and committed (Cohen's κ, agreement tables).
- [ ] `compute_kappa.py` committed and reproducible from the CSV.
- [ ] Spot-check `data/task_ability_mapping.csv`: 24,796 rows, 4,577 unique tasks,
      no stray `?` in `weight`, `uncertain` is 0/1.
- [ ] All docs current: `README.md`, `docs/SCHEMA.md`, `docs/METHODOLOGY.md`.

## Phase 1 — Credit & metadata

- [ ] Uncomment and finalize the **annotator names** in the README Acknowledgements
      (the `<!-- TBD ... -->` block). Confirm each person consents to being named
      (or mark anonymous on request).
- [ ] Add ORCIDs in `CITATION.cff` (Ravish, Saket) — leave blank if none.
- [ ] Confirm the paper citation / arXiv ID is final in README + `CITATION.cff`.
- [ ] Update the version number if changed (README, `CITATION.cff` → `version:`).

## Phase 2 — Go public

- [ ] Final review that **no private/unpublished framework code or credentials**
      leak in (`crowdsource/` has no secrets; `.clasp.json` is gitignored).
- [ ] Flip the repo public:
      ```bash
      gh repo edit ravyg/ate-task-ability-dataset --visibility public --accept-visibility-change-consequences
      ```
- [ ] Add repo topics for discoverability:
      ```bash
      gh repo edit ravyg/ate-task-ability-dataset \
        --add-topic onet --add-topic labor-economics --add-topic automation \
        --add-topic dataset --add-topic ai-and-work --add-topic task-analysis
      ```

## Phase 3 — Tag a versioned release

- [ ] Tag and push `v1.0.0`:
      ```bash
      git tag -a v1.0.0 -m "O*NET Task→Ability Mapping Dataset v1.0.0"
      git push origin v1.0.0
      ```
- [ ] Create the GitHub Release (this is what Zenodo snapshots):
      ```bash
      gh release create v1.0.0 \
        --title "O*NET Task→Ability Mapping Dataset v1.0.0" \
        --notes "First public release: 24,796 (task, ability) mappings over 4,577 O*NET tasks, human-validated (Cohen's κ). See README."
      ```

## Phase 4 — Mint the Zenodo DOI

- [ ] Log in at <https://zenodo.org> with the GitHub account (`ravyg`).
- [ ] **Settings → GitHub** → toggle **ON** for `ate-task-ability-dataset`.
      (Must be done **before** the release for auto-capture; if the release already
      exists, cut a `v1.0.1` release to trigger it.)
- [ ] Zenodo auto-creates a deposit from the release and mints a DOI.
- [ ] On the Zenodo record, confirm it reads from `CITATION.cff` (authors, title,
      CC-BY-4.0) and that **"cite the paper"** intent is clear in the description.
- [ ] Grab the DOI (e.g. `10.5281/zenodo.XXXXXXX`).

## Phase 5 — Wire the DOI back in

- [ ] Add the Zenodo DOI badge to the top of `README.md`:
      ```markdown
      [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
      ```
- [ ] Add a line under Citation: *"Data permanently archived at Zenodo
      (DOI: 10.5281/zenodo.XXXXXXX); please cite the paper above."*
- [ ] Put the **DOI into the paper's** Data Availability / supplement section.
- [ ] Commit + push the README update.

## Phase 6 — Announce

- [ ] Cross-link: add a pointer to this dataset (+ DOI) in the `ate-framework` README.
- [ ] Update `MEMORY.md` / project notes with the final DOI and public URL.
- [ ] Share the star/clone request (LinkedIn, personal site, co-authors) now that
      the repo is public and stars actually count.

---

### Rollback note
You **can** flip the repo back to private (`gh repo edit ... --visibility private`),
but you **cannot** un-mint a Zenodo DOI — only publish a new version. So treat
**Phase 4 as the point of no return** and be sure the data is final before it.
