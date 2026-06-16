# In-silico toxicity

> Predicting safety liabilities before synthesis. The high-impact panels: hERG, AMES, DILI, carcinogenicity.

The most mature ADMET predictors are in toxicity. They are not regulatory substitutes — they are *triage* tools that catch the obvious failures.

## hERG (cardiotoxicity)

The hERG (KCNH2) potassium channel sets the rapid delayed-rectifier current that ends a cardiac action potential. Drugs that block hERG prolong the action potential → QT prolongation → torsades de pointes → sudden cardiac death.

Several drugs (terfenadine, cisapride, astemizole) were withdrawn for hERG-mediated QT prolongation. Routine hERG screening is now mandatory in development.

- **Predictors**: TDC hERG benchmark, ChEMBL hERG dataset.
- **Typical performance**: AUROC ~0.85.
- **Chemistry levers**: reduce lipophilicity, reduce basicity (hERG likes basic + lipophilic), introduce H-bond donors, add para-fluorine on aromatic rings.

A hERG IC50 > 30× the therapeutic plasma concentration is the standard safety margin.

## AMES mutagenicity

The Ames test screens for bacterial mutagenicity using *S. typhimurium* strains. ICH M7 [ICH 2017](https://www.ich.org/page/safety-guidelines)[^ich-m7] mandates a structural alert / QSAR assessment of impurities for mutagenicity.

- **Predictors**: AUROC ~0.85 on TDC AMES benchmark.
- **Tools**: VEGA, Toxtree, Derek Nexus, ADMET-AI Ames module.
- **Chemistry levers**: avoid arenes with electron-withdrawing groups in the meta position, avoid bare aromatic amines, avoid epoxides, nitroaromatics.

A positive Ames flag in a final candidate is usually disqualifying.

## DILI (drug-induced liver injury)

Hepatotoxicity is a leading cause of late-stage attrition and post-marketing withdrawals. Mechanisms:

- **Direct (intrinsic)** — dose-dependent, predictable. Acetaminophen overdose.
- **Idiosyncratic** — dose-independent, rare, often immune-mediated. Troglitazone.

DILI predictors are weaker than hERG / AMES but improving:

- **DILIst, DILIrank** — curated datasets.
- **deepDILI / Chemprop-DILI** — AUROC ~0.75–0.80.
- **Mechanism-stratified predictors** (BSEP inhibition, mitochondrial toxicity, reactive metabolite formation) are often better than monolithic DILI classifiers.

## Carcinogenicity

- **2-year rodent bioassay** is the regulatory gold standard.
- In silico: weak. Most predictors trained on Carcinogenicity DB datasets reach AUROC ~0.7.
- Strategy: avoid known structural alerts, plan for 2-year studies on clinical candidates, monitor in carcinogenicity-prone scaffolds.

## CYP-mediated DDIs

Predicting *drug-drug interaction* risk = predicting CYP inhibition with high reliability. Covered in [Metabolism](metabolism.md). The TDC CYP datasets cover 3A4, 2D6, 2C9, 2C19, 1A2.

## Other panels

- **Cardiotoxicity panel** (Cav, Nav, Kv): beyond hERG, ion channels worth screening.
- **Mitochondrial toxicity**: a frequent cause of late attrition; specialised assays.
- **Phototoxicity**: skin reactivity in UV exposure; relevant for dermatology and chronic medications.
- **Ototoxicity, nephrotoxicity**: tissue-specific, organ-on-chip assays.

## Standard structural alerts

| Group | Concern |
| --- | --- |
| Aromatic nitro | mutagenicity |
| Aromatic amine (unsubstituted) | mutagenicity |
| Epoxide | genotoxicity |
| Aldehyde | covalent reactivity |
| Michael acceptor | covalent reactivity |
| α,β-unsaturated ketone | covalent reactivity |
| Acyl halide | reactivity |
| Hydrazine | genotoxicity |
| Catechol | redox cycling, PAINS |
| Quinone | redox cycling |

Run the **Brenk filter** [Brenk et al., 2008](https://doi.org/10.1002/cmdc.200700139)[^brenk] in RDKit as the first filter. PAINS as the second.

## In practice

- **Run the standard panel** (hERG, AMES, DILI, CYPs) on every compound. ADMET-AI is the easy default.
- **Treat ML predictions as priors**, not verdicts. A confident hERG hit prediction warrants a wet-lab confirmation before killing a series.
- **Structural alerts always**. PAINS + Brenk catches 80% of obvious tox liabilities.
- **Mechanism-stratified DILI** > monolithic DILI predictor.

## References

[^ich-m7]: International Council for Harmonisation. M7(R1) Assessment and control of DNA reactive (mutagenic) impurities in pharmaceuticals to limit potential carcinogenic risk. 2017. [URL](https://www.ich.org/page/safety-guidelines)
[^brenk]: Brenk R, Schipani A, James D, et al. Lessons learnt from assembling screening libraries for drug discovery for neglected diseases. *ChemMedChem.* 2008;3(3):435–444. [doi:10.1002/cmdc.200700139](https://doi.org/10.1002/cmdc.200700139)

## Where to next

[Safety pharmacology](safety.md) — secondary pharmacology and off-target panels.
