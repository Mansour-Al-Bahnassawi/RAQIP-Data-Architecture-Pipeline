"""
RAQIP Databricks Volume Loader
Loads validated raw batch files into Databricks Compute Volume (raqip_db Bronze Layer).
"""

import os
import shutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load_to_databricks_volume(local_file_path: str, volume_target_dir: str = "/Volumes/raqip_db/raw_landing/") -> str:
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"Source file does not exist: {local_file_path}")

    os.makedirs(volume_target_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(local_file_path)
    dest_path = os.path.join(volume_target_dir, f"{timestamp}_{base_name}")

    shutil.copy2(local_file_path, dest_path)
    logging.info(f"File staged to Databricks Volume: {dest_path}")
    return dest_path


if __name__ == "__main__":
    logging.info("Databricks Volume Loader configured for raqip_db.")
