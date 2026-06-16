# Testing pipelines

> The tests that catch real drug-discovery bugs. Golden datasets, contract tests, schema validation, regression tests.

## The four kinds of tests

1. **Unit tests** — single functions (canonicalise, compute fingerprint, fit Hill curve).
2. **Schema tests** — table contracts (column names, types, allowed values).
3. **Data tests** — properties of data ("no compound has MW > 2000", "no IC50 is negative").
4. **Regression tests** — golden datasets that should produce known outputs.

Each catches different bugs. Skipping any of them lets a class of bug live.

## Unit tests for cheminformatics

Standard pytest, with chemistry-specific assertions:

```python
import pytest
from rdkit import Chem

def test_canonical_smiles_is_stable():
    smis = ["OC(=O)c1ccccc1OC(C)=O", "CC(=O)Oc1ccccc1C(=O)O"]
    canon = [Chem.MolToSmiles(Chem.MolFromSmiles(s)) for s in smis]
    assert len(set(canon)) == 1
    assert canon[0] == "CC(=O)Oc1ccccc1C(=O)O"

def test_morgan_fingerprint_size():
    from rdkit.Chem import rdFingerprintGenerator
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    fp = gen.GetFingerprint(Chem.MolFromSmiles("CCO"))
    assert fp.GetNumBits() == 2048
```

Every standardisation, featurisation, or curve-fit utility should have a unit test with a small known case.

## Schema tests

Use `pandera` or `pydantic` to enforce table contracts:

```python
import pandera as pa
from pandera.typing import Series

class CompoundSchema(pa.SchemaModel):
    inchikey:     Series[str]   = pa.Field(unique=True, str_length={"min_value": 27, "max_value": 27})
    smiles_canon: Series[str]
    mw:           Series[float] = pa.Field(ge=0, le=5000)
    clogp:        Series[float] = pa.Field(ge=-10, le=15)
    source:       Series[str]   = pa.Field(isin=["chembl", "pubchem", "internal"])
    ingested_at:  Series[pa.DateTime]

# in the pipeline:
CompoundSchema.validate(df)
```

Schema validation is **cheap** (microseconds per row) and catches whole classes of upstream bugs.

## Data tests

Domain-specific invariants:

```python
def test_no_negative_ic50():
    assert (activities.value_nM >= 0).all()

def test_inchikey_format():
    assert activities.inchikey.str.match(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$").all()

def test_no_mw_outliers():
    assert (compounds.mw < 2000).all() or compounds[compounds.mw >= 2000].source.eq("biologic").all()
```

Tools like Great Expectations, Soda Core, and dbt tests automate large suites of these.

## Regression tests with golden datasets

For pipelines whose output is hard to spec exhaustively (a multi-step featurisation), keep a small **golden dataset** and check the output bit-for-bit.

```python
def test_pipeline_regression():
    golden_input = pd.read_parquet("tests/fixtures/golden_input.parquet")
    golden_output = pd.read_parquet("tests/fixtures/golden_output.parquet")
    actual_output = run_pipeline(golden_input)
    pd.testing.assert_frame_equal(actual_output, golden_output)
```

When the pipeline changes meaningfully, regenerate the golden output and review the diff. This catches subtle changes — a different RDKit version producing a different canonical SMILES, a CV-split changing because a sort became unstable — that escape unit tests.

## ML-specific tests

- **Reproducibility** — same data + same seed → same metrics.
- **Sanity** — model performs better than mean baseline.
- **Calibration** — predicted probabilities approximate empirical positive rates on a held-out set.
- **OOD behaviour** — predictions on noise-spiked input show appropriate uncertainty.

## CI integration

A drug-discovery codebase's CI typically runs:

```yaml
jobs:
  test:
    steps:
      - install env
      - pytest -q --cov                                # unit + regression
      - pandera-check compounds.parquet --schema ...   # schema
      - soda scan --tests data_tests.yaml              # data
      - python tests/check_calibration.py              # ML
```

Total time: minutes, not hours. Run on every PR.

## In practice

- **Schema validation on every ingest step**. Free, prevents most surprise bugs.
- **Golden-dataset regression tests for any featurisation pipeline**. They catch silent drift.
- **CI runs ALL tests on every PR**, not just unit tests.
- **Data tests and pipeline tests live in the same repo** as the pipeline code.

## Where to next

[HPC → industry](hpc-to-industry.md) — bridging academic patterns to industrial pipelines.
