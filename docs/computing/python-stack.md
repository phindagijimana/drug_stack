# Python scientific stack

> The packages every drug-discovery Python project ends up installing.

## The base

| Package | Role |
| --- | --- |
| `python` 3.10 or 3.11 | language |
| `numpy`, `scipy` | numerics |
| `pandas`, `polars` | tabular |
| `pyarrow` | columnar I/O, Parquet |
| `matplotlib`, `seaborn` | plotting |
| `jupyterlab` | interactive |
| `scikit-learn` | classical ML |
| `xgboost`, `lightgbm` | gradient-boosted trees |

## Chemistry

| Package | Role |
| --- | --- |
| `rdkit` | cheminformatics |
| `openbabel` | conversions, file formats |
| `mol2grid` | interactive molecule grids |
| `py3Dmol`, `nglview` | 3D viewers in notebooks |
| `chembl_downloader` | scripted ChEMBL access |
| `chemfp` / `FPSim2` | similarity search |

## Structure / MD

| Package | Role |
| --- | --- |
| `openmm` | MD engine |
| `mdtraj`, `MDAnalysis` | trajectory analysis |
| `prody` | protein dynamics |
| `biopython` | sequences, PDB IO |
| `pymol` (external) | structure visualisation |

## ML for chemistry

| Package | Role |
| --- | --- |
| `torch` | DL framework |
| `torch_geometric` | GNNs |
| `chemprop` | message-passing nets |
| `deepchem` | broader DL toolkit |
| `transformers` (HuggingFace) | LMs |
| `esm` | protein LMs |

## Generative chemistry

| Package | Role |
| --- | --- |
| `reinvent` | the workhorse RL generator |
| `aizynthfinder` | retrosynthesis |
| `selfies` | self-referential SMILES |
| `gflownet` | Bayesian flow nets |

## Docking and free energy

| Package | Role |
| --- | --- |
| `vina` (CLI) | docking |
| `gnina` (CLI) | ML-enhanced docking |
| `meeko` | ligand prep for AutoDock |
| `pyfreesa` | per-residue FEP analysis (academic) |

## Install recipe

```bash
micromamba create -n drugstack -c conda-forge \
    python=3.11 \
    numpy scipy pandas polars pyarrow matplotlib seaborn \
    jupyterlab ipywidgets \
    scikit-learn xgboost lightgbm \
    rdkit openbabel mol2grid py3dmol \
    openmm mdtraj MDAnalysis prody biopython \
    chemfp

micromamba activate drugstack
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install torch_geometric chemprop transformers esm-fold deepchem reinvent4 selfies aizynthfinder
```

## What to skip

- **Conda packages for everything Python-pure.** Mixing pip and conda creates ABI nightmares. Use conda only for C++-backed packages (RDKit, OpenMM, OpenBabel, NetCDF).
- **Massive monolith envs.** Use one env per project. Conda envs are cheap; broken envs are expensive.

## Where to next

[RDKit & OpenMM](rdkit-openmm.md) — the two non-Python-pure ones that need careful handling.
