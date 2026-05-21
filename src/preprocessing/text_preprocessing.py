"""
Sentilytics — Text Preprocessing
Indonesian text preprocessing pipeline for news articles.
Pipeline: combine title+summary → case folding → cleaning → tokenize →
          stopword removal (Sastrawi) → stemming (Sastrawi).

Usage:
    python -m src.preprocessing.text_preprocessing
"""

import os
import sys
import re
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import RAW_NEWS_DIR, PROCESSED_SENTIMENT_DIR
from src.utils.file_utils import save_csv, load_csv, ensure_dir

# Sastrawi imports
try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

    # Initialize Sastrawi
    _stemmer_factory = StemmerFactory()
    _stemmer = _stemmer_factory.create_stemmer()

    _stopword_factory = StopWordRemoverFactory()
    _stopwords = set(_stopword_factory.get_stop_words())

    SASTRAWI_AVAILABLE = True
    print("[INFO] Sastrawi loaded successfully")
except (ImportError, Exception) as e:
    SASTRAWI_AVAILABLE = False
    _stemmer = None
    _stopwords = set()
    print(f"[WARNING] Sastrawi not available: {e}. Using basic preprocessing.")


def combine_text(title, summary):
    """Combine title and summary into a single text."""
    parts = []
    if isinstance(title, str) and title.strip():
        parts.append(title.strip())
    if isinstance(summary, str) and summary.strip():
        parts.append(summary.strip())
    return ' '.join(parts)


def case_folding(text):
    """Convert text to lowercase."""
    if not isinstance(text, str):
        return ''
    return text.lower()


def clean_text(text):
    """
    Clean text by removing:
    - URLs
    - Email addresses
    - HTML tags
    - Non-relevant numbers (standalone)
    - Special characters and symbols
    - Emojis
    - Extra whitespace
    """
    if not isinstance(text, str):
        return ''

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove email
    text = re.sub(r'\S+@\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove special characters and numbers but keep Indonesian letters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def tokenize(text):
    """Simple whitespace tokenization."""
    if not isinstance(text, str):
        return []
    tokens = text.split()
    # Filter very short tokens
    tokens = [t for t in tokens if len(t) > 1]
    return tokens


def remove_stopwords(tokens):
    """Remove Indonesian stopwords using Sastrawi stopword list."""
    if not SASTRAWI_AVAILABLE or not _stopwords:
        return tokens
    return [t for t in tokens if t not in _stopwords]


def stem_tokens(tokens):
    """Stem tokens using Sastrawi stemmer."""
    if not SASTRAWI_AVAILABLE or _stemmer is None:
        return tokens
    return [_stemmer.stem(t) for t in tokens]


def preprocess_single(text):
    """
    Full preprocessing pipeline for a single text.

    Returns:
        dict with clean_text, tokens, stemmed_text
    """
    # Case folding
    text = case_folding(text)

    # Clean
    clean = clean_text(text)

    # Tokenize
    tokens = tokenize(clean)

    # Remove stopwords
    tokens_no_sw = remove_stopwords(tokens)

    # Stem
    stemmed = stem_tokens(tokens_no_sw)

    return {
        'clean_text': clean,
        'tokens': ' '.join(tokens_no_sw),
        'stemmed_text': ' '.join(stemmed),
    }


def preprocess_news():
    """
    Preprocess all news articles.
    Reads from news_raw.csv, applies full NLP pipeline, saves to news_processed.csv.
    """
    ensure_dir(PROCESSED_SENTIMENT_DIR)

    # Load raw news
    raw_path = os.path.join(RAW_NEWS_DIR, 'news_raw.csv')
    df = load_csv(raw_path)

    if df is None or df.empty:
        print("[WARNING] No news data to preprocess")
        return None

    print(f"\n[INFO] Preprocessing {len(df)} news articles...")

    # Combine title + summary
    df['raw_text'] = df.apply(
        lambda row: combine_text(row.get('title', ''), row.get('summary', '')),
        axis=1
    )

    # Apply preprocessing pipeline
    results = []
    total = len(df)

    for idx, row in df.iterrows():
        if idx % 50 == 0:
            print(f"[INFO] Processing article {idx+1}/{total}...")

        result = preprocess_single(row['raw_text'])
        results.append(result)

    # Add results to DataFrame
    result_df = pd.DataFrame(results)
    df['clean_text'] = result_df['clean_text']
    df['tokens'] = result_df['tokens']
    df['stemmed_text'] = result_df['stemmed_text']

    # Select output columns (per PRD schema)
    output_cols = [
        'date', 'published_at', 'source', 'stock', 'title', 'summary',
        'raw_text', 'clean_text', 'tokens', 'stemmed_text', 'url'
    ]
    # Keep only existing columns
    output_cols = [c for c in output_cols if c in df.columns]
    df = df[output_cols]

    # Save
    filepath = os.path.join(PROCESSED_SENTIMENT_DIR, 'news_processed.csv')
    save_csv(df, filepath)

    print(f"\n[INFO] Text preprocessing complete: {len(df)} articles processed")

    return df


if __name__ == '__main__':
    preprocess_news()
