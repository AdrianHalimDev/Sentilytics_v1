"""
Sentilytics — Master Pipeline Runner
Runs the complete offline data science pipeline end-to-end.

Steps:
1. Download stock data (yfinance)
2. Preprocess stock data
3. Scrape news (CNBC + Kontan)
4. Merge & deduplicate news
5. Preprocess text (Sastrawi)
6. Score sentiment (InSet Lexicon)
7. Create fusion datasets
8. Train Baseline LSTM
9. Train Hybrid LSTM
10. Evaluate models
11. Generate plots
12. Generate H+7 forecasts

Usage:
    python run_pipeline.py
    python run_pipeline.py --skip-scraping  (skip news scraping if CSV already exists)
"""

import argparse
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.config import ensure_directories


def main():
    parser = argparse.ArgumentParser(description='Sentilytics Pipeline Runner')
    parser.add_argument('--skip-scraping', action='store_true',
                        help='Skip news scraping (use existing CSV)')
    parser.add_argument('--skip-training', action='store_true',
                        help='Skip model training (use existing models)')
    args = parser.parse_args()

    print("=" * 60)
    print("  Sentilytics — Full Pipeline")
    print("=" * 60)

    # Step 0: Create directories
    print("\n[STEP 0] Creating directories...")
    ensure_directories()

    # Step 1: Download stock data
    print("\n[STEP 1] Downloading stock data...")
    from src.data_collection.stock_downloader import run_stock_download
    run_stock_download()

    # Step 2: Preprocess stock data
    print("\n[STEP 2] Preprocessing stock data...")
    from src.preprocessing.stock_preprocessing import run_stock_preprocessing
    run_stock_preprocessing()

    # Step 3-4: News scraping & merging
    if not args.skip_scraping:
        print("\n[STEP 3] Scraping CNBC Indonesia...")
        from src.data_collection.cnbc_scraper import run_cnbc_scraper
        run_cnbc_scraper()

        print("\n[STEP 3b] Scraping Kontan...")
        from src.data_collection.kontan_scraper import run_kontan_scraper
        run_kontan_scraper()

        print("\n[STEP 4] Merging & deduplicating news...")
        from src.data_collection.news_merger import merge_news
        merge_news()
    else:
        print("\n[STEP 3-4] Skipping scraping (using existing CSV)")

    # Step 5: Text preprocessing
    print("\n[STEP 5] Preprocessing text...")
    from src.preprocessing.text_preprocessing import preprocess_news
    preprocess_news()

    # Step 6: Sentiment scoring
    print("\n[STEP 6] Scoring sentiment...")
    from src.sentiment.sentiment_scorer import score_all_news
    score_all_news()

    # Step 7: Data fusion
    print("\n[STEP 7] Creating fusion datasets...")
    from src.preprocessing.data_fusion import run_data_fusion
    run_data_fusion()

    # Steps 8-9: Model training
    if not args.skip_training:
        print("\n[STEP 8] Training Baseline LSTM...")
        from src.modeling.train_baseline import run_baseline_training
        run_baseline_training()

        print("\n[STEP 9] Training Hybrid LSTM...")
        from src.modeling.train_hybrid import run_hybrid_training
        run_hybrid_training()
    else:
        print("\n[STEP 8-9] Skipping training (using existing models)")

    # Step 10: Evaluation
    print("\n[STEP 10] Evaluating models...")
    from src.evaluation.metrics import run_evaluation
    run_evaluation()

    # Step 11: Generate plots
    print("\n[STEP 11] Generating plots...")
    from src.evaluation.plots import run_plots
    run_plots()

    # Step 12: Generate forecasts
    print("\n[STEP 12] Generating H+7 forecasts...")
    from src.modeling.forecast import run_forecast
    run_forecast()

    print("\n" + "=" * 60)
    print("  Sentilytics Pipeline Complete!")
    print("=" * 60)
    print("\nYou can now start the dashboard:")
    print("  python run.py")
    print("\nThen open http://127.0.0.1:5000 in your browser.")


if __name__ == '__main__':
    main()
