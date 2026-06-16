# Python

> The language of drug-discovery computing. Enough to read the rest of the handbook fluently.

## Why Python

The scientific Python stack (NumPy, SciPy, pandas / Polars, scikit-learn, matplotlib, PyTorch, RDKit) is where the work happens. Everyone you collaborate with will hand you Python. Other languages exist (Julia for some MD, R for stats, Rust for new pipeline tools), but Python is the lingua franca.

## The 20 % of Python you will use 80 % of the time

```python
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass(frozen=True)
class Compound:
    chembl_id: str
    smiles: str
    pIC50: float | None = None

def load_jsonl(path: Path) -> list[Compound]:
    return [Compound(**json.loads(line)) for line in path.read_text().splitlines()]

mols = load_jsonl(Path("hits.jsonl"))
actives = [m for m in mols if m.pIC50 is not None and m.pIC50 > 7.0]
```

Things this snippet exercises that any data-scientist-shaped Python user should be solid on:

- `dataclass(frozen=True)` for immutable records.
- `pathlib` over `os.path`.
- Type hints (`list[Compound]`, `float | None`).
- List comprehensions.
- Truthy / Noneness conventions.

If any of those need a moment, work through the official [Python tutorial](https://docs.python.org/3/tutorial/) — it is short.

## The scientific stack

| Library | What it is | When |
| --- | --- | --- |
| **NumPy** | n-d arrays, vectorisation | Everywhere; rarely instantiate it directly any more |
| **SciPy** | scientific functions (stats, linalg, optimize, sparse) | Stats tests, optimisation, sparse FP arithmetic |
| **pandas** | DataFrame; column-major, indexable | Smallish (< 10 GB) tabular data |
| **Polars** | DataFrame; column-major, query-planned | Bigger tabular data; bigger than pandas, smaller than Spark |
| **PyArrow / Parquet** | Columnar binary format | The right on-disk format for any tabular drug-discovery dataset |
| **scikit-learn** | Classical ML | RF / GBT / SVM on fingerprints |
| **PyTorch** | DL framework | GNNs, sequence models, generative chemistry |
| **JAX** | DL + autograd, functional | Some recent biophysics work |
| **matplotlib / seaborn / plotly** | Plotting | Always |

## Idioms that turn up in this handbook

**Vectorise.** Avoid per-row Python loops where a column operation will do.

```python
import polars as pl
import numpy as np

df = pl.read_parquet("compounds.parquet")
df = df.with_columns(
    pIC50=-np.log10(df["ic50_nM"] * 1e-9),
    is_active=df["ic50_nM"] < 1000,
)
```

**Type your IO boundaries.** Functions that take or produce file paths and dataframes should annotate them; everything internal can stay informal.

**Cache expensive computations explicitly.** `functools.lru_cache` for pure-Python results; Parquet for dataframes; on-disk pickles for ML model artefacts.

```python
from functools import lru_cache
from rdkit import Chem

@lru_cache(maxsize=100_000)
def mol_from_smiles(smi: str):
    return Chem.MolFromSmiles(smi)
```

**Handle parsing failures.** RDKit and biology data are noisy; let bad rows surface but do not let them crash a pipeline.

```python
def safe_mw(smi: str) -> float | None:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    return Chem.Descriptors.MolWt(mol)
```

## What to skip

- **Multiple inheritance / metaclasses.** Almost never useful in drug-discovery code. If you reach for them, take a walk first.
- **Custom asyncio frameworks.** Async is fine; reinventing the wheel for a screening pipeline is not.
- **Premature parallelisation.** Profile first — most "slow" pipelines are really one un-vectorised pandas loop.

## Where to next

[Bash](bash.md) — because no one runs production cheminformatics from a notebook.
