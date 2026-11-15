"""
RAQIP Delta Lakehouse Medallion Flow (Bronze -> Silver -> Gold)
Builds ACID-compliant Delta tables inside raqip_db.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def run_lakehouse_pipeline(spark: SparkSession):
    # Read Silver cleaned Delta table
    silver_df = spark.table("raqip_db.silver_operational_metrics")

    # Aggregate into Gold KPI Summary table for Grafana & Web Portal
    gold_df = (
        silver_df.withColumn("summary_date", F.to_date("recorded_at"))
        .groupBy("entity_code", "summary_date")
        .agg(
            F.round(F.avg("metric_value"), 4).alias("avg_metric_value"),
            F.sum(F.when(F.col("threshold_status") == "CRITICAL", 1).otherwise(0)).alias("alert_count"),
            F.count("*").alias("total_readings")
        )
        .withColumn("updated_at", F.current_timestamp())
    )

    (
        gold_df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable("raqip_db.gold_kpi_summary")
    )
    print("[SUCCESS] Gold KPI Summary table updated in raqip_db.")


if __name__ == "__main__":
    spark = SparkSession.builder.appName("RAQIP-Delta-Lakehouse").getOrCreate()
    run_lakehouse_pipeline(spark)
