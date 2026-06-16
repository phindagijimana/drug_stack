# Tutorial 5 — Generative design

> REINVENT 4 against a multi-parameter objective. From "give me molecules for kinase X" to a ranked list of 50.

**Prerequisites**: [Generative chemistry](../molecular-design/generative.md), [MPO](../molecular-design/mpo.md), [REINVENT 4 docs](https://github.com/MolecularAI/REINVENT4).

## Install

```bash
pip install reinvent4
```

## The objective

For a kinase target with a known IC50 dataset:

```toml
# scoring.toml
[component.QED]
type = "QED"
weight = 1.0

[component.SAScore]
type = "SAScore"
weight = 0.5

[component.MW]
type = "MolecularWeight"
weight = 0.5
transform = { type = "double_sigmoid", high = 500, low = 200, coef_div = 50, coef_si = 20, coef_se = 20 }

[component.cLogP]
type = "SlogP"
weight = 0.5
transform = { type = "double_sigmoid", high = 4, low = 1, coef_div = 1, coef_si = 10, coef_se = 10 }

[component.kinase_pic50]
type = "PredictivePropertyComponent"
weight = 2.0
model_file = "kinase_qsar.joblib"
property = "pIC50"
transform = { type = "sigmoid", low = 6.5, high = 8.5 }
```

(The exact schema follows REINVENT 4's config format; check the docs.)

## Train

```bash
reinvent --config train.toml --scoring scoring.toml --output out/
```

`train.toml` selects a prior (Mol2Mol or REINVENT prior), sets RL hyperparameters, and points at the scoring config.

A typical training run:

- 1000–5000 RL steps.
- Batch size 64–128.
- KL anchoring to the prior (essential).

## Inspect the output

The output is a CSV of generated SMILES + scores. Filter:

- Validity, uniqueness, novelty (vs training set).
- Reject PAINS / Brenk.
- Cluster by scaffold and pick top-K from each cluster.

```python
import polars as pl
from rdkit import Chem
from rdkit.Chem.Scaffolds.MurckoScaffold import GetScaffoldForMol

gen = pl.read_csv("out/sampled.csv")
gen = gen.unique(subset=["smiles"])

# filter PAINS
from rdkit.Chem.rdfiltercatalog import FilterCatalog, FilterCatalogParams
params = FilterCatalogParams()
params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
params.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
cat = FilterCatalog(params)

def passes(smi):
    mol = Chem.MolFromSmiles(smi)
    return mol is not None and not cat.HasMatch(mol)

gen = gen.filter(pl.col("smiles").map_elements(passes))

# cluster by scaffold and pick top 5 per cluster
def scaffold(smi):
    return Chem.MolToSmiles(GetScaffoldForMol(Chem.MolFromSmiles(smi)))

gen = gen.with_columns(scaffold=pl.col("smiles").map_elements(scaffold))
gen = gen.sort("total_score", descending=True)
short = gen.group_by("scaffold").head(5).head(50)
short.write_csv("out/triaged.csv")
```

## Decision points called out

- **Choice of prior.** REINVENT's PRIOR is general; for kinase work, fine-tune on kinase actives first.
- **Reward shaping.** Geometric mean of normalised components > additive. The kinase score must dominate but not so much that ADMET / synthesisability collapse.
- **Uncertainty-aware scoring.** If the QSAR predictor has high uncertainty on a generated molecule, downweight the prediction.
- **Manual chemist triage non-optional.** Filter out 30%; the remaining 70% needs human review.

## Honest verdict

Generated molecules out of REINVENT 4 will look reasonable. They will *not* be a clinical candidate. They are *inputs to chemist triage*. The right success metric is "how many of the top 50 the chemist found worth ordering, and how many of those bound at all".

## Where to next

[Capstone — target to lead](capstone.md) — the full end-to-end synthesis exercise.
