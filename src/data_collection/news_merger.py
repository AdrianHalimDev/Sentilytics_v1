"""
Sentilytics — News Merger
Merges and deduplicates news from all scrapers (CNBC Indonesia + Kontan).
Also provides fallback CSV generation if scraping yields insufficient data.

Usage:
    python -m src.data_collection.news_merger
"""

import os
import sys
import re
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import RAW_NEWS_DIR, DATE_START, DATE_END, KEYWORDS_BBCA, KEYWORDS_BBRI
from src.utils.file_utils import save_csv, load_csv, ensure_dir


def normalize_title(title):
    """Normalize title for deduplication: lowercase, strip, remove extra whitespace."""
    if not isinstance(title, str):
        return ''
    title = title.lower().strip()
    title = re.sub(r'\s+', ' ', title)
    title = re.sub(r'[^\w\s]', '', title)
    return title


def map_sector_news(df):
    """
    Map sector news to specific stocks based on content.
    Sector news gets duplicated to both BBCA and BBRI.
    """
    sector_mask = df['stock'] == 'SECTOR'
    sector_news = df[sector_mask].copy()

    if sector_news.empty:
        return df[~sector_mask]

    # Duplicate sector news for both stocks
    bbca_sector = sector_news.copy()
    bbca_sector['stock'] = 'BBCA'
    bbca_sector['is_sector_news'] = 1

    bbri_sector = sector_news.copy()
    bbri_sector['stock'] = 'BBRI'
    bbri_sector['is_sector_news'] = 1

    # Combine specific news + mapped sector news
    specific_news = df[~sector_mask].copy()
    result = pd.concat([specific_news, bbca_sector, bbri_sector], ignore_index=True)

    return result


def deduplicate_news(df):
    """
    Remove duplicate news articles.
    Rules:
    1. Duplicate URLs removed
    2. Duplicate normalized titles removed
    3. Same article from different keywords kept once
    """
    before_count = len(df)

    # Deduplicate by URL
    df = df.drop_duplicates(subset=['url'], keep='first')
    after_url = len(df)

    # Deduplicate by normalized title + stock
    df['_norm_title'] = df['title'].apply(normalize_title)
    df = df.drop_duplicates(subset=['_norm_title', 'stock'], keep='first')
    df = df.drop(columns=['_norm_title'])
    after_title = len(df)

    print(f"[INFO] Deduplication: {before_count} → {after_url} (URL) → {after_title} (title)")

    return df.reset_index(drop=True)


def filter_date_range(df, start_date, end_date):
    """Filter news to the specified date range."""
    if 'date' not in df.columns:
        return df

    # Try to parse dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Keep rows with valid dates in range
    valid_mask = df['date'].notna()
    date_mask = (df['date'] >= start_date) & (df['date'] <= end_date)

    # Also keep rows with unparseable dates (we don't want to lose them)
    result = df[valid_mask & date_mask].copy()

    # Format date back to string
    result['date'] = result['date'].dt.strftime('%Y-%m-%d')

    dropped = len(df) - len(result)
    if dropped > 0:
        print(f"[INFO] Filtered {dropped} articles outside date range")

    return result.reset_index(drop=True)


def create_fallback_csv():
    """
    Create a fallback CSV with the correct schema if scraping failed.
    This allows the pipeline to continue with manual data entry.
    """
    print("[INFO] Creating fallback news CSV template...")

    fallback_data = {
        'date': [],
        'published_at': [],
        'source': [],
        'stock': [],
        'keyword': [],
        'title': [],
        'summary': [],
        'url': [],
        'is_sector_news': [],
    }

    df = pd.DataFrame(fallback_data)
    filepath = os.path.join(RAW_NEWS_DIR, 'news_raw_template.csv')
    save_csv(df, filepath)
    print(f"[INFO] Fallback template saved: {filepath}")
    print("[INFO] You can manually add news data following this schema.")

    return df


def merge_news():
    """Merge news from all scraper outputs."""
    ensure_dir(RAW_NEWS_DIR)

    dfs = []
    scraper_files = ['cnbc_raw.csv', 'kontan_raw.csv']

    for filename in scraper_files:
        filepath = os.path.join(RAW_NEWS_DIR, filename)
        df = load_csv(filepath)
        if df is not None and not df.empty:
            dfs.append(df)
            print(f"[INFO] Loaded {len(df)} articles from {filename}")

    if not dfs:
        print("[WARNING] No scraper output found. Creating fallback CSV.")
        create_fallback_csv()

        # Create an empty news_raw.csv with correct schema
        empty_df = pd.DataFrame(columns=[
            'date', 'published_at', 'source', 'stock', 'keyword',
            'title', 'summary', 'url', 'is_sector_news'
        ])
        filepath = os.path.join(RAW_NEWS_DIR, 'news_raw.csv')
        save_csv(empty_df, filepath)
        return empty_df

    # Merge all sources
    merged = pd.concat(dfs, ignore_index=True)
    print(f"\n[INFO] Total articles before processing: {len(merged)}")

    # Map sector news to specific stocks
    merged = map_sector_news(merged)
    print(f"[INFO] After sector mapping: {len(merged)}")

    # Filter date range
    merged = filter_date_range(merged, DATE_START, DATE_END)
    print(f"[INFO] After date filter: {len(merged)}")

    # Deduplicate
    merged = deduplicate_news(merged)

    # Sort by date
    merged = merged.sort_values('date').reset_index(drop=True)

    # Save merged result
    filepath = os.path.join(RAW_NEWS_DIR, 'news_raw.csv')
    save_csv(merged, filepath)

    print(f"\n[INFO] News merge complete: {len(merged)} final articles")

    return merged


if __name__ == '__main__':
    merge_news()
