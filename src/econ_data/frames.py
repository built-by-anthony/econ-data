from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import DateType, DecimalType, StringType, StructField, StructType

FRED_OBSERVATION_SCHEMA = StructType(
    [
        StructField("series_id", StringType(), nullable=False),
        StructField("obs_date", DateType(), nullable=False),
        StructField("value", DecimalType(20, 6), nullable=True),
        StructField("realtime_start", DateType(), nullable=False),
        StructField("realtime_end", DateType(), nullable=False),
    ]
)


def to_dataframe(spark: SparkSession, records: list[dict[str, Any]]) -> DataFrame:
    return spark.createDataFrame(schema=FRED_OBSERVATION_SCHEMA, data=records)
