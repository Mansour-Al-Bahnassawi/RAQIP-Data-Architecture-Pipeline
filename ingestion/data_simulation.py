"""
RAQIP Data Simulation Module
Generates realistic synthetic telemetry & operational metrics for pipeline testing.
"""

import json
import random
import uuid
from datetime import datetime, timezone
import pandas as pd


def generate_simulated_batch(num_records: int = 100) -> pd.DataFrame:
    entities = ["ENT-001", "ENT-002", "ENT-003", "ENT-004", "ENT-005"]
    batch_id = f"SIM-{uuid.uuid4().hex[:12].upper()}"
    records = []

    for _ in range(num_records):
        val = round(random.uniform(10.0, 150.0), 4)
        status = "NORMAL" if val < 100 else ("WARNING" if val < 130 else "CRITICAL")
        records.append({
            "batch_id": batch_id,
            "source_code": "SIMULATION",
            "entity_code": random.choice(entities),
            "metric_value": val,
            "threshold_status": status,
            "recorded_at": datetime.now(timezone.utc).isoformat()
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df_sim = generate_simulated_batch(50)
    output_file = "simulated_metrics_batch.csv"
    df_sim.to_csv(output_file, index=False)
    print(f"[INFO] Generated {len(df_sim)} simulated records -> {output_file}")
