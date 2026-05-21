"""
Sentilytics — LSTM Model Builder
Creates LSTM model architecture for stock price prediction.

Architecture (minimal):
    Input → LSTM(64) → Dropout(0.2) → Dense(1)

This module only builds the model structure.
Training is handled by train_baseline.py and train_hybrid.py.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import LSTM_UNITS, DROPOUT, DENSE_OUTPUT, OPTIMIZER, LOSS


def build_lstm_model(input_shape, lstm_units=None, dropout=None, name='lstm_model'):
    """
    Build LSTM model for stock price prediction.

    Args:
        input_shape: tuple (window_size, n_features)
        lstm_units: Number of LSTM units (default from config)
        dropout: Dropout rate (default from config)
        name: Model name

    Returns:
        Compiled Keras Sequential model
    """
    # Import TensorFlow/Keras here to avoid loading at import time
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Input

    units = lstm_units or LSTM_UNITS
    drop = dropout or DROPOUT

    model = Sequential(name=name)
    model.add(Input(shape=input_shape))
    model.add(LSTM(units=units))
    model.add(Dropout(drop))
    model.add(Dense(DENSE_OUTPUT))

    model.compile(optimizer=OPTIMIZER, loss=LOSS)

    print(f"\n[INFO] Model '{name}' built:")
    print(f"  Input shape: {input_shape}")
    print(f"  LSTM units: {units}")
    print(f"  Dropout: {drop}")
    print(f"  Output: {DENSE_OUTPUT}")
    model.summary()

    return model
