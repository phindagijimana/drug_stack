# Statistics

> The chemistry-and-biology relevant subset. Hypothesis tests, confidence intervals, multiple comparisons, calibration. Light on theory, heavy on common mistakes.

The statistics you actually need are not the statistics most curricula start with. This page is the working subset.

## Vocabulary, once

- **Effect size** — the magnitude of the thing you're measuring. The point estimate (and its CI) is almost always more informative than a p-value.
- **Sampling distribution** — the distribution of the estimator across hypothetical repeated experiments. Underlies every CI and test.
- **Type I / Type II error** — false positive / false negative. With finite data you trade them off.
- **Power** — 1 − Type II error. The probability of detecting an effect if it is real, at a given α and effect size.

If you remember only one rule: **report effect sizes with CIs**. P-values are a distant third.

## Confidence intervals are more useful than p-values

A 95 % CI on IC50 difference of [−0.1, 1.4] log units tells the reader:

- The compound *might* be inactive (CI includes 0).
- It might be a 25× improvement.
- The data does not yet resolve which.

A "p = 0.06" tells the reader nothing they can act on. Show the interval.

## The hypothesis tests you will reach for

| Situation | Test |
| --- | --- |
| Two groups, continuous outcome, normal-ish | Welch's t-test |
| Two groups, continuous outcome, skewed | Mann-Whitney U / Wilcoxon |
| Many groups, continuous outcome | ANOVA (then a *post hoc* with multiple-comparison correction) |
| Categorical 2×2 | Fisher's exact for small N; χ² otherwise |
| Survival | Log-rank for groups; Cox for covariate-adjusted |
| Paired (same compound, different assay) | Paired t-test or Wilcoxon signed-rank |

For each, the modelling assumption that fails most often is **independence**. Compounds in the same series, assay runs in the same plate, patients from the same site — none are independent. Account with mixed-effects models when it matters.

## Multiple comparisons

If you do 1000 univariate tests, ~50 are "significant" at α=0.05 by chance.

Corrections:

- **Bonferroni** — divide α by the number of tests. Strict, often too strict.
- **Holm-Bonferroni** — sequentially apply with relaxed threshold. Less conservative, still controls FWER.
- **Benjamini-Hochberg (BH) FDR** — controls the expected fraction of false discoveries. Standard for omics.

For high-dimensional comparisons (genes, fingerprints, residues), BH FDR is the default; FWER is reserved for the few flagship comparisons.

```python
from statsmodels.stats.multitest import multipletests
reject, pvals_adj, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")
```

## Sample size and power

Before you run an experiment with N compounds, ask: **what effect would I be able to detect at this N**?

For a two-sample comparison of means:

\[
N \approx \frac{2 \cdot (z_{1-\alpha/2} + z_{1-\beta})^2 \cdot \sigma^2}{\delta^2}
\]

where σ is the SD of the measurement and δ is the effect size you want to detect with power 1−β.

A 16-compound pilot detects effect sizes around 1 SD with 80% power. A 100-compound study detects ~0.5 SD. Anything claiming to detect 0.1-SD differences from 10 compounds is dreaming.

## Calibration — the under-used quality measure

For a probabilistic model, **calibration** asks: when the model says "80% probability active", are 80% of those compounds actually active?

A miscalibrated model is dangerous even when its AUROC is high — you cannot use its probabilities to triage. Calibration plots (reliability diagrams) and Brier scores are the standard diagnostics.

```python
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
# fit and then plot prob_true vs prob_pred in a reliability diagram
```

## Common drug-discovery statistics mistakes

1. **Random train / test splits** — gives optimistic AUROCs that collapse on new chemistry. Use scaffold or time splits.
2. **One-shot AUROC** — report a confidence interval; bootstrap it.
3. **Mean IC50** — use median; IC50 is log-normal.
4. **Equating "selectivity" with a ratio of point estimates** — propagate the variance of both measurements.
5. **Ignoring batch effects** — different assay plates / days are not interchangeable.
6. **Cherry-picked test sets** — pick test before training, lock it, do not iterate against it.
7. **Reporting at α = 0.05** without a multiple-comparison correction.
8. **Counting "compounds active" without an activity threshold definition.**

## In practice

- Effect size + CI is the unit of useful statistical reporting.
- Bootstrap aggressively — every AUROC, every IC50 ratio, every Spearman.
- Multiple-comparison-correct everywhere you tested > 1 hypothesis.
- For ML: report calibration, not just discrimination.

## Where to next

[Mathematics](mathematics.md) — linear algebra, calculus, probability, optimisation. The minimum for the AI chapters.
