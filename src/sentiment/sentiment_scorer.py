"""
Sentilytics — Sentiment Scorer
Calculates sentiment scores using InSet Lexicon.
Produces per-article scores and daily aggregated scores per stock.

Scoring formula:
    sentiment_score = sum(token_weights for tokens found in InSet)
    avg_sentiment_score = sentiment_score / count(valid_tokens)  [used as model feature]

Labels:
    score > 0  → positif
    score = 0  → netral
    score < 0  → negatif

Usage:
    python -m src.sentiment.sentiment_scorer
"""

import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import PROCESSED_SENTIMENT_DIR, STOCK_NAMES
from src.sentiment.inset_loader import load_lexicon, download_inset_lexicon
from src.utils.file_utils import save_csv, load_csv, ensure_dir


def calculate_sentiment_score(stemmed_text, positive_dict, negative_dict):
    """
    Calculate sentiment score for a single text using InSet lexicon.

    Args:
        stemmed_text: Space-separated stemmed tokens
        positive_dict: dict mapping word → positive weight
        negative_dict: dict mapping word → negative weight (negative values)

    Returns:
        tuple: (sentiment_score, avg_sentiment_score, valid_token_count)
    """
    if not isinstance(stemmed_text, str) or not stemmed_text.strip():
        return 0, 0.0, 0

    tokens = stemmed_text.strip().split()
    total_score = 0
    valid_count = 0

    for token in tokens:
        token = token.lower().strip()
        if token in positive_dict:
            total_score += positive_dict[token]
            valid_count += 1
        elif token in negative_dict:
            total_score += negative_dict[token]
            valid_count += 1

    avg_score = total_score / valid_count if valid_count > 0 else 0.0

    return total_score, avg_score, valid_count


def get_sentiment_label(score):
    """Assign sentiment label based on score."""
    if score > 0:
        return 'positif'
    elif score < 0:
        return 'negatif'
    else:
        return 'netral'


def score_all_news():
    """
    Calculate sentiment scores for all preprocessed news.
    Saves: news_processed.csv (with scores), daily sentiment CSVs.
    """
    ensure_dir(PROCESSED_SENTIMENT_DIR)

    # Ensure InSet lexicon is available
    download_inset_lexicon()

    # Load lexicon
    positive_dict, negative_dict = load_lexicon()

    if not positive_dict and not negative_dict:
        print("[ERROR] InSet lexicon not loaded. Cannot score.")
        return None

    # Load preprocessed news
    filepath = os.path.join(PROCESSED_SENTIMENT_DIR, 'news_processed.csv')
    df = load_csv(filepath)

    if df is None or df.empty:
        print("[WARNING] No preprocessed news to score")
        return None

    print(f"\n[INFO] Scoring sentiment for {len(df)} articles...")

    # Calculate scores
    scores = []
    avg_scores = []
    labels = []

    for idx, row in df.iterrows():
        stemmed = row.get('stemmed_text', '')
        total_score, avg_score, valid_count = calculate_sentiment_score(
            stemmed, positive_dict, negative_dict
        )
        scores.append(total_score)
        avg_scores.append(avg_score)
        labels.append(get_sentiment_label(avg_score))

    df['sentiment_score'] = avg_scores  # Use avg score as feature (per PRD §14.2)
    df['sentiment_label'] = labels
    df['raw_sentiment_score'] = scores  # Keep raw score for reference

    # Save updated processed news
    save_csv(df, filepath)

    # Print distribution
    label_counts = df['sentiment_label'].value_counts()
    print(f"\n[INFO] Sentiment distribution:")
    for label, count in label_counts.items():
        print(f"  {label}: {count} ({count/len(df)*100:.1f}%)")

    # Generate daily sentiment aggregation
    aggregate_daily_sentiment(df)

    return df


def aggregate_daily_sentiment(df):
    """
    Aggregate sentiment scores by date and stock.
    Saves: {STOCK}_daily_sentiment.csv

    Schema: date, stock, total_news, avg_sentiment_score, total_sentiment_score,
            positive_count, neutral_count, negative_count
    """
    if df is None or df.empty:
        return

    print(f"\n[INFO] Aggregating daily sentiment...")

    for stock_name in STOCK_NAMES:
        stock_df = df[df['stock'] == stock_name].copy()

        if stock_df.empty:
            print(f"[WARNING] No news for {stock_name}")
            continue

        # Group by date
        daily = stock_df.groupby('date').agg(
            total_news=('sentiment_score', 'count'),
            avg_sentiment_score=('sentiment_score', 'mean'),
            total_sentiment_score=('sentiment_score', 'sum'),
            positive_count=('sentiment_label', lambda x: (x == 'positif').sum()),
            neutral_count=('sentiment_label', lambda x: (x == 'netral').sum()),
            negative_count=('sentiment_label', lambda x: (x == 'negatif').sum()),
        ).reset_index()

        daily['stock'] = stock_name

        # Reorder columns
        daily = daily[['date', 'stock', 'total_news', 'avg_sentiment_score',
                        'total_sentiment_score', 'positive_count',
                        'neutral_count', 'negative_count']]

        # Sort by date
        daily = daily.sort_values('date').reset_index(drop=True)

        # Save
        filepath = os.path.join(PROCESSED_SENTIMENT_DIR, f'{stock_name}_daily_sentiment.csv')
        save_csv(daily, filepath)

        print(f"[INFO] {stock_name}: {len(daily)} trading days with news")

    print("\n[INFO] Daily sentiment aggregation complete!")


if __name__ == '__main__':
    score_all_news()
