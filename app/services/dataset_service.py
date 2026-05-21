"""
Sentilytics — Dataset Service
Provides dataset summary information for admin panel.
"""

import os
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def get_stock_counts():
    """Get row counts for stock datasets."""
    counts = {}
    for stock in ['BBCA', 'BBRI']:
        filepath = os.path.join(PROJECT_ROOT, 'data', 'raw', 'stock', f'{stock}_raw.csv')
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                counts[stock] = len(df)
            except Exception:
                counts[stock] = 0
        else:
            counts[stock] = 0
    return counts


def get_news_count():
    """Get total news article count."""
    filepath = os.path.join(PROJECT_ROOT, 'data', 'raw', 'news', 'news_raw.csv')
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            return len(df)
        except Exception:
            return 0
    return 0


def get_news_processed_count():
    """Get processed news count."""
    filepath = os.path.join(PROJECT_ROOT, 'data', 'processed', 'sentiment', 'news_processed.csv')
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            return len(df)
        except Exception:
            return 0
    return 0


def get_dataset_files():
    """Get status of all important dataset files."""
    files_to_check = [
        ('BBCA Stock Raw', 'data/raw/stock/BBCA_raw.csv'),
        ('BBRI Stock Raw', 'data/raw/stock/BBRI_raw.csv'),
        ('News Raw', 'data/raw/news/news_raw.csv'),
        ('News Processed', 'data/processed/sentiment/news_processed.csv'),
        ('BBCA Daily Sentiment', 'data/processed/sentiment/BBCA_daily_sentiment.csv'),
        ('BBRI Daily Sentiment', 'data/processed/sentiment/BBRI_daily_sentiment.csv'),
        ('BBCA Baseline Dataset', 'data/processed/fusion/BBCA_baseline_dataset.csv'),
        ('BBCA Hybrid Dataset', 'data/processed/fusion/BBCA_hybrid_dataset.csv'),
        ('BBRI Baseline Dataset', 'data/processed/fusion/BBRI_baseline_dataset.csv'),
        ('BBRI Hybrid Dataset', 'data/processed/fusion/BBRI_hybrid_dataset.csv'),
    ]

    results = []
    for name, rel_path in files_to_check:
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        exists = os.path.exists(full_path)
        size = ''
        if exists:
            size_bytes = os.path.getsize(full_path)
            if size_bytes > 1024 * 1024:
                size = f"{size_bytes / (1024*1024):.1f} MB"
            elif size_bytes > 1024:
                size = f"{size_bytes / 1024:.1f} KB"
            else:
                size = f"{size_bytes} B"
        results.append({
            'name': name,
            'path': rel_path,
            'exists': exists,
            'size': size,
        })

    return results


def get_sentiment_stats():
    """Get sentiment distribution per stock."""
    stats = {}
    for stock in ['BBCA', 'BBRI']:
        filepath = os.path.join(PROJECT_ROOT, 'data', 'processed', 'sentiment',
                                f'{stock}_daily_sentiment.csv')
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                stats[stock] = {
                    'positive': int(df['positive_count'].sum()) if 'positive_count' in df.columns else 0,
                    'neutral': int(df['neutral_count'].sum()) if 'neutral_count' in df.columns else 0,
                    'negative': int(df['negative_count'].sum()) if 'negative_count' in df.columns else 0,
                }
            except Exception:
                stats[stock] = {'positive': 0, 'neutral': 0, 'negative': 0}
    return stats


def get_model_status():
    """Get status of all model files."""
    status = []
    for stock in ['BBCA', 'BBRI']:
        for model_type in ['baseline', 'hybrid']:
            model_label = 'Baseline LSTM' if model_type == 'baseline' else 'Hybrid LSTM'
            model_file = os.path.join(PROJECT_ROOT, 'models', 'trained',
                                      f'{stock}_{model_type}_lstm.keras')
            scaler_file = os.path.join(PROJECT_ROOT, 'models', 'scalers',
                                       f'{stock}_{model_type}_scaler.pkl')
            pred_file = os.path.join(PROJECT_ROOT, 'results', 'predictions',
                                     f'{stock}_{model_type}_predictions.csv')

            status.append({
                'stock': stock,
                'model': model_label,
                'model_exists': os.path.exists(model_file),
                'scaler_exists': os.path.exists(scaler_file),
                'prediction_exists': os.path.exists(pred_file),
            })
    return status
