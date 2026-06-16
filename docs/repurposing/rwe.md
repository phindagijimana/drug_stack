# Clinical evidence & real-world data

> When the trial is "patients have already been taking it" — real-world evidence in repurposing.

## What RWE / RWD means

- **Real-world data (RWD)** — health data routinely collected outside clinical trials: EHRs, claims, registries, pharmacy records.
- **Real-world evidence (RWE)** — clinical evidence derived from analysing RWD.

For repurposing, RWE answers: *do patients on drug X for indication A have different outcomes on indication B than matched comparators?*

## The canonical analysis

Cohort study using EHR / claims:

1. **Define exposed cohort**: patients on drug X for indication A.
2. **Define comparator cohort**: similar patients not on drug X (or on a different drug).
3. **Match on observed confounders**: age, sex, comorbidities, prior treatments, socioeconomic.
4. **Measure outcome of interest**: incidence / progression of indication B over follow-up.
5. **Adjust for unmeasured confounders**: instrumental variables, MR, sensitivity analyses.

## Famous (and famously cautionary) examples

- **Metformin and cancer**. Observational data suggested lower cancer incidence in diabetics on metformin. Confounding by indication and immortal-time bias produced inflated effects; rigorous analyses and target-trial emulation [Hernán & Robins, 2016](https://doi.org/10.1093/aje/kwv254)[^hernan] tempered the claims.
- **Statins and dementia**. Similar story — early observational signals, mostly attenuated under careful analysis.
- **Hydroxychloroquine and COVID-19**. Misleading observational signals → ineffective in RCTs.

The pattern: RWE finds signals; only RCTs confirm them. RWE is the hypothesis-generator, RCTs the verdict.

## Target-trial emulation

The modern statistical framework [Hernán & Robins, 2016] for using RWD as if it were an RCT:

1. Specify the target trial protocol (eligibility, treatment, outcome).
2. Identify the cohort in RWD that matches the eligibility.
3. Apply the protocol exactly.
4. Analyse with intention-to-treat semantics.

Done right, target-trial emulation drastically reduces the confounding-by-indication bias.

## Data sources

- **CPRD, THIN** (UK).
- **Optum, IBM MarketScan, Truven, IQVIA** (US claims).
- **Mayo, Vanderbilt, Penn Medicine** (US EHR consortia).
- **TriNetX** — federated EHR network covering 80+ M patients.
- **All of Us** — NIH precision-medicine cohort, ~1M Americans.
- **OHDSI / OMOP CDM** — common data model + tools for federated analyses.
- **N3C** — COVID-focused EHR consortium.

## Why repurposing-via-RWE is hard

- **Confounding by indication** — patients on drug X often have a reason that itself predicts outcome.
- **Healthy-user bias** — drug-takers differ systematically.
- **Immortal-time bias** — the time before drug start can be miscounted.
- **Outcome misclassification** — EHR diagnoses are messy.

A naive analysis routinely overestimates effect sizes by 2×–10×.

## In practice

- **Use OHDSI / OMOP CDM** for any serious RWE analysis. The tooling is mature and battle-tested.
- **Always pre-specify** the analysis plan, the cohort definitions, and the sensitivity analyses.
- **Target-trial emulation > naive cohort study**.
- **Repurposing signals from RWE warrant a confirmatory RCT** — not a press release.

## References

[^hernan]: Hernán MA, Robins JM. Using big data to emulate a target trial when a randomized trial is not available. *Am J Epidemiol.* 2016;183(8):758–764. [doi:10.1093/aje/kwv254](https://doi.org/10.1093/aje/kwv254)

## Where to next

[Clinical translation](../clinical/index.md) — the rest of the trial / regulatory road.
