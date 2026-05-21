"""
Sentilytics — Evaluation Plots
Generates actual vs predicted plots using matplotlib.
Saves figures to results/figures/.

Usage:
    python -m src.evaluation.plots
"""

import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import STOCK_NAMES, RESULTS_PREDICTIONS_DIR, RESULTS_FIGURES_DIR
from src.utils.file_utils import load_csv, ensure_dir


def plot_actual_vs_predicted(stock_name, model_type):
    """
    Create actual vs predicted line chart for a given model.

    Args:
        stock_name: 'BBCA' or 'BBRI'
        model_type: 'baseline' or 'hybrid'
    """
    filename = f"{stock_name}_{model_type}_predictions.csv"
    filepath = os.path.join(RESULTS_PREDICTIONS_DIR, filename)
    df = load_csv(filepath)

    if df is None or df.empty:
        print(f"[WARNING] No predictions to plot: {filename}")
        return

    model_label = 'Baseline LSTM' if model_type == 'baseline' else 'Hybrid LSTM'

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(range(len(df)), df['actual_close'], label='Actual Close',
            color='#4361ee', linewidth=2, alpha=0.9)
    ax.plot(range(len(df)), df['predicted_close'], label='Predicted Close',
            color='#fd7e14', linewidth=2, linestyle='--', alpha=0.9)

    ax.set_title(f'{stock_name} — {model_label}: Actual vs Predicted Close Price',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Trading Day Index (Test Set)', fontsize=11)
    ax.set_ylabel('Close Price (IDR)', fontsize=11)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save figure
    ensure_dir(RESULTS_FIGURES_DIR)
    fig_path = os.path.join(RESULTS_FIGURES_DIR, f"{stock_name}_{model_type}_actual_vs_predicted.png")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"[INFO] Plot saved: {fig_path}")


def plot_comparison(stock_name):
    """
    Create baseline vs hybrid comparison plot for a given stock.

    Args:
        stock_name: 'BBCA' or 'BBRI'
    """
    baseline_path = os.path.join(RESULTS_PREDICTIONS_DIR, f"{stock_name}_baseline_predictions.csv")
    hybrid_path = os.path.join(RESULTS_PREDICTIONS_DIR, f"{stock_name}_hybrid_predictions.csv")

    baseline_df = load_csv(baseline_path)
    hybrid_df = load_csv(hybrid_path)

    if baseline_df is None or hybrid_df is None:
        print(f"[WARNING] Cannot create comparison plot for {stock_name}")
        return

    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Baseline
    axes[0].plot(range(len(baseline_df)), baseline_df['actual_close'],
                 label='Actual', color='#4361ee', linewidth=2)
    axes[0].plot(range(len(baseline_df)), baseline_df['predicted_close'],
                 label='Predicted', color='#fd7e14', linewidth=2, linestyle='--')
    axes[0].set_title(f'{stock_name} — Baseline LSTM', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Trading Day Index')
    axes[0].set_ylabel('Close Price (IDR)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Hybrid
    axes[1].plot(range(len(hybrid_df)), hybrid_df['actual_close'],
                 label='Actual', color='#4361ee', linewidth=2)
    axes[1].plot(range(len(hybrid_df)), hybrid_df['predicted_close'],
                 label='Predicted', color='#7b2ff7', linewidth=2, linestyle='--')
    axes[1].set_title(f'{stock_name} — Hybrid LSTM', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Trading Day Index')
    axes[1].set_ylabel('Close Price (IDR)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(f'{stock_name}: Baseline vs Hybrid LSTM Comparison',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    fig_path = os.path.join(RESULTS_FIGURES_DIR, f"{stock_name}_comparison.png")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"[INFO] Comparison plot saved: {fig_path}")


def run_plots():
    """Generate all evaluation plots."""
    ensure_dir(RESULTS_FIGURES_DIR)

    for stock_name in STOCK_NAMES:
        for model_type in ['baseline', 'hybrid']:
            plot_actual_vs_predicted(stock_name, model_type)
        plot_comparison(stock_name)

    print("\n[INFO] All plots generated!")


if __name__ == '__main__':
    run_plots()
