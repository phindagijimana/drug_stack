# Network & pathway biology

> Targets do not act in isolation. Methods that place a candidate in its protein-interaction, regulatory, or pathway context.

## Why networks

Two practical reasons to think in networks:

1. **A causal gene from genetics is sometimes not the right *drug* target** — the right drug target is a node downstream of it that is more tractable.
2. **Phenotypes emerge from modules, not individual proteins.** A target whose effect is dampened by parallel pathways will disappoint clinically.

## Network resources

- **STRING** — protein-protein interactions integrated across evidence types.
- **BioGRID** — manually curated PPIs.
- **OmniPath** — signed, directed signalling network (curated, used by signalling modelling tools).
- **BioPlex 3.0** — affinity-based PPI network.
- **Reactome** — curated pathways.
- **KEGG** — pathways (more textbook-style).
- **WikiPathways** — community-edited pathways.
- **DoRothEA** — transcription-factor regulons (high-confidence TF–target relationships).
- **CellPhoneDB / NicheNet** — cell-cell signalling networks.

For a quick "what does this gene do, who does it talk to" lookup, STRING + Reactome is the right pair.

## Network propagation — the canonical method

Given seed genes (e.g. GWAS hits, or known disease drivers), find genes that are *network-proximal* to the seeds.

The mechanic: model the seeds as heat sources, let heat diffuse over the PPI network, rank genes by the heat they accumulate.

```python
import networkx as nx
import numpy as np

# G is a weighted PPI graph; seeds is a list of seed-gene IDs
W = nx.normalized_laplacian_matrix(G).toarray()
S = np.zeros(len(G.nodes))
S[seed_idx] = 1.0
alpha = 0.5
# random-walk-with-restart steady state
F = np.linalg.solve(np.eye(len(W)) - (1 - alpha) * W, alpha * S)
```

This is the engine behind methods like NetworkPropagation, HotNet2 [Leiserson et al., 2015](https://doi.org/10.1038/ng.3168)[^hotnet], DIAMOND, and many disease-module tools.

The output is a ranked list of genes "close" to the seeds, often surfacing tractable candidates that would not otherwise be in the GWAS top-10.

## Pathway-enrichment analysis

For a set of candidate genes (DEGs, GWAS-prioritised, screening hits), enrichment analysis checks which pathways are over-represented relative to a background.

- **Tools**: g:Profiler, EnrichR, Reactome PathwayAnalysis, fgsea (rank-based).
- **Output**: pathways with adjusted p-values and gene-set overlap.

Use it as **hypothesis-organising**, not hypothesis-confirming. The same DEG list will look "immune", "metabolic", or "stress" depending on which pathway databases you query and how granular they are.

## Modern: graph neural networks on biological knowledge graphs

Recent work treats KGs as input to GNNs that learn embeddings predictive of disease-gene or drug-target relationships.

- **PrimeKG** [Chandak et al., 2023](https://doi.org/10.1038/s41597-023-01960-3)[^primekg] — precision-medicine KG used by several recent papers.
- **Bioteque, OpenBioLink, Hetionet** — earlier KG resources.
- **TxGNN** [Huang et al., 2024](https://doi.org/10.1038/s41591-024-03247-5)[^txgnn] — GNN for drug-disease prediction, including zero-shot for diseases with no approved drugs.

These methods are mostly used for repurposing and target prioritisation; see [Knowledge graphs](../repurposing/knowledge-graphs.md).

## In practice

- **Use networks to expand**, not to replace, the genetic signal.
- **Avoid the "central node" trap** — high-degree hubs (like p53, EGFR) appear in everyone's results because of network topology, not because they are the right answer.
- **Network results should be tested with a perturbation experiment** before they are advanced past "interesting".

## References

[^hotnet]: Leiserson MDM, Vandin F, Wu H-T, et al. Pan-cancer network analysis identifies combinations of rare somatic mutations across pathways and protein complexes. *Nat Genet.* 2015;47(2):106–114. [doi:10.1038/ng.3168](https://doi.org/10.1038/ng.3168)
[^primekg]: Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine. *Sci Data.* 2023;10:67. [doi:10.1038/s41597-023-01960-3](https://doi.org/10.1038/s41597-023-01960-3)
[^txgnn]: Huang K, Chandak P, Wang Q, et al. A foundation model for clinician-centered drug repurposing. *Nat Med.* 2024;30:3601–3613. [doi:10.1038/s41591-024-03247-5](https://doi.org/10.1038/s41591-024-03247-5)

## Where to next

[Literature & knowledge graphs](literature.md) — text mining and embedding-based prioritisation at scale.
