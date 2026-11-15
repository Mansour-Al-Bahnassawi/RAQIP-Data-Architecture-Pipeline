# 📊 RAQIP Grafana & BI Dashboard Configuration Notes

## Overview
Grafana connects directly to the **RAQIP Serving Layer (`raqip_db.gold_kpi_summary` & `fact_operational_metrics`)** to deliver real-time operational observability and business KPIs.

## Key Performance Indicators (KPIs) Tracked
1. **Ingestion Throughput (Records/Min):** Monitors batch and API ingestion health from `etl_ingestion_logs`.
2. **Entity Operational Health Score:** Tracks `avg_metric_value` across monitored entities (`dim_monitored_entities`).
3. **Critical Anomaly Alerts:** Real-time counter of `CRITICAL` threshold breaches triggering automated alerts.
4. **Pipeline Rejection Rate:** Ratio of `records_rejected` vs `records_ingested` for data quality monitoring.

## Sample Grafana SQL Query
```sql
SELECT
    recorded_at AS time,
    entity_code AS metric,
    metric_value AS value
FROM raqip_db.fact_operational_metrics
WHERE $__timeFilter(recorded_at)
ORDER BY recorded_at ASC;
```
