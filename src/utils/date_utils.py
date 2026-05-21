"""
Sentilytics — Date Utilities
Helper functions for date parsing and validation.
"""

from datetime import datetime


def parse_date(date_str):
    """Parse date string in various formats to datetime object."""
    formats = [
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date: {date_str}")


def format_date(dt, fmt='%Y-%m-%d'):
    """Format datetime object to string."""
    if isinstance(dt, str):
        dt = parse_date(dt)
    return dt.strftime(fmt)


def is_within_range(date_str, start_str, end_str):
    """Check if a date is within a given range (inclusive)."""
    d = parse_date(date_str)
    s = parse_date(start_str)
    e = parse_date(end_str)
    return s <= d <= e
