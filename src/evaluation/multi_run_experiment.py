"""
Sentilytics — Multiple Run Experiment
Trains both Baseline and Hybrid LSTM N times and reports
mean/std MAPE to determine if improvement is real or noise.

Usage:
    python -m src.evaluation.multi_run_experiment
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import (
    STOCK_NAMES, WINDOW_SIZE, EPOCHS, BATCH_SIZE,
    BASELINE_FEATURES, HYBRID_FEATURES,
    PROCESSED_FUSION_DIR, RESULTS_METRICS_DIR
)
from src.utils.file_utils import ensure_dir, load_csv
from src.preprocessing.sequence_builder import prepare_data
from src.modeling.lstm_model import build_lstm_model
from src.evaluation.metrics import calculate_rmse, calculate_mae, calculate_mape

N_RUNS = 5


def train_and_evaluate_once(stock_name, model_type, run_idx):
    """Train one model instance and return RMSE, MAE, MAPE."""
    import tensorflow as tf

    features = BASELINE_FEATURES if model_type == 'baseline' else HYBRID_FEATURES
    dataset_type = 'baseline' if model_type == 'baseline' else 'hybrid'

    filepath = os.path.join(PROCESSED_FUSION_DIR, f"{stock_name}_{dataset_type}_dataset.csv")
    df = load_csv(filepath)
    if df is None:
        return None

    # Prepare data using the same prepare_data as train scripts
    data = prepare_data(
        df=df,
        feature_columns=features,
        stock_name=stock_name,
        model_type=model_type
    )

    X_train = data['X_train']
    y_train = data['y_train']
    X_test  = data['X_test']
    y_test  = data['y_test']
    scaler  = data['scaler']
    n_features = len(features)

    input_shape = (WINDOW_SIZE, n_features)
    model = build_lstm_model(input_shape, name=f'{stock_name}_{model_type}_run{run_idx}')
    model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.1,
        verbose=0,
        shuffle=False
    )

    # Predict + inverse transform
    pred_scaled = model.predict(X_test, verbose=0)
    dummy_pred = np.zeros((len(pred_scaled), n_features + 1))
    dummy_pred[:, -1] = pred_scaled.flatten()
    predicted = scaler.inverse_transform(dummy_pred)[:, -1]

    dummy_actual = np.zeros((len(y_test), n_features + 1))
    dummy_actual[:, -1] = y_test
    actual = scaler.inverse_transform(dummy_actual)[:, -1]

    rmse = calculate_rmse(actual, predicted)
    mae  = calculate_mae(actual, predicted)
    mape = calculate_mape(actual, predicted)

    print(f"    Run {run_idx+1}: RMSE={rmse:.2f} | MAE={mae:.2f} | MAPE={mape:.4f}%")
    return {'rmse': rmse, 'mae': mae, 'mape': mape}


def run_multi_experiment():
    """Main experiment: N runs per stock x model combination."""
    ensure_dir(RESULTS_METRICS_DIR)

    summary = []

    for stock in STOCK_NAMES:
        for model_type in ['baseline', 'hybrid']:
            model_label = 'Baseline LSTM' if model_type == 'baseline' else 'Hybrid LSTM'
            print(f"\n[INFO] {stock} — {model_label} ({N_RUNS} runs)...")

            runs = []
            for i in range(N_RUNS):
                result = train_and_evaluate_once(stock, model_type, i)
                if result:
                    runs.append(result)

            if runs:
                mapes = [r['mape'] for r in runs]
                rmses = [r['rmse'] for r in runs]
                maes  = [r['mae']  for r in runs]

                entry = {
                    'stock': stock,
                    'model': model_label,
                    'mape_mean': round(np.mean(mapes), 4),
                    'mape_std':  round(np.std(mapes),  4),
                    'mape_min':  round(np.min(mapes),  4),
                    'mape_max':  round(np.max(mapes),  4),
                    'rmse_mean': round(np.mean(rmses), 4),
                    'mae_mean':  round(np.mean(maes),  4),
                    'n_runs': N_RUNS,
                }
                summary.append(entry)

    # Print final comparison
    print(f"\n{'='*65}")
    print(f"  MULTI-RUN EXPERIMENT RESULTS ({N_RUNS} runs each)")
    print(f"{'='*65}")
    for stock in STOCK_NAMES:
        rows = [r for r in summary if r['stock'] == stock]
        print(f"\n  {stock}:")
        for r in rows:
            print(f"    {r['model']:14s} | MAPE mean={r['mape_mean']:.4f}%  "
                  f"std={r['mape_std']:.4f}%  "
                  f"[{r['mape_min']:.4f}% - {r['mape_max']:.4f}%]")

        if len(rows) == 2:
            base = rows[0]['mape_mean']
            hybr = rows[1]['mape_mean']
            diff = base - hybr
            conclusion = "HYBRID LEBIH BAIK (konsisten)" if diff > rows[0]['mape_std'] else "TIDAK SIGNIFIKAN (mungkin noise)"
            print(f"    Selisih rata-rata: {diff:.4f}%  =>  {conclusion}")

    # Save
    df = pd.DataFrame(summary)
    out_path = os.path.join(RESULTS_METRICS_DIR, 'multi_run_experiment.csv')
    df.to_csv(out_path, index=False)
    print(f"\n[INFO] Hasil disimpan: {out_path}")

    return summary


if __name__ == '__main__':
    run_multi_experiment()
