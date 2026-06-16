# Descriptors & fingerprints

> Fixed-length feature vectors over molecules. The default input to classical ML and similarity search.

A descriptor is any scalar (or short vector) computed from a molecule. A fingerprint is a specific kind: a fixed-length bit (or count) vector encoding substructures.

## Physchem descriptors

```python
from rdkit.Chem import Descriptors as D

D.MolWt(mol)              # MW
D.MolLogP(mol)            # cLogP (Crippen)
D.TPSA(mol)               # polar surface area
D.NumHAcceptors(mol)
D.NumHDonors(mol)
D.NumRotatableBonds(mol)
D.NumAromaticRings(mol)
D.NumAliphaticRings(mol)
D.HeavyAtomCount(mol)
D.RingCount(mol)
D.FractionCSP3(mol)
D.qed(mol)                # quantitative estimate of druglikeness
D.MolMR(mol)              # molar refractivity
D.NumHeteroatoms(mol)
D.NumSpiroAtoms(mol)
D.NumBridgeheadAtoms(mol)
```

RDKit ships ~200 descriptors total at `Descriptors._descList`. For most ML work, the dozen above plus a fingerprint covers it.

## QED — quantitative drug-likeness

[Bickerton et al., 2012](https://doi.org/10.1038/nchem.1243)[^qed] folded eight physchem properties into a single 0–1 score, calibrated to historical drug data.

```python
from rdkit.Chem.QED import qed
qed(mol)  # 0 (not druglike) ↔ 1 (very druglike)
```

QED is a useful **soft prior** for filtering or for a generative-model reward signal. It is not a hard threshold — many approved drugs have QED < 0.5.

## SA score and synthesisability

[Ertl & Schuffenhauer, 2009](https://doi.org/10.1186/1758-2946-1-8)[^sa]:

```python
# via rdkit contrib/SA_Score module
from rdkit.Chem import RDConfig
import sys, os
sys.path.append(os.path.join(RDConfig.RDContribDir, 'SA_Score'))
import sascorer
sascorer.calculateScore(mol)  # 1 (easy) ↔ 10 (hard)
```

SA score is heuristic — newer learned-synthesis scores (SCScore, RAscore, AiZynthFinder retrosynthesis scoring) are closer to industrial reality but pricier. SA is the right fast filter.

## Morgan / ECFP — the default

Covered in [Cheminformatics](../fundamentals/foundations/cheminformatics.md). The default for similarity and the baseline input for classical QSAR.

Variations:

- **ECFP4** — radius 2, the standard.
- **ECFP6** — radius 3, more discriminative, less generalising.
- **FCFP** — functional-class fingerprints; substructures by class (donor/acceptor/aromatic/...) rather than atom identity. Better for scaffold hopping.
- **Count vs bit** — count fingerprints preserve multiplicity; useful for some regression tasks.

```python
from rdkit.Chem import rdFingerprintGenerator
gen_ecfp4 = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
gen_ecfp6 = rdFingerprintGenerator.GetMorganGenerator(radius=3, fpSize=2048)
gen_fcfp4 = rdFingerprintGenerator.GetMorganGenerator(
    radius=2, fpSize=2048,
    atomInvariantsGenerator=rdFingerprintGenerator.GetMorganFeatureAtomInvGen(),
)
```

## MACCS keys

166 binary substructure indicators. Small, interpretable, fast. Decent for crude similarity, weaker for QSAR.

```python
from rdkit.Chem import MACCSkeys
fp = MACCSkeys.GenMACCSKeys(mol)
```

## Atom-pair and topological-torsion

Capture pairs / triples of atoms at fixed topological distances. Strong for scaffold hopping (alternative scaffolds presenting the same substituent pattern produce similar atom-pair vectors).

## RDKit topological

Path-based hashing. Good general-purpose, sometimes better than Morgan on small molecules.

## When to use which

| Use case | Default |
| --- | --- |
| Similarity search / virtual screening | Morgan / ECFP4, 2048 bits, Tanimoto |
| Scaffold-hopping similarity | FCFP4 or atom-pair |
| Tiny-data QSAR | Morgan + RF |
| Small-data QSAR | Morgan or descriptors + GBDT |
| Interpretable filter | MACCS + physchem |
| Fast indexing of huge libraries | Morgan (FPSim2) |

## Avoidable mistakes

- **Comparing fingerprints with different radii or bit-lengths.** The Tanimoto values are not directly comparable.
- **Tanimoto > 0.85 ≡ same scaffold.** It is a rule of thumb, not a theorem; an activity cliff with similar fingerprints exists.
- **MACCS or 1024-bit ECFP for billion-compound screens.** The 2048-bit ECFP4 is now a near-universal standard; switching loses comparability.
- **Using ECFP without stereochemistry on stereosensitive targets.** ECFP loses stereo by default; for stereo-discriminating tasks include it explicitly.

## In practice

- **Default**: physchem (10 descriptors) + ECFP4 (2048 bits) + Tanimoto. Document this and you have explained 80% of any ML pipeline.
- **Use count fingerprints for regression**, bit fingerprints for similarity / classification.
- **Cache fingerprints to disk** as int8 / uint8 arrays; recomputing them on a 10M-compound library on every screen is wasteful.

## References

[^qed]: Bickerton GR, Paolini GV, Besnard J, Muresan S, Hopkins AL. Quantifying the chemical beauty of drugs. *Nat Chem.* 2012;4(2):90–98. [doi:10.1038/nchem.1243](https://doi.org/10.1038/nchem.1243)
[^sa]: Ertl P, Schuffenhauer A. Estimation of synthetic accessibility score of drug-like molecules. *J Cheminform.* 2009;1:8. [doi:10.1186/1758-2946-1-8](https://doi.org/10.1186/1758-2946-1-8)

## Where to next

[QSAR / property prediction](qsar.md) — turning descriptors and fingerprints into activity / property models.
