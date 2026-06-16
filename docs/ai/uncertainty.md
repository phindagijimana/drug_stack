# Uncertainty & calibration

> The most under-used tool in industry drug-AI. Ensembles, GPs, conformal prediction, and how to actually act on a model's "I don't know".

## Why uncertainty matters more here than in generic ML

In drug discovery, every model prediction triggers a real-world action: synthesise this molecule, advance this lead, kill this series. **A high-confidence wrong prediction is worse than no prediction**, because it consumes resources irreversibly.

Without uncertainty, a model that is 95% accurate looks the same as one that is 95% accurate but lies confidently when wrong. The latter is dangerous.

## The two flavours of uncertainty

- **Aleatoric** — irreducible noise. Assay variability, replicate variance.
- **Epistemic** — model ignorance. Test compound is far from anything the model has seen.

In drug discovery, **epistemic uncertainty dominates** because chemical space is enormous and labelled data is sparse. Generic NN losses ignore epistemic uncertainty entirely.

## Methods that estimate uncertainty

| Method | Aleatoric | Epistemic | Cost |
| --- | --- | --- | --- |
| Random forest tree variance | partial | partial | free |
| Gaussian process | yes | yes | O(n³) |
| Deep ensemble (5–10 models) | yes | yes | 5–10× train cost |
| MC dropout | partial | partial | small overhead |
| Bayesian last layer / SWAG | partial | yes | small |
| Conformal prediction | aleatoric (well calibrated) | no | calibration set |
| Evidential deep learning | yes | yes | overhead at train |

For drug discovery, **deep ensembles + conformal prediction** is the strongest practical combination. Deep ensembles capture epistemic uncertainty; conformal prediction gives finite-sample coverage guarantees.

## Calibration

A model is **calibrated** if when it predicts "80% probability active", 80% of those compounds turn out active. Most modern NNs are not calibrated out of the box.

Standard diagnostics:

- **Reliability diagram** — bin predictions by probability, plot empirical positive rate.
- **Expected calibration error (ECE)** — average bin-wise mismatch.
- **Brier score** — squared error on probabilities.

Standard fixes:

- **Temperature scaling** — one-parameter fit on a calibration set; fast, often sufficient.
- **Isotonic regression** — non-parametric; needs more calibration data.
- **Platt scaling** — sigmoid fit; older, sometimes better than temperature.

```python
from sklearn.isotonic import IsotonicRegression
iso = IsotonicRegression(out_of_bounds="clip")
iso.fit(probs_val, y_val)
probs_calibrated = iso.transform(probs_test)
```

## Conformal prediction

Conformal prediction produces **prediction sets** (for classification) or **prediction intervals** (for regression) with formal coverage guarantees:

\[
P(y_{test} \in C(x_{test})) \geq 1 - \alpha
\]

The 1−α coverage is guaranteed under the exchangeability assumption.

For drug-discovery regression, **split-conformal** is the practical recipe:

1. Train your model on training set.
2. Compute residuals on a held-out calibration set.
3. The 1−α quantile of residuals gives the prediction-interval half-width.
4. At test time, predict y + [-quantile, +quantile] interval.

This works with *any* model — RF, NN, GP — without modification.

## Acting on uncertainty

The point of uncertainty is to *change the decision*. Three patterns:

1. **Selective prediction** — refuse to predict when uncertainty exceeds a threshold; flag for follow-up.
2. **Active learning** — query compounds with high uncertainty (see [Active learning](../screening/active-learning.md)).
3. **Pessimistic decision-making** — in MPO, replace the point prediction with `mean − k·sd` so the optimiser cannot exploit confidently-wrong regions.

## Common mistakes

- **Confusing variance with uncertainty.** Some models have high prediction variance but low epistemic uncertainty.
- **MC dropout as a substitute for ensembles.** MC dropout is often miscalibrated and underestimates epistemic uncertainty.
- **Calibration on the test set.** Wrong; you'll be too optimistic. Use a held-out calibration set.
- **Ignoring uncertainty downstream.** A model that emits uncertainty but is used as a point predictor wastes the signal.

## In practice

- **Train an ensemble** of 5 models. Use variance for epistemic uncertainty.
- **Calibrate** with temperature scaling or isotonic on a held-out set.
- **Run conformal prediction** for formal intervals on regression tasks.
- **Use pessimistic estimates** in MPO and active-learning loops.

## Where to next

[Regulatory & clinical deployment](regulatory.md) — when a model touches a patient.
