# Safety pharmacology

> Secondary pharmacology and off-target screening. The "what else does it hit?" question.

## Why secondary pharmacology matters

Every small molecule binds more than its nominal target. The question is *what* — and at what concentration.

- **Receptor panels** (e.g. Cerep / Eurofins SafetyScreen44, Roche binding panel) screen against 40–80 receptors / channels / transporters known to drive adverse events.
- **In-silico panels** predict binding to the same set; computational triage prioritises which to test wet.

## The standard off-target panel

The Eurofins SafetyScreen44 / 87 panels are the industrial reference. They cover:

- GPCRs (adrenergic, muscarinic, serotonin, opioid, dopamine, histamine, …).
- Ion channels (hERG, Nav, Cav, NMDAR, GABA_A).
- Transporters (DAT, NET, SERT, MAO).
- Nuclear receptors (PXR, AhR — relevant to induction).
- Enzymes (acetylcholinesterase, PDE, COX).

A program characterises a candidate against the full panel before declaring it clean.

## Selectivity rules of thumb

- **30× margin** over therapeutic plasma concentration is the minimum acceptable for any off-target hit.
- **For CNS targets**, > 100× because CNS exposure can be higher than systemic.
- **For "social" off-targets** (DAT, σ1, etc.), selectivity ratios are even more important to avoid neurological side effects.

## In silico off-target prediction

ML predictors for ChEMBL/binding-DB-defined off-target panels reach reasonable accuracy on:

- **Major GPCR off-targets**: AUROC ~0.75–0.85.
- **Major ion channels** beyond hERG: variable, ~0.7–0.8.
- **Kinome promiscuity for non-kinase programs**: useful as a "is this dirty?" filter.

Resources: TDC, ChEMBL panel assays, Excape-DB.

The output is *triage*: "this compound has a 70% probability of being a μ-opioid hit at < 1 µM" tells you to bench-test before advancing, not that the compound is dead.

## CNS / behaviour panels

For CNS programs, additional in vivo safety screens (Irwin observations, FOB, modified Irwin) cover sedation, motor coordination, autonomic effects. Computational support is mostly through receptor-binding predictions feeding rule-of-thumb triage (e.g. μ-opioid binding flags sedation risk).

## In practice

- **Run an off-target panel prediction** before advancing into in vivo pharmacology. The cost is minutes; the cost of an unexpected in vivo finding is months.
- **Establish 30× selectivity margin** vs all expected off-targets at the candidate-selection stage.
- **Wet-lab follow-up the predicted hits** before triaging. Predictions are imperfect; confirm before killing.

## Where to next

[Blood-brain barrier](bbb.md) — the special-case distribution problem for CNS targets.
