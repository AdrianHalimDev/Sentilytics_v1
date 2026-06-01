"""
Sentilytics — Chart Service
Prepares data structures for Chart.js rendering.
"""


def prepare_actual_vs_predicted_chart(predictions, historical=None):
    """
    Build Chart.js-compatible data for the full-range Actual vs Predicted chart.

    If historical data is provided, the chart shows:
      - Dataset 1: All historical close prices (training + test period) — full actual line
      - Dataset 2: Predicted close prices only for the test set (nulls for training)
      - split_date: first date of test set (for vertical annotation line)
      - split_index: index position of the train/test split

    If historical data is NOT provided, falls back to test-set-only view.
    """
    if not predictions:
        return {}

    if historical and historical.get('dates'):
        hist_dates = historical['dates']
        hist_close = historical['close']

        # Build a lookup from date → predicted close (test set only)
        pred_map = {p.date: round(float(p.predicted_close), 2) for p in predictions}
        test_dates_set = set(p.date for p in predictions)

        # Find the split index (first date of test set in the full historical list)
        split_index = None
        for i, d in enumerate(hist_dates):
            if d in test_dates_set:
                split_index = i
                break

        # Build predicted array: None for training rows, value for test rows
        predicted_full = []
        for d in hist_dates:
            predicted_full.append(pred_map.get(d, None))

        split_date = predictions[0].date if predictions else None

        return {
            'dates': hist_dates,
            'actual': hist_close,
            'predicted': predicted_full,
            'split_index': split_index,
            'split_date': split_date,
            'train_count': split_index if split_index else 0,
            'test_count': len(predictions),
        }

    # Fallback: test-set only
    return {
        'dates': [p.date for p in predictions],
        'actual': [round(float(p.actual_close), 2) for p in predictions],
        'predicted': [round(float(p.predicted_close), 2) for p in predictions],
        'split_index': None,
        'split_date': None,
        'train_count': 0,
        'test_count': len(predictions),
    }


def prepare_forecast_chart(forecast):
    """
    Convert forecast data into Chart.js-compatible format.
    Returns dict with steps and predicted arrays.
    """
    if not forecast:
        return {}

    return {
        'steps': [f.step for f in forecast],
        'predicted': [round(float(f.predicted_close), 2) for f in forecast],
    }


def prepare_evaluation_chart(all_metrics):
    """
    Prepare evaluation comparison chart data.
    Returns dict with labels, rmse, mae, mape arrays.
    """
    if not all_metrics:
        return {}

    return {
        'labels': [f"{m.stock} {m.model}" for m in all_metrics],
        'rmse': [round(float(m.rmse), 2) for m in all_metrics],
        'mae': [round(float(m.mae), 2) for m in all_metrics],
        'mape': [round(float(m.mape), 4) for m in all_metrics],
    }


def prepare_error_over_time_chart(predictions):
    """
    Prepare APE (Absolute Percentage Error) over time chart data.
    Used in the evaluation page to show error distribution per date.
    """
    if not predictions:
        return {}

    return {
        'dates': [p.date for p in predictions],
        'ape': [round(float(p.absolute_percentage_error), 4) for p in predictions],
        'error': [round(float(p.error), 2) for p in predictions],
    }
