# Cheminformatics

> Working fluency in RDKit. Parsing, canonicalising, computing descriptors, generating fingerprints, doing substructure search, applying SMARTS transformations.

This is the chapter the rest of the handbook relies on more than any other. Skim if you are fluent; otherwise read carefully.

## RDKit object hierarchy

```python
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, Descriptors

mol = Chem.MolFromSmiles("Cn1cnc2c1c(=O)n(C)c(=O)n2C")   # caffeine
```

A `Mol` is a graph of `Atom` and `Bond` objects, plus optional **conformers** (3D coordinate sets). Every downstream operation starts from a `Mol`.

```python
mol.GetNumAtoms(), mol.GetNumBonds()         # 14, 15
for atom in mol.GetAtoms():
    print(atom.GetIdx(), atom.GetSymbol(), atom.GetIsAromatic())
```

## Canonicalisation

Always canonicalise before storage or comparison.

```python
canonical = Chem.MolToSmiles(mol)             # default is canonical
inchikey  = Chem.MolToInchiKey(mol)           # the database join key
```

## 3D coordinates

```python
mol_h = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol_h, randomSeed=0xf00d)
AllChem.UFFOptimizeMolecule(mol_h)
```

`EmbedMolecule` generates a random 3D conformer; the optimiser then relaxes it with a force field (UFF / MMFF94). For docking-quality 3D, use ETKDG followed by MMFF94s minimisation.

## Descriptors

A few hundred molecular descriptors ship with RDKit. The ones you actually use:

```python
from rdkit.Chem import Descriptors as D

D.MolWt(mol)               # MW
D.MolLogP(mol)             # Crippen logP
D.TPSA(mol)                # topological polar surface area
D.NumHAcceptors(mol)
D.NumHDonors(mol)
D.NumRotatableBonds(mol)
D.NumAromaticRings(mol)
D.HeavyAtomCount(mol)
D.RingCount(mol)
D.FractionCSP3(mol)
D.qed(mol)                 # quantitative estimate of drug-likeness (Bickerton et al.)
```

## Fingerprints

The three you should know:

```python
from rdkit.Chem import rdFingerprintGenerator as rfg

morgan = rfg.GetMorganGenerator(radius=2, fpSize=2048)
rdkit_topo = rfg.GetRDKitFPGenerator(fpSize=2048)
atom_pair = rfg.GetAtomPairGenerator(fpSize=2048)

fp = morgan.GetFingerprint(mol)
fp_count = morgan.GetCountFingerprint(mol)   # counts, not bits
```

- **Morgan / ECFP4 (radius 2, 2048 bits)** — the default for similarity, virtual screening, and most QSAR. Captures local circular substructures.
- **MACCS keys (166 bits)** — small, interpretable, fast; weaker discriminative power.
- **RDKit topological** — path-based; good for small molecules where Morgan struggles.
- **Atom-pair / topological torsion** — useful for scaffold-hopping signal.

## Tanimoto and friends

```python
from rdkit import DataStructs
DataStructs.TanimotoSimilarity(fp1, fp2)         # standard
DataStructs.DiceSimilarity(fp1, fp2)             # bias toward small mols
DataStructs.CosineSimilarity(fp1, fp2)
```

Tanimoto on Morgan is the canonical default. Anything else, document why.

## SMARTS — substructure queries

SMARTS is a query language for molecular substructures.

```python
sulfonamide = Chem.MolFromSmarts("[#6][S](=O)(=O)[N]")
mol.HasSubstructMatch(sulfonamide)
mol.GetSubstructMatches(sulfonamide)              # all matches
```

A few patterns to keep around:

```python
patterns = {
    "carboxylic_acid": "C(=O)[OH]",
    "primary_amine":   "[NX3;H2;!$(NC=O)]",
    "amide":           "[NX3][CX3](=[OX1])",
    "sulfonamide":     "[#6][S](=O)(=O)[N]",
    "michael_acceptor":"[CX3]=[CX3]-[CX3]=O",
    "aldehyde":        "[CX3H1](=O)",
    "nitro":           "[N+](=O)[O-]",
}
```

The full set of PAINS substructures is in the [Baell & Holloway, 2010](https://doi.org/10.1021/jm901137j)[^pains] supplement; RDKit ships a filter at `Chem.rdfiltercatalog.FilterCatalog`.

## SMARTS transformations (Reaction SMARTS)

For matched-molecular-pair (MMP) analyses and bioisostere replacement:

```python
from rdkit.Chem import AllChem

# replace a phenyl with a pyridyl
rxn = AllChem.ReactionFromSmarts("[c:1]1[cH:2][cH:3][cH:4][cH:5][cH:6]1>>[c:1]1[n:2][cH:3][cH:4][cH:5][cH:6]1")
products = rxn.RunReactants((mol,))
```

This is the same primitive generative-chemistry tools use; the difference is the rules come from learned models, not handwritten SMARTS.

## Standardisation — non-optional

Real-world SMILES are dirty: counter-ions, tautomers, mixtures, stereochemistry inconsistencies. Use a standardiser before you do anything else.

```python
from rdkit.Chem.MolStandardize import rdMolStandardize

cleaner   = rdMolStandardize.CleanupParameters()
neutraliser = rdMolStandardize.Reionizer()
tautomer  = rdMolStandardize.TautomerEnumerator()

mol_std = rdMolStandardize.Cleanup(mol)
mol_std = rdMolStandardize.ChargeParent(mol_std)
mol_std = tautomer.Canonicalize(mol_std)
```

A 30-line standardisation function avoids hours of "why does ChEMBL give a different number than PubChem".

## In practice

- **Canonicalise. Standardise. Use InChIKey for joins. Use ECFP4 for similarity.** These four rules cover 80 % of cheminformatics correctness bugs.
- **Wrap RDKit calls in `safe_*` functions** that return `None` on failure rather than raising. Useful in pipelines.
- **Cache fingerprints to disk.** Recomputing 10 M Morgan FPs is wasteful; store them once and reload.

## References

[^pains]: Baell JB, Holloway GA. New substructure filters for removal of pan assay interference compounds (PAINS). *J Med Chem.* 2010;53(7):2719–2740. [doi:10.1021/jm901137j](https://doi.org/10.1021/jm901137j)

## Where to next

[Structural biology](structural-biology.md) — PDBs, Ramachandran, ligand-binding sites, AlphaFold.
