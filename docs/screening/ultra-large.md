# Ultra-large libraries

> Enamine REAL, ZINC22, Wuxi GalaXi, and the billion-compound make-on-demand catalogues. What changes at this scale.

## The make-on-demand revolution

Until ~2015, the limit of computational screening was a few million purchaseable compounds in ZINC or in-house libraries. Then Enamine and others began publishing *make-on-demand* catalogues — billions of virtual compounds defined by combining building blocks via well-validated reactions, with ~80–90% chance of successful synthesis at lead time of 6–12 weeks.

The numbers in 2025:

- **Enamine REAL** — ~40 billion virtual compounds.
- **ZINC22** — billions of curated purchaseable + REAL-like.
- **Wuxi GalaXi** — similar scale, different reaction set.

A computationalist with access to one of these catalogues and a working virtual-screening pipeline can search a chemical space *four orders of magnitude larger* than was possible a decade ago.

## What this changes computationally

Brute-force docking is no longer an option:

| Library size | Docking @ 10 s/compound | Cost |
| --- | --- | --- |
| 10⁶ | ~115 CPU-days | hours on a cluster |
| 10⁸ | ~30 CPU-years | months on the same cluster |
| 10¹⁰ | ~3000 CPU-years | not feasible without rethink |

Three approaches scale:

### 1. ML-only screens

Train a fast ML model on a subset of dock scores, predict the rest with the model.

- **Pro**: orders of magnitude speedup once the model is trained.
- **Con**: the model is only as good as the docking labels — and dock-score quality is mediocre.

### 2. Hierarchical / coarse-to-fine

Apply progressively expensive scorers, surviving only the top fraction at each stage:

```
10¹⁰ → property + PAINS filter → 10⁹
10⁹  → cheap ML (ECFP + GBDT)  → 10⁷
10⁷  → fast docking (rDock)    → 10⁵
10⁵  → high-exhaustiveness Vina → 10⁴
10⁴  → ML rescoring + MM-GB/SA → 10³
10³  → manual triage           → 50
```

This is the workhorse pattern. Most published ultra-large screens follow some variant.

### 3. Active learning (the most efficient)

Rather than score every compound, repeatedly score a small *informative* subset, train a model, propose the next subset.

See [Active learning](active-learning.md).

## Practical pipeline: ZINC22 + GPU Vina

```bash
# 1) prefilter
zinc_filter.py --input zinc22.smi --max_mw 500 --min_mw 250 \
               --max_logp 5 --no_pains --output zinc22_filtered.smi

# 2) ECFP-similarity baseline (10⁹ → 10⁸)
fpsim2_search.py --query reference_actives.smi --library zinc22_filtered.smi \
                 --threshold 0.35 --output candidates_10M.smi

# 3) fast dock on GPU
vina-gpu --receptor receptor.pdbqt --ligand_directory candidates_10M_pdbqt/ \
         --output ranked.csv

# 4) ML rescoring of top 1M
gnina_rescore.py --input top_1M.csv --receptor receptor.pdb --output rescored.csv
```

Times: ~12 GPU-hours for step 3, ~6 GPU-hours for step 4, on a single A100. Total: a 10⁹-compound logical search in a day on one node.

## Notable published successes

- **AmpC β-lactamase** [Lyu et al., 2019](https://doi.org/10.1038/s41586-019-0917-9)[^lyu] — Shoichet lab, ~138 million docked, hit rate ~10% of synthesised compounds at sub-µM Ki. The proof point that ultra-large works.
- **D₄ dopamine receptor** [Lyu et al., 2019, same paper] — same campaign, GPCR.
- **σ2 receptor** [Alon et al., 2021](https://doi.org/10.1038/s41586-021-04175-x)[^alon] — Roth lab, structure of σ2 enabled an ultra-large screen → potent novel ligands.

The pattern: at billion-compound scale, hit rates per synthesised compound *go up*, not down. Most hits are out of reach of curated libraries.

## Caveats

- **Synthesis is the gate.** Top hits that fail synthesis are wasted. Filter for retrosynthesis success (AiZynthFinder, RAscore) before ordering.
- **The library distribution is biased** by the reactions available. New scaffolds are limited to building blocks × reactions; novelty in chemical-space terms is shallower than the size suggests.
- **The pocket gets re-validated against far-more-permissive chemistry.** Many "ultra-large hits" reveal that the docking pipeline finds ligands in a non-relevant sub-pocket; experimental validation is non-optional.
- **IP and patent space** become real concerns at scale; check before ordering.

## In practice

- **A good MPO filter pre-docking** reduces the candidate set by 10–100× at very low cost.
- **GPU Vina or DiffDock for the dock pass** if you have hardware; otherwise an active-learning loop.
- **Order 50–500 compounds in tranches**, not 50 all at once. The first tranche tells you whether your pipeline is calibrated.
- **Record hit rates per stage** — they are your early-warning system for a pipeline that has gone off.

## References

[^lyu]: Lyu J, Wang S, Balius TE, et al. Ultra-large library docking for discovering new chemotypes. *Nature.* 2019;566:224–229. [doi:10.1038/s41586-019-0917-9](https://doi.org/10.1038/s41586-019-0917-9)
[^alon]: Alon A, Lyu J, Braz JM, et al. Structures of the σ2 receptor enable docking for bioactive ligand discovery. *Nature.* 2021;600:759–764. [doi:10.1038/s41586-021-04175-x](https://doi.org/10.1038/s41586-021-04175-x)

## Where to next

[Active learning](active-learning.md) — the technique that makes 10¹⁰ tractable without docking each compound.
