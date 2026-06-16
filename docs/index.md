---
hide:
  - navigation
  - toc
---

# DrugStack — the drug-discovery documentation hub

> Welcome to **DrugStack** — the open documentation hub for everything you need to do credible computational drug-discovery work.

Here you'll find a tour of the **fundamentals** (drug modalities, biological targets, disease biology, medicinal chemistry, PK/PD, the maths, the chemistry, the cheminformatics), a **target-identification** book, a deep **molecular-design** library, an opinionated **virtual-screening** chapter, **ADMET / toxicity** and **drug-repurposing** sections, a **clinical-translation** primer, a focused **AI / ML** section, a **data-engineering** chapter taught against real cheminformatics workloads, a **computing** environment guide, and a curated **landmark-work** reading list — together with runnable tutorials.

DrugStack is written for **people getting started** in drug-discovery research and the engineering that supports them: graduate students, postdocs, research software engineers, data engineers arriving from outside biotech, ML engineers building therapeutic-AI products, and senior research engineers who want an opinionated map of the tool landscape. It tries to be the document we wish we had when we first walked into the field.

It is the sibling of [NeuroStack](https://github.com/phindagijimana/neuro_stack) — same depth tiers (beginner → PhD → senior engineer), same voice, different domain.

Found something missing, wrong, or out of date? We'd love to know — every page has an *edit-on-GitHub* link in the top right, and you can also open an issue or pull request on the [repo](https://github.com/phindagijimana/drug_stack). Suggestions, corrections, and contributions are all welcome.

---

## New to drug discovery? Start here

<div class="grid cards" markdown>

-   :material-rocket-launch: **[Getting started](getting-started/index.md)** — the 30-minute on-ramp. Install environment, load your first SMILES, run your first virtual screen, render your first figure.

-   :material-map-marker-path: **[Reading paths](paths/index.md)** — five named paths through the handbook for new researchers, software engineers pivoting in, chemists, ML engineers, and senior research engineers.

-   :material-school-outline: **[Tutorials](tutorials/index.md)** — six end-to-end walk-throughs from target to lead, including a synthesis capstone.

</div>

---

## Browse by topic

<div class="grid cards" markdown>

-   :material-school:{ .lg .middle } **Fundamentals**

    ---

    What a "drug" actually is. Small molecules, biologics, oligonucleotides, cell and gene therapy; targets, pathways, disease biology; PK/PD and ADMET in one place.

    [:octicons-arrow-right-24: Start here](fundamentals/index.md)

-   :material-target:{ .lg .middle } **Target identification**

    ---

    Genomics, transcriptomics, proteomics, network biology, knowledge graphs, and the awkward question of whether a target is actually druggable.

    [:octicons-arrow-right-24: Find a target](target-id/index.md)

-   :material-flask:{ .lg .middle } **Molecular design**

    ---

    Representations (SMILES, graphs, 3D), descriptors and fingerprints, QSAR, generative chemistry (VAE / RL / diffusion), structure-based design, docking, FEP.

    [:octicons-arrow-right-24: Design molecules](molecular-design/index.md)

-   :material-magnify-scan:{ .lg .middle } **Virtual screening**

    ---

    Ligand-based, structure-based, ultra-large libraries (Enamine REAL and friends), active learning, hit triage. When to use which.

    [:octicons-arrow-right-24: Screen libraries](screening/index.md)

-   :material-shield-cross:{ .lg .middle } **ADMET & toxicity**

    ---

    Absorption, distribution, metabolism, excretion. In-silico safety. The blood–brain barrier. Why "potent" is not enough.

    [:octicons-arrow-right-24: Predict safety](admet-tox/index.md)

-   :material-recycle:{ .lg .middle } **Drug repurposing**

    ---

    Signature-based methods (CMap / LINCS), knowledge-graph and embedding methods, and what real-world evidence can — and cannot — tell you.

    [:octicons-arrow-right-24: Repurpose drugs](repurposing/index.md)

-   :material-hospital-box:{ .lg .middle } **Clinical translation**

    ---

    Preclinical models, clinical-trial design, FDA and EMA basics, biomarkers, patient stratification. Where computational work meets patients.

    [:octicons-arrow-right-24: Translate to clinic](clinical/index.md)

-   :material-brain:{ .lg .middle } **AI / ML**

    ---

    Classical ML on fingerprints, message-passing networks for molecules, protein language models (ESM, AlphaFold), generative chemistry, foundation models, and the evaluation pitfalls specific to drug discovery.

    [:octicons-arrow-right-24: Train models](ai/index.md)

-   :material-pipe:{ .lg .middle } **Data engineering**

    ---

    DAGs, pipelines, idempotency, observability, testing — taught against real ChEMBL / PubChem / assay workloads. Lakehouse for chemistry. MLOps for drug discovery.

    [:octicons-arrow-right-24: Build pipelines](data-engineering/index.md)

-   :material-server:{ .lg .middle } **Computing**

    ---

    Python scientific stack, RDKit + OpenMM, containers, HPC + Slurm, cloud, GPUs, dependency management, the reproducibility checklist.

    [:octicons-arrow-right-24: Set up your env](computing/index.md)

-   :material-bookshelf:{ .lg .middle } **Landmark work**

    ---

    Foundational papers, reference datasets (ChEMBL, PubChem, BindingDB, PDB, UniProt, DrugBank), major pipelines (RDKit, AutoDock, OpenMM, AlphaFold), atlases.

    [:octicons-arrow-right-24: Read the field](landmark/index.md)

-   :material-tools:{ .lg .middle } **Tools landscape**

    ---

    Opinionated map of cheminformatics, structure prediction, screening, and ML tools — pointers, not exhaustive lists.

    [:octicons-arrow-right-24: Pick a tool](tools/index.md)

</div>

---

## How to read it

Pick the entry point that matches your background:

- **New to drug discovery?** Start with [Fundamentals → Drug modalities](fundamentals/drug-modalities.md). Then [Fundamentals → Biological targets](fundamentals/biological-targets.md) and [Computing](computing/index.md).
- **Software / data engineer coming in from outside?** Jump to [Fundamentals → Drug-discovery pipeline](fundamentals/pipeline.md), then go straight to [Data engineering → Foundations](data-engineering/foundations.md).
- **Medicinal chemist who needs to scale screening?** [Molecular design → Generative chemistry](molecular-design/generative.md) and [Virtual screening → Ultra-large libraries](screening/ultra-large.md) are the action items.
- **ML engineer building drug-AI?** [AI / ML → Classical ML](ai/classical-ml.md) → [Deep learning](ai/deep-learning.md) → [Evaluation](ai/evaluation.md). Read [Fundamentals → Medicinal chemistry](fundamentals/medicinal-chemistry.md) in parallel.
- **Senior research engineer / staff?** [Reading paths](paths/index.md) Path E.
- **Looking up something specific?** Use search (top bar) or the [Glossary](glossary.md).

## Companion code

This site is generated from a repository that also ships runnable examples:

```bash
git clone https://github.com/phindagijimana/drug_stack.git
cd drug_stack
pip install -e ".[docs,dev]"
mkdocs serve  # preview this site locally
```

The code in tutorials is intentionally small and readable. If a page on this site refers to a snippet, the snippet exists in the repo and is exercised in CI.

## Contributing

This is a community reference. The medicinal-chemistry parts reflect a particular team's experience; broader coverage is welcome. See the [repo](https://github.com/phindagijimana/drug_stack) for how to file issues and open PRs.

## License

Content and code are released under the [MIT license](https://github.com/phindagijimana/drug_stack/blob/main/LICENSE).

## Contact

Maintained by **Philbert Ndagijimana**.

- 💼 **LinkedIn** — <https://www.linkedin.com/in/philbert-ndagijimana-319570188/>
- ✉️ **Email** — <phindagiji@gmail.com>
- 🐛 **Issues / PRs** — <https://github.com/phindagijimana/drug_stack/issues>
