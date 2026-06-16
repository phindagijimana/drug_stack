# QSAR / property prediction

> The discipline of fitting "structure → activity" (or "structure → property") models. Classical and modern. Where most of practical computational chemistry actually lives.

## The basic framing

Given a dataset of (molecule, label) pairs, learn a function molecule → label that generalises. Labels can be:

- Continuous: pIC50, pKa, logP, logS, melting point, CL.
- Binary: active / inactive, hERG hit / non-hit, AMES positive / negative.
- Multi-task: a vector of properties at once.

The trick is *what generalisation means*. A model that predicts well on a random hold-out but collapses on a new chemical series is useless to a chemist. See [Evaluation pitfalls](../ai/evaluation.md).

## The hierarchy of models

| Model | Data regime | Notes |
| --- | --- | --- |
| Mean baseline | always | sanity check; any "ML" must beat it |
| k-NN on Tanimoto | < 200 mols | hard to beat for activity-by-analogy |
| Linear regression on descriptors | small | interpretable; weak on non-linear SAR |
| Random forest on ECFP | 200–10k | the workhorse; default; calibrated probabilities |
| Gradient-boosted trees (XGBoost, LightGBM) | 1k–100k | often beats RF; needs careful regularisation |
| SVM | small/medium | strong on small data with kernels |
| Gaussian process | small | calibrated uncertainty out of the box |
| Multitask NN on ECFP | 10k+ across multiple endpoints | transfer between related properties |
| Message-passing NN (Chemprop, MPNN) | 5k+ | strong on regression of physical properties |
| 3D equivariant NN | structure-dependent tasks | for binding-affinity prediction |
| Pretrained molecular LM + head | data-poor | often best when n < 1000 |

## A canonical baseline pipeline

```python
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold

gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

def fp(smi):
    mol = Chem.MolFromSmiles(smi)
    return np.zeros(2048) if mol is None else np.array(gen.GetFingerprint(mol))

X = np.stack([fp(s) for s in df["smiles"]])
y = df["pIC50"].values

# scaffold split, not random
scaffolds = df["scaffold_id"].values
cv = GroupKFold(n_splits=5)

scores = []
for train, test in cv.split(X, y, groups=scaffolds):
    m = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=0)
    m.fit(X[train], y[train])
    scores.append(m.score(X[test], y[test]))
print("scaffold-CV R²:", np.mean(scores), np.std(scores))
```

This is the right shape for almost any "predict activity from structure" project. Variations:

- Switch RF for XGBoost when n > 1k.
- Switch ECFP for descriptors + ECFP concatenated when physchem matters.
- Switch scaffold-split for time-split when you have timestamps.

## Chemprop / message-passing networks

When data exceeds ~5k and the structure-property relationship is smooth, message-passing networks (Chemprop in particular) often beat fingerprints + GBDT [Yang et al., 2019](https://doi.org/10.1021/acs.jcim.9b00237)[^chemprop]; updated comparisons in [Heid et al., 2024](https://doi.org/10.1021/acs.jcim.3c01250)[^chemprop2].

```bash
chemprop train \
    --data_path train.csv \
    --task_type regression \
    --target_columns pIC50 \
    --split_type scaffold_balanced \
    --num_folds 5 \
    --epochs 100
```

Notes from experience:

- Chemprop is opinionated. Read the defaults; do not tune for tuning's sake.
- Pretraining on activity-poor but property-rich data sometimes helps; sometimes hurts.
- The biggest win is multitask training across related endpoints (multiple kinases, multiple ADMET properties).

## Activity cliffs

A small chemical change producing a huge activity change. **The hardest case for QSAR** because the smoothness assumption fails.

Tools to study activity cliffs:

- **MMP / Matched-molecular-pair analysis** ([Kenny & Sadowski, 2005](https://doi.org/10.1007/0-387-23854-3_11) and many extensions) decomposes a series into single-substituent changes.
- **MoleculeACE** benchmark [Tilborg et al., 2022](https://doi.org/10.1021/acs.jcim.2c01073)[^ace] explicitly tests cliff-handling.

If your model crushes the random-split AUC but flops on the MoleculeACE cliff sets, you have a QSAR model that interpolates known SAR but does not understand pocket pharmacology.

## Multitask, transfer, few-shot

Where the data is sparse but you have related data:

- **Multitask Chemprop** — co-train across kinase panels.
- **Transfer learning** — pretrain on a large ChEMBL bioactivity set, fine-tune on your assay.
- **Meta-learning / few-shot** — MAML and friends; promising in the lab, mixed in production.
- **Pretrained LMs (ChemBERTa, MolFormer) + head** — strong when n < 200.

## Uncertainty

A QSAR model used for triage *must* report calibrated uncertainty. A high-confidence wrong prediction is worse than no prediction.

- **Random forests** give uncertainty via tree-variance, often well-calibrated.
- **Deep ensembles** (5–10 independently-trained networks) are the standard NN approach.
- **Monte-Carlo dropout** is cheap but often miscalibrated.
- **Gaussian processes** are gold-standard but scale poorly.

See [AI / ML → Uncertainty & calibration](../ai/uncertainty.md).

## In practice

- **Random-forest on ECFP is the bar**. Any deeper model must beat it on a *scaffold split*, not a random one.
- **Report scaffold-split R² / RMSE / AUROC with bootstrapped CIs**. A point estimate at AUROC 0.83 is not enough.
- **Multi-output multitask training is the highest-leverage upgrade** if you have correlated endpoints (ADMET panels, kinase panels).
- **Always report calibration**, not just discrimination.

## References

[^chemprop]: Yang K, Swanson K, Jin W, et al. Analyzing learned molecular representations for property prediction. *J Chem Inf Model.* 2019;59(8):3370–3388. [doi:10.1021/acs.jcim.9b00237](https://doi.org/10.1021/acs.jcim.9b00237)
[^chemprop2]: Heid E, Greenman KP, Chung Y, et al. Chemprop: a machine learning package for chemical property prediction. *J Chem Inf Model.* 2024;64(1):9–17. [doi:10.1021/acs.jcim.3c01250](https://doi.org/10.1021/acs.jcim.3c01250)
[^ace]: van Tilborg D, Alenicheva A, Grisoni F. Exposing the limitations of molecular machine learning with activity cliffs. *J Chem Inf Model.* 2022;62(23):5938–5951. [doi:10.1021/acs.jcim.2c01073](https://doi.org/10.1021/acs.jcim.2c01073)

## Where to next

[Generative chemistry](generative.md) — going from "predict" to "design".
