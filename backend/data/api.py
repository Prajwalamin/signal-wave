import requests
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Set your OANDA API key and account type
OANDA_API_KEY =   os.getenv("OANDA_API_KEY")  # Replace with your actual API key
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")  # Replace with your actual account ID
OANDA_API_URL = 'https://api-fxpractice.oanda.com/v3'  # Demo environment; use 'https://api-fxtrade.oanda.com/v3' for live trading

def fetch_historical_prices(instrument="EUR_USD", granularity="D", count=220):
    """Fetch historical daily closing prices for a given instrument."""
    url = f"{OANDA_API_URL}/instruments/{instrument}/candles"
    headers = {
        "Authorization": f"Bearer {OANDA_API_KEY}"
    }
    params = {
        "granularity": granularity,  # "D" for daily candles
        "count": count,  # Number of candles (days) to fetch
        "price": "M"  # Midpoint prices (M), to get OHLC
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")

    data = response.json()

    # Extract closing prices from the data
    closing_prices = [float(candle['mid']['c']) for candle in data['candles']]
    
    return closing_prices


