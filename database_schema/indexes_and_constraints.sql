-- ============================================================================
-- RAQIP Data Platform - Indexes & Data Quality Constraints
-- Author: Mansour Mohamed (Data Engineer)
-- ============================================================================

USE raqip_db;

-- Performance Indexes for Time-Series & Dashboard Queries
CREATE INDEX idx_fact_recorded_at ON fact_operational_metrics (recorded_at DESC);
CREATE INDEX idx_fact_entity_time ON fact_operational_metrics (entity_id, recorded_at);
CREATE INDEX idx_fact_status ON fact_operational_metrics (threshold_status);
CREATE INDEX idx_gold_date_entity ON gold_kpi_summary (summary_date, entity_id);

-- Unique Constraint to Prevent Duplicate Daily Summaries
ALTER TABLE gold_kpi_summary
ADD CONSTRAINT uq_entity_summary_date UNIQUE (entity_id, summary_date);

-- Check Constraints for Data Integrity
ALTER TABLE fact_operational_metrics
ADD CONSTRAINT chk_metric_value_non_negative CHECK (metric_value >= 0);

ALTER TABLE etl_ingestion_logs
ADD CONSTRAINT chk_records_non_negative CHECK (records_ingested >= 0 AND records_rejected >= 0);
