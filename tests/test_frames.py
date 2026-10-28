import json
from datetime import date

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from econ_data.frames import FRED_OBSERVATION_SCHEMA, to_dataframe
from econ_data.fred import parse_fred


def test_dataframe_uses_explicit_schema(spark: SparkSession) -> None:
    with open("tests/fixtures/dgs10_sample.json") as f:
        records = parse_fred(json.load(f), series_id="DGS10")

    df = to_dataframe(spark, records)

    assert df.schema == FRED_OBSERVATION_SCHEMA


def test_dataframe_keeps_all_rows(spark: SparkSession) -> None:
    with open("tests/fixtures/dgs10_sample.json") as f:
        records = parse_fred(json.load(f), series_id="DGS10")

    df = to_dataframe(spark, records)

    assert df.count() == 7


def test_missing_value_is_null(spark: SparkSession) -> None:
    with open("tests/fixtures/dgs10_sample.json") as f:
        records = parse_fred(json.load(f), series_id="DGS10")

    df = to_dataframe(spark, records)
    rows = df.where(F.col("obs_date") == date(2024, 1, 1)).collect()

    assert len(rows) == 1
    assert rows[0]["value"] is None
