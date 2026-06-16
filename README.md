# DrugStack

> *The open drug-discovery and -development handbook.*

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

---

**DrugStack** is an open reference for working on drug discovery and development with modern computational tools — biology of disease, medicinal chemistry, cheminformatics, structural biology, AI / ML, and the data engineering that makes any of it reproducible.

It is written for **people getting started** in drug-discovery research and the engineering that supports them: undergraduates and graduate students stepping into industry or academic pharma, postdocs pivoting from wet-lab work, software / data engineers arriving from outside biotech, ML engineers building therapeutic-AI products, and senior research engineers who need an opinionated map of the tool landscape.

It is a sibling project to [NeuroStack](https://github.com/phindagijimana/neuro_stack) — same mindset (depth tiers from beginner to PhD / senior engineer), same writing voice, same "the document we wish we had on day one" rule — but the subject is drugs instead of brains.

## What's inside

- `docs/` — the handbook content, rendered with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
  - **Fundamentals** — disease biology, drug modalities, medicinal chemistry, PK/PD, the math/stats/biology/chemistry/cheminformatics foundations.
  - **Target identification** — genomics, transcriptomics, proteomics, network biology, literature mining, target validation.
  - **Molecular design** — molecular representations, descriptors and fingerprints, QSAR, generative chemistry, structure-based design, docking, free-energy methods.
  - **Virtual screening** — ligand-based, structure-based, ultra-large libraries, active learning.
  - **ADMET / toxicity** — absorption, distribution, metabolism, excretion, in-silico safety, secondary pharmacology.
  - **Drug repurposing** — signature-based, knowledge-graph, real-world-evidence approaches.
  - **Clinical translation** — preclinical models, trial design, regulatory considerations, biomarkers, patient stratification.
  - **AI / ML** — classical ML on molecules, deep learning for chemistry and structure, protein language models, generative chemistry, foundation models.
  - **Data engineering** — DAGs, pipelines, observability, lakehouse patterns, MLOps — taught against real cheminformatics + assay workloads.
  - **Computing** — Python scientific stack, RDKit and OpenMM, containers, HPC, GPUs, cloud, reproducibility.
  - **Landmark work** — foundational papers, reference datasets (ChEMBL, PubChem, BindingDB, PDB, UniProt, DrugBank, …), major pipelines and atlases.
  - **Tutorials** — six end-to-end walk-throughs from target to molecule to figure, including a capstone.

## Quick start

```bash
# clone and install
git clone https://github.com/phindagijimana/drug_stack.git
cd drug_stack
pip install -e ".[docs,dev]"

# preview the site locally
mkdocs serve
```

## Reading the handbook online

Once GitHub Pages is enabled (see `.github/workflows/docs.yml`), the rendered site lives at **`https://<you>.github.io/drug_stack/`**.

## Status

Early. The skeleton and the high-traffic pages (fundamentals, target ID, molecular design, AI / ML, evaluation, tutorials) are written; some advanced chapters are deliberately concise pointers that will grow. Contributions and corrections are welcome — open an issue or PR.

## License

[MIT](LICENSE).
