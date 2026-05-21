"""
Sentilytics — Evaluation Metrics
Calculates RMSE, MAE, and MAPE for model evaluation.
Saves evaluation_metrics.csv with all model results.

Usage:
    python -m src.evaluation.metrics
"""

import os
import sys
import numpy as np
import pandas as pd
from math import sqrt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import (
    STOCK_NAMES, RESULTS_PREDICTIONS_DIR, RESULTS_METRICS_DIR,
    WINDOW_SIZE, EPOCHS, BATCH_SIZE,
    BASELINE_FEATURES, HYBRID_FEATURES
)
from src.utils.file_utils import save_csv, load_csv, ensure_dir


def calculate_rmse(actual, predicted):
    """Calculate Root Mean Squared Error."""
    return sqrt(np.mean((actual - predicted) ** 2))


def calculate_mae(actual, predicted):
    """Calculate Mean Absolute Error."""
    return np.mean(np.abs(actual - predicted))


def calculate_mape(actual, predicted):
    """Calculate Mean Absolute Percentage Error (%)."""
    # Avoid division by zero
    mask = actual != 0
    if mask.sum() == 0:
        return 0.0
    return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100


def evaluate_model(stock_name, model_type):
    """
    Evaluate a single model using its prediction CSV.

    Args:
        stock_name: 'BBCA' or 'BBRI'
        model_type: 'baseline' or 'hybrid'

    Returns:
        dict with evaluation metrics or None
    """
    filename = f"{stock_name}_{model_type}_predictions.csv"
    filepath = os.path.join(RESULTS_PREDICTIONS_DIR, filename)
    df = load_csv(filepath)

    if df is None or df.empty:
        print(f"[WARNING] No predictions found: {filename}")
        return None

    actual = df['actual_close'].values
    predicted = df['predicted_close'].values

    rmse = calculate_rmse(actual, predicted)
    mae = calculate_mae(actual, predicted)
    mape = calculate_mape(actual, predicted)

    model_label = 'Baseline LSTM' if model_type == 'baseline' else 'Hybrid LSTM'
    features = ', '.join(BASELINE_FEATURES if model_type == 'baseline' else HYBRID_FEATURES)

    result = {
        'stock': stock_name,
        'model': model_label,
        'features': features,
        'rmse': round(rmse, 4),
        'mae': round(mae, 4),
        'mape': round(mape, 4),
        'window_size': WINDOW_SIZE,
        'epochs': EPOCHS,
        'batch_size': BATCH_SIZE,
    }

    print(f"\n[INFO] {stock_name} {model_label}:")
    print(f"  RMSE  = {rmse:.4f}")
    print(f"  MAE   = {mae:.4f}")
    print(f"  MAPE  = {mape:.4f}%")

    return result


def run_evaluation():
    """Evaluate all models and save metrics."""
    ensure_dir(RESULTS_METRICS_DIR)

    all_results = []

    for stock_name in STOCK_NAMES:
        for model_type in ['baseline', 'hybrid']:
            result = evaluate_model(stock_name, model_type)
            if result:
                all_results.append(result)

    if all_results:
        metrics_df = pd.DataFrame(all_results)
        filepath = os.path.join(RESULTS_METRICS_DIR, 'evaluation_metrics.csv')
        save_csv(metrics_df, filepath)

        print(f"\n{'='*60}")
        print("  Evaluation Summary")
        print(f"{'='*60}")
        print(metrics_df[['stock', 'model', 'rmse', 'mae', 'mape']].to_string(index=False))
    else:
        print("[WARNING] No models to evaluate")

    return all_results


if __name__ == '__main__':
    run_evaluation()
