# Molecular design

> Once a target is set, how chemistry actually iterates on molecules — computationally. Representations, descriptors, QSAR, generative chemistry, docking, FEP, multi-parameter optimisation.

This section assumes you can write Python and understand fingerprints (covered in [Fundamentals → Cheminformatics](../fundamentals/foundations/cheminformatics.md)). It focuses on the parts of molecular design that are *specific* to drug discovery — the parts that bite teams arriving from generic ML.

## Chapters

- **[Molecular representations](representations.md)** — SMILES, SELFIES, InChI, molecular graphs, 3D conformer ensembles, what each enables and disables.
- **[Descriptors & fingerprints](descriptors.md)** — physchem descriptors, Morgan / ECFP, MACCS, atom-pair, topological, learned (Mol2Vec, ChemBERTa).
- **[QSAR / property prediction](qsar.md)** — classical and modern. Random forest baseline, GBDT, message-passing networks, what to use when.
- **[Generative chemistry](generative.md)** — autoregressive, VAE, RL, diffusion. SMILES-LM, GraphAF, MolGAN, REINVENT, DiffSBDD.
- **[Structure-based design](structure-based.md)** — pocket-aware design, hot-spot exploitation, growing/linking/merging fragments.
- **[Docking](docking.md)** — AutoDock Vina, Glide, GOLD, gnina, DiffDock, Boltz. When to trust scores and when not.
- **[Free-energy methods](free-energy.md)** — FEP, TI, λ-dynamics, ABFE. The expensive workhorse for lead optimisation.
- **[Multi-parameter optimization](mpo.md)** — the actual objective function. Why "potency-only" optimisation produces undeployable molecules.

## Why this is separate from generic ML

Three reasons molecular design is different enough to warrant its own section:

1. **The data is small, biased, and censored.** A reasonable target-specific assay set is 100–10 000 compounds, almost always from one chemical series, almost always with activity censored at the low-affinity tail. Standard ML scaling intuitions do not transfer.
2. **The objective is multi-dimensional and non-linear.** "Active" is necessary; potent + selective + permeable + soluble + metabolically stable + non-hERG + synthesisable is the actual goal. A model optimising one dimension produces unusable molecules.
3. **Synthesisability is a hard constraint.** A model that generates beautiful, low-binding-energy molecules a chemist cannot make is solving a math problem, not a drug problem. Synthesis-aware design is now mandatory.

Everything in this section is written with those three constraints in mind.
