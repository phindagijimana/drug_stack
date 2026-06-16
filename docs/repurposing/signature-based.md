# Signature-based repurposing

> "Find a drug whose transcriptomic signature reverses the disease." The CMap / LINCS playbook.

## The connectivity-map idea

[Lamb et al., 2006](https://doi.org/10.1126/science.1132939)[^cmap2006] introduced the Connectivity Map: a database of gene-expression changes caused by ~1300 drugs across a handful of cell lines. The query workflow:

1. Define a **disease signature**: genes up and down in disease vs. control tissue.
2. Search the database for **drugs whose signature is opposite** to the disease signature.
3. Those drugs are predicted to *reverse* the disease state — repurposing candidates.

This is "reversed connectivity" and it remains the canonical signature-based approach.

## LINCS L1000

The modern descendant. [Subramanian et al., 2017](https://doi.org/10.1016/j.cell.2017.10.049)[^lincs] scaled CMap by an order of magnitude:

- ~30 000 perturbagens (small molecules + CRISPR knockouts + shRNA).
- ~9 cell lines.
- Measured 978 "landmark" genes; ~80% of full transcriptome inferred.
- ~1.3M profiles in total.

Available via the LINCS portal (`clue.io`) and as raw GCT files.

## The scoring math

Standard CMap score: for query signature \(q\) (up- and down-regulated gene sets), and reference signature \(s\), compute the Kolmogorov-Smirnov enrichment of \(q\) in the ranked \(s\):

\[
\text{CS}(q, s) = \text{ES}_{up}(q_{up}, s) - \text{ES}_{down}(q_{down}, s)
\]

normalised against permutations. Negative CS → reversal → repurposing candidate.

```python
# pseudocode using cmappy
from cmapPy.pandasGEXpress.parse import parse
import numpy as np

signatures = parse("LINCS_signatures.gct")
# q_up, q_down — gene sets from the disease signature
for sig_id in signatures.col_metadata_df.index:
    s = signatures.data_df[sig_id].sort_values()
    cs = ks_enrichment(q_up, s) - ks_enrichment(q_down, s)
    yield sig_id, cs
```

## Pitfalls

- **Cell-line context matters.** A reversal in A549 may not translate to disease tissue.
- **L1000 landmark-only measurement** means many relevant signatures are inferred, not measured.
- **Noise** in expression signatures means modest CS scores are unreliable; require strong scores from multiple cell lines.
- **A reversed signature is a correlate**, not a causal link. A drug that incidentally tweaks the same genes for unrelated reasons gets a high CS.

## A worked example

The [SignatureSearch](https://doi.org/10.1093/nar/gkac1054) and the OpenTargets `Drug-Signature` repurposing tab pre-compute signature-based scores against LINCS for many diseases.

The pragmatic workflow:

1. Build a *robust* disease signature from multiple bulk RNA-seq studies (or a meta-analysis).
2. Run reversed-CS against LINCS.
3. Filter to candidates that are FDA-approved (or at least into clinical trials), with available formulation.
4. Triage by mechanism plausibility.
5. Validate in an appropriate disease model (organoid, animal).

## Newer single-cell variants

CMap / LINCS are bulk. Single-cell perturbation atlases (Perturb-seq, Sci-Plex) are starting to provide cell-state-resolved signatures. The reversed-connectivity idea extends naturally — and matters more — at single-cell resolution because diseases often affect specific cell states.

Tools in development: scQuery, scPerturb. Watch for cell-state-resolved repurposing in 2025–2027.

## In practice

- **Signature-based scores are a hypothesis generator**, not a verdict.
- **Always combine** with a mechanistic story: why would this drug's known target relate to the disease pathway?
- **Validate in disease-relevant models** before any clinical proposal.
- For well-characterised diseases with strong signatures (cancer cell-line specific, some viral infections), signature-based reproducibility is high. For multifactorial diseases (Alzheimer's, NASH), expect more noise.

## References

[^cmap2006]: Lamb J, Crawford ED, Peck D, et al. The Connectivity Map: using gene-expression signatures to connect small molecules, genes, and disease. *Science.* 2006;313(5795):1929–1935. [doi:10.1126/science.1132939](https://doi.org/10.1126/science.1132939)
[^lincs]: Subramanian A, Narayan R, Corsello SM, et al. A next generation Connectivity Map: L1000 Platform and the first 1 000 000 profiles. *Cell.* 2017;171(6):1437–1452. [doi:10.1016/j.cell.2017.10.049](https://doi.org/10.1016/j.cell.2017.10.049)

## Where to next

[Knowledge graphs](knowledge-graphs.md) — embedding-based repurposing.
