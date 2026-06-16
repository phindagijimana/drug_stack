# Data engineering for drug discovery

> DAGs, pipelines, idempotency, observability, testing — taught against real ChEMBL / PubChem / assay workloads.

Drug-discovery data engineering is a niche of the discipline. The general principles transfer; the specific pitfalls do not.

## Chapters

- **[Foundations](foundations.md)** — what every pipeline must do.
- **[The DAG mental model](dag.md)** — why pipelines are graphs.
- **[The five pillars](five-pillars.md)** — freshness, volume, distribution, schema, lineage.
- **[Cheminformatics pipelines](cheminformatics-pipelines.md)** — concrete ChEMBL ingestion + featurisation pipeline.
- **[Assay data pipelines](assay-data.md)** — HTS, dose-response, replicate aggregation.
- **[Lakehouse for chemistry & biology](lakehouse.md)** — schema, partitioning, file format choices.
- **[MLOps for drug discovery](mlops.md)** — model registries, retraining, drift detection.
- **[Testing pipelines](testing.md)** — golden datasets, contract tests, schema validation.
- **[HPC → industry](hpc-to-industry.md)** — bridging academic HPC habits to industrial pipelines.

## What's different about drug discovery

Three constraints that shape every choice:

1. **Compound identity is non-trivial.** SMILES are not unique. InChIKeys are. Pipelines that join on SMILES silently miscount.
2. **Assay data is noisy and biased.** Different plates, days, operators, batches; censored at the low-affinity tail; replicate counts vary. Naive aggregation produces wrong numbers.
3. **Provenance is regulatory-relevant.** Knowing which assay version produced a row matters for IND filings and FDA audits. Append-only schemas with timestamps are the default.

If you arrived here from generic data engineering, the rest of this section is a translation guide.

## Where computation usually fails

- **Joining on SMILES** without canonicalisation → miscounts.
- **Mixing CSV and Parquet** mid-pipeline → schema drift.
- **No replicate handling** → IC50 averaging across plates with different controls.
- **No domain-of-applicability gate** before ML predictions → confident OOD lies.
- **Manual ChEMBL releases** with no version tracking → reproducibility decays.
- **Pickled models without environment lock** → "works on my machine" months later.

The chapters that follow each address one of these.

## In practice

- **Parquet everywhere, InChIKey as the join key, append-only assay tables with timestamps, scaffold-aware splits.** Four rules that prevent more bugs than they cost.
- **Version control for data**, not just code (DVC, LakeFS, Pachyderm, simple git-LFS-of-parquet for small data).
- **Provenance metadata on every row** — source, version, ingested_at.
- **Schema validation at every boundary** — `pydantic`, `pandera`, or `dlt` schemas.

This is a compact section, not the full data-engineering book. For deeper coverage see the [NeuroStack data-engineering section](https://github.com/phindagijimana/neuro_stack) — the principles transfer almost line-for-line.
