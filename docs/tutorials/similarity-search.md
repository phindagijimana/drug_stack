# Tutorial 1 — Similarity search on ChEMBL

> A 10 000-compound similarity screen against a query, with property filters and a clean output figure.

**Prerequisites**: [Getting started](../getting-started/index.md), [Cheminformatics](../fundamentals/foundations/cheminformatics.md).

## The problem

Given a known kinase inhibitor (here: **imatinib**), produce a ranked shortlist of structurally related ChEMBL compounds that pass basic property filters, with a clean 2D figure of the top 20.

## Data

Download a ChEMBL chemicalreps file (~2.4M compounds). For the tutorial, sample 10 000:

```bash
wget https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_chemreps.txt.gz
gunzip chembl_chemreps.txt.gz
```

## The script

```python
import polars as pl
import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator, Descriptors, Draw, AllChem
from rdkit.Chem.Scaffolds.MurckoScaffold import GetScaffoldForMol
from pathlib import Path

# 1) sample
df = pl.read_csv("chembl_chemreps.txt", separator="\t").sample(n=10_000, seed=0)

# 2) standardise + featurise
gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

def featurise(smi: str):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    return {
        "mol": mol,
        "canon": Chem.MolToSmiles(mol),
        "fp": gen.GetFingerprint(mol),
        "mw": Descriptors.MolWt(mol),
        "logp": Descriptors.MolLogP(mol),
        "tpsa": Descriptors.TPSA(mol),
        "hba": Descriptors.NumHAcceptors(mol),
        "hbd": Descriptors.NumHDonors(mol),
        "rotb": Descriptors.NumRotatableBonds(mol),
        "qed": Descriptors.qed(mol),
    }

records = [featurise(s) for s in df["canonical_smiles"]]
records = [r for r in records if r is not None]
for r, cid in zip(records, df["chembl_id"]):
    r["chembl_id"] = cid

# 3) property filter (rule of 5, mild)
filtered = [
    r for r in records
    if r["mw"] < 500 and r["logp"] < 5
    and r["hba"] <= 10 and r["hbd"] <= 5
    and r["rotb"] <= 10 and r["tpsa"] <= 140
]

print(f"After property filter: {len(filtered)}/{len(records)}")

# 4) similarity
qsmi = "Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1"   # imatinib
qmol = Chem.MolFromSmiles(qsmi)
qfp = gen.GetFingerprint(qmol)

for r in filtered:
    r["sim"] = DataStructs.TanimotoSimilarity(qfp, r["fp"])

filtered.sort(key=lambda r: -r["sim"])
top20 = filtered[:20]

# 5) draw
core = Chem.MolFromSmiles("Nc1nccc(-c2cccnc2)n1")
mols = []
legends = []
for r in top20:
    mol = r["mol"]
    AllChem.Compute2DCoords(mol)
    if mol.HasSubstructMatch(core):
        AllChem.GenerateDepictionMatching2DStructure(mol, core)
    mols.append(mol)
    legends.append(f"{r['chembl_id']}\nT={r['sim']:.2f}")

img = Draw.MolsToGridImage(mols, legends=legends, molsPerRow=4, subImgSize=(300, 250))
Path("out").mkdir(exist_ok=True)
img.save("out/hits.png")
print("wrote out/hits.png")
```

## What you should see

- Of the 10 000 sampled compounds, ~6500 pass the rule-of-five-mild filter.
- The Tanimoto distribution is heavy-tailed; the top hit usually has Tanimoto > 0.7.
- The top 20 are mostly 4-anilino-quinazoline / pyrimidine variants — the imatinib scaffold cousins.

## Decision points called out

- **Filter aggressiveness.** Tight rule-of-5 throws away kinase chemistry that violates it slightly. Loosen if your target accepts that.
- **Fingerprint choice.** ECFP4 is the default; ECFP6 over-fits the query; FCFP4 better for scaffold hopping.
- **Library size.** 10 000 is a tutorial scale. Real screens hit 10⁷+; see [Ultra-large libraries](../screening/ultra-large.md).
- **Single-query.** For multiple known actives, average or max Tanimoto across the active set.

## Where to go next

[QSAR walkthrough](qsar-walkthrough.md) — turn a hit list and assay data into a predictive model.
