"""
Sentilytics — Kontan Scraper
Scrapes news articles from Kontan.co.id search results.

Target: https://www.kontan.co.id/search/?search=<keyword>
Extracts: date, source, title, summary, URL, stock mapping.

Usage:
    python -m src.data_collection.kontan_scraper
"""

import os
import sys
import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import (
    KEYWORDS_BBCA, KEYWORDS_BBRI, KEYWORDS_SECTOR,
    KEYWORD_STOCK_MAP, DATE_START, DATE_END, RAW_NEWS_DIR
)
from src.utils.file_utils import save_csv, ensure_dir

# Kontan search URL
KONTAN_SEARCH_URL = "https://www.kontan.co.id/search/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
}

# Indonesian month names for date parsing
MONTH_MAP = {
    'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
    'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
    'september': '09', 'oktober': '10', 'november': '11', 'desember': '12',
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
    'sep': '09', 'okt': '10', 'nov': '11', 'des': '12',
}


def parse_kontan_date(date_str):
    """Parse Kontan date format to YYYY-MM-DD."""
    if not date_str:
        return None
    try:
        date_str = date_str.strip().lower()

        # Try format: "Senin, 15 Januari 2024 / 10:30 WIB"
        match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
        if match:
            day = match.group(1).zfill(2)
            month_name = match.group(2).lower()
            year = match.group(3)
            month = MONTH_MAP.get(month_name, '')
            if month:
                return f"{year}-{month}-{day}"

        # Try dd/mm/yyyy
        match = re.search(r'(\d{2})/(\d{2})/(\d{4})', date_str)
        if match:
            day, month, year = match.groups()
            return f"{year}-{month}-{day}"

        # Try yyyy-mm-dd
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_str)
        if match:
            return match.group(0)

    except Exception:
        pass
    return None


def scrape_kontan_search(keyword, max_pages=5):
    """
    Scrape Kontan search results for a given keyword.

    Args:
        keyword: Search keyword
        max_pages: Maximum pages to scrape

    Returns:
        List of article dicts
    """
    articles = []
    stock = KEYWORD_STOCK_MAP.get(keyword, 'SECTOR')

    for page in range(1, max_pages + 1):
        try:
            params = {'search': keyword, 'page': page}
            response = requests.get(KONTAN_SEARCH_URL, params=params,
                                    headers=HEADERS, timeout=15)

            if response.status_code != 200:
                print(f"[WARNING] Kontan page {page} returned {response.status_code} for '{keyword}'")
                break

            soup = BeautifulSoup(response.text, 'lxml')

            # Find article containers
            article_elements = soup.select('.list-berita li') or \
                               soup.select('.news-list li') or \
                               soup.select('.result-content .card')

            if not article_elements:
                # Alternative selectors
                article_elements = soup.select('article') or soup.select('.media')

            if not article_elements:
                print(f"[INFO] No more articles found on page {page} for '{keyword}'")
                break

            for article in article_elements:
                try:
                    # Extract title and URL
                    title_el = article.select_one('h1 a') or article.select_one('h2 a') or \
                               article.select_one('h3 a') or article.select_one('.news-title a') or \
                               article.select_one('a')

                    if not title_el:
                        continue

                    title = title_el.get_text(strip=True)
                    url = title_el.get('href', '')

                    if not url.startswith('http'):
                        url = 'https://www.kontan.co.id' + url

                    # Skip non-article links
                    if not title or len(title) < 10:
                        continue

                    # Extract date
                    date_el = article.select_one('.date') or article.select_one('time') or \
                              article.select_one('.font-gray')
                    date_str = date_el.get_text(strip=True) if date_el else ''
                    parsed_date = parse_kontan_date(date_str)

                    # Extract summary
                    summary_el = article.select_one('p') or article.select_one('.desc')
                    summary = summary_el.get_text(strip=True) if summary_el else ''

                    articles.append({
                        'date': parsed_date or '',
                        'published_at': date_str,
                        'source': 'Kontan',
                        'stock': stock,
                        'keyword': keyword,
                        'title': title,
                        'summary': summary,
                        'url': url,
                        'is_sector_news': 1 if stock == 'SECTOR' else 0,
                    })

                except Exception as e:
                    continue

            # Polite delay
            time.sleep(1.5)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Kontan request failed for '{keyword}' page {page}: {e}")
            break

    return articles


def run_kontan_scraper():
    """Run Kontan scraper for all keywords."""
    ensure_dir(RAW_NEWS_DIR)

    all_keywords = KEYWORDS_BBCA + KEYWORDS_BBRI + KEYWORDS_SECTOR
    all_articles = []

    print(f"\n[INFO] Starting Kontan scraper...")
    print(f"[INFO] Keywords: {len(all_keywords)}")

    for keyword in all_keywords:
        print(f"\n[INFO] Scraping Kontan for: '{keyword}'")
        articles = scrape_kontan_search(keyword, max_pages=5)
        print(f"[INFO] Found {len(articles)} articles for '{keyword}'")
        all_articles.extend(articles)
        time.sleep(2)

    if all_articles:
        df = pd.DataFrame(all_articles)
        filepath = os.path.join(RAW_NEWS_DIR, 'kontan_raw.csv')
        save_csv(df, filepath)
        print(f"\n[INFO] Kontan scraping complete: {len(df)} total articles")
    else:
        print("[WARNING] No articles scraped from Kontan")

    return all_articles


if __name__ == '__main__':
    run_kontan_scraper()
