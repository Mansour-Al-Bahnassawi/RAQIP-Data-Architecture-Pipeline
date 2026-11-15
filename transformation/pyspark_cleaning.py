"""
RAQIP PySpark Data Cleaning & Quality Enforcement
Removes duplicates, handles null values, and enforces schema constraints.
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def clean_operational_metrics(df: DataFrame) -> DataFrame:
    cleaned_df = (
        df.dropna(subset=["entity_code", "metric_value", "recorded_at"])
          .filter(F.col("metric_value") >= 0)
          .withColumn("metric_value", F.col("metric_value").cast("decimal(18,4)"))
          .withColumn("recorded_at", F.to_timestamp("recorded_at"))
          .dropDuplicates(["entity_code", "recorded_at", "batch_id"])
          .withColumn(
              "threshold_status",
              F.when(F.col("metric_value") >= 130, "CRITICAL")
               .when(F.col("metric_value") >= 100, "WARNING")
               .otherwise("NORMAL")
          )
    )
    return cleaned_df


if __name__ == "__main__":
    spark = SparkSession.builder.appName("RAQIP-PySpark-Cleaning").getOrCreate()
    print("Spark Session initialized for RAQIP Data Quality Pipeline.")
