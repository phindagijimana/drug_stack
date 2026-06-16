# Reproducibility checklist

> Ten items. If you cannot check all ten, your analysis is not reproducible.

For any analysis you intend to share, publish, or use in a regulatory submission:

- [ ] **Data version pinned.** Exact Iceberg / Delta snapshot ID, ChEMBL release, internal-DB timestamp.
- [ ] **Code version pinned.** Git commit SHA, no `main` references.
- [ ] **Environment pinned.** Conda lockfile + pip lockfile committed; or a Docker image hash.
- [ ] **Random seeds set.** `torch.manual_seed`, `numpy.random.seed`, `random.seed`, plus any library-specific seeds (RDKit `randomSeed`).
- [ ] **Hardware noted.** GPU model, CUDA version, BLAS variant.
- [ ] **Splits documented.** Scaffold / time / cluster split, with split-defining code committed.
- [ ] **Calibration documented.** What calibration set, what calibrator.
- [ ] **Metrics with CIs.** Bootstrapped 95% CIs on every reported number.
- [ ] **Failure modes documented.** What the model does on OOD inputs.
- [ ] **Run logs archived.** Inputs, outputs, code version, env, timestamps stored, queryable.

If all ten are checked, the analysis is reproducible to within stochastic noise.

## Why this matters

- **A QSAR model in a paper without these is unverifiable.**
- **An IND-supporting in-silico analysis without these is non-compliant.**
- **A regulatory audit asking "what produced this number?" needs all ten to answer.**

## Common excuses (and rebuttals)

- "It's just exploratory work." — exploratory work that becomes important inherits the choices made when nobody was looking.
- "Pinning data is hard." — Iceberg / Delta snapshots make it free.
- "Pinning env is too restrictive." — lock files do not prevent upgrades; they capture *this* result.
- "Seeds don't matter." — they matter every time someone tries to reproduce a borderline result.

## In practice

- **Adopt the checklist as a PR template** for analytical work.
- **Make CI enforce items 1–4** automatically: refuse to merge code without a lockfile and a tagged data version.
- **Periodically replay** old analyses end-to-end. If they don't reproduce, fix the gap.

## A one-page provenance record

For every analysis report:

```yaml
analysis:
  title:        "QSAR for kinase X, scaffold-split eval"
  date:         2026-05-18
  author:       "researcher@example.org"
data:
  table:        "lakehouse://activities_v1"
  snapshot:     47
  chembl_release: "34"
code:
  repo:         "github.com/example/drugstack"
  commit:       "a1b2c3d4"
env:
  conda_lock:   "env.lock.yaml@a1b2c3d4"
  pip_lock:     "requirements.lock@a1b2c3d4"
  docker_image: "ghcr.io/example/drugstack@sha256:..."
hardware:
  gpu:          "A100 80GB"
  cuda:         "12.1"
seeds:
  python:       42
  numpy:        42
  torch:        42
splits:
  type:         "scaffold"
  generator:    "src/splits.py::scaffold_split"
metrics:
  scaffold_R2:  0.62  (95% CI 0.58 - 0.66)
  scaffold_RMSE: 0.81 (95% CI 0.77 - 0.85)
```

This file sits next to every report. Without it, every "reproduce my result" request becomes archaeology.
