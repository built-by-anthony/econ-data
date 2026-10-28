import pytest
import requests
import responses 
from responses import matchers 

from econ_data.fred import fetch_fred

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

@responses.activate
def test_fetch_fred_sends_expected_params() -> None: 
    responses.add(
        responses.GET, 
        FRED_URL, 
        json={"count": 0, "observations": []}, 
        status = 200, 
        match=[
            matchers.query_param_matcher(
                {"series_id": "DGS10", "api_key": "test-key", "file_type": "json"}
            )
        ],
    )

    result = fetch_fred("DGS10", api_key="test-key")
    assert result == {"count": 0, "observations": []}

@responses.activate
def test_fetch_fred_raises_on_http_error() -> None: 
    responses.add(
        responses.GET, 
        FRED_URL, 
        json={"error_code": 400, "error_message": "Bad Request"}, 
        status=400
    )

    with pytest.raises(requests.HTTPError):
        fetch_fred("DGS10", api_key="test-key")