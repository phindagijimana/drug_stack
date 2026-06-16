# Blood–brain barrier

> The CNS-specific distribution problem. Why CNS drugs look different, and how to engineer molecules that get into the brain.

## The barrier

The BBB is a tight endothelial layer with:

- **Tight junctions** — no paracellular leak; everything must cross transcellularly.
- **High P-gp efflux** — actively pumps many drug-like molecules back to blood.
- **Restricted vesicular transport** — no random pinocytosis.
- **Specialised transporters** — glucose (GLUT1), amino acids (LAT1), nucleosides, monocarboxylates.

Net: ~98% of small molecules and ~100% of biologics do not meaningfully cross.

## The CNS-MPO framework

[Wager et al., 2010](https://doi.org/10.1021/cn100008c) defined a multi-parameter score for CNS-suitable physchem:

| Property | CNS-friendly |
| --- | --- |
| cLogP | ≤ 3 |
| cLogD7.4 | ≤ 2 |
| MW | ≤ 360 Da |
| TPSA | 40–90 Å² |
| HBD | ≤ 0.5 (often ≤ 1) |
| pKa (most basic) | ≤ 8 |

Each property maps to a desirability ∈ [0, 1]; CNS MPO is the sum (max 6). Programs aiming for CNS aim for MPO ≥ 4.

## P-glycoprotein

The single most important molecular barrier for CNS drugs. A P-gp substrate is pumped out of brain endothelial cells.

- **Predictors**: AUROC ~0.75 for P-gp substrate; ~0.75 for inhibitor.
- **Chemistry levers**: increase H-bond donors (controversial — increases TPSA), reduce flexibility, alter scaffold curvature, deplete charged moieties.

A well-known story: loratadine (a hERG-prone P-gp substrate) → desloratadine improved properties → modern second-gen antihistamines are non-sedating in part because of P-gp efflux at the BBB.

## Brain-to-plasma ratio

The empirical measure of CNS penetration: ratio of unbound concentration in brain to unbound in plasma at steady state.

- **K_p,uu > 0.3** is considered "brain-penetrating".
- **K_p,uu < 0.05** is essentially excluded.

K_p,uu is measured in vivo (rat, dog) via brain homogenate + equilibrium dialysis or microdialysis. In silico predictors of logBB and K_p,uu reach AUROC ~0.8 for binary classification.

## Biologics and the BBB

Antibodies and other large biologics do not cross. Strategies to push them in:

- **Receptor-mediated transcytosis** — bispecifics or shuttle motifs targeting transferrin receptor or CD98hc on brain endothelium.
- **Focused ultrasound + microbubbles** to transiently open the BBB.
- **Intrathecal / intracerebroventricular delivery** — Nusinersen (SMA) is delivered this way.
- **AAV gene therapy** with brain-penetrant capsids.

This is an active and rapidly evolving area; classical CNS small-molecule rules-of-thumb do not transfer.

## In practice

- For CNS programmes, **compute CNS-MPO at every compound design step**. Aim for ≥ 4.
- **Predict P-gp substrate** early. P-gp-substrate compounds are CNS-dead unless you have a specific bypass strategy.
- **Validate K_p,uu in rat early** — sometimes a great CNS-MPO does not translate.
- For biologics, **plan delivery in parallel with target engineering**, not after.
