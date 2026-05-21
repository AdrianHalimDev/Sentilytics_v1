"""
Sentilytics — Configuration Loader
Loads settings from config.yaml and provides project-wide constants.
"""

import os
import yaml

# ============================================
# Resolve project root directory
# ============================================
# config.py is in src/, so project root is one level up
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# ============================================
# Load YAML configuration
# ============================================
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.yaml')

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    _cfg = yaml.safe_load(f)

# ============================================
# Stock Settings
# ============================================
STOCKS = _cfg['stocks']  # List of {ticker, name}
STOCK_TICKERS = {s['name']: s['ticker'] for s in STOCKS}  # e.g. {'BBCA': 'BBCA.JK'}
STOCK_NAMES = [s['name'] for s in STOCKS]  # ['BBCA', 'BBRI']
DATE_START = _cfg['date_range']['start']
DATE_END = _cfg['date_range']['end']

# ============================================
# Scraping Settings
# ============================================
SCRAPING_SOURCES = _cfg['scraping']['sources']
KEYWORDS_BBCA = _cfg['scraping']['keywords_bbca']
KEYWORDS_BBRI = _cfg['scraping']['keywords_bbri']
KEYWORDS_SECTOR = _cfg['scraping']['keywords_sector']

# Map keywords to stock names for scraping
KEYWORD_STOCK_MAP = {}
for kw in KEYWORDS_BBCA:
    KEYWORD_STOCK_MAP[kw] = 'BBCA'
for kw in KEYWORDS_BBRI:
    KEYWORD_STOCK_MAP[kw] = 'BBRI'
for kw in KEYWORDS_SECTOR:
    KEYWORD_STOCK_MAP[kw] = 'SECTOR'

# ============================================
# Model Hyperparameters
# ============================================
WINDOW_SIZE = _cfg['model']['window_size']
LSTM_UNITS = _cfg['model']['lstm_units']
DROPOUT = _cfg['model']['dropout']
DENSE_OUTPUT = _cfg['model']['dense_output']
OPTIMIZER = _cfg['model']['optimizer']
LOSS = _cfg['model']['loss']
EPOCHS = _cfg['model']['epochs']
BATCH_SIZE = _cfg['model']['batch_size']
TRAIN_SPLIT = _cfg['model']['train_split']

# ============================================
# Feature Columns
# ============================================
BASELINE_FEATURES = _cfg['features']['baseline']
HYBRID_FEATURES = _cfg['features']['hybrid']
TARGET_COLUMN = _cfg['features']['target']

# ============================================
# File Paths (absolute)
# ============================================
PATHS = {}
for key, rel_path in _cfg['paths'].items():
    PATHS[key] = os.path.join(PROJECT_ROOT, rel_path)

# Convenience shortcuts
RAW_STOCK_DIR = PATHS['raw_stock']
RAW_NEWS_DIR = PATHS['raw_news']
PROCESSED_STOCK_DIR = PATHS['processed_stock']
PROCESSED_SENTIMENT_DIR = PATHS['processed_sentiment']
PROCESSED_FUSION_DIR = PATHS['processed_fusion']
EXTERNAL_LEXICON_DIR = PATHS['external_lexicon']
MODELS_TRAINED_DIR = PATHS['models_trained']
MODELS_SCALERS_DIR = PATHS['models_scalers']
RESULTS_PREDICTIONS_DIR = PATHS['results_predictions']
RESULTS_METRICS_DIR = PATHS['results_metrics']
RESULTS_FORECAST_DIR = PATHS['results_forecast']
RESULTS_FIGURES_DIR = PATHS['results_figures']

# ============================================
# Forecast Settings
# ============================================
FORECAST_HORIZON = _cfg['forecast']['horizon']
SENTIMENT_LOOKBACK = _cfg['forecast']['sentiment_lookback']

# ============================================
# Helper: ensure all directories exist
# ============================================
def ensure_directories():
    """Create all required directories if they don't exist."""
    for path in PATHS.values():
        os.makedirs(path, exist_ok=True)
    # Also create notebooks and docs directories
    os.makedirs(os.path.join(PROJECT_ROOT, 'notebooks'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, 'docs'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, 'tests'), exist_ok=True)
