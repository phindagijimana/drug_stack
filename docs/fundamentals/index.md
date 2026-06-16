# Fundamentals

> What a "drug" actually is, what it acts on, what gets in the way, and the math / chemistry / biology you need to do anything serious.

This section is the prerequisite for everything else in the handbook. If you are coming from outside biotech, read in order. If you are an experienced medicinal chemist, you can skim the *Modalities* and *PK / PD* pages and jump to [Molecular design](../molecular-design/index.md).

## Chapters

- **[Drug modalities](drug-modalities.md)** — small molecules, biologics, oligonucleotides, peptides, PROTACs, cell and gene therapy. What each one is, when it is used, and what changes computationally.
- **[Biological targets](biological-targets.md)** — proteins, RNA, DNA, lipids, glycans, cells. GPCRs, kinases, ion channels, nuclear receptors, transcription factors, enzymes, transporters. Why some are "druggable" and others are not.
- **[Disease biology](disease-biology.md)** — how diseases become drug-discovery problems. Oncology, neurodegeneration, infectious disease, immunology, rare disease, metabolic. The big disease classes that drive most spend.
- **[Medicinal chemistry](medicinal-chemistry.md)** — bioisosteres, ring systems, scaffold hopping, structure–activity relationships, the rules of thumb chemists use.
- **[Pharmacology (PK / PD)](pharmacology.md)** — what the body does to the drug (PK) and what the drug does to the body (PD). One-compartment model, clearance, volume of distribution, half-life, the Hill equation, EC50 / IC50, Schild analysis.
- **[ADMET overview](admet-overview.md)** — the safety-and-disposition lens, summarised. Deep dives in [ADMET & toxicity](../admet-tox/index.md).
- **[Drug-discovery pipeline](pipeline.md)** — the end-to-end map. Target ID → hit ID → lead optimisation → preclinical → clinical phases → approval. Where computation slots in.

## Foundations sub-section

The **[Computational & math foundations](foundations/index.md)** chapter is the prerequisite mathematics, biology, chemistry, and tooling you will need to do the rest. If your background is uneven, read it.

## Why this is separate from generic life-science material

Drug discovery sits at a specific intersection: chemistry, biology, pharmacology, statistics, and engineering all have to compose. Three reasons it gets its own section:

1. **The objective function is multi-dimensional.** "Active against target" is necessary and nowhere near sufficient. A drug also has to absorb, distribute, not be metabolised too fast, not be toxic, not hit a dozen anti-targets, and ideally be synthesisable. Most of the failure happens *after* potency is achieved.
2. **The data is small, biased, and expensive.** A reasonable assay dataset is hundreds to low-thousands of compounds, almost always from one chemical series, almost always censored at the low-potency tail. Generic ML intuitions about scale do not transfer.
3. **The decisions are irreversible.** A compound advanced into a tox study is a six-figure commitment; into a phase II trial, a nine-figure one. The role of computation is to push *bad* decisions left.

Everything in this section is written with those three constraints in mind.
