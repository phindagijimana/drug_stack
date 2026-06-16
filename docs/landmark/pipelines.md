# Major pipelines

> The software stacks the field rests on. Open-source first; commercial where dominant.

## Cheminformatics

- **RDKit** — the cheminformatics standard. BSD-licensed.
- **OpenBabel** — file conversion, chemistry utilities.
- **chemfp, FPSim2** — billion-compound fingerprint search.

## Docking

- **AutoDock Vina** — the open-source docking baseline.
- **AutoDock-GPU / Vina-GPU** — GPU acceleration.
- **gnina** — Vina + ML scoring.
- **rDock** — fast, open, less famous than Vina.
- **Glide, GOLD, FlexX** — commercial; widely used in pharma.

## Structure prediction

- **AlphaFold 2** — original revolution.
- **AlphaFold 3** — biomolecular complex prediction (DeepMind / Isomorphic).
- **Boltz-1 / Boltz-2** — open-source AF3-class.
- **Chai-1** — open-source AF3-class.
- **ESMFold** — fast single-sequence.

## Molecular dynamics

- **OpenMM** — open-source MD engine, Python-friendly.
- **GROMACS** — open-source MD, classical HPC-friendly.
- **AMBER** — classical MD with mature force fields.
- **NAMD** — large-system MD.
- **Schrödinger Desmond** — commercial MD.

## Free energy

- **PMX** — automation around GROMACS for FEP.
- **Schrödinger FEP+** — commercial, industrial standard.
- **OpenFF + perses** — open-source FEP setup.

## QSAR / property prediction

- **Chemprop** — directed message-passing network.
- **DeepChem** — broader DL-for-chemistry toolkit.
- **scikit-learn** — classical baselines.
- **XGBoost / LightGBM** — gradient-boosted trees.

## Generative chemistry

- **REINVENT 4** — RL-based SMILES generation; the industrial workhorse.
- **MolDQN, GENTRL, JT-VAE, GraphAF** — academic landmarks.
- **DiffSBDD, Pocket2Mol, RFDiffusion / RFDock** — pocket-aware generation.

## Retrosynthesis

- **AiZynthFinder** — open-source MCTS retrosynthesis.
- **Synthia** (formerly Chematica) — commercial.
- **ASKCOS** — MIT open-source retrosynthesis.

## Protein design and biologics

- **RFdiffusion** — Baker lab structure-based diffusion.
- **ProteinMPNN** — sequence design.
- **ABodyBuilder3, IgFold, ABlooper** — antibody structure.
- **AbLang, IgLM** — antibody language models.

## ADMET / property

- **ADMET-AI** — Chemprop-based predictor.
- **ADMETlab** — web-based predictor.
- **DeepTox, Toxtree, VEGA** — toxicity-specific.

## Workflow / orchestration

- **Snakemake, Nextflow** — bioinformatics-friendly.
- **Airflow, Prefect, Dagster** — industrial DAG orchestrators.
- **Kedro** — data-pipeline framework with notebook integration.

## Lakehouse / DE

- **Delta Lake, Apache Iceberg** — open table formats.
- **DuckDB** — laptop-scale OLAP.
- **Polars** — fast DataFrame.

## In practice

- **Standardise on a small set per team.** Tool sprawl is more dangerous than choosing the "wrong" tool.
- **Open-source is the right default**; commercial only when functionality demands.
- **Watch the AlphaFold-3 class**. Open-source equivalents are catching up; pipelines should be portable.

## Where to next

[Targets, drugs, and atlases](atlases.md) — the lookup resources.
