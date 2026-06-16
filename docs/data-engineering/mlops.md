# MLOps for drug discovery

> Model registries, retraining, drift detection, deployment. The discipline that turns a notebook model into a system.

## What changes in drug discovery

Generic MLOps optimises for "the same model serves traffic indefinitely". Drug discovery is different:

- **Data drifts continuously** — new chemistry, new targets, new assay protocols.
- **Models are short-lived** — usually retrained weekly or per-project.
- **Many small models** — one QSAR per target, one ADMET per endpoint; not a single big serving model.
- **Audit trails matter** — IND filings need to know which model produced which number.

The right MLOps shape is closer to "many small ephemeral models with strong lineage" than "one big production model with serving SLAs".

## The minimum stack

| Concern | Tool | Notes |
| --- | --- | --- |
| Experiment tracking | MLflow / Weights & Biases | run per model fit, log params and metrics |
| Model registry | MLflow / SageMaker / Vertex Registry | versioned artefacts |
| Feature / dataset versioning | DVC, LakeFS, Iceberg time travel | reproducible inputs |
| Serving | FastAPI / BentoML | almost always batch in drug discovery |
| Monitoring | Evidently, Whylogs, custom | drift detection |
| CI/CD | GitHub Actions / GitLab CI | trigger retraining on data change |

For most drug-discovery teams, MLflow + DVC + a small FastAPI service is the right starting stack.

## A model registry entry

What you want stored, per model:

- **Artefact**: the serialised model (joblib, ONNX, ptr file).
- **Training data hash / table version** — Iceberg snapshot ID, DVC hash.
- **Featurisation code version** — git commit SHA.
- **Hyperparameters**.
- **Train / val / test metrics**, with split definition.
- **Calibration data and fitted calibrator**.
- **Domain of applicability** — covered set of training fingerprints, distance metric.
- **Owner, project, retire-by date**.

A registry without these fields is a file dump. With them, you can answer audit questions in minutes.

## Retraining cadence

Three triggers:

1. **Calendar** — weekly / monthly retrain on the latest data.
2. **Data event** — new assay batch ingested → retrain on the affected target.
3. **Drift detection** — predictions vs new ground-truth diverge → retrain.

Calendar is simplest; data-event is best for fresh-data programs; drift-triggered is most robust but requires drift instrumentation.

## Drift detection

Two complementary checks:

- **Input drift** — distribution of features changes (Tanimoto distance to training set, PSI / KL on descriptors).
- **Prediction drift** — model output distribution changes (might be legitimate or might be the model going off).
- **Performance drift** — predictions vs new labels disagree (the only direct evidence of model degradation).

Performance drift is the gold standard but lags labels; input/prediction drift are leading indicators.

Tools: Evidently, Whylogs, NannyML, MLflow's evaluators.

## Serving — usually batch

In drug discovery, "serving" is almost always batch scoring of a compound list, not a low-latency API:

```python
# nightly job:
new_compounds = read_table("compounds_v1") - read_table("scored_v1")
scores = []
for batch in chunks(new_compounds, 10_000):
    fps = featurise_batch(batch)
    scores.append(model.predict(fps))
write_table("scored_v1", concat(scores))
```

Low-latency serving (sub-second per molecule) is rare and usually a sign of over-engineering. Batch scoring on a fixed schedule meets most use cases.

## Audit and IND support

For models supporting IND filings or other regulatory artefacts:

- **Pin the exact training data version** (Iceberg snapshot, DVC commit).
- **Pin the code version** (git commit, Docker image hash).
- **Lock the Python environment** (conda lockfile, uv lockfile).
- **Document the validation set and metrics** in the IND dossier.
- **Keep the trained artefact** for the retention period (typically 5+ years).

The audit trail is part of the product.

## In practice

- **Many small models > one big model.** Build the registry around that shape.
- **MLflow + DVC is enough** for 80% of drug-discovery teams. Don't over-engineer.
- **Batch scoring on a schedule** beats real-time serving for almost every use case.
- **Drift detection is non-negotiable** for any model whose predictions drive synthesis decisions.

## Where to next

[Testing pipelines](testing.md) — how to make sure the lake doesn't lie.
