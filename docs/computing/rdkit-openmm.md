# RDKit & OpenMM

> The two C++-backed packages every drug-discovery Python developer hits. Practical install + usage notes.

## RDKit

The cheminformatics library you cannot escape. C++ with Python bindings.

- **Install via conda-forge.** Pip wheels exist but are flaky on some platforms.
- **Version regularly**; new releases improve standardisation, fingerprint generation, and rendering.
- **Performance**: for batch operations, use `rdFingerprintGenerator` (per-mol, with reused generators) rather than module-level functions.
- **Multiprocessing**: RDKit `Mol` objects pickle correctly; safe with `multiprocessing`. SDF / SMILES parsing in parallel is straightforward.

A few practical idioms:

```python
from rdkit import Chem, RDLogger
RDLogger.DisableLog("rdApp.*")           # silence the warnings flood
mol = Chem.MolFromSmiles("CCO", sanitize=True)
```

For long-running pipelines, capture or silence RDKit warnings — production logs unreadable otherwise.

## OpenMM

The modern MD engine, used for FEP, ABFE, ML/MM hybrid simulations, and conformer sampling.

- **Install via conda-forge** with explicit CUDA build matching the system driver.
- **`openmm.testInstallation()`** is the ground truth that the install works.
- **For GPU work**, choose the CUDA platform; verify with `Platform.getPlatformByName('CUDA')`.
- **Tools built on OpenMM**: openmmtools, openmm-ml, openff-toolkit (for molecule parameterisation).

A minimal OpenMM simulation script (water in a box) is < 50 lines; for real biomolecular work, use higher-level orchestrators (OpenMM-Setup, OpenMMTools, BioSimSpace).

## Common pitfalls

- **RDKit + PyTorch in the same env** can fight over NumPy ABI. Install RDKit via conda first; PyTorch via pip second.
- **OpenMM CUDA fail at runtime** despite test passing — usually a driver/runtime mismatch. `nvidia-smi` and `nvcc --version` should agree on major CUDA version.
- **MMFF / UFF parameter coverage** — RDKit's force fields cover most organic chemistry but fail on metals and unusual elements. For those, use OpenFF parameters via openff-toolkit.

## In practice

- Conda-forge for both; one env per project.
- Validate the install with a smoke test on day one.
- For GPU work, check `openmm.testInstallation()` against expected platforms.

## Where to next

[Containers](containers.md) — when "works on my machine" stops being acceptable.
