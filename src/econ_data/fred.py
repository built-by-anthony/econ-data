import os
import requests 
from dotenv import load_dotenv



def fetch_fred(series_id: str, api_key: str): 
    response = requests.get(
        "https://api.stlouisfed.org/fred/series/observations", 
        params={
        "series_id": series_id, 
        "api_key"  : api_key, 
        "file_type": "json",
        }, 
        timeout=10
    )

    response.raise_for_status()
    return(response.text)


