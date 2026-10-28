import json
from datetime import date
from decimal import Decimal

import pytest

from econ_data.fred import parse_fred


def test_missing_value_becomes_none():
    with open("tests/fixtures/dgs10_sample.json") as f:
        fred_dict = json.load(f)

    parsed = parse_fred(fred_dict, series_id="DGS10")

    holiday = None
    for record in parsed:
        if record["obs_date"] == date(2024, 1, 1):
            holiday = record

    assert holiday is not None
    assert holiday["value"] is None


def test_normal_value_parses_to_decimal():
    with open("tests/fixtures/dgs10_sample.json") as f:
        fred_dict = json.load(f)

    parsed = parse_fred(fred_dict, series_id="DGS10")

    target = None
    for record in parsed:
        if record["obs_date"] == date(2024, 1, 2):
            target = record

    assert target is not None
    assert target["value"] == Decimal("9.99")
    assert isinstance(record["value"], Decimal)
    assert isinstance(record["obs_date"], date)
    assert target["series_id"] == "DGS10"


def test_empty_observations_returns_empty_list():
    data = {"count": 0, "observations": []}
    assert parse_fred(data, series_id="DGS10") == []


def test_count_error_raises():
    with open("tests/fixtures/dgs10_sample.json") as f:
        fred_dict = json.load(f)

    fred_dict["count"] = 10

    with pytest.raises(ValueError, match="count check failed"):
        parse_fred(fred_dict, series_id="DGS10")


def test_decimal_value_error():
    with open("tests/fixtures/dgs10_sample.json") as f:
        fred_dict = json.load(f)

    fred_dict["observations"][1]["value"] = "abc"

    with pytest.raises(ValueError, match="Bad Value"):
        parse_fred(fred_dict, series_id="DGS10")
