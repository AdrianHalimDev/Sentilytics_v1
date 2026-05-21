"""
Sentilytics — Data Fusion
Merges processed stock data with daily sentiment scores.
Creates baseline (OHLCV only) and hybrid (OHLCV + sentiment) datasets.

Process:
1. Load processed stock data
2. Load daily sentiment
3. Left join on date + stock
4. Fill missing sentiment with 0
5. Create baseline dataset (OHLCV + target)
6. Create hybrid dataset (OHLCV + sentiment_score + target)

Usage:
    python -m src.preprocessing.data_fusion
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import (
    STOCK_NAMES, PROCESSED_STOCK_DIR, PROCESSED_SENTIMENT_DIR, PROCESSED_FUSION_DIR
)
from src.utils.file_utils import save_csv, load_csv, ensure_dir


def create_fusion_datasets(stock_name):
    """
    Create baseline and hybrid datasets for a given stock.

    Args:
        stock_name: Stock short name (e.g. 'BBCA')

    Returns:
        tuple: (baseline_df, hybrid_df)
    """
    print(f"\n[INFO] Creating fusion datasets for {stock_name}...")

    # Load processed stock data
    stock_path = os.path.join(PROCESSED_STOCK_DIR, f"{stock_name}_processed.csv")
    stock_df = load_csv(stock_path)

    if stock_df is None or stock_df.empty:
        print(f"[ERROR] No processed stock data for {stock_name}")
        return None, None

    # Load daily sentiment
    sentiment_path = os.path.join(PROCESSED_SENTIMENT_DIR, f"{stock_name}_daily_sentiment.csv")
    sentiment_df = load_csv(sentiment_path)

    # Ensure date columns are strings for consistent merge
    stock_df['date'] = pd.to_datetime(stock_df['date']).dt.strftime('%Y-%m-%d')

    if sentiment_df is not None and not sentiment_df.empty:
        sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.strftime('%Y-%m-%d')

        # Select only needed columns from sentiment
        sentiment_cols = sentiment_df[['date', 'avg_sentiment_score']].copy()
        sentiment_cols = sentiment_cols.rename(columns={'avg_sentiment_score': 'sentiment_score'})

        # Left join: keep all stock data, add sentiment where available
        merged = stock_df.merge(sentiment_cols, on='date', how='left')

        # Fill missing sentiment with 0 (days without news)
        merged['sentiment_score'] = merged['sentiment_score'].fillna(0)
    else:
        print(f"[WARNING] No sentiment data for {stock_name}. Setting all sentiment_score to 0.")
        merged = stock_df.copy()
        merged['sentiment_score'] = 0

    # Sort by date chronologically
    merged = merged.sort_values('date').reset_index(drop=True)

    # ==========================================
    # Baseline Dataset: OHLCV + target
    # ==========================================
    baseline_cols = ['date', 'stock', 'open', 'high', 'low', 'close', 'volume', 'target_close_h1']
    baseline_df = merged[baseline_cols].copy()

    # ==========================================
    # Hybrid Dataset: OHLCV + sentiment_score + target
    # ==========================================
    hybrid_cols = ['date', 'stock', 'open', 'high', 'low', 'close', 'volume',
                   'sentiment_score', 'target_close_h1']
    hybrid_df = merged[hybrid_cols].copy()

    # Validate: no NaN in target
    baseline_df = baseline_df.dropna(subset=['target_close_h1']).reset_index(drop=True)
    hybrid_df = hybrid_df.dropna(subset=['target_close_h1']).reset_index(drop=True)

    print(f"[INFO] Baseline dataset: {len(baseline_df)} rows")
    print(f"[INFO] Hybrid dataset: {len(hybrid_df)} rows")

    sentiment_non_zero = (hybrid_df['sentiment_score'] != 0).sum()
    print(f"[INFO] Days with sentiment data: {sentiment_non_zero}/{len(hybrid_df)}")

    return baseline_df, hybrid_df


def run_data_fusion():
    """Create fusion datasets for all stocks."""
    ensure_dir(PROCESSED_FUSION_DIR)

    for stock_name in STOCK_NAMES:
        baseline_df, hybrid_df = create_fusion_datasets(stock_name)

        if baseline_df is not None:
            filepath = os.path.join(PROCESSED_FUSION_DIR, f"{stock_name}_baseline_dataset.csv")
            save_csv(baseline_df, filepath)

        if hybrid_df is not None:
            filepath = os.path.join(PROCESSED_FUSION_DIR, f"{stock_name}_hybrid_dataset.csv")
            save_csv(hybrid_df, filepath)

    print("\n[INFO] Data fusion complete!")


if __name__ == '__main__':
    run_data_fusion()
