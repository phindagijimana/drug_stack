# Lakehouse for chemistry & biology

> Parquet + Delta / Iceberg + a query engine. The dominant pattern for serious drug-discovery data platforms.

## What "lakehouse" means

A lakehouse stores data as **open columnar files** (Parquet) with a **table layer** (Delta Lake, Apache Iceberg, Apache Hudi) on top giving ACID, schema evolution, time travel, and concurrent writes.

It is the union of a data lake (cheap blob storage, open formats) and a warehouse (transactional integrity, queryable).

## The stack

| Layer | Pick (in 2025) |
| --- | --- |
| Storage | S3 / GCS / Azure Blob (or HDFS on-prem) |
| File format | Parquet (zstd compression) |
| Table format | Delta Lake or Iceberg |
| Catalog | Unity, AWS Glue, Hive metastore, Polaris |
| Query engine | DuckDB (local), Trino / Athena (federated), Spark (heavy ETL) |
| Stream | Kafka if needed; rare in drug discovery |
| Orchestration | Airflow / Prefect / Dagster |

## Why this matters for drug discovery

- **Schema evolution** — assay tables grow columns over time; Iceberg / Delta handle that without rewrites.
- **Time travel** — query "what was activities_v1 on 2025-08-15?" — exactly what you need for IND filings and audits.
- **Partition pruning** — query by target_chembl_id or assay_version, skipping irrelevant data.
- **Concurrent writes** — multiple pipelines can ingest into the same table without races.

## Partitioning chemistry data

Choosing partitions matters more than choosing tools.

**Compound table** — partition by InChIKey prefix (first 2 characters → 32^2 = ~1024 partitions). Joins on InChIKey hit one partition. Good for both scan and point lookup.

**Activity table** — partition by `(target_chembl_id, assay_version)` if you query per-target; by `measured_at_year_month` if you query by date.

**Fingerprint table** — usually you want all rows; partition by InChIKey prefix matches the compound table.

Wrong partitioning (e.g. partitioning the compound table by `mw_bucket`) leads to scans across thousands of partitions for every query.

## Schema example

```python
import pyarrow as pa

compounds_schema = pa.schema([
    pa.field("inchikey",       pa.string(), nullable=False),
    pa.field("smiles_canon",   pa.string(), nullable=False),
    pa.field("smiles_input",   pa.string(), nullable=True),
    pa.field("mw",             pa.float32()),
    pa.field("clogp",          pa.float32()),
    pa.field("tpsa",           pa.float32()),
    pa.field("hba",            pa.uint8()),
    pa.field("hbd",            pa.uint8()),
    pa.field("rotb",           pa.uint8()),
    pa.field("qed",            pa.float32()),
    pa.field("source",         pa.string(), nullable=False),
    pa.field("source_version", pa.string(), nullable=False),
    pa.field("ingested_at",    pa.timestamp("us", tz="UTC"), nullable=False),
])
```

Use Iceberg or Delta tables to enforce this schema; the table format will refuse writes that violate it.

## DuckDB as the everyday query layer

For analytics-style queries on a developer laptop, [DuckDB](https://duckdb.org) is the right default:

```python
import duckdb
con = duckdb.connect()
con.sql("""
    SELECT target_chembl_id,
           COUNT(*) AS n,
           median(pAct_median) AS pAct_median
    FROM 'lakehouse/activities_v1/*/*.parquet'
    WHERE pAct_median > 7
    GROUP BY 1
    ORDER BY n DESC
    LIMIT 50
""").df()
```

DuckDB reads Parquet, Iceberg, and Delta directly; queries 100 GB datasets locally with no setup. For most drug-discovery analytics, DuckDB on a laptop beats a Spark cluster.

## When to use Spark / Trino

- Tables larger than a single machine can scan.
- Federated queries across many sources.
- Production scheduled ETL with retries / monitoring.

Drug-discovery datasets rarely exceed terabyte scale outside of HTS / DNA-encoded libraries. Reserve Spark for ETL that actually needs distribution.

## Time travel and audit

```sql
SELECT * FROM activities_v1 VERSION AS OF 47
SELECT * FROM activities_v1 TIMESTAMP AS OF '2025-08-15 09:00:00'
```

Both Delta and Iceberg support these queries. For IND-supporting analyses, you can pin the exact table snapshot the model was trained on.

## In practice

- **Iceberg or Delta over raw Parquet** for production tables. The ACID / evolution / time-travel features pay back fast.
- **DuckDB as the everyday analytic layer**; promote to Spark / Trino only when you need to.
- **Partition by the column you actually query on.** Not by what felt intuitive.
- **Catalog your tables.** Unity, Glue, Polaris — pick one; data without a catalog is data nobody can find.

## Where to next

[MLOps for drug discovery](mlops.md) — when the lake meets the model.
