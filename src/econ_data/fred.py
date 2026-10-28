import logging
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

import requests

logger = logging.getLogger(__name__)


def fetch_fred(series_id: str, api_key: str) -> dict[str, Any]:
    response = requests.get(
        "https://api.stlouisfed.org/fred/series/observations",
        params={
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()
    if not isinstance(data, dict):
        raise TypeError(
            f"expected a JSON object from FRED for {series_id}, got {type(data).__name__}"
        )
    return data


def parse_fred(data: dict[str, Any], series_id: str) -> list[dict[str, Any]]:
    meta_count = data["count"]
    obs_count = len(data["observations"])

    if meta_count != obs_count:
        raise ValueError(
            f"count check failed, {series_id}, expected: {meta_count}, got: {obs_count}"
        )

    logger.info("count check passed for %s: %d observations", series_id, obs_count)
    results = []
    for obs in data["observations"]:
        obs_date = date.fromisoformat(obs["date"])

        if obs["value"] == ".":
            value = None
        else:
            try:
                value = Decimal(obs["value"])
            except InvalidOperation:
                raise ValueError(
                    f"Bad Value. {series_id}, {obs['date']}, {obs['value']!r}"
                ) from None

        realtime_start = date.fromisoformat(obs["realtime_start"])
        realtime_end = date.fromisoformat(obs["realtime_end"])

        record = {
            "series_id": series_id,
            "obs_date": obs_date,
            "value": value,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        }

        results.append(record)
    return results
