# Generative chemistry models

> Architectures, training dynamics, reward shaping. The ML side of [Molecular design → Generative chemistry](../molecular-design/generative.md).

This chapter assumes you've read the molecular-design overview. Here we focus on training mechanics.

## Architecture cheat sheet

| Family | Example | Best for |
| --- | --- | --- |
| SMILES LM (RNN) | REINVENT base | small, fast, decent novelty |
| SMILES Transformer | MolGPT, ChemLM | scaling base model |
| SELFIES LM | SELFIES-RL | guaranteed-valid generation |
| VAE | JT-VAE, CDDD | latent-space optimisation |
| Normalising flow | MoFlow, GraphAF | bijection; tractable likelihood |
| GAN | MolGAN | small molecules |
| Diffusion (2D / 3D) | DiffSBDD, MolDiff | 3D-aware design, in-pocket gen |
| RL fine-tuning | REINVENT, GENTRL | any base + a reward signal |

## RL fine-tuning in detail

The reinforcement-learning loop that drives REINVENT and its descendants:

```python
for step in range(num_steps):
    # 1) sample
    smiles, log_probs = agent.sample(batch_size=64)

    # 2) score
    rewards = scoring_function(smiles)            # multi-component
    advantages = rewards - rewards.mean()         # subtract baseline

    # 3) policy gradient update
    loss = -(advantages.detach() * log_probs).mean()

    # 4) prior anchoring (KL to pretrained agent)
    loss += alpha * KL(agent, prior)

    optimiser.zero_grad()
    loss.backward()
    optimiser.step()
```

Key practical details:

- **Prior anchoring** (KL term) is non-negotiable. Without it, the agent collapses onto reward-maximising but unphysical chemistry.
- **Baseline subtraction** stabilises the gradient.
- **Score normalisation** — components on different scales must be normalised, or one dominates.
- **Curriculum** — start with one objective; add components gradually.

## Reward shaping

The reward function combines multiple objectives. Common forms:

```python
def reward(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None or not passes_filters(mol):
        return 0.0

    components = {
        "potency":      sigmoid(qsar_predict(mol) - 7.0),
        "selectivity":  sigmoid(selectivity_predict(mol) - 2.0),
        "qed":          qed_score(mol),
        "sa":           1.0 - (sa_score(mol) - 1) / 9.0,
        "p_herg":       1.0 - hERG_predict(mol),
        "p_ames":       1.0 - AMES_predict(mol),
    }
    return geometric_mean(components.values())   # multi-objective collapse
```

**Multiplicative (geometric mean) > additive (weighted sum)** for desirability scoring: one bad property tanks the score, which is the right behaviour.

For Pareto-frontier optimisation, modern REINVENT and similar tools support multi-objective RL natively.

## Common failure modes

- **Mode collapse** — generator outputs one repetitive scaffold. Fix: diversity penalty, KL anchoring, entropy regularisation.
- **Reward hacking** — generator finds molecules that score well artificially (e.g. exploits SA-score weakness, finds OOD region of QSAR). Fix: uncertainty-aware scoring, structural-novelty penalty, manual triage.
- **Validity collapse** — RL pushes agent toward invalid SMILES. Fix: SELFIES, or post-hoc validity filter, or RL only on valid trajectories.
- **OOD exploitation** — generator produces molecules where all scoring models are unreliable. Fix: pessimistic uncertainty (`mean - k * sd`) or in-distribution penalty.

## Constrained generation

Often you want generation *near* a known active. Two main techniques:

- **Scaffold-constrained generation** — fix the scaffold, generate substituents. REINVENT supports this via SMILES-templating.
- **Latent-space optimisation around a known molecule** — encode the seed, optimise in latent space, decode.

The "scaffold hopping with constraints" use case is the most common production application of generative chemistry today.

## Synthesis-aware generation

Already mentioned in [Generative chemistry](../molecular-design/generative.md). The pragmatic options:

- **SA-score in reward** — fast, weak.
- **SCScore / RAscore** — better predictors of synthesisability.
- **AiZynthFinder retrosynthesis success in reward** — slow but real.
- **Generate only from reaction-product spaces** — REINVENT's "reaction-based generation" mode constrains the search to chemistry that retrosyntheses cleanly by construction.

## Evaluation

Standard generative-chemistry metrics:

- **Validity** — fraction of generated SMILES parsable.
- **Uniqueness** — fraction of unique molecules.
- **Novelty** — fraction not in training set.
- **Internal diversity** — Tanimoto pairwise diversity within batch.
- **Property match** — fraction satisfying constraints.
- **FCD / Fréchet ChemNet Distance** — distributional similarity to a reference set.

For production work, the only metric that matters is **fraction of generated molecules that synthesise and bind**. Everything else is a proxy.

## In practice

- **REINVENT 4 with a multi-component desirability reward is the right industrial default.**
- **KL anchoring + multiplicative reward + uncertainty-aware scoring** are the three load-bearing tricks.
- **Manual chemist triage of generated batches is non-optional.**
- **Pair generation with active learning** — synthesise the top-K, measure, retrain the scorers, repeat.

## Where to next

[Foundation models](foundation-models.md) — the upstream side of the stack.
