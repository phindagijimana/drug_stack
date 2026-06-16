# Preclinical models

> What experiments precede first-in-human. PK/PD modelling, allometric scaling, toxicology.

## The stages

1. **In vitro PK** — microsomal stability, hepatocyte clearance, plasma protein binding, CYP inhibition, hERG, BSEP, mitochondrial toxicity.
2. **In vivo PK in rodents** — typically rat and mouse — single- and repeat-dose, IV / oral.
3. **In vivo PK in larger species** — dog and / or monkey for allometric scaling.
4. **In vivo efficacy** — disease-model animals (e.g. xenografts in oncology, transgenic mice in neurodegeneration).
5. **GLP toxicology** — Good Laboratory Practice 28-day, 90-day, 6-month studies in two species.
6. **Safety pharmacology** — CV (telemetry), CNS (FOB), respiratory.
7. **Genotoxicity** — Ames, micronucleus, comet.
8. **DMPK supporting documentation** — PBPK models, projected human dose, accumulation.

## Allometric scaling

Predicting human PK from animal data. Classical methods:

- **Simple allometry** — assume parameter scales as a power of body weight: \(P_{human} = P_{animal} \cdot (BW_{human} / BW_{animal})^x\).
- **CL_int scaling with weight**^0.75 is a workable first pass.
- **Volumes of distribution** scale ~linearly (exponent ~1).
- **Rule of exponents** improves predictions when CL scales sub-linearly.

Modern method: **PBPK modelling** (Simcyp, PK-Sim, GastroPlus). Mechanistic compartmental models that integrate species-specific physiology with in vitro inputs.

The starting human dose is usually derived from:

- **HED (Human Equivalent Dose)** = NOAEL × (BW_human / BW_animal)^0.67.
- **MABEL (Minimum Anticipated Biological Effect Level)** — based on pharmacology, not toxicology. Used for biologics, especially first-in-class.

## Animal-model selection

Different therapeutic areas have established animal models:

| Area | Common models |
| --- | --- |
| Oncology | Xenograft, PDX, syngeneic, GEMM |
| Alzheimer's | APP/PS1, 5xFAD, tau-transgenic |
| Parkinson's | MPTP, 6-OHDA, α-synuclein PFF |
| MS | EAE |
| Diabetes | db/db, ob/ob, STZ-induced |
| Asthma | Ovalbumin / HDM challenge |

Each has known translational limitations. A drug clean in EAE may fail in human MS; a drug efficacious in xenograft may fail in heterogeneous patient tumours.

## In practice

- **PBPK from day one** — even rough models help triage compounds.
- **Pick animal models with translational track record**, not novelty.
- **Plan the IND-enabling tox studies** alongside the medicinal-chemistry plan; they have long lead times.

## Where to next

[Clinical trials](trials.md) — what happens in humans.
