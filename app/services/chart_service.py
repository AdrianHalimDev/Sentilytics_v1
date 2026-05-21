"""
Sentilytics — Chart Service
Prepares data structures for Chart.js rendering.
"""


def prepare_actual_vs_predicted_chart(predictions):
    """
    Convert prediction data into Chart.js-compatible format.
    Returns dict with dates, actual, predicted arrays.
    """
    if not predictions:
        return {}

    return {
        'dates': [p.date for p in predictions],
        'actual': [p.actual_close for p in predictions],
        'predicted': [p.predicted_close for p in predictions],
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
        'predicted': [f.predicted_close for f in forecast],
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
        'rmse': [m.rmse for m in all_metrics],
        'mae': [m.mae for m in all_metrics],
        'mape': [m.mape for m in all_metrics],
    }
