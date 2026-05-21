"""
Sentilytics — Dashboard Routes
User-facing routes for viewing prediction results, evaluation, and forecasts.
All routes only READ pre-computed results from CSV files.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from app.services.prediction_service import (
    get_predictions, get_metrics, get_all_metrics,
    get_forecast, get_prediction_h1
)
from app.services.chart_service import (
    prepare_actual_vs_predicted_chart,
    prepare_forecast_chart,
    prepare_evaluation_chart
)
from app.services.dataset_service import (
    get_stock_counts, get_news_count, get_news_processed_count,
    get_dataset_files, get_sentiment_stats
)

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page with filters, metrics, and charts."""
    stock = request.args.get('stock', 'BBCA')
    model = request.args.get('model', 'baseline')

    predictions = get_predictions(stock, model)
    metrics = get_metrics(stock, model)
    prediction_h1 = get_prediction_h1(stock, model)
    forecast = get_forecast(stock, model)

    chart_data = prepare_actual_vs_predicted_chart(predictions)
    forecast_data = prepare_forecast_chart(forecast)

    return render_template('dashboard.html',
                           stock=stock,
                           model=model,
                           predictions=predictions,
                           metrics=metrics,
                           prediction_h1=prediction_h1,
                           chart_data=chart_data,
                           forecast_data=forecast_data)


@dashboard_bp.route('/prediction')
@login_required
def prediction():
    """Detailed prediction results page."""
    stock = request.args.get('stock', 'BBCA')
    model = request.args.get('model', 'baseline')
    model_label = 'Baseline LSTM' if model == 'baseline' else 'Hybrid LSTM'

    predictions = get_predictions(stock, model)

    return render_template('prediction.html',
                           stock=stock,
                           model=model,
                           model_label=model_label,
                           predictions=predictions)


@dashboard_bp.route('/evaluation')
@login_required
def evaluation():
    """Model evaluation comparison page."""
    all_metrics = get_all_metrics()
    eval_chart_data = prepare_evaluation_chart(all_metrics)

    return render_template('evaluation.html',
                           all_metrics=all_metrics,
                           eval_chart_data=eval_chart_data)


@dashboard_bp.route('/forecast')
@login_required
def forecast():
    """Forecast simulation H+7 page."""
    stock = request.args.get('stock', 'BBCA')
    model = request.args.get('model', 'baseline')
    model_label = 'Baseline LSTM' if model == 'baseline' else 'Hybrid LSTM'

    forecast_data = get_forecast(stock, model)
    forecast_chart_data = prepare_forecast_chart(forecast_data)

    return render_template('forecast.html',
                           stock=stock,
                           model=model,
                           model_label=model_label,
                           forecast=forecast_data,
                           forecast_chart_data=forecast_chart_data)


@dashboard_bp.route('/dataset-summary')
@login_required
def dataset_summary():
    """Dataset summary page (admin feature, but accessible to users for info)."""
    stock_counts = get_stock_counts()
    news_count = get_news_count()
    news_processed_count = get_news_processed_count()
    dataset_files = get_dataset_files()
    sentiment_stats = get_sentiment_stats()

    return render_template('dataset_summary.html',
                           stock_counts=stock_counts,
                           news_count=news_count,
                           news_processed_count=news_processed_count,
                           dataset_files=dataset_files,
                           sentiment_stats=sentiment_stats)


# ==========================================
# API Routes (JSON endpoints)
# ==========================================

@dashboard_bp.route('/api/results')
@login_required
def api_results():
    """API endpoint for prediction results."""
    stock = request.args.get('stock', 'BBCA')
    model = request.args.get('model', 'baseline')

    predictions = get_predictions(stock, model)
    metrics = get_metrics(stock, model)
    model_label = 'Baseline LSTM' if model == 'baseline' else 'Hybrid LSTM'

    return jsonify({
        'stock': stock,
        'model': model_label,
        'metrics': {
            'rmse': metrics.rmse if metrics else None,
            'mae': metrics.mae if metrics else None,
            'mape': metrics.mape if metrics else None,
        },
        'predictions': [
            {
                'date': p.date,
                'actual': p.actual_close,
                'predicted': p.predicted_close,
            } for p in predictions
        ]
    })


@dashboard_bp.route('/api/forecast')
@login_required
def api_forecast():
    """API endpoint for forecast data."""
    stock = request.args.get('stock', 'BBCA')
    model = request.args.get('model', 'baseline')
    model_label = 'Baseline LSTM' if model == 'baseline' else 'Hybrid LSTM'

    forecast_data = get_forecast(stock, model)

    return jsonify({
        'stock': stock,
        'model': model_label,
        'forecast_type': 'simulation',
        'sentiment_assumption': '7-day average sentiment' if model == 'hybrid' else None,
        'data': [
            {
                'step': f.step,
                'predicted_close': f.predicted_close,
            } for f in forecast_data
        ]
    })


@dashboard_bp.route('/api/metrics')
@login_required
def api_metrics():
    """API endpoint for all evaluation metrics."""
    all_metrics = get_all_metrics()

    return jsonify({
        'metrics': [
            {
                'stock': m.stock,
                'model': m.model,
                'rmse': m.rmse,
                'mae': m.mae,
                'mape': m.mape,
            } for m in all_metrics
        ]
    })


@dashboard_bp.route('/api/dataset-summary')
@login_required
def api_dataset_summary():
    """API endpoint for dataset summary."""
    return jsonify({
        'stock_counts': get_stock_counts(),
        'news_count': get_news_count(),
        'news_processed': get_news_processed_count(),
    })


@dashboard_bp.route('/api/model-status')
@login_required
def api_model_status():
    """API endpoint for model file status."""
    from app.services.dataset_service import get_model_status
    return jsonify({'models': get_model_status()})
