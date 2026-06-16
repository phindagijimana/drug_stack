# 1. Installing your environment

> The minimum stack: Python 3.10+, conda or `uv`, RDKit, a few well-chosen packages. Reproducible, isolated, no system-wide installs.

## The stack at a glance

| Layer | Pick | Why |
| --- | --- | --- |
| Python | 3.10 or 3.11 | RDKit wheels and most ML libraries are tested here. |
| Environment manager | `micromamba` (or `mamba`/`conda`) | RDKit's C++ stack is most painless via conda-forge. |
| Cheminformatics | `rdkit` | The non-negotiable. |
| Numeric / DataFrame | `numpy`, `pandas`, `polars` | Standard. |
| Plotting | `matplotlib`, `seaborn` | And `mols2grid` for molecule grids. |
| ML | `scikit-learn`, `xgboost`, `torch`, `torch-geometric` | Add `chemprop` or `deepchem` only when needed. |
| Structure | `openmm`, `mdtraj`, `biopython`, `prody` | For docking and MD. |
| Notebooks | `jupyterlab` | The interactive surface. |

## Install (recommended path)

```bash
# 1. install micromamba (fast, conda-compatible)
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)

# 2. create the environment
micromamba create -n drugstack -c conda-forge \
    python=3.11 rdkit pandas polars numpy matplotlib seaborn \
    jupyterlab scikit-learn xgboost ipywidgets \
    openmm mdtraj biopython prody py3dmol mols2grid

# 3. (optional) add PyTorch on a CUDA machine
micromamba activate drugstack
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install torch_geometric  # then follow torch_geometric install notes for your CUDA build
```

## Verify

```python
import rdkit, numpy, pandas
from rdkit import Chem
from rdkit.Chem import AllChem, Draw

print("RDKit:", rdkit.__version__)
mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")   # aspirin
print("Atoms:", mol.GetNumAtoms())
print("MW:", Chem.Descriptors.MolWt(mol))
print("LogP:", Chem.Descriptors.MolLogP(mol))
```

You should see the atom count (13), molecular weight (~180), and a clogP near 1.2. If that runs, the rest of the handbook will run.

## Optional but useful

- **`uv`** — a fast pip / pip-tools replacement for pure-Python deps you'll add later.
- **`conda-lock`** — pin the full conda solve to a lockfile for reproducibility.
- **`direnv`** — auto-activate the env when you `cd` into the repo.
- **`pre-commit`** — guardrails for code you'll commit. The handbook repo ships a config.

## Common install gotchas

- **RDKit via pip on macOS Apple Silicon** sometimes hangs or installs a broken wheel. Stay on conda-forge.
- **PyTorch + RDKit in the same env** can dispute on Numpy ABI versions if you mix wheels. Install via conda-forge first, *then* pip for PyTorch with `--no-deps` if needed.
- **`torch_geometric`** has CUDA-version-specific wheels for `torch_scatter`, `torch_sparse`. Follow the [official table](https://pytorch-geometric.readthedocs.io/) — don't guess.
- **OpenMM CUDA build** needs a CUDA toolkit version that matches the driver. `openmm.testInstallation()` is the only ground truth.

## Where to next

[Your first SMILES](first-smiles.md) — turn a string into a molecule and learn the three minimum descriptors every cheminformatician memorises.
