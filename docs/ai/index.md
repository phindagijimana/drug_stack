# AI / ML for drug discovery

> What machine learning on chemistry and biology actually looks like. The parts that are specific to drug discovery, not generic ML.

This section assumes you can write training loops in PyTorch (or are willing to learn). It focuses on the parts of ML that are *specific* to drug discovery — the parts that bite teams who arrive from generic computer vision or NLP.

## Chapters

- **[Classical ML on molecules](classical-ml.md)** — when you don't need deep learning. Random forests, GBDT, SVMs on fingerprints and descriptors. The bar everything else has to beat.
- **[Deep learning for chemistry](deep-learning.md)** — message-passing networks, transformers on SMILES, 3D-equivariant models, multitask learning.
- **[Protein language models](protein-models.md)** — ESM, ProtTrans, ProGen, AbLang. What they capture, what they don't.
- **[Generative chemistry models](generative-models.md)** — the ML side of the generative-chemistry chapter, with more depth on training mechanics and reward shaping.
- **[Foundation models](foundation-models.md)** — large pretrained models for chemistry and biology, what's actually available, when fine-tuning beats training from scratch.
- **[Evaluation pitfalls](evaluation.md)** — scaffold leakage, time-split sanity, activity cliffs, AUROC inflation. The chapter that prevents most embarrassments.
- **[Uncertainty & calibration](uncertainty.md)** — ensembles, GPs, conformal prediction. The most under-used tool in industry drug-AI.
- **[Regulatory & clinical deployment](regulatory.md)** — what changes when a model touches patients. SaMD, GMLP, MDR.

## Why this is separate from generic ML

Three reasons drug-discovery ML is different enough to warrant its own section:

1. **The data is small, biased, and censored.** A target-specific assay set is typically hundreds to low-thousands of compounds, almost always from one chemical series, almost always with the low-affinity tail censored. Generic scaling intuitions do not transfer.
2. **The objective is multi-dimensional.** "Active" is necessary; potent + selective + permeable + soluble + non-toxic + synthesisable is the actual goal. A model optimising one dimension produces unusable molecules.
3. **Distribution shift dominates.** A model that aces a random split fails on a new scaffold, a new target paralog, or a new cell line. Generalisation matters more than peak performance.

Everything in this section is written with those three constraints in mind.
