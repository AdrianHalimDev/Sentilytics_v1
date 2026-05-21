"""
Sentilytics — Test: Sequence Builder
Unit tests for time-series data preparation.
"""

import pytest
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing.sequence_builder import chronological_split, create_sequences


class TestChronologicalSplit:
    """Tests for chronological train/test split."""

    def test_80_20_split(self):
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'date': dates.strftime('%Y-%m-%d'),
            'close': np.random.randn(100),
        })

        train, test, split_idx = chronological_split(df, 0.8)

        assert len(train) == 80
        assert len(test) == 20
        assert split_idx == 80

    def test_no_shuffle(self):
        """Ensure split preserves chronological order."""
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        df = pd.DataFrame({
            'date': dates.strftime('%Y-%m-%d'),
            'value': range(50),
        })

        train, test, _ = chronological_split(df, 0.8)

        # Train should have earlier dates
        assert train['date'].iloc[-1] < test['date'].iloc[0]

    def test_train_before_test(self):
        """Train data must come before test data chronologically."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'date': dates.strftime('%Y-%m-%d'),
            'close': np.random.randn(100),
        })

        train, test, _ = chronological_split(df, 0.8)

        train_last = pd.to_datetime(train['date'].iloc[-1])
        test_first = pd.to_datetime(test['date'].iloc[0])
        assert train_last < test_first


class TestCreateSequences:
    """Tests for sliding window sequence creation."""

    def test_sequence_shape(self):
        data = np.random.randn(50, 6)  # 5 features + 1 target
        X, y = create_sequences(data, window_size=10)

        assert X.shape[0] == 40  # 50 - 10
        assert X.shape[1] == 10  # window_size
        assert X.shape[2] == 5   # features (exclude target)
        assert y.shape[0] == 40

    def test_sequence_values(self):
        """Check that sequences contain correct values."""
        data = np.arange(20).reshape(10, 2)  # 10 samples, 1 feature + 1 target
        X, y = create_sequences(data, window_size=3)

        # First sequence should be rows 0-2, feature column
        np.testing.assert_array_equal(X[0, :, 0], [0, 2, 4])
        # First target should be row 3, target column
        assert y[0] == 7  # data[3, 1]

    def test_window_size_1(self):
        data = np.random.randn(10, 3)
        X, y = create_sequences(data, window_size=1)

        assert X.shape[0] == 9
        assert X.shape[1] == 1

    def test_insufficient_data(self):
        """If data length equals window size, no sequences produced."""
        data = np.random.randn(5, 3)
        X, y = create_sequences(data, window_size=5)

        assert X.shape[0] == 0
