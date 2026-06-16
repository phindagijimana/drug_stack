# Literature & knowledge graphs

> Reading the literature at scale. NER, relation extraction, KG construction, and the increasing role of LLMs.

PubMed has ~37 million abstracts. Nobody reads them. Computational target-ID often needs to summarise what is known about a target-disease pair in minutes, not days.

## Biomedical text mining

The classical NLP stack:

1. **Named entity recognition (NER)** — find mentions of genes, proteins, diseases, drugs, cell types.
2. **Entity normalisation** — map "TNF-α", "TNFA", "tumour necrosis factor alpha" all to the same UniProt entry.
3. **Relation extraction** — find statements like "drug A inhibits target B in disease C".
4. **Confidence scoring** — quantify how strongly the evidence supports a relation.

Reliable open tools:

- **PubTator Central** [Wei et al., 2019](https://doi.org/10.1093/nar/gkz389)[^pubtator] — NIH-hosted, pre-computes NER + linking over PubMed.
- **SciBERT, BioBERT, BlueBERT, BioMegatron** — biomedical-domain BERT variants; the standard backbone for fine-tuning.
- **PubMedBERT** — out-of-the-box decent NER and embedding.
- **BERN2** — modern biomedical NER+normaliser web service.

## Knowledge graphs from the literature

A KG is the natural representation of relation-extraction output:

```
(TNF, INHIBITED_BY, adalimumab)
(adalimumab, TREATS, rheumatoid_arthritis)
(rheumatoid_arthritis, ASSOCIATED_WITH, TNF)
```

When KGs are merged with structured sources (ChEMBL, DrugBank, OpenTargets), they become the substrate for embedding-based target prioritisation.

Representative resources:

- **OpenTargets** — already half-KG-shaped; surfaces evidence per drug-target-disease tuple.
- **Hetionet** [Himmelstein et al., 2017](https://doi.org/10.7554/eLife.26726)[^hetionet] — heterogeneous network combining 29 sources.
- **PrimeKG** [Chandak et al., 2023](https://doi.org/10.1038/s41597-023-01960-3)[^primekg] — precision-medicine KG with 20+ relation types.
- **CKG** (Clinical Knowledge Graph) — proteomics-leaning.

## Embedding methods

Once you have a KG with millions of edges, embedding methods produce dense representations that support link prediction:

- **TransE / DistMult / ComplEx** — translational and bilinear embedding models, baseline.
- **RotatE / GraIL** — modern improvements.
- **GNNs (GraphSAGE, GAT, R-GCN)** — the current default; better than transE for heterogeneous relations.
- **PrimeKG + TxGNN** [Huang et al., 2024](https://doi.org/10.1038/s41591-024-03247-5)[^txgnn] — zero-shot drug-disease prediction.

The interpretation: a drug-disease edge predicted by the model is a candidate repurpose; a target-disease edge predicted is a candidate target.

## LLMs in target ID

Recent LLMs (GPT-4.5, Claude 4.7, Gemini 2.5, Llama 4-class) can:

- **Summarise the prior** on a target-disease pair from PubMed.
- **Critique a target hypothesis** with explicit caveats.
- **Translate genetic / GWAS findings** into a target-validation narrative.
- **Suggest competitor activity** based on patents and conference abstracts.

They cannot, reliably:

- Predict numerical effect sizes.
- Cite specific PMIDs correctly without grounding.
- Distinguish between conflicting findings without explicit prompting.

Retrieval-augmented generation (RAG) over a curated corpus (e.g. just PubMed abstracts from the last 5 years for the target gene) is the standard pattern. Reading the cited evidence directly is non-optional; trusting model summaries without verification is malpractice.

## In practice

- **Curated KGs (OpenTargets, PrimeKG) > raw LLM output** for target prioritisation. LLMs are best at *narrative* synthesis, not ranking.
- **PubTator + retrieval** gives you the evidence-with-citation a downstream chemist actually needs.
- **The KG you build is only as good as the entity normalisation.** "BCL2", "BCL-2", "B-cell lymphoma 2" must map to one node.

## References

[^pubtator]: Wei C-H, Allot A, Leaman R, Lu Z. PubTator Central: automated concept annotation for biomedical full text articles. *Nucleic Acids Res.* 2019;47(W1):W587–W593. [doi:10.1093/nar/gkz389](https://doi.org/10.1093/nar/gkz389)
[^hetionet]: Himmelstein DS, Lizee A, Hessler C, et al. Systematic integration of biomedical knowledge prioritizes drugs for repurposing. *eLife.* 2017;6:e26726. [doi:10.7554/eLife.26726](https://doi.org/10.7554/eLife.26726)
[^primekg]: Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine. *Sci Data.* 2023;10:67. [doi:10.1038/s41597-023-01960-3](https://doi.org/10.1038/s41597-023-01960-3)
[^txgnn]: Huang K, Chandak P, Wang Q, et al. A foundation model for clinician-centered drug repurposing. *Nat Med.* 2024;30:3601–3613. [doi:10.1038/s41591-024-03247-5](https://doi.org/10.1038/s41591-024-03247-5)

## Where to next

[Target validation](validation.md) — the wet-lab side of target ID that computationalists must read.
