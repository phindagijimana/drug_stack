# Free-energy methods

> When docking is too noisy and experiment is too slow. FEP, TI, ABFE, λ-dynamics. The expensive workhorse for lead optimisation.

## Why this matters

Lead optimisation is a series of "I'm thinking of replacing this methyl with a CF₃ — what will it do to affinity?" decisions. A chemist who asks ten of these per week and waits two months for assay data is bottlenecked.

Free-energy methods predict the **relative binding affinity** between two close analogues with ~1 kcal/mol accuracy. That accuracy is enough to triage which analogues are worth synthesising.

## The fundamental idea

The thermodynamic cycle:

```
A_solvated  ──ΔG_bind(A)──→  A_bound
   │                              │
ΔG_solv(A→B)              ΔG_complex(A→B)
   ↓                              ↓
B_solvated  ──ΔG_bind(B)──→  B_bound
```

Closing the cycle: `ΔΔG_bind(B – A) = ΔG_complex(A→B) − ΔG_solv(A→B)`.

Computing **ΔΔG** is much cheaper than computing **ΔG** for each side independently because A and B share a scaffold; you only sample the difference.

## Methods

### Free-energy perturbation (FEP)

Run MD at intermediate λ-states between A and B; compute free-energy differences with the **Bennett acceptance ratio (BAR)** or its multistate variant (MBAR).

- **FEP+** (Schrödinger) [Wang et al., 2015](https://doi.org/10.1021/ja512751q)[^fep+] — the industrial benchmark.
- **AMBER TI, GROMACS FEP, OpenMM-based stacks (perses, perses-equilibrate)** — open-source.
- **PMX** — automation for setting up perturbation pairs.

### Thermodynamic integration (TI)

Compute `dG/dλ` at each λ and integrate. Mathematically equivalent to FEP under correct sampling; differs in numerics.

### Replica-exchange (REST, REST2)

Combines λ-windows with temperature replicas to improve sampling. Often necessary for buried polar interactions and ring flips.

### Absolute binding free energy (ABFE)

Compute `ΔG_bind` from scratch rather than relative to a reference. Used when no reference ligand exists, when you compare across scaffolds, or for fragment-to-lead.

ABFE is computationally heavier than FEP and notoriously sensitive to setup. It is becoming routine but is still a domain-expert workflow.

## How accurate?

On well-set-up calculations on tractable proteins, FEP+ delivers Mean Absolute Error of ~0.8–1.2 kcal/mol on ΔΔG. Translation: roughly 80–90% of the time, the FEP ordering matches the experimental ordering. That's good enough to triage but not to substitute experiment.

Common failure modes:

- **Insufficient sampling** of buried waters, side-chain rotamers, ring flips.
- **Force-field deficiencies** — modern force fields (OPLS4, AMBER FF19SB, ESPALOMA-2 for small molecules) help.
- **Charge-changing perturbations** — perturbing a +1 to neutral requires careful corrections.
- **Large structural rearrangements** — A→B differs by more than a small substituent; FEP assumption breaks.

## When to use FEP

| Situation | Recommendation |
| --- | --- |
| Triage 20 analogues for synthesis | FEP+ or open-source FEP |
| Cross-scaffold comparison | ABFE, or carefully-set-up multi-scaffold FEP |
| Million-compound screening | **Not FEP** — use docking + ML |
| Sub-1 kcal/mol decisions | Experiment, not FEP |
| Ranking enantiomers / tautomers | FEP works |
| Predicting absolute affinity | ABFE; expect ~2 kcal/mol error |

## ML-augmented free energy

Recent work uses neural-network potentials (ANI, AIMNet2, MACE) in place of or alongside classical force fields:

- **NNP/MM** hybrid simulations [Rufa et al., 2022](https://doi.org/10.1101/2020.07.29.227959)[^nnpmm] — quantum-accurate ligand within a classical protein.
- **MACE-OFF** [Kovács et al., 2023](https://doi.org/10.48550/arXiv.2312.15211)[^maceoff] — universal organic-chemistry NNP.

Adoption in routine FEP is still limited but increasing; expect this to be standard within a few years.

## In practice

- **Don't use FEP for screening**. Reserve it for lead optimisation where each analogue costs $10k+ to synthesise.
- **Set it up carefully or don't bother**. A poorly equilibrated FEP returns numbers that look authoritative but are not.
- **Validate against retrospective experimental data** on the same scaffold before relying on predictions.
- **Pair FEP with docking and QSAR**: the QSAR model trains on everything, docking provides poses, FEP refines the close-call analogues.

## References

[^fep+]: Wang L, Wu Y, Deng Y, et al. Accurate and reliable prediction of relative ligand binding potency in prospective drug discovery. *J Am Chem Soc.* 2015;137(7):2695–2703. [doi:10.1021/ja512751q](https://doi.org/10.1021/ja512751q)
[^nnpmm]: Rufa DA, Macdonald HEB, Fass J, et al. Towards chemical accuracy for alchemical free energy calculations with hybrid physics-based machine learning / molecular-mechanics potentials. *bioRxiv.* 2022. [doi:10.1101/2020.07.29.227959](https://doi.org/10.1101/2020.07.29.227959)
[^maceoff]: Kovács DP, Moore B, Browning N, et al. MACE-OFF23: transferable machine learning force fields for organic molecules. *arXiv:2312.15211.* 2023. [doi:10.48550/arXiv.2312.15211](https://doi.org/10.48550/arXiv.2312.15211)

## Where to next

[Multi-parameter optimization](mpo.md) — combining potency with ADMET into one objective.
