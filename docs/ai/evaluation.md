# Evaluation pitfalls

> Why your model's AUROC of 0.95 means nothing. The chapter that prevents most drug-AI embarrassments.

## The single most common mistake

**Random train/test split.** A QSAR model trained on a random split of a series-rich dataset learns the *series* — when the test set is from the same series, performance looks excellent. Deployed on a new series, it collapses.

Always use **scaffold split** or **time split** for reported numbers. Random split is for "does the pipeline even run" sanity check.

## Splitting strategies

| Split | What it simulates | When to use |
| --- | --- | --- |
| Random | nothing realistic | code sanity only |
| Scaffold | a new chemical series | the default for prospective evaluation |
| Time | the actual production scenario | when timestamps are available |
| Cluster (FP-Tanimoto) | "test is far from train" | benchmarking |
| Series-out | held-out series in a multi-series dataset | the harshest split |
| Out-of-distribution / OOD | inference on a different distribution | for distribution-shift studies |

## Activity cliffs

[MoleculeACE](https://doi.org/10.1021/acs.jcim.2c01073) showed that most reported deep-learning advances on standard benchmarks **do not translate** to activity-cliff-rich subsets. A model that wins on overall AUROC and flops on the cliff subset is interpolating, not understanding.

Report cliff-subset performance separately when you can.

## Metrics — what to actually report

For classification:

- **AUROC** — useful only when class balance and operating threshold are sensible.
- **AUPRC** — better than AUROC under class imbalance.
- **Calibration plot + Brier score** — non-optional for any model used for triage.
- **Confusion matrix** at the deployed threshold.

For regression:

- **R²** — scale-free.
- **RMSE / MAE** — same units as the label.
- **Spearman rank correlation** — rank-only, robust to monotonic distortions.
- **Bootstrap CIs** on all of the above.

A single number is never enough. Report at least 4 metrics with bootstrapped intervals.

## Bootstrapping

```python
import numpy as np
from sklearn.metrics import roc_auc_score

def bootstrap_auroc(y_true, y_pred, n_boot=1000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    scores = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        scores.append(roc_auc_score(y_true[idx], y_pred[idx]))
    return np.median(scores), np.percentile(scores, [2.5, 97.5])
```

A point estimate of 0.83 vs 0.85 may both have 95% CIs spanning 0.78–0.90. Reporting only the points implies a difference that the data does not support.

## Distribution shift

A model trained on past chemistry may have its predictions silently degrade as the team explores new scaffolds. Two diagnostics:

1. **Track prediction-vs-experiment over time** on prospective compounds. If correlation degrades, retrain.
2. **Compute distance to training set** (Tanimoto to nearest training compound). High-distance predictions are out of domain.

## Domain of applicability

A QSAR model is only valid within the chemical region it was trained on. Quantify the region:

- **Nearest-neighbour Tanimoto** to training set. Threshold: 0.4–0.5 (problem-dependent).
- **Feature-space density** — k-NN density, isolation forest, Mahalanobis distance.
- **Conformal prediction** — formal coverage guarantees.

Compounds outside the applicability domain should be flagged, not relied on.

## Selection bias

Training compounds are not random. They are designed by chemists for reasons that correlate with activity. Predictions on those reasons may not generalise to compounds *not* designed by the same chemists.

A subtler effect: training on top of a hit series means the training set is enriched for that series. Predictions on a different series are silently out-of-distribution.

## A reporting template

A defensible QSAR / property-prediction publication reports:

1. Dataset source, size, timestamp, deduplication policy.
2. Featurisation, exact preprocessing.
3. Train/test split *type* (scaffold / time / series), with rationale.
4. Hyperparameter selection protocol (held-out validation, not test).
5. Multiple metrics with bootstrapped CIs.
6. Baseline (RF + ECFP) for comparison.
7. Per-split variance, not just mean.
8. Calibration (Brier / reliability diagram).
9. OOD performance check.
10. Failure-mode analysis (where does it break?).

This is the minimum. Falling short of it produces papers that don't reproduce.

## In practice

- **Scaffold split as the default.** Always.
- **Bootstrap your numbers.** Always.
- **Calibration is half the story.** Always.
- **Pre-register your evaluation** before model selection if you can.
- **Beat the RF baseline** before publishing the deep result.

## Where to next

[Uncertainty & calibration](uncertainty.md) — the related half of this chapter.
