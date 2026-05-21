"""
Sentilytics — Stock Data Downloader
Downloads OHLCV data for BBCA.JK and BBRI.JK from Yahoo Finance using yfinance.
Period: 2023-01-01 to 2024-12-31.

Includes retry logic and fallback data generation if Yahoo Finance is unavailable.

Usage:
    python -m src.data_collection.stock_downloader
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import yfinance as yf

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import STOCKS, DATE_START, DATE_END, RAW_STOCK_DIR
from src.utils.file_utils import save_csv, ensure_dir


def download_stock_data(ticker, stock_name, start_date, end_date, retries=3):
    """
    Download OHLCV data from Yahoo Finance for a given ticker.
    Tries yf.download first, then yf.Ticker().history() as fallback.

    Args:
        ticker: Yahoo Finance ticker symbol (e.g. 'BBCA.JK')
        stock_name: Short name for the stock (e.g. 'BBCA')
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        retries: Number of retry attempts

    Returns:
        DataFrame with columns: date, stock, open, high, low, close, volume
    """
    print(f"\n[INFO] Downloading {stock_name} ({ticker}) from {start_date} to {end_date}...")

    df = None

    # Method 1: yf.download (standard approach)
    for attempt in range(retries):
        try:
            df = yf.download(ticker, start=start_date, end=end_date,
                             auto_adjust=True, progress=False)
            if not df.empty:
                print(f"[INFO] yf.download succeeded on attempt {attempt + 1}")
                break
            else:
                print(f"[WARNING] Empty result on attempt {attempt + 1}, retrying...")
                time.sleep(2)
        except Exception as e:
            print(f"[WARNING] yf.download attempt {attempt + 1} failed: {e}")
            time.sleep(2)

    # Method 2: yf.Ticker().history() as fallback
    if df is None or df.empty:
        print(f"[INFO] Trying yf.Ticker().history() for {ticker}...")
        try:
            t = yf.Ticker(ticker)
            df = t.history(start=start_date, end=end_date, auto_adjust=True)
            if df.empty:
                print(f"[WARNING] Ticker.history() also returned empty for {ticker}")
                df = None
            else:
                print(f"[INFO] Ticker.history() succeeded!")
        except Exception as e:
            print(f"[WARNING] Ticker.history() failed: {e}")
            df = None

    if df is None or df.empty:
        print(f"[WARNING] All download methods failed for {ticker}")
        return None

    # Handle MultiIndex columns (yfinance sometimes returns multi-level columns)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Reset index to make date a column
    df = df.reset_index()

    # Rename columns to match schema
    col_map = {}
    for col in df.columns:
        col_lower = col.lower()
        if col_lower == 'date' or col_lower == 'datetime':
            col_map[col] = 'date'
        elif col_lower == 'open':
            col_map[col] = 'open'
        elif col_lower == 'high':
            col_map[col] = 'high'
        elif col_lower == 'low':
            col_map[col] = 'low'
        elif col_lower == 'close':
            col_map[col] = 'close'
        elif col_lower == 'volume':
            col_map[col] = 'volume'
    df = df.rename(columns=col_map)

    # Add stock column
    df['stock'] = stock_name

    # Select and order columns per schema
    required_cols = ['date', 'stock', 'open', 'high', 'low', 'close', 'volume']
    for c in required_cols:
        if c not in df.columns:
            print(f"[ERROR] Missing column: {c}")
            return None
    df = df[required_cols]

    # Format date
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)

    print(f"[INFO] Downloaded {len(df)} rows for {stock_name}")
    print(f"[INFO] Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")

    return df


def generate_fallback_data(stock_name, start_date, end_date):
    """
    Generate realistic fallback OHLCV data when Yahoo Finance is unavailable.
    Uses actual known price ranges for BBCA and BBRI.

    This is a DEVELOPMENT FALLBACK only — users should replace this with
    real data for the final thesis submission.
    """
    print(f"\n[INFO] Generating fallback data for {stock_name}...")
    print("[WARNING] This is SIMULATED data for development. Replace with real data for final thesis!")

    # Known approximate price ranges (IDR)
    price_config = {
        'BBCA': {'base': 8800, 'std': 200, 'trend': 0.0005, 'vol_base': 15_000_000},
        'BBRI': {'base': 5500, 'std': 150, 'trend': 0.0003, 'vol_base': 40_000_000},
    }
    config = price_config.get(stock_name, {'base': 5000, 'std': 100, 'trend': 0.0003, 'vol_base': 20_000_000})

    # Generate business days
    dates = pd.bdate_range(start=start_date, end=end_date)

    np.random.seed(42 + hash(stock_name) % 100)

    n = len(dates)
    # Generate close prices using random walk with drift
    returns = np.random.normal(config['trend'], 0.015, n)
    log_prices = np.log(config['base']) + np.cumsum(returns)
    close_prices = np.exp(log_prices)

    # Generate OHLV from close
    daily_range = np.random.uniform(0.005, 0.025, n)
    open_prices = close_prices * (1 + np.random.uniform(-0.01, 0.01, n))
    high_prices = np.maximum(open_prices, close_prices) * (1 + daily_range * 0.5)
    low_prices = np.minimum(open_prices, close_prices) * (1 - daily_range * 0.5)
    volumes = np.random.normal(config['vol_base'], config['vol_base'] * 0.3, n).astype(int)
    volumes = np.maximum(volumes, 1_000_000)

    # Round to nearest 25 (IDX lot rules)
    close_prices = np.round(close_prices / 25) * 25
    open_prices = np.round(open_prices / 25) * 25
    high_prices = np.round(high_prices / 25) * 25
    low_prices = np.round(low_prices / 25) * 25

    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'stock': stock_name,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volumes,
    })

    print(f"[INFO] Generated {len(df)} rows of fallback data for {stock_name}")

    return df


def run_stock_download():
    """Download stock data for all configured tickers."""
    ensure_dir(RAW_STOCK_DIR)

    for stock_info in STOCKS:
        ticker = stock_info['ticker']
        name = stock_info['name']

        # Try downloading from Yahoo Finance
        df = download_stock_data(ticker, name, DATE_START, DATE_END)

        # Use fallback if download fails
        if df is None:
            print(f"[WARNING] Yahoo Finance unavailable for {name}. Using fallback data.")
            df = generate_fallback_data(name, DATE_START, DATE_END)

        filepath = os.path.join(RAW_STOCK_DIR, f"{name}_raw.csv")
        save_csv(df, filepath)

    print("\n[INFO] Stock download complete!")


if __name__ == '__main__':
    run_stock_download()

