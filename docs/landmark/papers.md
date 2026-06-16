# Foundational papers

> Thirty papers with one-line takeaways. The reading list this handbook would have wanted on day one.

## Druglikeness and physchem

- **[Lipinski 1997 — Rule of 5](https://doi.org/10.1016/S0169-409X(96)00423-1)** — MW < 500, cLogP < 5, HBA ≤ 10, HBD ≤ 5 for oral. Descriptive; treat as a prior, not a gate.
- **[Veber 2002 — Oral bioavailability](https://doi.org/10.1021/jm020017n)** — RotB ≤ 10 and TPSA ≤ 140 Å² complete the picture.
- **[Bickerton 2012 — QED](https://doi.org/10.1038/nchem.1243)** — quantitative druglikeness score (0–1).
- **[Bemis & Murcko 1996 — Scaffolds](https://doi.org/10.1021/jm9602928)** — ~50% of drugs share ~30 scaffolds.
- **[Lovering 2009 — Fsp3](https://doi.org/10.1021/jm901241e)** — escape from flatland; sp3 fraction matters.
- **[Wager 2010 — CNS MPO](https://doi.org/10.1021/cn100008c)** — CNS-friendly physchem score.

## Pharmacology and PK

- **[Manning 2002 — Kinome](https://doi.org/10.1126/science.1075762)** — the 518 human kinases mapped.
- **[Santos 2017 — Drug targets](https://doi.org/10.1038/nrd.2016.230)** — comprehensive map of approved-drug targets.
- **[Kola 2004 — Attrition](https://doi.org/10.1038/nrd1470)** — where drug programs die.
- **[DiMasi 2016 — R&D costs](https://doi.org/10.1016/j.jhealeco.2016.01.012)** — the $2B-per-drug study.

## Genetics and target ID

- **[Cohen 2006 — PCSK9 LoF](https://doi.org/10.1056/NEJMoa054013)** — natural LoF carriers had low LDL.
- **[Sabatine 2017 — FOURIER](https://doi.org/10.1056/NEJMoa1615664)** — anti-PCSK9 mAb confirms genetics in patients.
- **[Nelson 2015 — Genetic support](https://doi.org/10.1038/ng.3314)** — genetics doubles approval probability.
- **[Minikel 2024 — Update](https://doi.org/10.1038/s41586-024-07316-0)** — refined modern estimate.
- **[Ochoa 2021 — Open Targets](https://doi.org/10.1093/nar/gkaa1027)** — the integrated target-evidence platform.

## Cheminformatics and ML

- **[Trott 2010 — AutoDock Vina](https://doi.org/10.1002/jcc.21334)** — the open-source docker.
- **[Mayr 2018 — RF beats DL](https://doi.org/10.1039/C8SC00148K)** — classical ML hard to beat on most ChEMBL.
- **[Yang 2019 — Chemprop](https://doi.org/10.1021/acs.jcim.9b00237)** — directed message-passing for property prediction.
- **[Heid 2024 — Chemprop 2](https://doi.org/10.1021/acs.jcim.3c01250)** — modern Chemprop reference.
- **[van Tilborg 2022 — Activity cliffs](https://doi.org/10.1021/acs.jcim.2c01073)** — MoleculeACE shows deep models often fail at cliffs.

## Structure prediction

- **[Jumper 2021 — AlphaFold](https://doi.org/10.1038/s41586-021-03819-2)** — protein structure prediction at atomic accuracy.
- **[Lin 2023 — ESM-2](https://doi.org/10.1126/science.ade2574)** — single-sequence structure from language models.
- **[Abramson 2024 — AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w)** — joint biomolecular complex prediction.

## Screening and design

- **[Lyu 2019 — Ultra-large docking](https://doi.org/10.1038/s41586-019-0917-9)** — 138M-compound screens find genuine novel chemotypes.
- **[Graff 2021 — MolPAL](https://doi.org/10.1039/D1SC03044F)** — active learning for screening, 90% recall at 10⁻³ compute.
- **[Loeffler 2024 — REINVENT 4](https://doi.org/10.1186/s13321-024-00812-5)** — the open-source generative workhorse.
- **[Wang 2015 — FEP+](https://doi.org/10.1021/ja512751q)** — practical relative-binding-affinity calculations.
- **[Buttenschoen 2023 — PoseBusters](https://doi.org/10.48550/arXiv.2308.05777)** — ML dockers fail physical-validity checks.

## Repurposing and KG

- **[Lamb 2006 — CMap](https://doi.org/10.1126/science.1132939)** — connectivity-map foundation.
- **[Subramanian 2017 — LINCS](https://doi.org/10.1016/j.cell.2017.10.049)** — modern-scale CMap.
- **[Himmelstein 2017 — Hetionet](https://doi.org/10.7554/eLife.26726)** — KG for drug repurposing.
- **[Huang 2024 — TxGNN](https://doi.org/10.1038/s41591-024-03247-5)** — KG GNN for clinician-centered repurposing.

## ADMET

- **[Swanson 2024 — ADMET-AI](https://doi.org/10.1093/bioinformatics/btae416)** — the commodity ADMET predictor.
- **[Bickerton 2012 — QED](https://doi.org/10.1038/nchem.1243)** — also under druglikeness.

## A note on what's missing

This list is small and opinionated. Major omissions: biologics-specific landmarks (mAb humanisation, ADC linkers), specific therapeutic-area landmarks (BTK / venetoclax / GLP-1 stories), regulatory-science landmarks. Add as your work demands.
