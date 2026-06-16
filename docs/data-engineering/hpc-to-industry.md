# HPC → industry

> Bridging academic-HPC habits to industrial drug-discovery data engineering. What translates and what doesn't.

Many drug-discovery computational scientists arrive from an academic HPC background — Slurm, Singularity, shared filesystems, conda environments stored in `$HOME`. Industry pipelines look different. This chapter is the translation guide.

## What transfers

- **Familiarity with batch scheduling.** Airflow / Prefect look complicated but their mental model is "submit jobs with dependencies".
- **Bash + scripting.** Still the lingua franca of pipelines.
- **Reproducibility instincts.** Pinning seeds, versioning data — the habit translates.
- **Comfort with text files.** YAML, JSON, Parquet all behave like the files you already wrangle.

## What changes

- **Mutable shared filesystems → immutable object stores.** S3 / GCS instead of `/scratch/$USER`. No `rm -rf` to fix a bug; you version instead.
- **Conda envs on a shared cluster → containers.** Docker / Apptainer images shipped via a registry. The environment is part of the artefact.
- **`sbatch` jobs → DAGs.** A pipeline is no longer 30 sbatch scripts; it is a DAG the orchestrator manages.
- **No CI → mandatory CI.** Every change goes through tests before reaching the lake.
- **Loose data → strict schemas.** `.tsv` files with named columns from "whoever wrote them" become typed Parquet tables.
- **One model in a notebook → many models in a registry.** Versioning is non-optional.

## Mistakes academic-HPC people make

- **Writing pipelines that only run on one cluster.** Hard-coded paths, scheduler-specific syntax.
- **Storing raw data in `$HOME`** with no versioning. When the disk fills, history evaporates.
- **Mutating "the" CSV in place** instead of writing new tables.
- **Notebook-only workflows** that cannot be run programmatically.
- **No tests.** Justified as "research code" until research code lands in a clinical analysis.
- **`pickle.dump(model, "/scratch/model.pkl")`** with no env lock.

Each of these is invisible in a single-PI lab and catastrophic in a 50-person team.

## Survival skills to develop

- **Containerise.** Even a Dockerfile that lists `pip install` lines is leagues ahead of "follow these README steps".
- **Adopt git LFS or DVC.** Don't commit Parquet files; do version them.
- **Move from CSV to Parquet.** Smaller, faster, typed.
- **Adopt a small orchestrator.** Even `Snakefile` is enough to formalise dependencies.
- **Write at least one test per pipeline.** A pipeline with one test is fundamentally different from one with zero.

## What industry can learn from HPC

The HPC world is unusually good at:

- **Reproducibility-by-convention** — module systems, Slurm provenance.
- **Cost awareness** — every job has a wall-clock cost.
- **Numerical care** — bit-exact reproducibility across nodes.
- **Long-running computations** — MD, FEP, QM all live there natively.

Industrial drug-discovery teams that hire HPC-experienced engineers often get sharper numerical-correctness instincts than typical SaaS teams.

## In practice

- **The transition takes 3–6 months.** Habits are hard; the payoff is large.
- **Pair HPC-trained scientists with industry-trained engineers.** They teach each other; both teams become better.
- **The DAG mental model is the load-bearing translation step.** Once "DAGs not Slurm scripts" clicks, the rest follows.

## Where to next

[Computing](../computing/index.md) — the environment side of the same story.
