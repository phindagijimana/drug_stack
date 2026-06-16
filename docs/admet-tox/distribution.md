# Distribution

> Where the drug goes in the body. Plasma-protein binding, volume of distribution, tissue partitioning, efflux.

## Free vs total drug

In plasma, drugs are partitioned between **bound** (to albumin and α1-acid-glycoprotein) and **unbound (free)** fractions. **Only the free fraction binds the target and crosses membranes.**

- Many oral drugs are 95–99% bound. A 1% free fraction is enormous.
- The two main binding proteins:
  - **Albumin** — binds acids and neutrals preferentially.
  - **AAG (α1-acid glycoprotein)** — binds basic drugs.

For modelling, **fu (free fraction in plasma)** is the key parameter. Programs that ignore it overestimate effective potency.

## Volume of distribution (V_d)

A descriptor of how widely a drug partitions out of plasma:

\[
V_d = \frac{\text{Total drug in body}}{\text{Concentration in plasma}}
\]

- V_d < 0.2 L/kg: plasma-confined (heparin, warfarin).
- V_d ~0.5 L/kg: typical hydrophilic drug.
- V_d > 5 L/kg: heavily tissue-bound (digoxin, chloroquine, amiodarone).

V_d depends on lipophilicity, basicity (for tissue ion-trapping), and protein binding.

## Tissue partitioning

For most targets, what matters is the **unbound concentration at the target tissue**, not in plasma. Tissues differ:

- **Highly perfused** (liver, kidney, lung, brain): rapid equilibration with plasma.
- **Slow** (fat, muscle): time-delayed accumulation.
- **Specialised barriers**: BBB, blood-testis, placental.

PBPK (physiologically-based pharmacokinetic) modelling explicitly compartmentalises and is the right tool for predicting tissue concentrations from plasma data.

## P-glycoprotein and other efflux pumps

P-gp (ABCB1, MDR1) is the most clinically important efflux transporter:

- Expressed at the BBB, intestinal epithelium, hepatocytes, renal tubules.
- Pumps lipophilic substrates *out* of cells.
- A P-gp substrate fails the BBB; a P-gp inhibitor causes DDIs.

Other efflux: BCRP (ABCG2), MRPs.

Predictors: AUROC ~0.7–0.8 for P-gp substrate; ~0.7 for inhibition.

## CNS — the BBB special case

See [BBB](bbb.md).

## Plasma-protein binding prediction

QSAR for log fu reaches ~0.4 log unit RMSE on TDC PPB benchmarks; sufficient to triage between "high binding" and "moderate binding" but not for precise dosing prediction.

The TDC and ChEMBL PPB datasets are the right training sources.

## In practice

- **Always report free unbound exposure** (Cu, AUCu = total × fu) when comparing programs.
- **Predict P-gp substrate** for any CNS or oral program; it is the cheap pre-flight check.
- **For deep tissue distribution**, PBPK modelling (Simcyp, PK-Sim) is the industrial tool; in silico predictors of partition coefficients feed into it.

## Where to next

[Metabolism](metabolism.md) — what happens to the drug once it lands in the liver.
