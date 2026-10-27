import os
from dotenv import load_dotenv
from econ_data.fred import fetch_fred

FRED_KEY = os.getenv("FRED_KEY")
series_id = "DGS10"

def main():
    load_dotenv()
    print(fetch_fred(series_id=series_id, api_key=FRED_KEY))
