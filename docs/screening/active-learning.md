# Active learning & iterative screens

> The most sample-efficient way to search a huge library. The only sane way to do it at 10⁹ compounds.

## The intuition

If a docking score is expensive and a model is cheap, the loop:

1. Dock a small random subset.
2. Train a model on those (dock_score | compound).
3. Use the model to *propose* the next subset — molecules predicted to score well that the model is uncertain about.
4. Dock those.
5. Retrain. Repeat.

…converges to "find all the high-scoring compounds" with a fraction of the docking calls a full screen would need.

The same loop works with experimental potency (slower, more expensive) replacing docking scores. That is how modern industry "ML-in-the-loop" screens actually work.

## Acquisition functions

The question "which compounds should we score next?" is the **acquisition function**. The main choices:

- **Greedy** — pick top-K predicted. Maximises exploitation; risks getting stuck in a local optimum.
- **Random** — robust to model collapse; under-exploits.
- **Upper-confidence bound (UCB)** — `mean + κ * sd`. Balances exploration and exploitation; κ controls.
- **Expected improvement (EI)** — Bayesian-optimisation classic; tractable for GPs and ensembles.
- **Thompson sampling** — pick the best under a draw from the posterior; very robust.
- **Diversity-aware** — combines any of the above with a clustering penalty to ensure variety.

For most ultra-large screening contexts, **UCB or Thompson sampling + diversity penalty** are the sweet spot.

## A canonical loop

```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# library: large pool of unscored compounds
labeled_smiles, labeled_scores = [], []
pool_smiles = list(library_smiles)
X_pool = featurise(pool_smiles)

# 1) seed with random sample
seed = np.random.choice(len(pool_smiles), size=200, replace=False)
seed_scores = dock_batch([pool_smiles[i] for i in seed])
labeled_smiles += [pool_smiles[i] for i in seed]
labeled_scores += seed_scores

for round_idx in range(10):
    # 2) train
    X_labeled = featurise(labeled_smiles)
    models = [RandomForestRegressor(n_estimators=200, random_state=k).fit(X_labeled, labeled_scores)
              for k in range(5)]
    preds  = np.stack([m.predict(X_pool) for m in models])
    mu     = preds.mean(axis=0)
    sd     = preds.std(axis=0)
    ucb    = mu + 2.0 * sd

    # 3) select next batch (top-K by UCB with diversity)
    batch_idx = diverse_top_k(ucb, X_pool, k=200)

    # 4) score
    batch_smis  = [pool_smiles[i] for i in batch_idx]
    batch_scores = dock_batch(batch_smis)

    # 5) update
    labeled_smiles += batch_smis
    labeled_scores += batch_scores
    pool_smiles = [s for i, s in enumerate(pool_smiles) if i not in set(batch_idx)]
    X_pool      = np.delete(X_pool, list(batch_idx), axis=0)
```

This 50-line loop, with diversity-aware UCB and a 5-model RF ensemble, is the prototype of essentially every modern ultra-large-screening pipeline.

## How much does it save?

Empirically: an active-learning screen of a 10⁹-compound library identifies > 80% of the top 1% with only ~10⁻³ of the compounds actually scored. [Graff et al., 2021](https://doi.org/10.1039/D1SC03044F)[^graff] (MolPAL) characterised this for docking; subsequent industrial work (e.g. Boltz-2, AstraZeneca papers) reports similar savings.

## When AL fails

- **Single-shot generative + score** is a poor fit. AL assumes you can re-score; if you cannot, it degenerates.
- **The model collapses on a weak scaffold** and over-exploits — diversity penalty fixes this.
- **The cost per "experiment" is too variable** to amortise (some compounds dock in seconds, some in hours). Use random subsampling within batches to smooth.
- **The "score" you are learning is the wrong thing.** AL on docking score still gives docking-hits, not necessarily binders.

## Experimental active learning

The biggest win is when "the experiment" is a *wet* assay, not a docking score.

- Round 1: synthesise + test 50 chemically diverse compounds from the virtual-screen top 10 000.
- Train a QSAR model on the wet data.
- Use the QSAR + uncertainty to propose the next 50.
- Iterate 4–8 rounds.

Several published industrial programs have reached lead-candidate quality in ≤ 8 rounds (≤ 400 synthesised compounds) [Konze et al., 2019](https://doi.org/10.1021/acs.jcim.9b00367)[^konze]; [Reker, 2019](https://doi.org/10.1016/j.drudis.2019.02.013)[^reker].

This is the single highest-leverage technique in modern small-molecule discovery.

## In practice

- **Always seed with a *diverse* random batch**, not "the top of a similarity search". Otherwise the model learns one neighbourhood and never explores.
- **Use a deep ensemble or RF for calibrated uncertainty.** Bayesian-deep alternatives exist; ensembles work and are simple.
- **Pair AL with diversity-aware selection** — top-K by UCB always — without diversity converges to one scaffold.
- **Watch the saturation curve.** When new batches stop improving the model's top-K predictions, stop and triage.

## References

[^graff]: Graff DE, Shakhnovich EI, Coley CW. Accelerating high-throughput virtual screening through molecular pool-based active learning. *Chem Sci.* 2021;12:7866–7881. [doi:10.1039/D1SC03044F](https://doi.org/10.1039/D1SC03044F)
[^konze]: Konze KD, Bos PH, Dahlgren MK, et al. Reaction-based enumeration, active learning, and free energy calculations to rapidly explore synthetically tractable chemical space and optimize potency of cyclin-dependent kinase 2 inhibitors. *J Chem Inf Model.* 2019;59(9):3782–3793. [doi:10.1021/acs.jcim.9b00367](https://doi.org/10.1021/acs.jcim.9b00367)
[^reker]: Reker D. Practical considerations for active machine learning in drug discovery. *Drug Discov Today Technol.* 2019;32–33:73–79. [doi:10.1016/j.drudis.2019.02.013](https://doi.org/10.1016/j.drudis.2019.02.013)

## Where to next

[Hit triage](hit-triage.md) — turning a ranked list into a synthesis-and-test plan.
