"""
Sentilytics — InSet Lexicon Loader
Loads the InSet (Indonesia Sentiment Lexicon) positive and negative word lists.
Auto-downloads from GitHub if not present locally.

Usage:
    python -m src.sentiment.inset_loader
"""

import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import EXTERNAL_LEXICON_DIR
from src.utils.file_utils import ensure_dir

# InSet Lexicon GitHub URLs
INSET_POSITIVE_URL = "https://raw.githubusercontent.com/fajri91/InSet/master/positive.tsv"
INSET_NEGATIVE_URL = "https://raw.githubusercontent.com/fajri91/InSet/master/negative.tsv"


def download_inset_lexicon():
    """
    Download InSet lexicon files from GitHub if not present locally.
    Files: positive.tsv, negative.tsv
    """
    ensure_dir(EXTERNAL_LEXICON_DIR)

    files = [
        ('positive.tsv', INSET_POSITIVE_URL),
        ('negative.tsv', INSET_NEGATIVE_URL),
    ]

    for filename, url in files:
        filepath = os.path.join(EXTERNAL_LEXICON_DIR, filename)

        if os.path.exists(filepath):
            print(f"[INFO] InSet lexicon already exists: {filename}")
            continue

        print(f"[INFO] Downloading InSet lexicon: {filename}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"[INFO] Downloaded: {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to download {filename}: {e}")


def load_lexicon():
    """
    Load InSet lexicon files and return positive and negative dictionaries.

    Returns:
        tuple: (positive_dict, negative_dict)
        Each dict maps word → weight (int)
    """
    positive_dict = {}
    negative_dict = {}

    # Load positive lexicon
    pos_path = os.path.join(EXTERNAL_LEXICON_DIR, 'positive.tsv')
    if os.path.exists(pos_path):
        try:
            with open(pos_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        word = parts[0].strip().lower()
                        try:
                            weight = int(parts[1].strip())
                        except ValueError:
                            weight = 1
                        positive_dict[word] = weight
            print(f"[INFO] Loaded {len(positive_dict)} positive words")
        except Exception as e:
            print(f"[ERROR] Loading positive lexicon: {e}")
    else:
        print(f"[WARNING] Positive lexicon not found: {pos_path}")

    # Load negative lexicon
    neg_path = os.path.join(EXTERNAL_LEXICON_DIR, 'negative.tsv')
    if os.path.exists(neg_path):
        try:
            with open(neg_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        word = parts[0].strip().lower()
                        try:
                            weight = int(parts[1].strip())
                        except ValueError:
                            weight = -1
                        negative_dict[word] = weight
            print(f"[INFO] Loaded {len(negative_dict)} negative words")
        except Exception as e:
            print(f"[ERROR] Loading negative lexicon: {e}")
    else:
        print(f"[WARNING] Negative lexicon not found: {neg_path}")

    return positive_dict, negative_dict


if __name__ == '__main__':
    download_inset_lexicon()
    pos, neg = load_lexicon()
    print(f"\nTotal lexicon: {len(pos)} positive, {len(neg)} negative words")
