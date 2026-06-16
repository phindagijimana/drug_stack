# Molecular representations

> SMILES, SELFIES, InChI, graphs, 3D ensembles, learned embeddings. What each gives you, what each costs.

The single most consequential choice in computational chemistry is the molecular representation. It silently sets what your model can and cannot learn.

## The seven representations you will meet

| Representation | Carries | Loses | Typical use |
| --- | --- | --- | --- |
| **SMILES** | connectivity, bond order, stereo (optional) | 3D geometry | storage, ML input, similarity |
| **SELFIES** [Krenn et al., 2020](https://doi.org/10.1088/2632-2153/aba947)[^selfies] | same as SMILES, every string is valid | same | generative ML |
| **InChI / InChIKey** | canonical hash of the graph | substring intuition | DB join keys |
| **Molfile / SDF** | 2D or 3D coords + connectivity | nothing crucial | pipelines, chemists' tools |
| **Molecular graph** | atoms, bonds, features per node / edge | not human-readable | GNNs |
| **3D conformer ensemble** | full geometry | discrete (not a continuous distribution) | docking, FEP, structure-based |
| **Learned embedding** | what the model captures | interpretability, often stereo | downstream ML |

## SMILES

The lingua franca. Covered exhaustively in [Getting started → first SMILES](../getting-started/first-smiles.md).

Important reminders:

- Always canonicalise.
- Stereochemistry is optional — `@`, `@@`, `/`, `\` — be explicit about whether you keep it.
- Aromaticity perception varies between toolkits; RDKit and OpenBabel disagree on edge cases.
- Tautomer canonicalisation is a separate step beyond SMILES canonicalisation.

## SELFIES

A self-referential string grammar where every string is a valid molecule. Solves the "generative model produces invalid SMILES" problem.

Most modern generative-chemistry papers ship a SELFIES variant. For non-generative work (similarity, ML on fixed corpora), SMILES is still fine.

```python
import selfies
selfies.encoder("CC(=O)Oc1ccccc1C(=O)O")  # aspirin → SELFIES
selfies.decoder("[C][C][=Branch1][C][=O][O][C]...")  # back
```

## Molecular graphs

The right representation for **message-passing networks**. Each atom is a node with features (element, formal charge, hybridisation, H-count); each bond is an edge with features (order, aromaticity, ring-membership).

```python
from torch_geometric.utils import from_smiles
data = from_smiles("CC(=O)Oc1ccccc1C(=O)O")
# data.x  — node features, shape [num_atoms, num_node_features]
# data.edge_index, data.edge_attr — edges
```

Trade-offs:

- **Pro**: respects molecular topology directly; permutation-invariant; learnable features.
- **Con**: no 3D context; stereo is awkward; large molecules are heavier than SMILES.

## 3D conformer ensembles

A *single* 3D structure for a flexible molecule misrepresents it. Real molecules sample many conformations; binding selects one.

```python
from rdkit import Chem
from rdkit.Chem import AllChem
mol = Chem.AddHs(Chem.MolFromSmiles("..."))
AllChem.EmbedMultipleConfs(mol, numConfs=50, randomSeed=0xf00d)
AllChem.MMFFOptimizeMoleculeConfs(mol)
```

ETKDG (Riniker & Landrum) is the recommended embedder. For docking, the receptor scoring function selects among the conformers; for FEP, you sample dynamically.

## Learned embeddings

Pretrained models produce dense vectors per molecule:

- **Mol2Vec** [Jaeger et al., 2018](https://doi.org/10.1021/acs.jcim.7b00616)[^mol2vec] — word2vec on Morgan substructures.
- **ChemBERTa** — RoBERTa on 77 M SMILES from PubChem; transformers for SMILES.
- **MolFormer** — IBM's pretrained SMILES transformer.
- **Uni-Mol** — 3D-aware pretraining.
- **MolE / GROVER** — graph-based pretraining.

For downstream tasks with tiny data (< 1k labels), pretrained embeddings + a small head often beat training from scratch. For tasks with 10k+ labels, train end-to-end.

## SMILES vs graph vs embedding for ML

Practical guidance:

- **Tiny data (< 200 mols)**: descriptors + random forest. Often beats fancier methods.
- **Small data (200–5000 mols)**: fingerprints + GBDT, or pretrained embeddings + MLP.
- **Medium data (5k–100k mols)**: message-passing networks (Chemprop, DimeNet++).
- **Large data (> 100k mols)**: large GNNs or transformers; consider end-to-end.

Pretrained embeddings are mostly useful at the tiny/small end; large data is enough to train from scratch.

## 3D models

For tasks that depend on geometry (docking-score prediction, binding-mode prediction, FEP-friendly ranking):

- **SchNet** — continuous-filter convolutions on 3D point clouds.
- **DimeNet / DimeNet++** — directional message passing with angular features.
- **GemNet** — explicit dihedral information.
- **EquiformerV2 / e3nn-based** — E(3)-equivariant transformers; current state-of-the-art for many tasks.

A 3D model with E(3) equivariance respects rotational symmetry by construction; this is a strong inductive bias for binding-affinity prediction.

## In practice

- **For ML on activity** — SMILES + Morgan FPs + RF is the right baseline. Beat it before adopting anything fancier.
- **For ML on properties tied to geometry** (binding affinity, conformer energy) — go 3D, with an equivariant model.
- **For generative chemistry** — SELFIES if you need validity; fragment-based or RL-on-SMILES if you can post-process.
- **For database joins** — InChIKey, always.

## References

[^selfies]: Krenn M, Häse F, Nigam A, et al. Self-Referencing Embedded Strings (SELFIES): a 100% robust molecular string representation. *Mach Learn: Sci Technol.* 2020;1:045024. [doi:10.1088/2632-2153/aba947](https://doi.org/10.1088/2632-2153/aba947)
[^mol2vec]: Jaeger S, Fulle S, Turk S. Mol2vec: unsupervised machine learning approach with chemical intuition. *J Chem Inf Model.* 2018;58(1):27–35. [doi:10.1021/acs.jcim.7b00616](https://doi.org/10.1021/acs.jcim.7b00616)

## Where to next

[Descriptors & fingerprints](descriptors.md) — what to compute from a representation when you want a fixed-length feature vector.
