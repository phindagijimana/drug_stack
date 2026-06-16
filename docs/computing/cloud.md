# Cloud (AWS, GCP, Azure)

> When to leave HPC, what the choice between providers actually means, and the drug-discovery-specific patterns.

## When cloud beats HPC

- **Spiky workloads** — large screens once a quarter; HPC quota is wasted between.
- **Bursty GPU needs** — short, very large training runs.
- **External data sharing** — collaborators expect S3 / GCS URIs.
- **Compliance constraints** — HIPAA / SOC2 / EU GDPR controls that HPC environments may not meet.
- **Cloud-native services** — Sagemaker, Vertex, BigQuery, when integration is worth it.

## When HPC beats cloud

- **Long sustained workloads** — months of MD / FEP at academic discount on owned hardware.
- **Cost-sensitive** — cloud GPU prices are non-trivial; 100k GPU-hours is real money.
- **Local data gravity** — clinical-scale data that cannot leave a controlled environment.
- **Existing investment** — universities and large pharmas have GPU farms paid for.

## The big three, briefly

| Provider | Strengths for drug discovery |
| --- | --- |
| **AWS** | S3 + EC2 ubiquity; SageMaker; broadest service set; HealthLake for EHR |
| **GCP** | Vertex AI; BigQuery for omics analytics; TPUs (rare in drug discovery, useful in some) |
| **Azure** | Tight Microsoft enterprise integration; Synapse; Azure ML; HIPAA-friendly defaults |

For most drug-discovery teams, AWS is the safe default; GCP if you do heavy genomics on BigQuery; Azure if you're already a Microsoft shop.

## Drug-discovery-specific cloud patterns

### 1. Spot / preemptible GPU for screens

Virtual screening is embarrassingly parallel and restartable. Run on spot / preemptible GPUs at 60–80% discount; checkpoint frequently.

### 2. Lambda / Cloud Functions for triggers

When a new ChEMBL release lands in S3, a Lambda kicks off ingestion. Serverless triggers fit ETL.

### 3. Sagemaker / Vertex for ML pipelines

Hosted ML pipelines have come a long way. For teams without a Kubernetes infra investment, they're a reasonable fit.

### 4. Use the data services

BigQuery for omics analytics (single query over the GTEx tissue panels). Athena for ad-hoc Parquet queries. Cosmos DB for graph (KG) workloads on Azure.

## Cost discipline

- **GPU instances at retail price hurt.** Reserve and savings plans for steady workloads; spot for bursty.
- **Data egress costs.** Pulling data out of S3 to another region or cloud is the silent budget killer.
- **Tag every resource by project.** A team without tagging cannot do FinOps.
- **Auto-shutdown notebooks.** A handful of GPU notebooks left on for the weekend can cost more than the team's monthly cloud bill.

## In practice

- **Decide cloud-vs-HPC per workload**, not org-wide.
- **Containerise + push to a registry**; the same image runs on both.
- **Use object storage as the primary data plane**; computation moves to the data.
- **Track spend with tags + per-project budgets** from day one.

## Where to next

[GPUs](gpus.md) — what hardware to pick when you do go to cloud.
