# Knowledge graphs for repurposing

> Drug → target → pathway → disease. KGs and embedding methods that predict the missing edge.

## The KG view

A biomedical KG has nodes (drugs, targets, diseases, pathways, side effects) and typed edges (drug-target binding, gene-disease association, drug-disease treatment). A repurposing question becomes: *which (drug, disease) pairs are missing edges that the model thinks should be there?*

## Representative KGs

| KG | Scale | Notes |
| --- | --- | --- |
| Hetionet | ~50k nodes, ~2.3M edges | classic; 11 node types, 24 edge types |
| OpenTargets | ~60k targets, ~25k diseases | curated evidence per edge |
| PrimeKG | ~130k nodes, ~4M edges | precision-medicine focused |
| BioKG, BIOSNAP | various | benchmarks and competitions |
| DRKG | 97k nodes, 5.9M edges | drug-repurposing knowledge graph |

## Embedding methods

The classical recipe: learn an embedding per node such that valid edges score higher than invalid ones.

- **TransE** [Bordes et al., 2013](https://doi.org/10.5555/2999792.2999923)[^transe] — translation in embedding space.
- **DistMult, ComplEx** — bilinear scoring functions; handle symmetric / antisymmetric relations.
- **RotatE** — rotations in complex space.

For heterogeneous graphs:

- **R-GCN** — relation-aware graph convolutions.
- **GraphSAGE / GAT** — neighbour sampling + attention.
- **HetGNN, HAN** — explicit heterogeneous attention.

## TxGNN — the 2024 standout

[Huang et al., 2024](https://doi.org/10.1038/s41591-024-03247-5)[^txgnn] trained a GNN on PrimeKG to perform zero-shot drug-disease prediction, specifically targeting diseases with *no* approved drugs.

Key ideas:

- Multi-relational message passing on the biomedical KG.
- A target-disease auxiliary task that strengthens drug-disease prediction.
- An explainability interface ("TxGNN Explorer") that surfaces the KG path supporting each prediction.

For computational repurposing in 2025, TxGNN is the right baseline.

## How to evaluate KG-based repurposing

Pitfalls:

- **Random link splits leak.** Drug-disease pairs sharing a known target appear in both train and test, inflating performance.
- **The right split**: time-based (predict drug-disease links that appeared after a cutoff) or disease-based (hold out all edges of test diseases).
- **Negative sampling** affects ranking metrics; sampling random negatives produces optimistic numbers.

For a published model that did time-based and disease-based splits to back up its claims, see [TxGNN](https://doi.org/10.1038/s41591-024-03247-5).

## Interpretability and the clinician

For repurposing, *why* a prediction was made is at least as important as *that* it was made. A KG path (drug → target → pathway → disease) is far more actionable than a top-K list. Tools like TxGNN Explorer and OpenTargets' evidence pages are designed for this.

Without an interpretable story, no clinician will move a predicted repurposing into a trial.

## In practice

- **Start with OpenTargets** as the KG; it is the most curated.
- **Use TxGNN or a similar GNN** for ranking; use evidence paths for triage.
- **Combine with signature-based and target-target overlap**; single-signal predictions are weak.
- **Always check the predicted link manually** before trial planning. The model has neither clinical knowledge nor common sense.

## References

[^transe]: Bordes A, Usunier N, Garcia-Duran A, Weston J, Yakhnenko O. Translating embeddings for modeling multi-relational data. *NeurIPS.* 2013. [URL](https://papers.nips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html)
[^txgnn]: Huang K, Chandak P, Wang Q, et al. A foundation model for clinician-centered drug repurposing. *Nat Med.* 2024;30:3601–3613. [doi:10.1038/s41591-024-03247-5](https://doi.org/10.1038/s41591-024-03247-5)

## Where to next

[Clinical evidence & RWE](rwe.md) — when patients themselves tell you a drug works.
