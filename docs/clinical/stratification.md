# Patient stratification

> Picking the right patients for the right drug. Where AI for trial enrichment lives.

## What stratification means

A drug rarely works equally in all patients with the nominal disease. Stratification is the discipline of:

1. Identifying patient subgroups likely to respond.
2. Designing trials that recruit them preferentially.
3. Eventually, labelling the drug for that subgroup.

## How stratification is done

- **Biomarker-driven**: HER2-positive, EGFR-mutant, BRCA-deficient.
- **Disease-subtype-driven**: triple-negative breast cancer, KRAS G12C non-small-cell lung cancer.
- **Multi-feature ML scores** combining clinical, omics, and imaging features.
- **Real-world-data-derived** populations matching trial criteria.

## Computational tools

- **Survival analysis with covariates** — Cox proportional hazards.
- **Subgroup identification** — Virtual Twins, model-based recursive partitioning, the SIDES family.
- **Causal forests** for heterogeneous treatment-effect estimation.
- **Predictive enrichment** — pre-trial scoring of likely responders.

## Pitfalls

- **Post-hoc subgroup analyses** are exploratory. Pre-specify subgroups in the protocol.
- **Multiple testing** across many subgroups inflates false-positive rates.
- **Overfitting to a discovery cohort** without validation in an independent set.

The CONSORT extension for trial reporting includes guidance on subgroup-analysis reporting.

## Modern AI-driven enrichment

A growing class of tools uses ML on EHR + omics + imaging to predict trial-eligibility and likely response. Used for:

- **Prescreen at sites** — identify candidate patients from EHRs.
- **Adaptive enrichment** — let the trial enrol more from responding subgroups as data accumulates.
- **Real-world external controls** — match trial arms against historical RWD.

Most regulatory agencies accept these only as supportive, not primary, evidence.

## In practice

- **Pre-specify stratification** in protocols.
- **AI-driven enrichment** should be transparent and validated.
- **For drug-discovery work**, contribute by *finding the biomarker that predicts response* — that is the upstream half of stratification.
