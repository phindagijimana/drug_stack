# Excretion

> How the body gets rid of the drug and its metabolites. Renal, biliary, the parameters that set half-life.

## Two main routes

- **Renal** — kidney filtration + active secretion / reabsorption. Dominates for small, polar molecules.
- **Biliary / faecal** — liver secretes into bile; molecule (or its metabolites) exits via stool. Dominates for larger, lipophilic molecules.

The **fraction excreted unchanged (f_e)** is the canonical descriptor.

- f_e > 0.5: drug is renally cleared as parent. Examples: metformin (~99%), amoxicillin, lithium.
- f_e < 0.2: drug is mostly metabolised first; metabolites carry the elimination load. Examples: most lipophilic small molecules.

## Renal mechanics

- **Glomerular filtration** (GFR) — passive; depends on free fraction and renal blood flow.
- **Tubular secretion** — active; organic anion / cation transporters (OATs, OCTs, OATPs). Drugs that compete here cause DDIs (probenecid + penicillin).
- **Tubular reabsorption** — passive, pH-dependent; lipophilic drugs reabsorb; polar ones excrete.

Renal-impaired patients (CKD) get reduced clearance for renally-cleared drugs; dose adjustment is mandatory and on the label.

## Biliary mechanics

- Hepatocytes secrete drug or metabolite into bile via efflux transporters (MRP2, BCRP).
- Biliary excretion of glucuronide conjugates can be followed by **enterohepatic recirculation** — gut bacteria cleave the conjugate, free drug is reabsorbed, prolonging exposure (extends half-life of e.g. mycophenolate).

## Half-life and dose frequency

Once a day (q.d.) dosing requires half-life ~12–24 h. Twice a day (b.i.d.), 6–12 h. Half-life < 4 h is generally a non-starter for chronic oral therapy without modified-release formulation.

\[
t_{1/2} = \frac{0.693 \, V_d}{CL}
\]

A drug with low CL and moderate V_d → long half-life → simple dosing. A drug with high CL → short half-life → frequent dosing or formulation engineering.

## In practice

- **Predict if the compound is likely a transporter substrate** (renal OATs, hepatic OATPs, BCRP). DDI risk lives here.
- **Half-life is set by clearance and V_d together** — adjust either to fix.
- **Renal-impairment labelling** is a fact of life for renally-cleared drugs; build PBPK models that include it.

## Where to next

[In-silico toxicity](toxicity.md) — the predictors that triage safety risk.
