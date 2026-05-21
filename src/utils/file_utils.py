"""
Sentilytics — File Utilities
Helper functions for file I/O operations.
"""

import os
import json
import pandas as pd


def ensure_dir(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def save_csv(df, filepath, index=False):
    """Save DataFrame to CSV, creating directories as needed."""
    ensure_dir(os.path.dirname(filepath))
    df.to_csv(filepath, index=index, encoding='utf-8')
    print(f"[INFO] Saved CSV: {filepath} ({len(df)} rows)")


def load_csv(filepath):
    """Load CSV file as DataFrame. Returns None if file doesn't exist."""
    if not os.path.exists(filepath):
        print(f"[WARNING] File not found: {filepath}")
        return None
    df = pd.read_csv(filepath, encoding='utf-8')
    print(f"[INFO] Loaded CSV: {filepath} ({len(df)} rows)")
    return df


def save_json(data, filepath):
    """Save data to JSON file."""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    print(f"[INFO] Saved JSON: {filepath}")


def load_json(filepath):
    """Load JSON file. Returns None if file doesn't exist."""
    if not os.path.exists(filepath):
        print(f"[WARNING] File not found: {filepath}")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"[INFO] Loaded JSON: {filepath}")
    return data


def file_exists(filepath):
    """Check if a file exists."""
    return os.path.exists(filepath)


def get_file_size(filepath):
    """Get file size in bytes. Returns 0 if file doesn't exist."""
    if not os.path.exists(filepath):
        return 0
    return os.path.getsize(filepath)
