# Getting started

> A 30-minute on-ramp. By the end you will have an environment that can read SMILES, screen a tiny library, and render a publication-style figure of the hits.

There are four short pages. Each one assumes the previous is done.

1. **[Installing your environment](install.md)** — Python, conda, RDKit, a few packages. A working `import rdkit; print(rdkit.__version__)`.
2. **[Your first SMILES](first-smiles.md)** — parse a SMILES string, compute a fingerprint and three descriptors, draw a molecule.
3. **[Your first virtual screen](first-screen.md)** — similarity search a 10k-compound subset of ChEMBL against a query.
4. **[Your first figure](first-figure.md)** — render the top-N hits as an aligned 2D grid suitable for a slide or a paper.

If something breaks, jump to [Computing → Dependency management](../computing/dependencies.md) and [Computing → Reproducibility checklist](../computing/reproducibility.md).

## Conventions used in this handbook

- **Code blocks** are runnable. If a snippet has unstated dependencies, the page says so explicitly.
- **References** use footnotes with DOIs at the bottom of the page. If a claim has no citation, it is a rule of thumb, not a finding.
- **Admonitions** flag depth:

!!! note "Beginner"
    Optional reading you can skip on a first pass; included so the rest of the page makes sense.

!!! info "PhD-level depth"
    Treatments suitable for a methods committee or a thesis chapter.

!!! tip "Senior research engineer"
    Pragmatic engineering trade-offs, scale, observability, organisational notes.

- **"In practice"** sections at the end of most chapters are the actionable summary.

## What this handbook is *not*

- It is not a substitute for a medicinal-chemistry textbook (Patrick's *Introduction to Medicinal Chemistry* or Silverman & Holladay's *Organic Chemistry of Drug Design and Drug Action* are still the references).
- It is not an FDA / EMA regulatory consultancy. The [Clinical translation](../clinical/index.md) section is a literate primer, not a compliance manual.
- It is not an exhaustive software directory. It is opinionated. When two tools do the same thing we usually pick one.
