from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def forward_fill(df: DataFrame) -> DataFrame:
    window = (
        Window.partitionBy(F.col("series_id"))
        .orderBy(F.col("obs_date"))
        .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )

    return df.withColumn("value_filled", F.last("value", ignorenulls=True).over(window))
