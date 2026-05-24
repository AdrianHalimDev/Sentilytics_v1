"""
Sentilytics — Forecast H+7
Generates 7-day forward forecast simulation using trained LSTM models.

For Hybrid LSTM:
    future_sentiment = mean(sentiment_score of last 7 trading days)

Process:
1. Load last 30 days of data
2. Predict H+1
3. Append prediction to sequence
4. Repeat for H+7
5. Save forecast CSV with disclaimer flag

IMPORTANT: This is a SIMULATION for dashboard visualization only.
           Not used for evaluation metrics.

Usage:
    python -m src.modeling.forecast
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import (
    STOCK_NAMES, BASELINE_FEATURES, HYBRID_FEATURES,
    PROCESSED_FUSION_DIR, MODELS_TRAINED_DIR, MODELS_SCALERS_DIR,
    RESULTS_FORECAST_DIR, WINDOW_SIZE, FORECAST_HORIZON, SENTIMENT_LOOKBACK
)
from src.utils.file_utils import save_csv, load_csv, ensure_dir


def load_model_and_scaler(stock_name, model_type):
    """Load trained model and scaler."""
    import tensorflow as tf

    model_path = os.path.join(MODELS_TRAINED_DIR, f"{stock_name}_{model_type}_lstm.keras")
    scaler_path = os.path.join(MODELS_SCALERS_DIR, f"{stock_name}_{model_type}_scaler.pkl")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        print(f"[ERROR] Model or scaler not found for {stock_name} {model_type}")
        return None, None

    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)

    return model, scaler


def generate_forecast(stock_name, model_type):
    """
    Generate H+7 forecast for a given stock and model type.

    Args:
        stock_name: 'BBCA' or 'BBRI'
        model_type: 'baseline' or 'hybrid'

    Returns:
        DataFrame with forecast results
    """
    print(f"\n[INFO] Generating {model_type} forecast for {stock_name}...")

    model, scaler = load_model_and_scaler(stock_name, model_type)
    if model is None:
        return None

    # Determine features
    if model_type == 'baseline':
        feature_columns = BASELINE_FEATURES
    else:
        feature_columns = HYBRID_FEATURES

    # Load dataset
    dataset_type = 'baseline' if model_type == 'baseline' else 'hybrid'
    filepath = os.path.join(PROCESSED_FUSION_DIR, f"{stock_name}_{dataset_type}_dataset.csv")
    df = load_csv(filepath)

    if df is None or df.empty:
        print(f"[ERROR] No dataset for {stock_name}")
        return None

    df = df.sort_values('date').reset_index(drop=True)

    # Get last WINDOW_SIZE rows for initial sequence
    last_data = df.tail(WINDOW_SIZE).copy()
    all_cols = feature_columns + ['target_close_h1']

    # For hybrid: calculate sentiment assumption
    sentiment_assumption = None
    if model_type == 'hybrid' and 'sentiment_score' in df.columns:
        last_sentiments = df['sentiment_score'].tail(SENTIMENT_LOOKBACK)
        sentiment_assumption = float(last_sentiments.mean())
        print(f"[INFO] Sentiment assumption (7-day avg): {sentiment_assumption:.4f}")

    # Scale the initial sequence
    scaled_data = scaler.transform(last_data[all_cols].values)

    # Extract features only (exclude target)
    current_sequence = scaled_data[:, :-1].copy()  # Shape: (30, n_features)

    # Iterative forecast
    forecasts = []
    model_label = 'Baseline LSTM' if model_type == 'baseline' else 'Hybrid LSTM'

    for step in range(1, FORECAST_HORIZON + 1):
        # Reshape for LSTM input: (1, window_size, n_features)
        input_seq = current_sequence.reshape(1, WINDOW_SIZE, len(feature_columns))

        # Predict
        pred_scaled = model.predict(input_seq, verbose=0)[0, 0]

        # Inverse transform to get actual price
        n_features = len(feature_columns)
        dummy = np.zeros((1, n_features + 1))
        dummy[0, -1] = pred_scaled
        inverse = scaler.inverse_transform(dummy)
        predicted_price = inverse[0, -1]

        forecasts.append({
            'step': f'H+{step}',
            'stock': stock_name,
            'model': model_label,
            'predicted_close': round(float(predicted_price), 2),
            'sentiment_assumption': f"{sentiment_assumption:.4f}" if sentiment_assumption is not None else '',
            'forecast_type': 'simulation',
        })

        # Update sequence: shift and add new prediction
        # Create new row with predicted values
        new_row = current_sequence[-1].copy()

        # For the close feature (index 3 in OHLCV), use predicted value scaled
        # We need to figure out the scaled value of the predicted close
        new_features = np.zeros(n_features + 1)
        # Copy last known features as approximation
        new_features[:-1] = current_sequence[-1]
        new_features[-1] = pred_scaled
        # The close column index
        close_idx = feature_columns.index('close')
        new_row[close_idx] = pred_scaled

        if model_type == 'hybrid' and sentiment_assumption is not None:
            sent_idx = feature_columns.index('sentiment_score')

            sent_min = scaler.data_min_[sent_idx]
            sent_max = scaler.data_max_[sent_idx]

            if sent_max != sent_min:
                scaled_sentiment = (sentiment_assumption - sent_min) / (sent_max - sent_min)
            else:
                scaled_sentiment = 0

            new_row[sent_idx] = scaled_sentiment

        # Shift sequence: remove first, add new
        current_sequence = np.vstack([current_sequence[1:], new_row.reshape(1, -1)])

    # Create DataFrame
    forecast_df = pd.DataFrame(forecasts)

    # Save
    ensure_dir(RESULTS_FORECAST_DIR)
    filepath = os.path.join(RESULTS_FORECAST_DIR, f"{stock_name}_{model_type}_forecast_h7.csv")
    save_csv(forecast_df, filepath)

    print(f"[INFO] Forecast H+7 saved for {stock_name} {model_type}")

    return forecast_df


def run_forecast():
    """Generate forecasts for all stocks and models."""
    for stock_name in STOCK_NAMES:
        for model_type in ['baseline', 'hybrid']:
            generate_forecast(stock_name, model_type)

    print(f"\n{'='*60}")
    print(f"  All forecasts generated!")
    print(f"{'='*60}")


if __name__ == '__main__':
    run_forecast()
