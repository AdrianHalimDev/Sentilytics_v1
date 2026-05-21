"""
Sentilytics — Test: Evaluation Metrics
Unit tests for RMSE, MAE, and MAPE calculation.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evaluation.metrics import calculate_rmse, calculate_mae, calculate_mape


class TestRMSE:
    """Tests for Root Mean Squared Error."""

    def test_perfect_prediction(self):
        actual = np.array([100, 200, 300])
        predicted = np.array([100, 200, 300])
        assert calculate_rmse(actual, predicted) == 0.0

    def test_known_rmse(self):
        actual = np.array([100, 200, 300])
        predicted = np.array([110, 190, 310])
        rmse = calculate_rmse(actual, predicted)
        assert rmse == pytest.approx(10.0, abs=0.01)

    def test_single_value(self):
        actual = np.array([100])
        predicted = np.array([110])
        assert calculate_rmse(actual, predicted) == pytest.approx(10.0, abs=0.01)


class TestMAE:
    """Tests for Mean Absolute Error."""

    def test_perfect_prediction(self):
        actual = np.array([100, 200, 300])
        predicted = np.array([100, 200, 300])
        assert calculate_mae(actual, predicted) == 0.0

    def test_known_mae(self):
        actual = np.array([100, 200, 300])
        predicted = np.array([110, 190, 310])
        mae = calculate_mae(actual, predicted)
        assert mae == pytest.approx(10.0, abs=0.01)

    def test_asymmetric_errors(self):
        actual = np.array([100, 200])
        predicted = np.array([90, 230])
        mae = calculate_mae(actual, predicted)
        assert mae == pytest.approx(20.0, abs=0.01)


class TestMAPE:
    """Tests for Mean Absolute Percentage Error."""

    def test_perfect_prediction(self):
        actual = np.array([100, 200, 300])
        predicted = np.array([100, 200, 300])
        assert calculate_mape(actual, predicted) == 0.0

    def test_known_mape(self):
        actual = np.array([100, 200])
        predicted = np.array([110, 210])
        mape = calculate_mape(actual, predicted)
        # (10/100 + 10/200) / 2 * 100 = (0.1 + 0.05) / 2 * 100 = 7.5
        assert mape == pytest.approx(7.5, abs=0.1)

    def test_zero_actual_handling(self):
        actual = np.array([0, 100])
        predicted = np.array([10, 110])
        # Should handle zero actual gracefully
        mape = calculate_mape(actual, predicted)
        assert mape >= 0
