import os

from dotenv import load_dotenv

from econ_data.fred import parse_fred

FRED_KEY = os.getenv("FRED_KEY")
series_id = "DGS10"


def main():
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    load_dotenv()

    # Sample data
    import json

    with open("tests/dgs10_sample.json") as f:
        fred_dict = json.load(f)
    # End Sample data

    # fred_dict = fetch_fred(series_id=series_id, api_key=FRED_KEY)
    parse_fred(fred_dict, series_id=series_id)
