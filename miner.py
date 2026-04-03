import requests
import os

API_KEY = os.getenv("CMC_API_KEY")

def get_market_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    params = {
        "start": "1",
        "limit": "50",
        "convert": "USD"
    }

    headers = {
        "X-CMC_PRO_API_KEY": API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data.get("data", [])