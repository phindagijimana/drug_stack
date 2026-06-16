# Containers (Docker, Apptainer)

> Reproducibility's load-bearing technology. The non-optional production layer.

## Why containers

A container ships **code + environment + dependencies** as one artefact. Three problems they solve:

1. **Reproducibility** — "works on my laptop" survives the trip to the cluster.
2. **Onboarding** — new team members run `docker pull` and have the env in minutes.
3. **Regulatory audit** — pin the exact environment used to produce IND-supporting analyses.

## Docker vs Apptainer

| Aspect | Docker | Apptainer (formerly Singularity) |
| --- | --- | --- |
| Runtime | daemon (root) | rootless (user) |
| Best for | dev laptops, cloud | HPC (shared cluster) |
| Image format | OCI | SIF (single file) |
| GPU | `--gpus all` | `--nv` |
| Filesystem | overlay | bind-mount user dirs |
| Network | flexible | host network by default |

Most teams build images with Docker (`docker build`), push to a registry, and pull with either Docker (cloud / dev) or Apptainer (HPC).

## A drug-discovery Dockerfile

```dockerfile
FROM mambaorg/micromamba:1.5.6 AS base

ARG MAMBA_DOCKERFILE_ACTIVATE=1
USER root
RUN apt-get update && apt-get install -y --no-install-recommends git wget && rm -rf /var/lib/apt/lists/*
USER mambauser

COPY env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

WORKDIR /work
COPY . /work
RUN pip install -e ".[dev]"

ENTRYPOINT ["python"]
CMD ["-m", "drug_handbook.cli", "--help"]
```

Practical tips:

- **`mambaorg/micromamba`** for fast conda-based env builds.
- **Pin everything** (`env.lock.yaml` or `conda-lock`) — unpinned envs are non-reproducible.
- **Multi-stage builds** when including heavy build deps (CUDA tooling) that should not be in the runtime image.
- **Tag releases** (`registry/drugstack:v0.5.0`), don't rely on `:latest`.

## Apptainer on HPC

```bash
# build SIF from a Docker image
apptainer build drugstack.sif docker://registry/drugstack:v0.5.0

# run with GPU + bind-mounting cluster home
apptainer exec --nv \
    --bind /scratch/$USER:/scratch \
    drugstack.sif python -m drug_handbook.cli train
```

The bind-mount pattern keeps the code reproducible while letting the container read your cluster data.

## CI for images

```yaml
jobs:
  build:
    steps:
      - uses: docker/build-push-action@v5
        with:
          context: .
          tags: registry/drugstack:${{ github.sha }}
      - run: docker push registry/drugstack:${{ github.sha }}
  test:
    needs: build
    steps:
      - run: docker run registry/drugstack:${{ github.sha }} pytest -q
```

Build, push, test on every commit. Promote to a `vX.Y.Z` tag at release.

## In practice

- **Containerise as soon as the project has > 1 contributor.**
- **Pin the env file** — that is most of the reproducibility win.
- **For HPC, use Apptainer.** For cloud / laptops, Docker.
- **Don't commit secrets** into images. Build-arg secrets, runtime env vars, or a vault.

## Where to next

[HPC and Slurm](hpc-slurm.md) — using containers in batch.
