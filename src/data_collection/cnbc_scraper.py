"""
Sentilytics — CNBC Indonesia Scraper
Scrapes news articles from CNBC Indonesia search results.

Target: https://www.cnbcindonesia.com/search?query=<keyword>
Extracts: date, source, title, summary, URL, stock mapping.

Usage:
    python -m src.data_collection.cnbc_scraper
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

# CNBC Indonesia search URL
CNBC_SEARCH_URL = "https://www.cnbcindonesia.com/search"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
}


def parse_cnbc_date(date_str):
    """Parse CNBC Indonesia date string to YYYY-MM-DD format."""
    if not date_str:
        return None
    try:
        # Clean the date string
        date_str = date_str.strip()
        # Try common formats
        for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d %B %Y', '%d %b %Y',
                     '%A, %d/%m/%Y %H:%M WIB', '%d/%m/%Y %H:%M']:
            try:
                dt = datetime.strptime(date_str.split(' WIB')[0].strip(), fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        # Try parsing with regex for dd/mm/yyyy pattern
        match = re.search(r'(\d{2})/(\d{2})/(\d{4})', date_str)
        if match:
            day, month, year = match.groups()
            return f"{year}-{month}-{day}"
    except Exception:
        pass
    return None


def scrape_cnbc_search(keyword, max_pages=5):
    """
    Scrape CNBC Indonesia search results for a given keyword.

    Args:
        keyword: Search keyword
        max_pages: Maximum number of pages to scrape

    Returns:
        List of article dicts
    """
    articles = []
    stock = KEYWORD_STOCK_MAP.get(keyword, 'SECTOR')

    tag_keyword = keyword.lower().replace(" ", "-")
    url = f"https://www.cnbcindonesia.com/tag/{tag_keyword}"

    session = requests.Session()
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    retry = Retry(total=5, connect=5, read=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    for page in range(1, max_pages + 1):
        try:
            params = {'page': page}
            response = session.get(url, params=params,
                                    headers=HEADERS, timeout=15)

            if response.status_code != 200:
                print(f"[WARNING] CNBC page {page} returned {response.status_code} for '{keyword}'")
                break

            soup = BeautifulSoup(response.text, 'lxml')

            # Find article containers
            article_elements = soup.select('article') or soup.select('.list-content article')
            if not article_elements:
                # Alternative selectors
                article_elements = soup.select('.media_rows .media_rows__item') or \
                                   soup.select('.result-content .media')

            if not article_elements:
                print(f"[INFO] No more articles found on page {page} for '{keyword}'")
                break

            for article in article_elements:
                try:
                    # Extract title and URL
                    title_el = article.select_one('h2 a') or article.select_one('h3 a') or \
                               article.select_one('.media__title a') or article.select_one('a')

                    if not title_el:
                        continue

                    title = title_el.get_text(strip=True)
                    url = title_el.get('href', '')

                    if not url.startswith('http'):
                        url = 'https://www.cnbcindonesia.com' + url

                    # Extract date
                    date_el = article.select_one('.date') or article.select_one('time') or \
                              article.select_one('.media__date') or article.select_one('.text-sm')
                    date_str = date_el.get_text(strip=True) if date_el else ''
                    date_time = date_el.get('datetime', '') if date_el else ''
                    parsed_date = parse_cnbc_date(date_time or date_str)

                    # Extract summary
                    summary_el = article.select_one('p') or article.select_one('.media__desc')
                    summary = summary_el.get_text(strip=True) if summary_el else ''

                    if title:
                        articles.append({
                            'date': parsed_date or '',
                            'published_at': date_str,
                            'source': 'CNBC Indonesia',
                            'stock': stock,
                            'keyword': keyword,
                            'title': title,
                            'summary': summary,
                            'url': url,
                            'is_sector_news': 1 if stock == 'SECTOR' else 0,
                        })

                except Exception as e:
                    continue

            # Polite delay between pages
            time.sleep(1.5)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] CNBC request failed for '{keyword}' page {page}: {e}")
            break

    return articles


def run_cnbc_scraper():
    """Run CNBC Indonesia scraper for all keywords."""
    ensure_dir(RAW_NEWS_DIR)

    all_keywords = KEYWORDS_BBCA + KEYWORDS_BBRI + KEYWORDS_SECTOR
    all_articles = []

    print(f"\n[INFO] Starting CNBC Indonesia scraper...")
    print(f"[INFO] Keywords: {len(all_keywords)}")

    for keyword in all_keywords:
        print(f"\n[INFO] Scraping CNBC for: '{keyword}'")
        articles = scrape_cnbc_search(keyword, max_pages=15)
        print(f"[INFO] Found {len(articles)} articles for '{keyword}'")
        all_articles.extend(articles)
        time.sleep(2)  # Delay between keywords

    if all_articles:
        df = pd.DataFrame(all_articles)
        filepath = os.path.join(RAW_NEWS_DIR, 'cnbc_raw.csv')
        save_csv(df, filepath)
        print(f"\n[INFO] CNBC scraping complete: {len(df)} total articles")
    else:
        print("[WARNING] No articles scraped from CNBC Indonesia")

    return all_articles


if __name__ == '__main__':
    run_cnbc_scraper()
