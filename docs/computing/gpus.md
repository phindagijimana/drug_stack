# GPUs and accelerators

> Picking hardware for drug-discovery training and screening.

## The 2025 GPU lineup (NVIDIA)

| GPU | VRAM | Best for |
| --- | --- | --- |
| H100 / H200 | 80–144 GB | LLM, large foundation model training |
| A100 (40/80GB) | 40–80 GB | most ML training, FEP, large docking screens |
| L40S | 48 GB | inference + light training |
| A40 | 48 GB | smaller training, screening |
| L4 | 24 GB | inference, cheap GPUs |
| RTX 6000 Ada | 48 GB | workstation |
| Consumer (4090 / 5090) | 24–32 GB | dev / prototyping |

For most drug-discovery workloads (Chemprop training, classical QSAR, docking, modest MD), an A100 80GB is the workhorse. H100 / H200 are needed for foundation-model fine-tuning and very large generative work.

## Memory matters more than throughput (often)

A 24 GB consumer GPU trains a small Chemprop fine. A 24 GB GPU does **not** train a multitask Chemprop with 30 ADMET endpoints + a large hidden size. The batch-size collapse pushes you to gradient accumulation, slowing training.

For ML on molecules, the rule of thumb: pick the largest VRAM you can afford. Throughput is secondary.

## TPUs / other accelerators

- **TPUs** — Google's accelerator. Rarely the right call for drug-discovery work outside JAX-native MD groups (e.g. Google DeepMind's AlphaFold development).
- **Cerebras / Graphcore** — niche; useful for select foundation-model training.
- **AMD MI300** — closing the gap with NVIDIA; rare in drug discovery libraries.

For practical purposes in 2025, NVIDIA is the default and will be for the foreseeable future.

## Multi-GPU training

For models that fit on one GPU, distributed-data-parallel (DDP) across nodes is straightforward in PyTorch and worth the speedup.

For large generative models (REINVENT-scale), single-GPU is often fine; the bottleneck is rarely the model size.

For protein-language-model fine-tuning (ESM at 650M+ params), DDP across 2–8 GPUs is the standard pattern.

## CPU-only is fine too

A lot of drug-discovery work doesn't need GPUs:

- **Classical QSAR (RF, GBDT)** on 10k compounds — CPU.
- **Similarity search and clustering** — CPU.
- **Vina docking** at moderate exhaustiveness — CPU.
- **Standardisation, descriptor calculation** — CPU.

A team that defaults to GPU for everything is wasting money. Default to CPU; reach for GPU when a profiler says so.

## In practice

- **A100 80GB is the workhorse** for most drug-discovery ML.
- **Memory > throughput** for small-data molecular work.
- **Default to CPU**; profile before adding GPU.
- **Spot GPU instances** for screens; on-demand for training that can't checkpoint.

## Where to next

[Dependency management](dependencies.md) — pinning everything that runs on those GPUs.
