# Multi-parameter optimization (MPO)

> The actual objective. Potency alone produces molecules that fail. The chapter every project lead should read before opening a generative tool.

## Why MPO exists

A small molecule that succeeds clinically must, simultaneously:

- Engage its target potently.
- Be selective against close paralogs.
- Be orally bioavailable (or otherwise dosable).
- Cross the right barriers (BBB or not, depending).
- Not be metabolised too fast (or, in pro-drugs, exactly right).
- Not inhibit CYP3A4 at therapeutic concentrations.
- Not block hERG.
- Not be Ames-positive.
- Be synthesisable.
- Have acceptable IP.

A model that optimises only IC50 finds molecules that win on potency and fail on everything else. **The actual objective is multi-parameter.**

## Three approaches

### 1. Linear-weighted sum

```python
def score(mol, weights, predictors):
    return sum(w * f(mol) for w, f in zip(weights, predictors))
```

- **Pro**: dead simple, fits any optimiser.
- **Con**: weights are arbitrary, scales differ wildly, dominated by whichever term has the largest range.

Workable as a starting point if you normalise each term to [0, 1] and document the weights.

### 2. Desirability functions

[Harrington, 1965](https://doi.org/10.1080/00224065.1965.11980248); operationalised in drug-discovery as in [Bickerton et al., 2012](https://doi.org/10.1038/nchem.1243).

Each property maps via a *desirability function* into [0, 1]:

- **Smaller-the-better** (e.g. CL): \(d = 1\) below a target value, decays smoothly above.
- **Larger-the-better** (e.g. pIC50): mirror of above.
- **Target-window** (e.g. logP): triangle / trapezoid centred on the desirable range.

Composite desirability is the geometric mean:

\[
D = \left( \prod_i d_i \right)^{1/n}
\]

A single near-zero \(d_i\) tanks \(D\) — this is the right behaviour. A molecule that nails potency but fails hERG must not score well.

### 3. Pareto frontiers

Instead of collapsing to a scalar, maintain the set of molecules where no single property can be improved without worsening another.

- **Pro**: defensible, no arbitrary weights, captures trade-offs explicitly.
- **Con**: harder to optimise; harder to convey to a chemist asking "what's the top hit".

In practice, modern generative tools (REINVENT 4, OptunaSearch) support Pareto-style multi-objective optimisation. Pareto is the right framing for *exploration*; desirability is the right framing for *triage*.

## Worked example: CNS MPO

[Wager et al., 2010](https://doi.org/10.1021/cn100008c)[^cnsmpo]: a CNS-focused desirability score combining:

| Property | Desirable range | Notes |
| --- | --- | --- |
| cLogP | ≤ 3 | Lipophilicity, BBB penetration |
| cLogD7.4 | ≤ 2 | Ionised partition |
| MW | ≤ 360 Da | Permeability |
| TPSA | 40–90 Å² | BBB compatibility |
| HBD | ≤ 0.5 | BBB compatibility |
| pKa (most basic) | ≤ 8 | P-gp avoidance |

Each property gets a trapezoidal desirability; CNS MPO is the sum. CNS programs that consistently produce molecules with CNS MPO ≥ 4 (out of 6) achieve much better hit rates in PK studies.

## Building your own MPO

A realistic small-molecule MPO might look like:

```python
def mpo(mol):
    return desirability_geomean({
        "pIC50":      f_larger_is_better(qsar_predict(mol), target=8.0),
        "selectivity":f_larger_is_better(selectivity_predict(mol), target=2.0),  # log ratio
        "logD":       f_window(logd_predict(mol), low=1.0, high=3.5),
        "PAMPA":      f_larger_is_better(pampa_predict(mol), target=2e-6),
        "CLint":      f_smaller_is_better(clint_predict(mol), target=10),       # uL/min/mg
        "p_hERG":     f_smaller_is_better(herg_predict(mol), target=0.5),
        "p_AMES":     f_smaller_is_better(ames_predict(mol), target=0.3),
        "SA":         f_smaller_is_better(sa_score(mol), target=4),
    })
```

Each `*_predict` is a QSAR model with its own uncertainty. **Uncertainty-aware MPO** uses pessimistic estimates (mean − k·sd) instead of point predictions — this discourages the generator from exploiting model overconfidence in regions where it has no data.

## Failure modes

- **One predictor dominates the score** because its scale wasn't normalised.
- **The model rewards out-of-distribution chemistry** because the predictors are confidently wrong there.
- **The desirability function shape is too steep**, creating a non-smooth objective the optimiser can't navigate.
- **The MPO is set up against historical data** that doesn't represent the chemical space you're now exploring.
- **The chemist disagrees with the weights**. This is usually the chemist being right.

## In practice

- **Build the MPO with the chemist** in the room. They have priors on which property matters more.
- **Calibrate component models on their own splits**, then validate the composite MPO on a held-out series.
- **Inspect the top-scoring molecules manually** before any next-cycle commitment. The MPO is a heuristic; humans catch what it missed.
- **Use pessimistic uncertainty** to discourage OOD exploitation.

## References

[^cnsmpo]: Wager TT, Hou X, Verhoest PR, Villalobos A. Moving beyond rules: the development of a central nervous system multiparameter optimization (CNS MPO) approach to enable alignment of druglike properties. *ACS Chem Neurosci.* 2010;1(6):435–449. [doi:10.1021/cn100008c](https://doi.org/10.1021/cn100008c)

## Where to next

[Virtual screening](../screening/index.md) — applying these tools at library scale.
