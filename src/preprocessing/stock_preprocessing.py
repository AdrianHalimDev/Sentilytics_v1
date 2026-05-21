"""
Sentilytics — Stock Data Preprocessing
Cleans, validates, and prepares stock data for modeling.
Creates target_close_h1 (next-day close price).

Usage:
    python -m src.preprocessing.stock_preprocessing
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import STOCK_NAMES, RAW_STOCK_DIR, PROCESSED_STOCK_DIR
from src.utils.file_utils import save_csv, load_csv, ensure_dir


def preprocess_stock(stock_name):
    """
    Preprocess raw stock data:
    1. Load raw CSV
    2. Sort by date chronologically
    3. Handle missing values (forward fill)
    4. Validate OHLCV values
    5. Create target_close_h1 = close.shift(-1)
    6. Drop last row (no target)
    7. Save processed CSV

    Args:
        stock_name: Stock short name (e.g. 'BBCA')

    Returns:
        Processed DataFrame or None
    """
    print(f"\n[INFO] Preprocessing stock data for {stock_name}...")

    # Load raw data
    raw_path = os.path.join(RAW_STOCK_DIR, f"{stock_name}_raw.csv")
    df = load_csv(raw_path)

    if df is None or df.empty:
        print(f"[ERROR] No raw data found for {stock_name}")
        return None

    # Ensure date column is datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # Remove duplicates by date
    before_dedup = len(df)
    df = df.drop_duplicates(subset=['date'], keep='first')
    after_dedup = len(df)
    if before_dedup > after_dedup:
        print(f"[INFO] Removed {before_dedup - after_dedup} duplicate dates")

    # Forward fill missing values in OHLCV
    ohlcv_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in ohlcv_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    missing_before = df[ohlcv_cols].isnull().sum().sum()
    if missing_before > 0:
        df[ohlcv_cols] = df[ohlcv_cols].fillna(method='ffill')
        df[ohlcv_cols] = df[ohlcv_cols].fillna(method='bfill')
        print(f"[INFO] Filled {missing_before} missing values")

    # Validate: remove rows with zero or negative close
    invalid_mask = df['close'] <= 0
    if invalid_mask.any():
        print(f"[WARNING] Removing {invalid_mask.sum()} rows with invalid close price")
        df = df[~invalid_mask].reset_index(drop=True)

    # Create target: Close Price H+1 (next day's close)
    df['target_close_h1'] = df['close'].shift(-1)

    # Drop last row (no target available)
    df = df.iloc[:-1].reset_index(drop=True)

    # Ensure stock column
    df['stock'] = stock_name

    # Format date back to string
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    # Select final columns
    df = df[['date', 'stock', 'open', 'high', 'low', 'close', 'volume', 'target_close_h1']]

    print(f"[INFO] Processed {len(df)} rows for {stock_name}")
    print(f"[INFO] Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")

    return df


def run_stock_preprocessing():
    """Preprocess all stock data."""
    ensure_dir(PROCESSED_STOCK_DIR)

    for stock_name in STOCK_NAMES:
        df = preprocess_stock(stock_name)
        if df is not None:
            filepath = os.path.join(PROCESSED_STOCK_DIR, f"{stock_name}_processed.csv")
            save_csv(df, filepath)

    print("\n[INFO] Stock preprocessing complete!")


if __name__ == '__main__':
    run_stock_preprocessing()
