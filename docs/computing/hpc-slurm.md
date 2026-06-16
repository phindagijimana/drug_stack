# HPC and Slurm

> The shared cluster substrate where much drug-discovery compute happens. Slurm survival kit.

## What HPC is good for

- **Embarrassingly parallel docking** of millions of compounds.
- **MD / FEP campaigns** spanning thousands of GPU-hours.
- **Bulk ML training** with multi-GPU nodes.
- **Long-running, low-bandwidth workloads** that AWS / GCP would price expensively.

## Slurm survival kit

```bash
# submit
sbatch run.slurm

# inspect queue
squeue -u $USER
squeue -j 1234567

# cancel
scancel 1234567

# resource accounting
sacct -u $USER --format=JobID,JobName,Elapsed,State,MaxRSS,ReqGRES

# interactive
srun --pty --partition=interactive --time=2:00:00 --gres=gpu:1 bash
```

A typical drug-discovery `run.slurm`:

```bash
#!/bin/bash
#SBATCH --job-name=vs_dock
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err
#SBATCH --time=24:00:00
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G

module load apptainer cuda/12.1

apptainer exec --nv \
    --bind /scratch/$USER:/scratch \
    /shared/images/drugstack-v0.5.0.sif \
    python -m drug_handbook.docking.run --library /scratch/library.parquet \
                                        --receptor /scratch/receptor.pdb \
                                        --out /scratch/dock_out/
```

## Array jobs for embarrassing parallelism

For "dock 100 batches of 10 000 compounds each":

```bash
#SBATCH --array=0-99%10        # 100 tasks, max 10 concurrent
#SBATCH --time=4:00:00

apptainer exec --nv image.sif python -m drug_handbook.docking.run \
    --shard $SLURM_ARRAY_TASK_ID --total 100
```

Array jobs are the right shape for screens; one big job with internal parallelism less so on most schedulers.

## Common pitfalls

- **Filling `$HOME`** with conda envs / pickles. Quotas catch you eventually.
- **Writing to network home from many tasks simultaneously.** Use node-local scratch.
- **Forgetting `--gres=gpu:1`** and silently running on CPU.
- **Long jobs at 100% wall-clock.** Slurm preempts; checkpoint regularly.
- **No checkpointing.** A 24-hour FEP that dies at hour 22 is not the worst thing — but you should be able to resume.

## Module systems

Most clusters use `module load` for software. A drug-discovery user's `module load` set is usually:

```bash
module load apptainer cuda/12.1 git python/3.11
```

For everything else (RDKit, OpenMM, PyTorch), use a container. Avoid relying on cluster-provided versions you cannot pin.

## In practice

- **One env per project, captured in a container.** Avoid cluster-version-specific installs.
- **Array jobs for screens, single jobs for training.**
- **Checkpoint long jobs.** Slurm preemption is real.
- **Node-local scratch for I/O-heavy work.**

## Where to next

[Cloud](cloud.md) — when to leave the cluster.
