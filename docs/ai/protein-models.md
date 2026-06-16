# Protein language models

> ESM, ProtTrans, ProGen, AbLang. What they capture, what they don't, and the drug-discovery use cases.

## The premise

A protein sequence is a string over 20 letters. Pretraining a large transformer on hundreds of millions of these strings produces embeddings that encode structural, functional, and evolutionary information.

The most influential family is **ESM** [Rives et al., 2021](https://doi.org/10.1073/pnas.2016239118)[^esm1]; [Lin et al., 2023](https://doi.org/10.1126/science.ade2574)[^esm2]:

- **ESM-2 (15B parameters)** — the largest open protein LM.
- **ESM-IF** — inverse-folding: predict sequence from structure.
- **ESMFold** — single-sequence structure prediction.

## Drug-discovery use cases

| Task | Approach |
| --- | --- |
| Variant effect prediction | ESM zero-shot or fine-tune |
| Target tractability / function | ESM embeddings → classifier |
| Antibody design | AbLang, IgLM, OmegaFold |
| Protein-protein interface prediction | ESM-IF, MaSIF, ESM-MSA |
| Fitness landscape / directed evolution | ESM zero-shot scoring |
| Structure prediction | AlphaFold2/3, ESMFold, Boltz, Chai |

## Variant effect prediction

A core target-validation question: does this variant gain or lose function?

ESM zero-shot can score variants by likelihood ratios:

\[
\text{score}(X^{aa→aa'}_i) = \log P(aa' | X_{\setminus i}) - \log P(aa | X_{\setminus i})
\]

This correlates with deep mutational scanning measurements at Spearman ~0.5–0.7 across many proteins — useful for prioritising variants for follow-up.

The **Tranception, ESM-1v, ESM-2 zero-shot** methods are now standard baselines for variant effect prediction.

## Antibody-specific models

Antibodies have constrained sequence statistics (V/D/J recombination, CDR composition). General protein LMs underperform antibody-specific ones:

- **AbLang** — BERT trained on observed antibody repertoires.
- **IgLM** — generative for antibodies.
- **AntiBERTy, BALM, AntiBERTa** — variants.
- **AbDeep, ABodyBuilder3** — antibody structure prediction.

For developability prediction (humanness, aggregation), antibody-specific LMs are now standard in mAb pipelines.

## Inverse folding and design

**ESM-IF** [Hsu et al., 2022](https://doi.org/10.1101/2022.04.10.487779)[^esmif]: given a structure, predict the sequence that folds to it.

Combined with structure-design tools (RFdiffusion, ProteinMPNN), this enables **de novo protein design** — designing binders, enzymes, or scaffolds with target properties.

For drug discovery this is mostly relevant to biologics and protein therapeutics. For small molecules, the protein-side use is target structure prediction (AlphaFold class) and binding-pocket characterisation.

## ESM as feature extractor

The most common drug-discovery use of ESM is not generation but **feature extraction**:

```python
import torch
import esm

model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
batch_converter = alphabet.get_batch_converter()
data = [("target_seq", "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQK")]
_, _, batch_tokens = batch_converter(data)
with torch.no_grad():
    out = model(batch_tokens, repr_layers=[33], return_contacts=False)
embedding = out["representations"][33].mean(dim=1)
```

The resulting embedding can be:

- Concatenated with molecular features for ligand-protein affinity prediction.
- Used as a target representation for cross-target activity prediction.
- A drop-in feature for any downstream "protein-aware" task.

## In practice

- **Use ESM as feature extractor first** before training your own from scratch.
- **For antibodies use antibody-specific models** (AbLang, IgLM).
- **Variant effect prediction**: ESM zero-shot is the right baseline.
- **Structure prediction**: AlphaFold3 / Boltz / Chai for production; ESMFold for fast iteration.

## References

[^esm1]: Rives A, Meier J, Sercu T, et al. Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *Proc Natl Acad Sci.* 2021;118(15):e2016239118. [doi:10.1073/pnas.2016239118](https://doi.org/10.1073/pnas.2016239118)
[^esm2]: Lin Z, Akin H, Rao R, et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science.* 2023;379(6637):1123–1130. [doi:10.1126/science.ade2574](https://doi.org/10.1126/science.ade2574)
[^esmif]: Hsu C, Verkuil R, Liu J, et al. Learning inverse folding from millions of predicted structures. *bioRxiv.* 2022. [doi:10.1101/2022.04.10.487779](https://doi.org/10.1101/2022.04.10.487779)

## Where to next

[Generative chemistry models](generative-models.md) — back to small molecules, with more training-side depth.
