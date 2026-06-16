# Clinical trials

> The four phases, what they answer, and the design knobs a computational scientist will encounter.

## The phases

| Phase | Question | Subjects | Duration | Cost |
| --- | --- | --- | --- | --- |
| 0 / Exploratory IND | Micro-dose PK in humans | ≤ 15 | weeks | low |
| I | Safety, tolerability, PK | 20–80 healthy / patient | months | $1–10M |
| II | Efficacy signal, dose | 100–500 patients | 1–3 yr | $10–50M |
| III | Confirmatory efficacy + safety | 1k–10k patients | 2–5 yr | $100M–1B+ |
| IV | Post-marketing surveillance | thousands | indefinite | varies |

A single phase III trial routinely costs more than the rest of preclinical + clinical combined for a typical small molecule.

## Trial design knobs

- **Endpoints** — primary, secondary, exploratory. Pre-specified.
- **Population** — eligibility / exclusion. Tighter = cleaner trial, smaller market.
- **Comparator** — placebo, standard-of-care, active control.
- **Randomisation** — 1:1, 2:1, adaptive.
- **Blinding** — single, double, open-label.
- **Adaptive elements** — interim analyses, sample-size re-estimation, response-adaptive randomisation.
- **Stratification** — biomarker-defined subgroups, baseline characteristics.

## Modern trial innovations

- **Adaptive trials** — pre-specified rules to modify the trial based on accumulated data (e.g. drop futile arms).
- **Basket trials** — one drug across multiple tumour types defined by a shared genetic feature.
- **Umbrella trials** — multiple drugs against one disease, sub-stratified.
- **Platform trials** — multiple drugs, multiple arms, ongoing addition/removal.
- **Master protocols** — shared protocol across multiple drugs (I-SPY in breast cancer, RECOVERY in COVID, GBM AGILE in glioblastoma).

For computational scientists: adaptive trials use **Bayesian decision rules**. Familiarity with posterior predictive probabilities matters.

## Real-world data and trials

- **Hybrid designs** that combine clinical-trial data with EHR-derived comparator arms.
- **External / synthetic control arms** based on RWD where placebo is unethical (e.g. ALS, glioblastoma).
- **Pragmatic trials** in real-world settings.

These are the growth areas of trial methodology.

## Statistical significance vs clinical significance

A small statistically significant effect may be clinically meaningless. The **minimum clinically important difference (MCID)** is the threshold below which a benefit doesn't matter for patients. Trial design should target effect sizes above MCID, not the smallest detectable.

## In practice

- **Computational scientists rarely design trials but often inform them.** Biomarker prediction, patient stratification, dose-finding all overlap.
- **Read the protocol before reading the results.** Pre-specified analyses are credible; post-hoc analyses are exploratory.
- **For drug-AI tools used in trial conduct** (enrolment, adherence, monitoring), regulatory scrutiny is similar to SaMD.

## Where to next

[Regulatory science](regulatory.md) — the FDA / EMA / MHRA basics.
