# Virtual screening

> Searching libraries computationally before paying for synthesis. Ligand-based, structure-based, ultra-large, ML-driven, iterative.

A *physical* screen of 10⁶ compounds at a few cents per well still costs hundreds of thousands of dollars and weeks of time. A *virtual* screen of 10⁹ compounds costs a few thousand dollars of GPU time. The virtual screen does not get you compound in a tube — it gets you a 10× shorter, 100× narrower shopping list.

## Chapters

- **[Ligand-based screening](ligand-based.md)** — similarity, pharmacophore, ML scoring. When you have actives but no structure.
- **[Structure-based screening](structure-based.md)** — docking-based, ML pose-scoring. When you have structure.
- **[Ultra-large libraries](ultra-large.md)** — Enamine REAL, ZINC22, Wuxi GalaXi, billion-compound make-on-demand chemistry.
- **[Active learning & iterative screens](active-learning.md)** — the only sane way to screen 10⁹ compounds.
- **[Hit triage](hit-triage.md)** — turning a ranked list into a synthesis-and-test plan.

## The five regimes

| Regime | Size | Method |
| --- | --- | --- |
| Small (< 10⁵) | corporate library, ChEMBL subset | docking + ML rescoring; everything fits in memory |
| Medium (10⁵–10⁷) | ZINC drug-like, building-blocks | docking with parallelism; ECFP similarity index |
| Large (10⁷–10⁸) | full ZINC, vendor catalogues | active learning, GPU docking, ML rescoring |
| Ultra-large (10⁹–10¹⁰) | Enamine REAL, virtual catalogues | iterative ML screens; no full docking pass |
| Generative (∞) | designed on demand | covered in [Generative chemistry](../molecular-design/generative.md) |

Each regime has different bottlenecks. The right pipeline for 10⁵ compounds is the *wrong* pipeline for 10⁹. Industry teams maintain different pipelines for each.

## What virtual screening is not

- It is not "drug discovery in a box". A virtual screen produces a hypothesis-rich shopping list, not a clinical candidate.
- It is not a substitute for a good biological hypothesis. Screening against the wrong protein produces hits against the wrong protein.
- It is not a replacement for medicinal chemistry. Hits need optimisation; that part is unchanged.

## Where computation makes the biggest difference

- **Ultra-large search** is the killer use case. No HTS can touch a 10⁹-compound library.
- **Active learning** is the killer technique. Iterative re-ranking with experimental feedback typically finds hits in 10× fewer wet-lab plates.
- **ML rescoring of docked poses** improves hit rates on top-X over Vina alone, especially when trained on prospective experimental data.
- **Polypharmacology / off-target screening** — once you screen one library, run it across all known anti-targets.

## In practice

The classical "dock a million compounds, take the top 100" pipeline is now a baseline, not the state of the art. Modern pipelines:

1. Quickly **prefilter** the library (physchem, PAINS, in-house liabilities) — eliminate 50% before any expensive step.
2. **Coarse ranker** (ML on fingerprint, or fast docker like rDock/Vina-GPU) — rank 10⁸ → keep top 10⁶.
3. **Fine ranker** (high-exhaustiveness docking, ML-rescoring, MD-MM-PBSA on top hits) — rank 10⁶ → keep top 10⁴.
4. **Active-learning loop**: synthesise + test top 50, retrain, re-rank, repeat.
5. **Hit triage** — manual chemist review, structural sanity, novelty / IP check.

The chapters that follow each take one of these stages in detail.
