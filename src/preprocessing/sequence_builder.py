"""
Sentilytics — Sequence Builder
Prepares time-series sequences for LSTM input.
- Chronological 80:20 train/test split (no shuffle)
- MinMaxScaler fit on train only
- Sliding window sequences (window_size=30)

Usage:
    Called by train_baseline.py and train_hybrid.py
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import WINDOW_SIZE, TRAIN_SPLIT, MODELS_SCALERS_DIR
from src.utils.file_utils import ensure_dir


def chronological_split(df, train_ratio=0.8):
    """
    Split data chronologically (no shuffle).
    First train_ratio rows are train, remaining are test.

    Args:
        df: DataFrame sorted by date
        train_ratio: Fraction of data for training

    Returns:
        tuple: (train_df, test_df, split_index)
    """
    split_idx = int(len(df) * train_ratio)
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()

    print(f"[INFO] Chronological split: {len(train_df)} train, {len(test_df)} test")
    print(f"[INFO] Train period: {train_df['date'].iloc[0]} to {train_df['date'].iloc[-1]}")
    print(f"[INFO] Test period: {test_df['date'].iloc[0]} to {test_df['date'].iloc[-1]}")

    return train_df, test_df, split_idx


def fit_scaler(train_data, feature_columns, stock_name, model_type):
    """
    Fit MinMaxScaler on training data ONLY.
    Saves scaler as .pkl file.

    Args:
        train_data: Training DataFrame
        feature_columns: List of feature column names
        stock_name: Stock name for file naming
        model_type: 'baseline' or 'hybrid'

    Returns:
        Fitted MinMaxScaler
    """
    ensure_dir(MODELS_SCALERS_DIR)

    scaler = MinMaxScaler(feature_range=(0, 1))

    # Fit only on training features + target
    all_cols = feature_columns + ['target_close_h1']
    scaler.fit(train_data[all_cols].values)

    # Save scaler
    scaler_path = os.path.join(MODELS_SCALERS_DIR, f"{stock_name}_{model_type}_scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"[INFO] Scaler saved: {scaler_path}")

    return scaler


def create_sequences(data, window_size=30):
    """
    Create sliding window sequences for LSTM.

    Args:
        data: Scaled numpy array with shape (n_samples, n_features+1)
              Last column is target
        window_size: Number of timesteps per sequence

    Returns:
        tuple: (X, y) where X has shape (samples, window_size, n_features)
               and y has shape (samples,)
    """
    X, y = [], []

    for i in range(window_size, len(data)):
        # Features: all columns except last (target)
        X.append(data[i - window_size:i, :-1])
        # Target: last column
        y.append(data[i, -1])

    X = np.array(X)
    y = np.array(y)

    print(f"[INFO] Created sequences: X={X.shape}, y={y.shape}")

    return X, y


def prepare_data(df, feature_columns, stock_name, model_type,
                 window_size=None, train_ratio=None):
    """
    Full data preparation pipeline for LSTM training.

    Steps:
    1. Chronological split
    2. Fit scaler on train only
    3. Scale train and test data
    4. Create sequences
    5. Return prepared data

    Args:
        df: Full dataset DataFrame
        feature_columns: List of feature column names
        stock_name: Stock name
        model_type: 'baseline' or 'hybrid'
        window_size: Override config window size
        train_ratio: Override config train ratio

    Returns:
        dict with X_train, y_train, X_test, y_test, scaler, dates_test, split_info
    """
    ws = window_size or WINDOW_SIZE
    tr = train_ratio or TRAIN_SPLIT

    print(f"\n[INFO] Preparing data for {stock_name} {model_type}...")
    print(f"[INFO] Features: {feature_columns}")
    print(f"[INFO] Window size: {ws}, Train ratio: {tr}")

    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)

    # Split chronologically
    train_df, test_df, split_idx = chronological_split(df, tr)

    # Fit scaler on train only
    scaler = fit_scaler(train_df, feature_columns, stock_name, model_type)

    # Scale data
    all_cols = feature_columns + ['target_close_h1']

    train_scaled = scaler.transform(train_df[all_cols].values)
    test_scaled = scaler.transform(test_df[all_cols].values)

    # Create sequences
    X_train, y_train = create_sequences(train_scaled, ws)
    X_test, y_test = create_sequences(test_scaled, ws)

    # Get test dates (offset by window_size because first window_size entries are consumed)
    dates_test = test_df['date'].values[ws:]

    result = {
        'X_train': X_train,
        'y_train': y_train,
        'X_test': X_test,
        'y_test': y_test,
        'scaler': scaler,
        'dates_test': dates_test,
        'feature_columns': feature_columns,
        'split_index': split_idx,
        'train_size': len(train_df),
        'test_size': len(test_df),
    }

    return result
