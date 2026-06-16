# Computational & math foundations

> The prerequisite mathematics, biology, chemistry, statistics, and tooling for the rest of the handbook. Skip what you already have; come back when a later chapter assumes too much.

These chapters exist because drug discovery sits at an unusual intersection — chemistry, biology, pharmacology, statistics, distributed engineering — and almost no one walks in with all five. Use the table below to find your gaps.

| If you can't… | Read | Why |
| --- | --- | --- |
| read a SMILES and reason about RDKit objects | [Cheminformatics](cheminformatics.md) | The rest of the handbook assumes RDKit fluency |
| write a parquet pipeline in Polars or pandas | [Python](python.md), [Data analysis](data-analysis.md) | Everything is tabular under the hood |
| explain a t-test, a confidence interval, and a multiple-comparison correction | [Statistics](statistics.md) | Assay variance is real; "p < 0.05" is not enough |
| derive a gradient, eigenvalue, or KL divergence | [Mathematics](mathematics.md) | Generative-chemistry and force-field maths require it |
| explain the central dogma and a signalling pathway | [Biology](biology.md) | Target validation depends on it |
| describe sp³ vs sp² hybridisation and a Friedel–Crafts | [Chemistry](chemistry.md) | Talking to a synthetic chemist requires basics |
| read a PDB / mmCIF file and a Ramachandran plot | [Structural biology](structural-biology.md) | Docking and FEP assume it |
| ssh to a cluster and run a screen / tmux session | [Bash](bash.md), [CLI](cli.md) | Production work is not in a notebook |

## Chapters

- **[Python](python.md)** — language essentials, the scientific stack, what to actually install.
- **[Bash](bash.md)** — interactive shell + scripting basics. The minimum competent baseline.
- **[CLI commands](cli.md)** — `grep`, `awk`, `xargs`, `parallel`, `jq`, the standard Unix toolbox.
- **[Data analysis](data-analysis.md)** — pandas / Polars idioms specific to chemistry / assay data.
- **[Statistics](statistics.md)** — the chemistry-and-biology relevant subset: hypothesis tests, confidence intervals, multiple comparisons, calibration.
- **[Mathematics](mathematics.md)** — linear algebra, calculus, probability, optimisation. The bare minimum for the AI / ML chapters.
- **[Biology](biology.md)** — central dogma, signalling, pathways, immunology, neuroscience pointers.
- **[Chemistry](chemistry.md)** — organic, physical, and analytical chemistry priors.
- **[Cheminformatics](cheminformatics.md)** — RDKit deep dive, descriptors, fingerprints, transformations.
- **[Structural biology](structural-biology.md)** — protein structure, PDB / mmCIF, AlphaFold, Ramachandran, ligand-binding.

Each chapter is short — these are *foundations*, not graduate courses. The goal is a working baseline that the rest of the handbook can assume.
