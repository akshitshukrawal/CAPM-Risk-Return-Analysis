# src/data_fetcher.py

import yfinance as yf
import pandas as pd

def download_price_data(tickers, start_date, end_date):
    """
    Downloads adjusted closing prices for a list of tickers from Yahoo Finance.

    Args:
        tickers (list): A list of stock/index tickers.
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.

    Returns:
        pandas.DataFrame: A DataFrame with the adjusted closing prices.
    """
    print("Downloading historical price data...")
    try:
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        # Forward-fill any missing values
        data.ffill(inplace=True)
        print("Data download complete.")
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None