# Absorption

> Will the drug get into the body when dosed? Solubility, permeability, oral bioavailability.

## The two-resistance problem

Oral absorption is gated by two things:

1. **Solubility** — the drug must dissolve in intestinal fluid.
2. **Permeability** — once dissolved, it must cross the intestinal epithelium into the portal circulation.

A drug with great permeability but terrible solubility never dissolves and is not absorbed. A drug with great solubility but no permeability sits in the gut and is excreted. Both have to be acceptable.

## Solubility

The relevant solubility is **kinetic solubility at intestinal pH** (~6–7 in the small intestine, ~1–2 in the stomach). Thermodynamic solubility (from crystal lattice) differs from kinetic (no equilibration time).

Standard predictors:

- **ESOL** (Delaney) — fast empirical model.
- **logS-AqSolDB** — community dataset, modern ML benchmarks.
- **OpenEye OEChem solubility** — commercial baseline.
- **Chemprop / GNN regressors** on AqSolDB ([Sorkun et al., 2019](https://doi.org/10.1038/s41597-019-0151-1)[^aqsoldb]) — current SOTA at ~0.6–0.8 log units RMSE.

A logS > -4 is good for oral; -4 to -5 is borderline; below -5 needs formulation work or modality change.

## Permeability

- **PAMPA** (parallel artificial membrane permeability assay) — passive permeability proxy.
- **Caco-2** — colonic cell-line monolayer; better captures active transport and efflux.
- **MDCK** — kidney-cell variant; often used for P-gp efflux assessment.

In silico, Caco-2 and PAMPA values can be predicted to AUROC ~0.8 for binary "permeable / non-permeable" labels. Continuous-value prediction is less accurate.

## Oral bioavailability — F

The fraction of an oral dose reaching systemic circulation. Compounded from:

- **Fraction dissolved** (Fa)
- **Fraction crossing the gut wall and not metabolised in the wall** (Fg)
- **Fraction surviving first-pass hepatic metabolism** (Fh)

\[
F = F_a \cdot F_g \cdot F_h
\]

Each component has its own predictor; multiplying gives a rough F estimate. Better: train an end-to-end F-predictor on rat / dog / human bioavailability data.

## The classical rules

| Rule | Statement |
| --- | --- |
| Lipinski's rule-of-five | MW < 500, cLogP < 5, HBA ≤ 10, HBD ≤ 5 |
| Veber | TPSA ≤ 140 Å², RotB ≤ 10 |
| Ghose | 160 < MW < 480, cLogP -0.4 to 5.6, refractivity 40–130 |
| Egan | logP ≤ 5.88, TPSA ≤ 131.6 Å² |

These describe historical oral drugs; new modalities (PROTACs, macrocycles) frequently violate them. Use as priors, not gates.

## Why drugs fail oral absorption

- **High crystallinity** — too stable in the solid form, low dissolution rate.
- **High polarity / many HBDs** — passive permeability collapses.
- **P-gp substrate** — pumped back out of cells.
- **Gut-wall CYP3A4 metabolism** — eaten by the enterocytes before reaching portal vein.

Modern formulation rescue:

- **Amorphous solid dispersions (ASD)** — improves solubility of poorly soluble drugs.
- **Nanocrystal suspensions** — increased surface area.
- **Salt forms / co-crystals** — modify dissolution behaviour.

A clever formulation can rescue a borderline drug; it cannot fix one with intrinsic permeability < 1 nm/s.

## In practice

- **Predict logS and PAMPA at compound design time.** Cheap, mature, immediately useful.
- **Don't fight Lipinski for the sake of it.** New modalities can violate the rules; conventional small molecules ignoring the rules usually fail.
- **Test permeability in two systems** (PAMPA + Caco-2) before believing it. They disagree usefully when efflux or active transport matters.

## References

[^aqsoldb]: Sorkun MC, Khetan A, Er S. AqSolDB, a curated reference set of aqueous solubility and 2D descriptors for a diverse set of compounds. *Sci Data.* 2019;6:143. [doi:10.1038/s41597-019-0151-1](https://doi.org/10.1038/s41597-019-0151-1)

## Where to next

[Distribution](distribution.md) — once in circulation, where does it go?
