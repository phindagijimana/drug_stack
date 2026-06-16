# Ligand-based screening

> When you have actives but no structure (or structure isn't useful). Similarity, pharmacophore, ML scoring.

The simplest, oldest, and still surprisingly effective screening framing: rank a library by similarity to known actives.

## Similarity search

Already covered in [Getting started → first screen](../getting-started/first-screen.md). The recap:

```python
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator
import numpy as np

gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
qfp = gen.GetFingerprint(Chem.MolFromSmiles(query_smiles))
lib_fps = [gen.GetFingerprint(Chem.MolFromSmiles(s)) for s in lib_smiles]
sims = np.array([DataStructs.TanimotoSimilarity(qfp, fp) for fp in lib_fps])
```

For multiple actives, average Tanimoto against the set, or take the max — both are reasonable; max is more sensitive to the closest analogue, mean averages over the cluster.

## Pharmacophore screening

A **pharmacophore** is a 3D arrangement of features (H-bond donors, acceptors, aromatic centroids, hydrophobic centres, positive / negative charges) hypothesised to drive binding.

Workflow:

1. Build a pharmacophore from a co-crystal or a series of known actives.
2. Generate 3D conformers for library compounds.
3. Check which conformers can match the pharmacophore within tolerances.

Tools:

- **RDKit pharmacophore module** — open source, basic.
- **LigandScout** — commercial, mature.
- **Phase** (Schrödinger) — commercial.

Pharmacophore screening trades scale for selectivity. It is slower than 2D similarity but produces ligands that share the *3D recognition pattern*, including non-obvious scaffold hops.

## Shape-based screening

Ranking by 3D shape similarity. The classical method is **ROCS** [Hawkins et al., 2007](https://doi.org/10.1021/jm0603365)[^rocs], which compares Gaussian-based volume overlap.

- **Pro**: scaffold-hopping signal — finds molecules with similar 3D shape but different 2D structure.
- **Con**: needs reasonable conformer ensembles; slower than fingerprint similarity.

Open-source alternatives: **Shape-IT**, **OE_Shape** (academic licence).

## Quantum / dipole / property-based similarity

Rarely the right call as a primary screen, but useful as a secondary filter. ESP similarity (Electronic ESP comparison via EON) catches electrostatic mimics that shape-based methods miss.

## ML-based rescoring of ligand-based hits

Standard practice: after a similarity screen, train an ML model on actives vs decoys and *rescore* the top hits.

```python
# pseudo:
top_k_smiles = top_by_similarity(query_smis, library, k=10_000)
X = featurise(top_k_smiles)
qsar_model = load_qsar()              # trained on the target's bioactivity data
proba = qsar_model.predict_proba(X)
final = sort(top_k_smiles, by=proba)
```

A QSAR model trained on the actual target activity is more discriminating than similarity alone; using both as a sieve catches more genuine actives.

## Decoys done right

A common mistake: building a "decoys" set as random ChEMBL compounds. They are *too* dissimilar from the actives, and the model learns trivial physchem differences.

**DUD-E** [Mysinger et al., 2012](https://doi.org/10.1021/jm300687e)[^dude] and **DEKOIS** matched-physchem decoys are the standard for benchmarking. For your *own* screening project, build matched-property decoys (similar MW, logP, HBA, HBD distributions) from a library the actives were drawn from.

The newer **LIT-PCBA** [Tran-Nguyen et al., 2020](https://doi.org/10.1021/acs.jcim.0c00155)[^litpcba] avoids many DUD-E biases and is the right modern benchmark.

## In practice

- **Tanimoto on ECFP4 is the right default similarity.** Variations exist; documenting them is non-optional.
- **For scaffold hopping**, run shape or pharmacophore on top of 2D similarity.
- **Always rescore with a QSAR model** if you have one — similarity alone is a weak signal.
- **Benchmark on LIT-PCBA, not DUD-E**, if you must benchmark.

## References

[^rocs]: Hawkins PCD, Skillman AG, Nicholls A. Comparison of shape-matching and docking as virtual screening tools. *J Med Chem.* 2007;50(1):74–82. [doi:10.1021/jm0603365](https://doi.org/10.1021/jm0603365)
[^dude]: Mysinger MM, Carchia M, Irwin JJ, Shoichet BK. Directory of useful decoys, enhanced (DUD-E): better ligands and decoys for better benchmarking. *J Med Chem.* 2012;55(14):6582–6594. [doi:10.1021/jm300687e](https://doi.org/10.1021/jm300687e)
[^litpcba]: Tran-Nguyen V-K, Jacquemard C, Rognan D. LIT-PCBA: an unbiased data set for machine learning and virtual screening. *J Chem Inf Model.* 2020;60(9):4263–4273. [doi:10.1021/acs.jcim.0c00155](https://doi.org/10.1021/acs.jcim.0c00155)

## Where to next

[Structure-based screening](structure-based.md) — when you have a pocket.
