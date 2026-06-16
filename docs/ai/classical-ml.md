# Classical ML on molecules

> The bar deep learning has to beat. Random forest, GBDT, SVM on fingerprints + descriptors. The right default in most regimes.

The most under-used result in drug-AI: **a random forest on Morgan fingerprints often matches or beats a GNN with a fraction of the engineering cost** — *especially* in the small-data, scaffold-split regime that drug discovery lives in [Mayr et al., 2018](https://doi.org/10.1039/C8SC00148K)[^mayr]; [van Tilborg et al., 2022](https://doi.org/10.1021/acs.jcim.2c01073)[^ace].

## The default pipeline

```python
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator, Descriptors
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold

gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

DESC_FNS = [Descriptors.MolWt, Descriptors.MolLogP, Descriptors.TPSA,
            Descriptors.NumHAcceptors, Descriptors.NumHDonors,
            Descriptors.NumRotatableBonds, Descriptors.NumAromaticRings,
            Descriptors.FractionCSP3, Descriptors.qed]

def featurise(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    fp = np.array(gen.GetFingerprint(mol))
    descs = np.array([f(mol) for f in DESC_FNS])
    return np.concatenate([fp, descs])

X = np.stack([featurise(s) for s in df["smiles"]])
y = df["pIC50"].values
groups = df["scaffold"].values    # Murcko scaffold

cv = GroupKFold(n_splits=5)
scores = []
for tr, te in cv.split(X, y, groups):
    m = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=0)
    m.fit(X[tr], y[tr])
    scores.append(m.score(X[te], y[te]))
print("scaffold R²:", np.mean(scores), "±", np.std(scores))
```

This 25-line baseline reproduces or beats most published deep models on small-data benchmarks. **Show this beats your fancy model on a scaffold split before claiming improvement.**

## When to upgrade past RF

- **n > 5k mols, single endpoint**: try XGBoost / LightGBM with proper regularisation. Typically 1–2% AUROC gain.
- **n > 5k, multiple endpoints**: try multitask Chemprop. Transfer between related tasks often helps.
- **n < 200**: try pretrained molecular language models + small head; sometimes beats RF on small data.
- **n very large + structure-tied label**: try 3D-equivariant nets.

## SVMs with Tanimoto kernel

For very small datasets (< 500), an SVM with a Tanimoto kernel on Morgan FPs is a strong, often overlooked baseline.

```python
from sklearn.svm import SVR
import numpy as np

def tanimoto_kernel(X, Y):
    XX = X @ Y.T
    Xsum = X.sum(axis=1)[:, None]
    Ysum = Y.sum(axis=1)[None, :]
    return XX / (Xsum + Ysum - XX)

svr = SVR(kernel="precomputed", C=1.0)
K_train = tanimoto_kernel(X_train, X_train)
svr.fit(K_train, y_train)
```

## Gaussian processes

For tasks where calibrated uncertainty matters (active learning, Bayesian optimisation), GPs are the gold standard:

- **Pro**: calibrated uncertainty out of the box; great with small data.
- **Con**: O(n³) scaling; tricky kernel choice on molecules.

Sparse approximations and inducing points let GPs scale to 10k+ on a good GPU.

## Multitask classical ML

If you have correlated endpoints (e.g. multiple kinase IC50s), training one model jointly often helps. With trees / GBDT:

- **MultiOutputRegressor wrappers** treat each endpoint independently — no transfer.
- **scikit-multilearn** offers chained / stacked classifiers.
- **NNs are usually the right tool** for multi-output transfer at scale.

## Featurisation matters more than algorithm

The single biggest variance source: which fingerprint, which descriptors.

- **ECFP4 + 10 physchem** is a strong default.
- **ECFP6 + ECFP4** concatenation occasionally helps.
- **Add atom-pair fingerprints** for scaffold-hopping signal.
- **Add learned embeddings (ChemBERTa, MolFormer)** for very small data.

## In practice

- **RF on ECFP + physchem on a scaffold split is the bar.** Always run it. Always report it.
- **For multitask, use Chemprop.** For single-task, classical ML.
- **Calibrate the model** — see [Uncertainty](uncertainty.md). An RF that says "I don't know" is more useful than a deeper model that confidently lies.
- **Beat the baseline on a scaffold split**, not a random one.

## References

[^mayr]: Mayr A, Klambauer G, Unterthiner T, et al. Large-scale comparison of machine learning methods for drug target prediction on ChEMBL. *Chem Sci.* 2018;9:5441–5451. [doi:10.1039/C8SC00148K](https://doi.org/10.1039/C8SC00148K)
[^ace]: van Tilborg D, Alenicheva A, Grisoni F. Exposing the limitations of molecular machine learning with activity cliffs. *J Chem Inf Model.* 2022;62(23):5938–5951. [doi:10.1021/acs.jcim.2c01073](https://doi.org/10.1021/acs.jcim.2c01073)

## Where to next

[Deep learning for chemistry](deep-learning.md) — when and how it actually helps.
