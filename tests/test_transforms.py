from datetime import date
from decimal import Decimal
from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from econ_data.frames import FRED_OBSERVATION_SCHEMA
from econ_data.transforms import forward_fill

READTIME = date(2026, 10, 26)


def make_row(series_id: str, d: date, value: str | None) -> dict[str, Any]:
    return {
        "series_id": series_id,
        "obs_date": d,
        "value": Decimal(value) if value is not None else None,
        "realtime_start": date(2026, 10, 26),
        "realtime_end": date(2026, 10, 26),
    }


def make_df(spark: SparkSession, rows: list[dict[str, Any]]) -> DataFrame:
    return spark.createDataFrame(rows, schema=FRED_OBSERVATION_SCHEMA)


def column_values(df: DataFrame, series_id: str, column: str) -> list[Any]:
    rows = df.where(F.col("series_id") == series_id).orderBy("obs_date").collect()
    return [row[column] for row in rows]


def test_mid_series_gap_is_filled(spark: SparkSession) -> None:
    df = make_df(
        spark,
        [
            make_row("DGS10", date(2024, 1, 2), "3.95"),
            make_row("DGS10", date(2024, 1, 3), None),
            make_row("DGS10", date(2024, 1, 4), "3.99"),
        ],
    )

    result = column_values(forward_fill(df), "DGS10", "value_filled")
    assert result == [Decimal("3.95"), Decimal("3.95"), Decimal("3.99")]


def test_leading_null_stays_null(spark: SparkSession) -> None:
    df = make_df(
        spark,
        [
            make_row("DGS10", date(2024, 1, 1), None),
            make_row("DGS10", date(2024, 1, 2), "3.95"),
        ],
    )

    result = column_values(forward_fill(df), "DGS10", "value_filled")
    assert result == [None, Decimal("3.95")]


def test_original_value_is_unchanged(spark: SparkSession) -> None:
    df = make_df(
        spark,
        [
            make_row("DGS10", date(2024, 1, 2), "3.95"),
            make_row("DGS10", date(2024, 1, 3), None),
            make_row("DGS10", date(2024, 1, 4), "3.99"),
        ],
    )

    result = column_values(forward_fill(df), "DGS10", "value")
    assert result == [Decimal("3.95"), None, Decimal("3.99")]


def test_series_do_not_fill_from_each_other(spark: SparkSession) -> None:
    df = make_df(
        spark,
        [
            make_row("DGS10", date(2024, 1, 2), "3.95"),
            make_row("UNRATE", date(2024, 1, 3), None),
            make_row("UNRATE", date(2024, 1, 4), "4.10"),
        ],
    )

    result = column_values(forward_fill(df), "UNRATE", "value_filled")
    assert result == [None, Decimal("4.10")]
