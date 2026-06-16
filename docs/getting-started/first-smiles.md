# 2. Your first SMILES

> SMILES strings are the lingua franca of cheminformatics. By the end of this page you can parse them, canonicalise them, compute a fingerprint, and draw a molecule.

## SMILES in one minute

A **SMILES** (Simplified Molecular-Input Line-Entry System) is a 1-D string encoding a molecular graph. Atoms are written by element symbol; bonds are implicit between consecutive atoms; ring closures use digits; branches use parentheses; aromaticity is lowercase. Aspirin is `CC(=O)Oc1ccccc1C(=O)O`. Caffeine is `Cn1cnc2c1c(=O)n(C)c(=O)n2C`.

SMILES are **not unique** — the same molecule can be written many ways. The fix is *canonicalisation*: a deterministic algorithm that picks one representation. RDKit does this by default.

```python
from rdkit import Chem

mol = Chem.MolFromSmiles("OC(=O)c1ccccc1OC(C)=O")
canonical = Chem.MolToSmiles(mol)
print(canonical)  # CC(=O)Oc1ccccc1C(=O)O — canonical aspirin
```

Two SMILES are the same molecule iff their canonical forms match. This is the only legitimate way to deduplicate compound libraries; never compare raw strings.

## The other three representations you will meet

| Format | What it captures | When to use |
| --- | --- | --- |
| **SMILES** | Connectivity, bond order, stereo (optional) | Storage, ML input, fast similarity |
| **InChI / InChIKey** | Canonical hash of the molecular graph | Cross-database lookup |
| **Molfile / SDF** | 2D or 3D coords + connectivity | Pipelines that depend on geometry |
| **PDB / mol2** | 3D coords + (rough) bonding | Structure-based work, docking, MD |

The **InChIKey** is the 27-character hash you put in URLs and database joins. ChEMBL, PubChem, and DrugBank all index by it.

```python
inchi = Chem.MolToInchi(mol)
key   = Chem.MolToInchiKey(mol)
print(key)   # BSYNRYMUTXBXSQ-UHFFFAOYSA-N (aspirin's InChIKey)
```

## Three descriptors every cheminformatician memorises

```python
from rdkit.Chem import Descriptors, Lipinski

mw      = Descriptors.MolWt(mol)         # molecular weight, ~180 for aspirin
clogp   = Descriptors.MolLogP(mol)       # octanol-water partition (Crippen)
hba     = Lipinski.NumHAcceptors(mol)    # H-bond acceptors
hbd     = Lipinski.NumHDonors(mol)       # H-bond donors
tpsa    = Descriptors.TPSA(mol)          # polar surface area
rotb    = Descriptors.NumRotatableBonds(mol)

print(f"MW {mw:.1f}, cLogP {clogp:.2f}, HBA {hba}, HBD {hbd}, TPSA {tpsa:.1f}, RotB {rotb}")
```

These five (plus rotatable bonds) underlie almost every "rule of thumb" you'll encounter:

- **Lipinski's rule of five** [Lipinski et al., 1997](https://doi.org/10.1016/S0169-409X(96)00423-1)[^lipinski] — oral bioavailability sweet spot. MW < 500, cLogP < 5, HBA ≤ 10, HBD ≤ 5. One violation is fine; two is a warning.
- **Veber rules** [Veber et al., 2002](https://doi.org/10.1021/jm020017n)[^veber] — RotB ≤ 10 and TPSA ≤ 140 Å² for good oral absorption.
- **CNS MPO** [Wager et al., 2010](https://doi.org/10.1021/cn100008c)[^cns-mpo] — central-nervous-system multi-parameter score, used in CNS programmes.

!!! warning "These are filters, not laws"
    The rule of five is descriptive of *historical* oral drugs. Modern modalities (PROTACs, macrocycles, peptides) routinely violate it. Use rules as soft priors, not as gates.

## Compute a fingerprint

A **molecular fingerprint** is a fixed-length bit-vector encoding substructures. The default workhorse is the **Morgan / ECFP4** fingerprint (radius 2, 2048 bits).

```python
from rdkit.Chem import rdFingerprintGenerator

gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fp = gen.GetFingerprint(mol)
print(fp.GetNumBits(), fp.GetNumOnBits())  # 2048 total, ~30 set
```

Tanimoto similarity between two fingerprints is the canonical drug-discovery similarity metric:

```python
from rdkit import DataStructs

ibuprofen = Chem.MolFromSmiles("CC(C)Cc1ccc(C(C)C(=O)O)cc1")
fp2 = gen.GetFingerprint(ibuprofen)
sim = DataStructs.TanimotoSimilarity(fp, fp2)
print(f"Aspirin–ibuprofen Tanimoto: {sim:.3f}")   # ~0.18
```

Two molecules with Tanimoto ≥ 0.85 on ECFP4 are usually treated as "similar". 0.7–0.85 is "related". Below 0.5 is essentially unrelated.

## Draw the molecule

```python
from rdkit.Chem.Draw import rdMolDraw2D

drawer = rdMolDraw2D.MolDraw2DCairo(400, 400)
drawer.DrawMolecule(mol)
drawer.FinishDrawing()
drawer.WriteDrawingText("aspirin.png")
```

That single PNG, with an InChIKey caption, is the minimum-viable molecule figure for any slide.

## In practice

- **Always canonicalise** before you store, deduplicate, or compare.
- **Always log MW, cLogP, TPSA, HBA, HBD, RotB** in any compound report.
- **Always use ECFP4 (radius 2, 2048 bits)** as your default similarity descriptor unless you have a reason not to. Document the radius and bit length anywhere you share results.
- **InChIKey is the right database join key**; SMILES is not.

## References

[^lipinski]: Lipinski CA, Lombardo F, Dominy BW, Feeney PJ. Experimental and computational approaches to estimate solubility and permeability in drug discovery and development settings. *Adv Drug Deliv Rev.* 1997;23(1–3):3–25. [doi:10.1016/S0169-409X(96)00423-1](https://doi.org/10.1016/S0169-409X(96)00423-1)
[^veber]: Veber DF, Johnson SR, Cheng H-Y, Smith BR, Ward KW, Kopple KD. Molecular properties that influence the oral bioavailability of drug candidates. *J Med Chem.* 2002;45(12):2615–2623. [doi:10.1021/jm020017n](https://doi.org/10.1021/jm020017n)
[^cns-mpo]: Wager TT, Hou X, Verhoest PR, Villalobos A. Moving beyond rules: the development of a central nervous system multiparameter optimization (CNS MPO) approach to enable alignment of druglike properties. *ACS Chem Neurosci.* 2010;1(6):435–449. [doi:10.1021/cn100008c](https://doi.org/10.1021/cn100008c)

## Where to next

[Your first virtual screen](first-screen.md) — turn a query molecule into a ranked hit list against a small library.
