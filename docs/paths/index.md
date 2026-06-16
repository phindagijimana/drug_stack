# Reading paths

> With 100+ pages the question "where do I start?" matters. Five named paths through the handbook based on your background and target depth.

After [Getting started](../getting-started/index.md), pick the path that matches you. Each path tells you what to read, in what order, and what you'll be able to do by the end.

## Path A — Brand-new researcher (e.g. first-year graduate student)

You've taken some biology and statistics; you've written *some* Python; you've never run a cheminformatics pipeline.

1. [Fundamentals → Drug modalities](../fundamentals/drug-modalities.md)
2. [Fundamentals → Biological targets](../fundamentals/biological-targets.md)
3. [Fundamentals → Disease biology](../fundamentals/disease-biology.md)
4. [Fundamentals → Drug-discovery pipeline](../fundamentals/pipeline.md)
5. [Fundamentals → Medicinal chemistry](../fundamentals/medicinal-chemistry.md)
6. [Fundamentals → Pharmacology (PK/PD)](../fundamentals/pharmacology.md)
7. [Fundamentals → ADMET overview](../fundamentals/admet-overview.md)
8. [Target identification → index](../target-id/index.md)
9. [Tutorials → Similarity search on ChEMBL](../tutorials/similarity-search.md)
10. [Tutorials → QSAR walkthrough](../tutorials/qsar-walkthrough.md)
11. [Fundamentals → Foundations → Statistics](../fundamentals/foundations/statistics.md)
12. [Landmark → Foundational papers](../landmark/papers.md)

**Goal at the end**: you can read a drug-discovery methods section critically and design a small in-silico study yourself.

## Path B — Software / data engineer pivoting in

You're senior in Python and infra; you've never seen a SMILES string.

1. [Fundamentals → Foundations → Biology](../fundamentals/foundations/biology.md)
2. [Fundamentals → Foundations → Chemistry](../fundamentals/foundations/chemistry.md)
3. [Fundamentals → Drug modalities](../fundamentals/drug-modalities.md)
4. [Fundamentals → Drug-discovery pipeline](../fundamentals/pipeline.md)
5. [Fundamentals → Foundations → Cheminformatics](../fundamentals/foundations/cheminformatics.md)
6. [Molecular design → Molecular representations](../molecular-design/representations.md)
7. [Molecular design → Descriptors & fingerprints](../molecular-design/descriptors.md)
8. [Data engineering → Foundations](../data-engineering/foundations.md) → [DAG mental model](../data-engineering/dag.md) → [Five pillars](../data-engineering/five-pillars.md)
9. [Data engineering → Cheminformatics pipelines](../data-engineering/cheminformatics-pipelines.md)
10. [Data engineering → Lakehouse for chemistry & biology](../data-engineering/lakehouse.md)
11. [Computing → Containers + HPC + Cloud + GPUs](../computing/index.md)
12. [Tutorials → Capstone](../tutorials/capstone.md)

**Goal**: you can ship a production cheminformatics pipeline and have a defensible opinion on every tool choice.

## Path C — Medicinal chemist learning the computational side

You can draw a Michael acceptor in your sleep; you've never written a Python data-frame.

1. [Getting started → all four pages](../getting-started/index.md)
2. [Fundamentals → Foundations → Python](../fundamentals/foundations/python.md)
3. [Fundamentals → Foundations → CLI commands](../fundamentals/foundations/cli.md)
4. [Fundamentals → Foundations → Data analysis](../fundamentals/foundations/data-analysis.md)
5. [Fundamentals → Foundations → Cheminformatics](../fundamentals/foundations/cheminformatics.md)
6. [Molecular design → Molecular representations](../molecular-design/representations.md)
7. [Molecular design → Descriptors & fingerprints](../molecular-design/descriptors.md)
8. [Molecular design → QSAR / property prediction](../molecular-design/qsar.md)
9. [Molecular design → Multi-parameter optimization](../molecular-design/mpo.md)
10. [Molecular design → Generative chemistry](../molecular-design/generative.md)
11. [Virtual screening → Ligand-based screening](../screening/ligand-based.md)
12. [Virtual screening → Hit triage](../screening/hit-triage.md)
13. [AI / ML → Evaluation pitfalls](../ai/evaluation.md)
14. [Landmark → Datasets + Pipelines](../landmark/datasets.md)

**Goal**: you can review a computational-chemistry paper, replicate its workflow on your own series, and spot the methodological problems.

## Path D — ML engineer building drug-AI products

You've trained transformers; you've never thought about activity cliffs or scaffold hopping.

1. [Fundamentals → Drug modalities + Biological targets + Drug-discovery pipeline](../fundamentals/drug-modalities.md)
2. [Fundamentals → Foundations → Chemistry + Biology](../fundamentals/foundations/chemistry.md)
3. [Fundamentals → Foundations → Cheminformatics + Structural biology](../fundamentals/foundations/cheminformatics.md)
4. [Molecular design → Representations + Descriptors + QSAR](../molecular-design/representations.md)
5. [AI / ML → Classical ML on molecules](../ai/classical-ml.md)
6. [AI / ML → Deep learning for chemistry](../ai/deep-learning.md)
7. [AI / ML → Protein language models](../ai/protein-models.md)
8. [AI / ML → Generative chemistry models](../ai/generative-models.md)
9. [AI / ML → Foundation models](../ai/foundation-models.md)
10. [AI / ML → Evaluation pitfalls](../ai/evaluation.md)
11. [AI / ML → Uncertainty & calibration](../ai/uncertainty.md)
12. [Data engineering → MLOps for drug discovery](../data-engineering/mlops.md)
13. [Tutorials → Generative design](../tutorials/generative-design.md)

**Goal**: you can build a drug-AI model that survives a held-out scaffold split, an out-of-distribution target, and an FDA-style audit.

## Path E — Senior research engineer / tech-lead

You will not read 200 pages in order. You want the rules-of-thumb, the trade-offs, the tool landscape, and the failure modes.

1. [Fundamentals → Drug-discovery pipeline](../fundamentals/pipeline.md) — the 30-minute map.
2. [Fundamentals → Medicinal chemistry](../fundamentals/medicinal-chemistry.md) — enough to talk to chemists.
3. [Molecular design → Multi-parameter optimization](../molecular-design/mpo.md) — the actual objective function.
4. [Virtual screening → Ultra-large libraries](../screening/ultra-large.md) — what changes at billion-compound scale.
5. [Virtual screening → Active learning & iterative screens](../screening/active-learning.md) — the only sane way to do that scale.
6. [ADMET → In-silico toxicity](../admet-tox/toxicity.md) — what kills programmes late.
7. [AI / ML → Evaluation pitfalls](../ai/evaluation.md) — what kills models in production.
8. [AI / ML → Uncertainty & calibration](../ai/uncertainty.md) — the most under-used tool in industry.
9. [AI / ML → Regulatory & clinical deployment](../ai/regulatory.md) — what changes when a model touches a patient.
10. [Data engineering → MLOps for drug discovery](../data-engineering/mlops.md) — drift, retraining, model registries.
11. [Data engineering → Lakehouse for chemistry & biology](../data-engineering/lakehouse.md) — your central data plane.
12. [Computing → Reproducibility checklist](../computing/reproducibility.md) — the ten-question checklist before you ship.
13. [Tools landscape](../tools/index.md) — opinionated buy/build matrix.
14. [Landmark → Pipelines](../landmark/pipelines.md) — what your competitors stand on.

**Goal**: you can architect a drug-discovery AI platform, defend the design at a leadership review, and onboard the next staff engineer in a day.

## Re-using and remixing

These five paths cover the most common entry points. If you don't fit cleanly, mix them:

- **Postdoc switching from biology to ML** → Path A + Path D for ML side.
- **Industry SWE doing a rotation in a discovery team** → Path B then Path A's design chapters.
- **MD / PhD interested in repurposing** → Path C, then jump to [Drug repurposing](../repurposing/index.md) + [Clinical translation](../clinical/index.md).
- **Computational chemist becoming a tech lead** → Path C, then Path E.

When you finish a path, do the [end-to-end capstone tutorial](../tutorials/capstone.md). It's the synthesis exercise that turns reading into competence.
