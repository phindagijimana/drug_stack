# Data analysis

> pandas / Polars patterns specific to drug-discovery data. Tabular work without the rookie mistakes.

This chapter is not "intro to pandas". It is the handful of idioms that come up in cheminformatics that are not obvious from the docs.

## Choose the right frame library

| Data size | Library | Why |
| --- | --- | --- |
| < 1 GB | pandas | The ecosystem; every plot library speaks it |
| 1–100 GB | Polars | 10–100× faster, lazy queries, low memory |
| > 100 GB | DuckDB / Spark | Out-of-core / distributed |

For most non-ultra-large screening work, **Polars in lazy mode** is the sweet spot. Pandas is fine for plotting and small joins.

## Parquet is the right on-disk format

CSV is text. Parquet is binary, columnar, compressed, and schema-aware. For any cheminformatics dataset:

```python
import polars as pl
df = pl.read_csv("chembl_chemreps.txt", separator="\t")
df.write_parquet("chembl_chemreps.parquet", compression="zstd")
```

Disk: ~5× smaller. Read: ~10× faster. Schema preserved.

## Standard "compound table" schema

In practice, almost every project's primary table looks roughly like this:

```python
schema = {
    "compound_id":   pl.Utf8,    # ChEMBL ID, internal ID
    "smiles_input":  pl.Utf8,    # whatever you got
    "smiles_canon":  pl.Utf8,    # RDKit-canonical
    "inchikey":      pl.Utf8,    # the join key
    "mw":            pl.Float32,
    "clogp":         pl.Float32,
    "tpsa":          pl.Float32,
    "hba":           pl.UInt8,
    "hbd":           pl.UInt8,
    "rotb":          pl.UInt8,
    "qed":           pl.Float32,
    "ic50_nM":       pl.Float32,
    "is_active":     pl.Boolean,
    "source":        pl.Utf8,
    "ingested_at":   pl.Datetime,
}
```

A few non-obvious choices:

- **Canonical and raw SMILES both** — round-tripping reveals stereochemistry loss.
- **InChIKey** is the right join key, not SMILES.
- **IC50 in nM**, not pIC50 — the unit is unambiguous and the conversion is trivial. Keep both if downstream tools want both.
- **Source and ingestion timestamp** — provenance is non-negotiable.

## Joining chemistry tables

```python
# canonical join: by InChIKey, not SMILES
chembl  = pl.read_parquet("chembl.parquet")
pubchem = pl.read_parquet("pubchem.parquet")

joined = chembl.join(pubchem, on="inchikey", how="left")
```

If you ever find yourself joining on SMILES, stop and canonicalise. Two databases will agree on InChIKey ~99.9% of the time and on raw SMILES ~70%.

## Activity columns done right

Three columns, not one:

- `ic50_nM` (or `ki_nM`, `kd_nM`) — the raw number, in known units.
- `pIC50` — \(-\log_{10}(\text{IC}_{50}\text{ in M})\). Symmetric; multiplicative becomes additive; better for modelling.
- `is_active` — boolean using a documented threshold (typically pIC50 > 6 or pIC50 > 7).

Storing only "active / inactive" throws away most of the information. Storing only "pIC50" is fine if everyone knows to use it.

## Group-by patterns that matter

**One row per compound** is the right shape for QSAR training. Aggregate replicates carefully:

```python
agg = (
    df.group_by("inchikey")
      .agg([
          pl.col("smiles_canon").first(),
          pl.col("ic50_nM").median().alias("ic50_median"),
          pl.col("ic50_nM").std().alias("ic50_sd"),
          pl.col("ic50_nM").count().alias("n_replicates"),
      ])
)
```

Use **median**, not mean — IC50 distributions are log-normal and outliers wreck the mean. Always carry replicate counts.

## Splits that matter for ML

The single most common ML mistake in cheminformatics is a random split. The realistic train / test splits:

- **Scaffold split** — group by Bemis-Murcko scaffold, then split groups. Approximates "test is a new chemical series".
- **Time split** — train on data before date *t*, test after. Approximates the actual deployment scenario.
- **Cluster split** — cluster by fingerprint similarity, split clusters. Approximates "test is far from train in chemical space".
- **Random split** — only for "sanity-check the pipeline runs"; never for reported numbers.

DeepChem and OGB ship scaffold-split utilities; otherwise [Skipper et al., 2025](https://doi.org/10.26434/chemrxiv-2024-pq2nl) and similar provide reference implementations.

## In practice

- **Always Parquet, always InChIKey, always typed schema.** Three rules that prevent more bugs than they cost.
- **Never report numbers from a random split.** Scaffold split or time split.
- **Store both raw and canonical SMILES.** You will eventually need both.

## Where to next

[Statistics](statistics.md) — the experimental-design and inferential subset you will use most.
