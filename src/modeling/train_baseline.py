"""
Sentilytics — Train Baseline LSTM
Trains Baseline LSTM models (OHLCV only) for BBCA and BBRI.
Saves models (.keras), scalers (.pkl), predictions (CSV), and history (CSV).

IMPORTANT: This script runs OFFLINE, never from Flask routes.

Usage:
    python -m src.modeling.train_baseline
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import (
    STOCK_NAMES, BASELINE_FEATURES, PROCESSED_FUSION_DIR,
    MODELS_TRAINED_DIR, RESULTS_PREDICTIONS_DIR,
    EPOCHS, BATCH_SIZE, WINDOW_SIZE
)
from src.preprocessing.sequence_builder import prepare_data
from src.modeling.lstm_model import build_lstm_model
from src.utils.file_utils import save_csv, load_csv, ensure_dir


def inverse_transform_target(scaler, y_scaled, n_features):
    """
    Inverse transform the target column from scaled values.
    The target is the last column in the scaler's feature set.
    """
    # Create a dummy array with the right number of columns
    dummy = np.zeros((len(y_scaled), n_features + 1))
    # Place scaled target in the last column
    dummy[:, -1] = y_scaled.flatten()
    # Inverse transform
    inverse = scaler.inverse_transform(dummy)
    # Return only the target column
    return inverse[:, -1]


def train_baseline_model(stock_name):
    """
    Train Baseline LSTM for a single stock.

    Args:
        stock_name: 'BBCA' or 'BBRI'
    """
    print(f"\n{'='*60}")
    print(f"  Training Baseline LSTM — {stock_name}")
    print(f"{'='*60}")

    # Load baseline dataset
    filepath = os.path.join(PROCESSED_FUSION_DIR, f"{stock_name}_baseline_dataset.csv")
    df = load_csv(filepath)

    if df is None or df.empty:
        print(f"[ERROR] No baseline dataset for {stock_name}")
        return

    # Prepare data
    data = prepare_data(
        df=df,
        feature_columns=BASELINE_FEATURES,
        stock_name=stock_name,
        model_type='baseline'
    )

    X_train = data['X_train']
    y_train = data['y_train']
    X_test = data['X_test']
    y_test = data['y_test']
    scaler = data['scaler']
    dates_test = data['dates_test']
    n_features = len(BASELINE_FEATURES)

    # Build model
    input_shape = (WINDOW_SIZE, n_features)
    model = build_lstm_model(input_shape, name=f'{stock_name}_baseline_lstm')

    # Train
    print(f"\n[INFO] Training for {EPOCHS} epochs, batch size {BATCH_SIZE}...")
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.1,
        verbose=1,
        shuffle=False  # IMPORTANT: do NOT shuffle time-series
    )

    # Save model
    ensure_dir(MODELS_TRAINED_DIR)
    model_path = os.path.join(MODELS_TRAINED_DIR, f"{stock_name}_baseline_lstm.keras")
    model.save(model_path)
    print(f"[INFO] Model saved: {model_path}")

    # Save training history
    history_df = pd.DataFrame(history.history)
    history_path = os.path.join(MODELS_TRAINED_DIR, f"{stock_name}_baseline_history.csv")
    save_csv(history_df, history_path, index=True)

    # Predict on test set
    y_pred_scaled = model.predict(X_test, verbose=0)

    # Inverse transform
    y_actual = inverse_transform_target(scaler, y_test, n_features)
    y_predicted = inverse_transform_target(scaler, y_pred_scaled, n_features)

    # Calculate errors
    errors = y_actual - y_predicted
    abs_errors = np.abs(errors)
    ape = np.abs(errors / y_actual) * 100

    # Save predictions
    ensure_dir(RESULTS_PREDICTIONS_DIR)
    pred_df = pd.DataFrame({
        'date': dates_test[:len(y_actual)],
        'stock': stock_name,
        'model': 'Baseline LSTM',
        'actual_close': y_actual,
        'predicted_close': y_predicted,
        'error': errors,
        'absolute_error': abs_errors,
        'absolute_percentage_error': ape,
    })

    pred_path = os.path.join(RESULTS_PREDICTIONS_DIR, f"{stock_name}_baseline_predictions.csv")
    save_csv(pred_df, pred_path)

    print(f"\n[INFO] Baseline LSTM training complete for {stock_name}!")
    print(f"[INFO] Test samples: {len(y_actual)}")


def run_baseline_training():
    """Train Baseline LSTM for all stocks."""
    for stock_name in STOCK_NAMES:
        train_baseline_model(stock_name)

    print(f"\n{'='*60}")
    print(f"  All Baseline LSTM training complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    run_baseline_training()
