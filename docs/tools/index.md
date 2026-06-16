# Tools landscape

> Opinionated map of the cheminformatics, structure, screening, and ML tools you'll meet. Pointers, not exhaustive lists.

## Cheminformatics

- **RDKit** (open) — the default. Everything else fits around it.
- **OpenBabel** (open) — file conversion, format glue.
- **OEChem / OEDepict / OMEGA** (OpenEye, commercial) — strong in industry, esp. conformer generation.
- **Schrödinger Maestro / Phase / FEP+** — industrial commercial suite.
- **MOE** (CCG) — academic / industrial.

## Visualisation

- **PyMOL** (open + paid) — 3D structures.
- **ChimeraX** (open) — modern structural visualisation.
- **VMD** (open) — MD trajectories.
- **NGLView / py3Dmol** — notebooks.
- **mols2grid** — interactive molecule grids.

## Docking

- **AutoDock Vina** (open) — workhorse.
- **gnina** (open) — Vina + ML scoring.
- **rDock** (open) — fast.
- **Glide** (commercial) — gold-standard industrial.
- **GOLD** (CCDC, commercial).
- **DiffDock, EquiBind, Boltz, Chai-1** (open) — ML / diffusion dockers.

## Structure prediction

- **AlphaFold 2 / 3** — DeepMind / Isomorphic.
- **ESMFold** (open) — Meta / ESM.
- **Boltz-1, Boltz-2** (open).
- **Chai-1** (open).
- **RoseTTAFold / RFdiffusion / RFdock** (Baker lab).

## MD

- **OpenMM, GROMACS, AMBER, NAMD** — open.
- **Schrödinger Desmond** — commercial.

## ML / DL

- **PyTorch** — default.
- **Chemprop** — message-passing.
- **DeepChem** — broader DL.
- **ESM** — protein LMs.
- **REINVENT 4** — generative chemistry.
- **AiZynthFinder** — retrosynthesis.

## ADMET

- **ADMET-AI** — Chemprop-based commodity predictor.
- **DeepTox, Toxtree, VEGA** — toxicity-specific.
- **Simcyp, GastroPlus, PK-Sim** — PBPK (commercial).

## Workflow / DE

- **Airflow, Prefect, Dagster** — DAG orchestrators.
- **Snakemake, Nextflow** — bioinformatics-friendly.
- **MLflow, Weights & Biases** — experiment tracking.
- **DuckDB, Polars** — laptop-scale data.
- **Iceberg, Delta Lake** — table formats.

## In practice

- **Standardise per team.** A team that uses RDKit + Chemprop + Vina + OpenMM + REINVENT covers 90% of small-molecule needs.
- **Commercial tools earn their keep** when functionality is decisive (FEP+, Glide); otherwise open-source is the right default.
- **Watch the AF3 / Boltz space.** Open-source biomolecular generalists are the most rapid-moving tool category in 2025.
