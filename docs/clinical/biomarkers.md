# Biomarkers

> The measurements that connect a drug's mechanism to a clinical effect. Diagnostic, prognostic, predictive, pharmacodynamic.

## Four kinds

- **Diagnostic** — does the patient have the disease? (HbA1c for diabetes, cardiac troponin for MI, BRCA1/2 for hereditary breast cancer.)
- **Prognostic** — what will happen without treatment? (Tumour stage, BNP for heart failure.)
- **Predictive** — will the patient respond to this treatment? (PD-L1 for immunotherapy, EGFR mutation for erlotinib, HER2 for trastuzumab.)
- **Pharmacodynamic (PD)** — is the drug doing what it should? (Phospho-AKT for PI3K inhibitor, c-tau for tau therapy.)

A *companion diagnostic* (CDx) is a predictive biomarker formalised as a regulatory test that determines drug eligibility.

## Why biomarkers matter

A trial with a good predictive biomarker:

- **Tighter inclusion** — only enrol patients likely to respond → smaller sample size, larger effect.
- **Faster path to approval**.
- **Higher commercial value** in stratified markets.
- **Cleaner mechanism story** to regulators and physicians.

Examples: trastuzumab + HER2, vemurafenib + BRAF V600E, pembrolizumab + PD-L1. Each transformed an indication.

## Biomarker discovery — computational angle

Most modern biomarker discovery is computational + omics:

- **Bulk RNA-seq, proteomics** for differential expression in responders vs non-responders.
- **Single-cell** for cell-state stratification.
- **Imaging biomarkers** (MRI, PET, CT) — image-derived quantitative features.
- **EHR / claims** for clinical biomarker discovery.
- **Multi-omics integration** — combining genomic, transcriptomic, proteomic, metabolomic signals.

## Validation

A biomarker is not validated until:

1. **Analytical validation** — the assay is reproducible.
2. **Clinical validation** — it correlates with the clinical outcome.
3. **Clinical utility** — using the biomarker improves patient outcomes vs not using it.

Computational biomarker scores reach (2) but rarely (3) without a prospective trial.

## In practice

- **Plan biomarker strategy at trial design**, not after.
- **Predictive biomarkers in oncology** are a saturated space; non-oncology is increasingly important and underdeveloped.
- **For computational scientists**, the highest-leverage contributions are multi-omics integration and image-derived biomarkers.

## Where to next

[Patient stratification](stratification.md) — using biomarkers to pick patients.
