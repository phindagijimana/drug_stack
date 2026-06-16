# Tutorial 4 — Target ID from RNA-seq

> A disease vs. control bulk RNA-seq dataset → DEGs → druggable-target candidates → ranked shortlist.

**Prerequisites**: [Transcriptomics](../target-id/transcriptomics.md), [Druggability](../target-id/druggability.md), [Genomics](../target-id/genomics.md).

## The data

For the tutorial, use a GEO dataset for a disease with a small published cohort — e.g. Alzheimer's hippocampus vs control bulk RNA-seq, ~50 samples per group.

For real work, replace with your own cohort or a TCGA / GTEx slice.

## Process (R / Python)

A standard differential-expression call using DESeq2 (R) or pyDESeq2:

```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# counts: gene × sample matrix; metadata: sample × covariate table
dds = DeseqDataSet(counts=counts, metadata=metadata, design="~group")
dds.deseq2()
stats = DeseqStats(dds, contrast=["group", "AD", "Ctrl"])
stats.summary()
res = stats.results_df  # log2FC, pvalue, padj
```

## Filter and intersect with druggable genes

```python
import polars as pl

degs = pl.from_pandas(res.reset_index()).filter(
    (pl.col("padj") < 0.05) & (pl.col("log2FoldChange").abs() > 1.0)
)

# druggable gene list from IDG / TCRD
druggable = pl.read_parquet("idg_tcrd_druggable.parquet").select("gene_symbol", "dev_level")

ranked = degs.join(druggable, on="gene_symbol", how="inner")
ranked = ranked.sort(by=["padj", "log2FoldChange"], descending=[False, True])
print(ranked.head(30))
```

## Bring in genetics

For each candidate, query Open Targets Genetics for genetic-support evidence:

```python
import requests
GQL = """
query gene($id: String!) {
  target(ensemblId: $id) {
    associatedDiseases(efoIds: ["EFO_0000249"]) {  # Alzheimer's
      rows {
        score
        disease { id name }
      }
    }
  }
}
"""
def open_targets_score(ensembl_id):
    r = requests.post("https://api.platform.opentargets.org/api/v4/graphql",
                      json={"query": GQL, "variables": {"id": ensembl_id}}).json()
    rows = r["data"]["target"]["associatedDiseases"]["rows"]
    return max((row["score"] for row in rows), default=0.0)

ranked = ranked.with_columns(
    ot_score=ranked["ensembl_id"].map_elements(open_targets_score)
)
```

## Final scoring

A simple composite:

\[
S = w_1 \cdot z_{\log_2FC} + w_2 \cdot (1 - p_{adj}) + w_3 \cdot \text{OT\_score} + w_4 \cdot \text{druggable\_level}
\]

with normalised components. Sort and triage the top 30 by hand.

## Decision points called out

- **DEG cutoff** — adj. p < 0.05 + |log2FC| > 1 is conservative; relax for low-power studies.
- **Druggable-gene list** — IDG TCRD or DrugBank-implied target sets; document the version.
- **Genetics integration** — Open Targets is a good proxy for "ground-truth disease relevance".
- **Manual triage at top 30** — there is no substitute.

## Where to next

[Generative design](generative-design.md) — design molecules for one of the top targets.
