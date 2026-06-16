# Drug repurposing

> Finding new uses for existing drugs. The fastest path to a clinic, when it works.

A drug that has already passed safety and PK studies for one indication is, biologically, more than half-way through development for a second. Repurposing aims to identify those connections.

## Chapters

- **[Signature-based](signature-based.md)** — CMap / LINCS connectivity, signature reversal.
- **[Knowledge graphs](knowledge-graphs.md)** — KG embeddings, GNN-based ranking, TxGNN.
- **[Clinical evidence & RWE](rwe.md)** — claims data, EHR, randomised pragmatic trials.

## Why repurposing is attractive

- **Safety is largely known.** Phase I and much of phase II/III safety has been demonstrated.
- **Manufacturing and formulation exist.** No CMC ramp.
- **Off-patent drugs are cheap.** Generic ivermectin, metformin, statins are essentially free.
- **Time to clinic is short.** A repurposing trial can launch in months, not years.

## Why repurposing fails

- **Dosing.** The new indication may need a different dose; off-patent drugs may not have data at that dose.
- **Trial design.** Funding a phase III on an off-patent drug is hard — no IP, no exclusivity.
- **The biology may be wrong.** Computational predictions of new indication frequently fail clinical confirmation.

The classic illustration: **hydroxychloroquine for COVID-19**. Computational repurposing predicted activity. Early observational studies looked positive. Properly-designed RCTs showed no benefit. The case study is informative about both the promise and the pitfalls.

## The three signal types

| Signal | Example | Strength |
| --- | --- | --- |
| Transcriptomic signature reversal | drug X reverses Alzheimer hippocampal signature | weak alone, strong in combination |
| Target-disease KG link | drug X binds protein Y, Y is in disease Z's pathway | moderate, depends on KG quality |
| Real-world evidence (RWE) | patients on drug X for disease A have lower incidence of disease B | strong, hard to do well |

## Notable successes

- **Sildenafil** — angina trial side effect → erectile dysfunction.
- **Thalidomide** — emesis → leprosy → multiple myeloma.
- **Aspirin** — pain → cardiovascular prevention.
- **Minoxidil** — hypertension → male pattern baldness.
- **Bupropion** — antidepressant → smoking cessation.
- **Metformin** — diabetes → currently being studied in oncology, aging, COVID.

Most happened serendipitously, not computationally. Computational repurposing is meant to compress that timeline.

## When to attempt computational repurposing

Strong fit:

- **Rare disease** with an unmet need and a clear target hypothesis.
- **Mechanistic overlap** between a well-treated and an under-treated disease.
- **Available signatures** (LINCS profiles for many candidate drugs).

Weak fit:

- **Diseases with diffuse mechanism** (Alzheimer's, chronic pain) — signature-based approaches struggle.
- **Diseases with strong commercial pull** — there is rarely a leftover patent space for a repurposed generic.

## In practice

- **Combine signal types.** A target hit by a known-safe drug, supported by signature reversal, in a patient population where RWE shows reduced incidence — that's a strong story.
- **Always plan the clinical trial first.** Without a funded trial path, a computational ranking is just a paper.
- **OpenTargets repurposing tab + Connectivity Map + RWE platforms** is the right toolchain for an entry-level repurposing campaign.
