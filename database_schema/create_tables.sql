-- ============================================================================
-- RAQIP Data Platform - Core Database Schema (raqip_db)
-- Author: Mansour Mohamed (Data Engineer)
-- Description: DDL script for creating Dimension, Fact, and Audit tables.
-- ============================================================================

CREATE DATABASE IF NOT EXISTS raqip_db;
USE raqip_db;

-- 1. Dimension: Data Sources
CREATE TABLE IF NOT EXISTS dim_data_sources (
    source_id INT PRIMARY KEY AUTO_INCREMENT,
    source_name VARCHAR(100) NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- e.g., 'CSV_API', 'SIMULATION'
    endpoint_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Dimension: Monitored Entities
CREATE TABLE IF NOT EXISTS dim_monitored_entities (
    entity_id INT PRIMARY KEY AUTO_INCREMENT,
    entity_code VARCHAR(50) UNIQUE NOT NULL,
    entity_name VARCHAR(150) NOT NULL,
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Audit Table: ETL Ingestion Logs
CREATE TABLE IF NOT EXISTS etl_ingestion_logs (
    batch_id VARCHAR(64) PRIMARY KEY,
    source_id INT NOT NULL,
    records_ingested INT DEFAULT 0,
    records_rejected INT DEFAULT 0,
    status VARCHAR(30) NOT NULL, -- 'SUCCESS', 'PARTIAL', 'FAILED'
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_source FOREIGN KEY (source_id) REFERENCES dim_data_sources(source_id)
);

-- 4. Fact Table: Operational Metrics
CREATE TABLE IF NOT EXISTS fact_operational_metrics (
    metric_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    source_id INT NOT NULL,
    entity_id INT NOT NULL,
    batch_id VARCHAR(64) NOT NULL,
    metric_value DECIMAL(18, 4) NOT NULL,
    threshold_status VARCHAR(20) DEFAULT 'NORMAL', -- 'NORMAL', 'WARNING', 'CRITICAL'
    recorded_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_metric_source FOREIGN KEY (source_id) REFERENCES dim_data_sources(source_id),
    CONSTRAINT fk_metric_entity FOREIGN KEY (entity_id) REFERENCES dim_monitored_entities(entity_id),
    CONSTRAINT fk_metric_batch FOREIGN KEY (batch_id) REFERENCES etl_ingestion_logs(batch_id)
);

-- 5. Gold Layer Summary Table (BI & Grafana Serving)
CREATE TABLE IF NOT EXISTS gold_kpi_summary (
    summary_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    entity_id INT NOT NULL,
    summary_date DATE NOT NULL,
    avg_metric_value DECIMAL(18, 4),
    alert_count INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_summary_entity FOREIGN KEY (entity_id) REFERENCES dim_monitored_entities(entity_id)
);
