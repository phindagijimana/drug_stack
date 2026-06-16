# The five pillars of data quality

> Freshness, volume, distribution, schema, lineage. The dimensions a serious pipeline monitors.

Borrowed from the data-engineering literature (Monte Carlo, Anomalo, others) and recontextualised for drug discovery.

## 1. Freshness

How recently was the data updated?

- **ChEMBL releases**: quarterly. A pipeline running on a release 9 months stale is losing actives.
- **Internal assay data**: usually daily. Monitor end-to-end latency.
- **External catalogues** (Enamine, ZINC): monthly to weekly. Stale catalogues lead to stale virtual-screen results.

Operationalise as: each table has a `last_updated` timestamp; an alert fires when latency exceeds the SLA.

## 2. Volume

How much data arrived?

- **A ChEMBL ingestion that processed 100 rows instead of the usual 100 000** is a silent failure that downstream "looks fine".
- **A daily assay file with zero new rows** is either a holiday or a broken connector. Either way, alert.

Operationalise as: rolling-window expected ranges per source; alert on excursions.

## 3. Distribution

Are the values consistent with history?

- **A sudden shift in pIC50 medians** across an assay → likely a control or calibration change.
- **A sudden drop in mean MW** of a "drug-like" library → likely a filter regression.
- **A shift in null-rate per column** → likely an upstream schema change.

Operationalise as: rolling distributional checks (KS test, Jensen-Shannon divergence on histograms) per column.

## 4. Schema

Has the schema changed unexpectedly?

- **Column added / removed** without notice.
- **Type changed** (float → string for some encoding nightmare).
- **Allowed-values set changed** for an enum column.

Operationalise as: contract test on every ingest (`pydantic`, `pandera`); fail loudly if the schema drifts.

## 5. Lineage

For each row, which sources produced it?

- **Auditing for a regulatory filing**: which raw measurements went into the IC50 cited in the IND?
- **Bug investigation**: which upstream change caused yesterday's QSAR mismatch?

Operationalise as: every step records the source partition(s) it consumed. Tools like OpenLineage, Marquez, or simple `lineage.json` files per partition.

## A monitoring dashboard

A drug-discovery pipeline's dashboard usually shows:

- **Freshness per table** (heatmap of "hours since last update").
- **Volume per source** (rolling rate vs expected window).
- **Distribution health per key column** (KS-test p-value, histogram).
- **Schema drift events** in the last 7 days.
- **Failed runs** in the last 24 hours.

A team that has *not* built this dashboard discovers the problems via failed papers, not pages.

## In practice

- **The five pillars are observability, not testing.** Tests catch *known* bad cases at write-time; pillars catch *unknown* drift at run-time.
- **Make the SLAs explicit per table.** "Daily assay table updated by 09:00, < 5% null on IC50".
- **Tooling**: Monte Carlo, Anomalo, soda-core (open-source) — pick one and stick with it.

## Where to next

[Cheminformatics pipelines](cheminformatics-pipelines.md) — a concrete worked example.
