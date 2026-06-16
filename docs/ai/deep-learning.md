# Deep learning for chemistry

> Message-passing networks, SMILES transformers, 3D equivariant nets, multitask learning. When deep learning actually helps in drug discovery.

## The hierarchy

| Architecture | Input | Strength |
| --- | --- | --- |
| MLP on FP | 2048-bit Morgan FP | baseline; matches RF in small-data |
| 1D CNN / RNN / Transformer on SMILES | SMILES tokens | sequence-style; data-hungry |
| GCN / GAT | Molecular graph | structural inductive bias |
| MPNN / D-MPNN (Chemprop) | Molecular graph | the workhorse for medium-size data |
| 3D GNN (SchNet, DimeNet++) | 3D coords | physical-property prediction |
| E(3)-equivariant (Equiformer, MACE) | 3D coords | force fields, binding affinity |
| Pretrained LM + head (ChemBERTa, MolFormer) | SMILES | small-data fine-tuning |

## Message-passing networks (MPN)

The canonical 2D drug-discovery architecture. Each atom is a node; each bond is an edge. At each layer, atoms aggregate messages from their neighbours; this builds up substructure-aware features.

**Chemprop** [Yang et al., 2019](https://doi.org/10.1021/acs.jcim.9b00237)[^chemprop] is the reference implementation. It uses **directed message-passing** (D-MPNN) and ships strong defaults.

```bash
chemprop train \
    --data_path train.csv \
    --task_type regression \
    --target_columns pIC50 \
    --split_type scaffold_balanced \
    --num_folds 5 \
    --depth 3 --hidden_size 300 \
    --epochs 50
```

On the MoleculeNet / TDC benchmarks with proper scaffold splits, Chemprop performance is usually within a few percent of much larger architectures.

## SMILES transformers

A transformer trained on SMILES (RoBERTa / GPT-style) treats molecules as token sequences.

- **ChemBERTa, MolBERT, MolFormer** are pretrained on 10⁶–10⁸ SMILES.
- For downstream tasks, **fine-tune** the encoder + add a regression / classification head.
- **In small-data regimes** (< 500 labels), pretrained transformers + MLP head often beats MPN.
- **In larger regimes**, MPN catches up or wins.

A token-level SMILES transformer learns scaffold-level features; it does not natively know about 3D geometry, stereo, or pocket interactions.

## 3D equivariant models

For tasks where geometry matters (binding affinity prediction, conformer energy, forces), 3D models with E(3) equivariance are now the state of the art:

- **SchNet** [Schütt et al., 2017](https://doi.org/10.48550/arXiv.1706.08566)[^schnet] — continuous-filter convolutions.
- **DimeNet++** — directional message passing.
- **NequIP, MACE** [Batatia et al., 2022](https://doi.org/10.48550/arXiv.2206.07697)[^mace] — strict E(3) equivariance; the basis for modern ML force fields.
- **Equiformer / EquiformerV2** — equivariant transformer.

For binding-affinity prediction from co-crystals (PDBBind / Astex benchmarks), 3D equivariant models lead. For property prediction from 2D, MPN still wins or ties.

## Multitask learning

Training one model across multiple related endpoints (a kinase panel, multiple ADMET tasks, multiple cell-line viabilities) usually transfers usefully.

Chemprop ships multitask mode out of the box; specify multiple target columns:

```bash
chemprop train \
    --data_path admet_panel.csv \
    --task_type classification regression \
    --target_columns pIC50 herg pampa clint
```

The gains are largest when:

- Endpoints are mechanistically related.
- Sample sizes are imbalanced across endpoints (smaller endpoint benefits from the larger one's training).
- The model has shared "physchem-like" intermediate features.

## Pretraining strategies

| Strategy | Data | Use case |
| --- | --- | --- |
| Masked atom prediction | ~100M SMILES | broad downstream transfer |
| Contrastive (SimCLR-style) on conformers | 3D ensembles | 3D-aware tasks |
| Multi-task supervised pretraining on PubChem / ChEMBL | bioactivity panel | property-prediction transfer |
| Self-supervised graph pretraining | molecular graphs | property prediction |

For most projects, the pretrained checkpoint to **start from** is more important than the pretraining recipe — pick MolFormer, ChemBERTa, or Uni-Mol depending on what your downstream task is.

## When deep learning fails

- **n < 200 labels**: RF + descriptors usually wins. Deep models overfit.
- **Single-scaffold dataset**: deep models memorise the scaffold and confuse the test split.
- **Activity-cliff-rich tasks**: deep models that interpolate fail; classical methods on Tanimoto kernels often handle cliffs better.
- **Cross-scaffold generalisation**: deep models often produce miscalibrated probabilities OOD.

These failures are well-documented in [MoleculeACE](https://doi.org/10.1021/acs.jcim.2c01073) and similar benchmarks.

## In practice

- **Start with a Chemprop baseline.** For most regimes it is competitive with everything more complex.
- **Use pretrained molecular LMs only when n < 1000** and you have a fine-tuning recipe.
- **For 3D-tied tasks**, go equivariant. For 2D-tied tasks, stay graph-MPN.
- **Always report scaffold-split metrics with bootstrapped CIs.**

## References

[^chemprop]: Yang K, Swanson K, Jin W, et al. Analyzing learned molecular representations for property prediction. *J Chem Inf Model.* 2019;59(8):3370–3388. [doi:10.1021/acs.jcim.9b00237](https://doi.org/10.1021/acs.jcim.9b00237)
[^schnet]: Schütt KT, Kindermans P-J, Sauceda HE, Chmiela S, Tkatchenko A, Müller K-R. SchNet: a continuous-filter convolutional neural network for modeling quantum interactions. *arXiv:1706.08566.* 2017. [doi:10.48550/arXiv.1706.08566](https://doi.org/10.48550/arXiv.1706.08566)
[^mace]: Batatia I, Kovacs DP, Simm GNC, Ortner C, Csányi G. MACE: higher-order equivariant message passing neural networks for fast and accurate force fields. *arXiv:2206.07697.* 2022. [doi:10.48550/arXiv.2206.07697](https://doi.org/10.48550/arXiv.2206.07697)

## Where to next

[Protein language models](protein-models.md) — the protein side of the same revolution.
