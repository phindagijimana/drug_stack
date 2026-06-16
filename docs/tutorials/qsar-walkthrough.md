# Tutorial 2 — QSAR walkthrough

> Train a QSAR model from a CSV of (SMILES, pIC50) to a calibrated, scaffold-validated, ready-to-deploy predictor.

**Prerequisites**: [Cheminformatics](../fundamentals/foundations/cheminformatics.md), [Classical ML](../ai/classical-ml.md), [Evaluation pitfalls](../ai/evaluation.md).

## The data

Use a ChEMBL bioactivity slice for a well-studied target — e.g. CHEMBL244 (Factor Xa).

Download via `chembl_downloader` or the API; the input table:

| chembl_id | smiles | pIC50 |
| --- | --- | --- |
| CHEMBL... | C... | 7.45 |
| ... | ... | ... |

Aim for ~2 000–10 000 rows with strict `standard_relation = '='` filtering.

## The script

```python
import polars as pl
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator, Descriptors
from rdkit.Chem.Scaffolds.MurckoScaffold import GetScaffoldForMol
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold
import joblib

# 1) load
df = pl.read_csv("factor_xa.csv")
print(df.shape)

# 2) standardise + scaffold
def scaffold(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None: return None
    return Chem.MolToSmiles(GetScaffoldForMol(mol))

df = df.with_columns(
    scaffold=pl.col("smiles").map_elements(scaffold),
).drop_nulls(["scaffold"])

# 3) featurise
gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

def fp(smi):
    mol = Chem.MolFromSmiles(smi)
    return np.zeros(2048) if mol is None else np.array(gen.GetFingerprint(mol))

DESC = [Descriptors.MolWt, Descriptors.MolLogP, Descriptors.TPSA,
        Descriptors.NumHAcceptors, Descriptors.NumHDonors,
        Descriptors.NumRotatableBonds, Descriptors.NumAromaticRings,
        Descriptors.FractionCSP3, Descriptors.qed]

def featurise(smi):
    mol = Chem.MolFromSmiles(smi)
    fpa = np.zeros(2048) if mol is None else np.array(gen.GetFingerprint(mol))
    desc = np.zeros(len(DESC)) if mol is None else np.array([f(mol) for f in DESC])
    return np.concatenate([fpa, desc])

X = np.stack([featurise(s) for s in df["smiles"]])
y = df["pIC50"].to_numpy()
groups = df["scaffold"].to_numpy()

# 4) scaffold CV
cv = GroupKFold(n_splits=5)
scaff_r2 = []
scaff_rmse = []
for tr, te in cv.split(X, y, groups):
    m = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=0).fit(X[tr], y[tr])
    pred = m.predict(X[te])
    scaff_r2.append(np.corrcoef(pred, y[te])[0,1] ** 2)
    scaff_rmse.append(np.sqrt(np.mean((pred - y[te])**2)))
print("scaffold R²:", np.mean(scaff_r2), "±", np.std(scaff_r2))
print("scaffold RMSE:", np.mean(scaff_rmse), "±", np.std(scaff_rmse))

# 5) bootstrap CI on best fold
def bootstrap_r2(y_true, y_pred, n_boot=1000, rng=None):
    rng = rng or np.random.default_rng(0)
    n = len(y_true)
    out = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        out.append(np.corrcoef(y_pred[idx], y_true[idx])[0,1]**2)
    return np.median(out), np.percentile(out, [2.5, 97.5])

# 6) fit final model on all data
final = RandomForestRegressor(n_estimators=1000, n_jobs=-1, random_state=0).fit(X, y)
joblib.dump(final, "factor_xa_rf.joblib")

# 7) calibration helper — uncertainty from tree variance
preds_per_tree = np.stack([t.predict(X) for t in final.estimators_])
mean_pred = preds_per_tree.mean(axis=0)
sd_pred = preds_per_tree.std(axis=0)
```

## Decision points called out

- **Scaffold CV not random.** This is the bar for any number you report.
- **RandomForest with 500 trees, no tuning.** Often beats hyperparameter-tuned deep models on scaffold CV at this scale.
- **Bootstrap CIs.** A point estimate without CIs is misleading.
- **Tree-variance uncertainty.** Free; not perfectly calibrated; use it as a soft signal.
- **Domain of applicability check at deployment.** Reject predictions on compounds with low max-Tanimoto to training set.

## Going further

- Compare to Chemprop on the same scaffold split.
- Add a calibration step (isotonic regression) on a held-out set.
- Train a multi-task model across multiple coagulation-cascade targets.
- Use the trained model in [Generative design](generative-design.md) as a scoring component.

## Where to next

[Docking walkthrough](docking-walkthrough.md) — when you have a structure and need pocket-aware ranking.
