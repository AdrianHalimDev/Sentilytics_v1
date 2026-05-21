"""
Sentilytics — Prediction Service
Reads prediction results, metrics, and forecast data from CSV files.
Dashboard only reads pre-computed results — never trains models.
"""

import os
import pandas as pd
from types import SimpleNamespace


# Base paths (relative to project root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PREDICTIONS_DIR = os.path.join(PROJECT_ROOT, 'results', 'predictions')
METRICS_DIR = os.path.join(PROJECT_ROOT, 'results', 'metrics')
FORECAST_DIR = os.path.join(PROJECT_ROOT, 'results', 'forecast')


def get_predictions(stock, model):
    """
    Load prediction results for a given stock and model.
    Returns list of SimpleNamespace objects or empty list.
    """
    model_name = 'baseline' if model == 'baseline' else 'hybrid'
    filename = f"{stock}_{model_name}_predictions.csv"
    filepath = os.path.join(PREDICTIONS_DIR, filename)

    if not os.path.exists(filepath):
        return []

    try:
        df = pd.read_csv(filepath)
        results = []
        for _, row in df.iterrows():
            results.append(SimpleNamespace(
                date=row.get('date', ''),
                stock=row.get('stock', stock),
                model=row.get('model', model_name),
                actual_close=float(row.get('actual_close', 0)),
                predicted_close=float(row.get('predicted_close', 0)),
                error=float(row.get('error', 0)),
                absolute_error=float(row.get('absolute_error', 0)),
                absolute_percentage_error=float(row.get('absolute_percentage_error', 0)),
            ))
        return results
    except Exception as e:
        print(f"[ERROR] Loading predictions: {e}")
        return []


def get_metrics(stock, model):
    """
    Load evaluation metrics for a given stock and model.
    Returns SimpleNamespace with rmse, mae, mape or None.
    """
    filepath = os.path.join(METRICS_DIR, 'evaluation_metrics.csv')

    if not os.path.exists(filepath):
        return None

    try:
        df = pd.read_csv(filepath)
        model_label = 'Baseline LSTM' if model == 'baseline' else 'Hybrid LSTM'
        row = df[(df['stock'] == stock) & (df['model'] == model_label)]

        if row.empty:
            return None

        row = row.iloc[0]
        return SimpleNamespace(
            rmse=float(row['rmse']),
            mae=float(row['mae']),
            mape=float(row['mape']),
        )
    except Exception as e:
        print(f"[ERROR] Loading metrics: {e}")
        return None


def get_all_metrics():
    """
    Load all evaluation metrics for the comparison table.
    Returns list of SimpleNamespace objects.
    """
    filepath = os.path.join(METRICS_DIR, 'evaluation_metrics.csv')

    if not os.path.exists(filepath):
        return []

    try:
        df = pd.read_csv(filepath)
        results = []
        for _, row in df.iterrows():
            results.append(SimpleNamespace(
                stock=row.get('stock', ''),
                model=row.get('model', ''),
                features=row.get('features', ''),
                rmse=float(row.get('rmse', 0)),
                mae=float(row.get('mae', 0)),
                mape=float(row.get('mape', 0)),
                window_size=int(row.get('window_size', 30)),
                epochs=int(row.get('epochs', 50)),
                batch_size=int(row.get('batch_size', 32)),
            ))
        return results
    except Exception as e:
        print(f"[ERROR] Loading all metrics: {e}")
        return []


def get_forecast(stock, model):
    """
    Load forecast H+7 data for a given stock and model.
    Returns list of SimpleNamespace objects.
    """
    model_name = 'baseline' if model == 'baseline' else 'hybrid'
    filename = f"{stock}_{model_name}_forecast_h7.csv"
    filepath = os.path.join(FORECAST_DIR, filename)

    if not os.path.exists(filepath):
        return []

    try:
        df = pd.read_csv(filepath)
        results = []
        for _, row in df.iterrows():
            results.append(SimpleNamespace(
                step=row.get('step', ''),
                stock=row.get('stock', stock),
                model=row.get('model', ''),
                predicted_close=float(row.get('predicted_close', 0)),
                sentiment_assumption=row.get('sentiment_assumption', ''),
                forecast_type=row.get('forecast_type', 'simulation'),
            ))
        return results
    except Exception as e:
        print(f"[ERROR] Loading forecast: {e}")
        return []


def get_prediction_h1(stock, model):
    """Get the last predicted close price (H+1)."""
    predictions = get_predictions(stock, model)
    if predictions:
        return predictions[-1].predicted_close
    return None
