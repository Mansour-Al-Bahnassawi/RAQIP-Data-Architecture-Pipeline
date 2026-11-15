"""
RAQIP CSV & API Data Ingestion Script
Extracts records from REST API endpoints and local CSV feeds with schema validation.
"""

import os
import uuid
import logging
import requests
import pandas as pd
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

REQUIRED_COLUMNS = {"entity_code", "metric_value", "recorded_at"}


def validate_schema(df: pd.DataFrame) -> bool:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        logging.error(f"Schema validation failed. Missing columns: {missing}")
        return False
    return True


def ingest_from_csv(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV source not found: {file_path}")
    df = pd.read_csv(file_path)
    if not validate_schema(df):
        raise ValueError("Invalid CSV schema structure.")
    df["batch_id"] = f"CSV-{uuid.uuid4().hex[:12].upper()}"
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    logging.info(f"Successfully ingested {len(df)} rows from {file_path}")
    return df


def ingest_from_api(api_url: str, timeout: int = 15) -> pd.DataFrame:
    response = requests.get(api_url, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    df = pd.DataFrame(payload)
    if not validate_schema(df):
        raise ValueError("Invalid API payload schema.")
    df["batch_id"] = f"API-{uuid.uuid4().hex[:12].upper()}"
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    logging.info(f"Successfully ingested {len(df)} rows from API")
    return df


if __name__ == "__main__":
    logging.info("RAQIP Ingestion Module Ready.")
