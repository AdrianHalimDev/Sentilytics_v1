"""
Sentilytics — Test: Sentiment Scoring
Unit tests for sentiment scoring with InSet lexicon.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sentiment.sentiment_scorer import (
    calculate_sentiment_score, get_sentiment_label
)


class TestSentimentScore:
    """Tests for sentiment score calculation."""

    def test_positive_score(self):
        positive_dict = {'bagus': 4, 'naik': 3, 'untung': 5}
        negative_dict = {'turun': -3, 'rugi': -4}

        total, avg, count = calculate_sentiment_score(
            "bagus naik untung", positive_dict, negative_dict
        )
        assert total > 0
        assert avg > 0
        assert count == 3

    def test_negative_score(self):
        positive_dict = {'bagus': 4}
        negative_dict = {'turun': -3, 'rugi': -4}

        total, avg, count = calculate_sentiment_score(
            "turun rugi", positive_dict, negative_dict
        )
        assert total < 0
        assert avg < 0
        assert count == 2

    def test_mixed_score(self):
        positive_dict = {'bagus': 3}
        negative_dict = {'turun': -5}

        total, avg, count = calculate_sentiment_score(
            "bagus turun", positive_dict, negative_dict
        )
        assert total == -2  # 3 + (-5)
        assert count == 2

    def test_no_match(self):
        positive_dict = {'bagus': 4}
        negative_dict = {'turun': -3}

        total, avg, count = calculate_sentiment_score(
            "kata tidak ada di kamus", positive_dict, negative_dict
        )
        assert total == 0
        assert avg == 0.0
        assert count == 0

    def test_empty_text(self):
        total, avg, count = calculate_sentiment_score("", {}, {})
        assert total == 0
        assert avg == 0.0
        assert count == 0

    def test_none_text(self):
        total, avg, count = calculate_sentiment_score(None, {}, {})
        assert total == 0


class TestSentimentLabel:
    """Tests for sentiment label assignment."""

    def test_positive_label(self):
        assert get_sentiment_label(2.5) == 'positif'

    def test_negative_label(self):
        assert get_sentiment_label(-1.3) == 'negatif'

    def test_neutral_label(self):
        assert get_sentiment_label(0) == 'netral'

    def test_zero_is_neutral(self):
        assert get_sentiment_label(0.0) == 'netral'
