# Dependency management

> Conda, pip, uv, lockfiles. The chain of reproducibility from a `git clone` to a running model.

## The hierarchy

| Tool | Use |
| --- | --- |
| **micromamba / conda / mamba** | manage envs containing C++/native libs (RDKit, OpenMM, OpenBabel) |
| **pip** | Python-pure packages, latest versions |
| **uv** | fast pip-compatible installer; great for pure-Python deps |
| **conda-lock** | reproducible conda lockfile |
| **pip-tools / uv pip compile** | reproducible pip lockfile |
| **Poetry / hatch** | package management for libraries |

## The recipe

1. `env.yaml` for the conda environment (Python + RDKit + OpenMM + ...).
2. `pyproject.toml` for project deps installable via pip.
3. `conda-lock.yml` (committed) pinning the conda solve.
4. `uv.lock` (committed) pinning the pip resolution.
5. Dockerfile that materialises both into an image.
6. CI rebuilds the image weekly to catch upstream breaks early.

The point: every commit at every moment is reproducible to a single conda+pip resolution.

## A workable env.yaml

```yaml
name: drugstack
channels: [conda-forge]
dependencies:
  - python=3.11
  - rdkit=2024.03
  - openmm=8.1
  - openbabel=3.1
  - numpy
  - scipy
  - pandas
  - polars
  - pyarrow
  - scikit-learn
  - xgboost
  - matplotlib
  - seaborn
  - jupyterlab
  - pip
  - pip:
    - torch==2.4.1+cu121
    - torch_geometric
    - chemprop==2.0.4
    - transformers==4.45
    - reinvent4==4.6.0
```

Two simultaneous constraints: conda for native, pip for Python-pure. The pip section inside conda is the conventional way to bridge.

## Lockfiles

```bash
# generate conda lock
conda-lock lock -f env.yaml -p linux-64 -p osx-arm64

# generate pip lock for the pure-Python deps
uv pip compile pyproject.toml -o requirements.lock
```

Commit both. CI checks they install cleanly.

## Why this matters in drug discovery

Three specific drug-discovery reasons reproducibility is harder than generic ML:

1. **RDKit minor versions change canonical SMILES** for edge cases. A version drift produces silent join failures.
2. **PyTorch + CUDA + native bindings (torch_geometric)** compatibility is fragile.
3. **Models pickled with one library version** may fail to load on another. Version-pin the load path.

## In practice

- **Conda for native; pip for Python-pure.** Don't mix.
- **Lock conda *and* pip.** Both lockfiles in source control.
- **Build a fresh image weekly in CI.** Catches upstream breakage when it's small, not when you're trying to file an IND.
- **Pin model artefact versions** in the model registry against the lockfile version that produced them.

## Where to next

[Reproducibility checklist](reproducibility.md) — the ten-item check before you ship anything.
