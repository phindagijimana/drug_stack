# Foundation models for drug discovery

> Large pre-trained models that generalise across many downstream tasks. What's available, when fine-tuning beats from-scratch.

## What "foundation model" means here

Borrowed from NLP / vision: a large model pretrained on a broad corpus, then adapted to many tasks. In drug discovery, the equivalents are pretrained on:

- **Sequences** — protein LMs (ESM, ProGen) trained on UniProt.
- **Molecules** — SMILES / graph LMs trained on PubChem / ChEMBL.
- **Bioactivity** — supervised multitask models on ChEMBL.
- **Structures** — AlphaFold-class joint biomolecular predictors.
- **Multi-modal** — text + molecule (Galactica, BioMedGPT), text + protein (BioMedLM).

## The major families in 2025

| Model | Trained on | Use |
| --- | --- | --- |
| **ESM-2 / ESMFold** | UniProt sequences | protein representation + structure |
| **ProGen** | UniProt + functional labels | protein generation |
| **MolFormer (IBM)** | 1.1B PubChem SMILES | small-molecule embeddings, properties |
| **ChemBERTa** | 77M PubChem SMILES | molecule classification / regression |
| **Uni-Mol** | ZINC15 3D conformers | 3D-aware molecular tasks |
| **GROVER** | ZINC15 + ChEMBL graphs | property prediction |
| **MolGPS** | 100M molecules | scaling-law studies |
| **AlphaFold3 / Boltz / Chai** | PDB + ligands | structure of complexes |
| **NeuralMR / Boltz-2** | bioactivity + structure | bioactivity prediction |
| **TxGNN** | PrimeKG biomedical | drug-disease prediction |
| **BioMedGPT, Galactica** | Biomedical text + molecules + sequences | LLM-style biomedical |

## The "small data" framing

Drug-discovery foundation models are most useful when the labeled data for a downstream task is small:

- **n < 500 labels** → fine-tune a pretrained model (MolFormer, ChemBERTa). Often beats from-scratch deep models and matches or beats RF.
- **n 500–5000** → from-scratch Chemprop with carefully-set defaults catches up.
- **n > 5000** → from-scratch usually wins, foundation models provide marginal lift.
- **n > 50000** → no benefit from pretraining; from-scratch matches.

## When pretraining helps in production

Three regimes where pretrained molecular models clearly help:

1. **Cross-target activity prediction** — predict activity on target *Y* given a labeled dataset on related target *X*. ESM embeddings + small molecule embeddings are the input.
2. **Zero-shot ADMET on new chemotypes** — well-pretrained predictors generalise to chemistry the QSAR has not seen.
3. **Multi-task ADMET panels** — pretrained backbone + task-specific heads beats per-task models when tasks are related.

## Limitations

- **Pretraining benefits saturate** quickly. Adding 10× more SMILES rarely yields proportional gains.
- **Out-of-distribution chemistry** (covalent warheads, macrocycles, peptides) — most foundation models trained on standard drug-like sets fail OOD.
- **Stereo and tautomers** — most SMILES-pretrained models drop stereo; explicit stereo handling is rare.
- **Confidence calibration** — pretrained models are often miscalibrated, especially OOD.

## Recent generalist models

- **AlphaFold3** [Abramson et al., 2024](https://doi.org/10.1038/s41586-024-07487-w) — predicts protein + small molecule + ion + RNA complexes jointly. The first practical "biomolecular generalist".
- **Boltz-1 / Boltz-2** — open-source AF3-class.
- **Chai-1** — open-source AF3-class.
- **Roche / Novartis pretrained internal models** — proprietary, no public benchmarks.

The trend is clear: drug discovery is moving from many specialised models to a few large generalists fine-tuned per task. The 2025–2027 window will reshape industry pipelines around this shift.

## In practice

- **For new projects with small labeled data**, try MolFormer / ChemBERTa / Uni-Mol fine-tune *before* training from scratch.
- **For structure-based tasks**, AlphaFold3 / Boltz / Chai are now the right baseline.
- **For property prediction at scale**, Chemprop is still highly competitive; foundation models help but rarely dominate.
- **Treat pretrained embeddings as features**, not endpoints. They are a representation; you still need a head and a sane training loop.

## Where to next

[Evaluation pitfalls](evaluation.md) — the chapter that prevents most embarrassments.
