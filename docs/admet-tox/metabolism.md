# Metabolism

> The chemistry the body does to your drug. CYP-mediated and phase II metabolism, metabolite identification, soft-spot prediction.

## The CYP zoo

Cytochrome P450s are the main drug-metabolising enzymes. The clinically dominant isoforms:

| CYP | Drugs metabolised (approx) | Notes |
| --- | --- | --- |
| 3A4/5 | ~50% of marketed drugs | grapefruit juice inhibits; many DDIs |
| 2D6 | ~25% | strongly polymorphic — poor / intermediate / extensive / ultra-rapid metabolisers |
| 2C9 | ~15% | warfarin, NSAIDs |
| 2C19 | ~10% | omeprazole, clopidogrel |
| 1A2 | ~10% | caffeine, theophylline; induced by smoking |
| 2E1 | minor | acetaminophen toxic metabolite |

A drug program needs to know: which CYP metabolises it (clearance), and which it inhibits (DDI risk).

## Substrate vs inhibitor

- **Substrate**: the CYP eats the drug. Affects clearance and inter-patient variability (if the CYP is polymorphic).
- **Inhibitor**: the drug blocks the CYP. Causes drug-drug interactions for co-medications cleared by that CYP.

A drug being both substrate and inhibitor of the same CYP is normal; substrate of one and strong inhibitor of another is the highest-risk DDI profile.

## CYP inhibition prediction

Predicting CYP inhibition (binary, IC50 < 10 µM) is one of the most-published ADMET ML tasks. Standard benchmark: PubChem AID 1851 dataset.

Performance on the TDC CYP benchmarks reaches AUROC ~0.85 across all five major isoforms. ADMET-AI ships pre-trained predictors out of the box.

## Microsomal clearance

The hepatic intrinsic clearance (CL_int) measured in human liver microsomes is the standard early metabolic-stability assay. Goal: low CL_int (long half-life in microsomes).

- **In vitro**: incubate drug with HLM, measure substrate disappearance.
- **In silico**: predict CL_int from structure. AUROC ~0.75 for binary stable / unstable; RMSE on continuous log-CL_int ~0.5–0.7.

## Soft-spot prediction

Where on the molecule the CYP attacks. Critical for chemistry intervention: a methyl group three bonds from the soft spot does nothing; blocking the soft spot itself (deuterium, fluorine, ring substitution) extends half-life dramatically.

- **MetaPredict, FAME 3** [Šícho et al., 2019](https://doi.org/10.1021/acs.jcim.9b00376)[^fame] — soft-spot ML models.
- **MoleculeNet metabolism datasets** — training data.

A chemist with a soft-spot prediction map can iterate on metabolic stability in days, not weeks.

## Reactive metabolites

Some scaffolds produce **reactive metabolites** (RMs) — electrophiles that covalently bind cellular proteins. Linked to idiosyncratic hepatotoxicity (acetaminophen, troglitazone, felbamate withdrawals).

Structural alerts (aniline, furan, thiazolidinedione, nitroaromatic) are routinely flagged. RM-trapping assays (glutathione, cyanide, methoxylamine trapping with mass-spec detection) confirm in vitro.

Computational predictors are improving but not yet quantitative. The pragmatic stance: avoid known RM-prone scaffolds unless they are essential.

## Phase II

Beyond CYP-mediated phase I oxidation, drugs are conjugated via:

- **Glucuronidation** (UGTs) — adds glucuronic acid; the major polar-conjugation pathway.
- **Sulfation** (SULTs).
- **Glutathione conjugation** (GSTs) — defence against reactive species.
- **Acetylation, methylation**.

Phase II metabolism is less commonly modelled in silico but matters for some scaffolds (acetaminophen sulfation, morphine glucuronidation).

## In practice

- **Predict CYP inhibition for the 5 major isoforms** at compound design time. Standard, cheap, mature.
- **Predict microsomal clearance** when iterating for metabolic stability.
- **Run soft-spot prediction** for compounds with marginal CL_int — it tells you where to add a methyl or fluorine.
- **Avoid known reactive-metabolite scaffolds** unless the program has a specific reason for them.

## References

[^fame]: Šícho M, Stork C, Mazzolari A, et al. FAME 3: predicting the sites of metabolism in synthetic compounds and natural products for phase 1 and phase 2 metabolic enzymes. *J Chem Inf Model.* 2019;59(8):3400–3412. [doi:10.1021/acs.jcim.9b00376](https://doi.org/10.1021/acs.jcim.9b00376)

## Where to next

[Excretion](excretion.md) — and now where does it leave the body.
