"""
Sentilytics — CNBC Indonesia Scraper
Scrapes news articles from CNBC Indonesia tag pages (historical).

Target: https://www.cnbcindonesia.com/tag/<keyword-slug>?page=<n>
Extracts: date, source, title, summary, URL, stock mapping.

Strategy:
  - Tag pages are server-rendered HTML (no JS needed) and go far back in time
  - Date is extracted from the URL timestamp (YYYYMMDDHHMMSS) — 100% reliable for CNBC
  - Articles are filtered to DATE_START..DATE_END on-the-fly
  - Skip-ahead: starts from page 1, skips pages that are all too new
  - Early stop: stops as soon as a whole page pre-dates DATE_START
  - max_pages safety cap per keyword

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
from datetime import datetime, date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import (
    KEYWORDS_BBCA, KEYWORDS_BBRI, KEYWORDS_SECTOR,
    KEYWORD_STOCK_MAP, DATE_START, DATE_END, RAW_NEWS_DIR
)
from src.utils.file_utils import save_csv, ensure_dir

CNBC_TAG_URL = "https://www.cnbcindonesia.com/tag/{slug}"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.cnbcindonesia.com/',
}

# Parse configured date boundaries once
_DATE_START = datetime.strptime(DATE_START, '%Y-%m-%d').date()
_DATE_END   = datetime.strptime(DATE_END,   '%Y-%m-%d').date()

# -----------------------------------------------------------------------
# Probe result: for keyword "BBCA" (most articles), the 2023-2024 window
# sits roughly around page 8-32.  For less popular keywords the window
# is at lower page numbers, so we start scanning from page 1 and stop
# when we've gone past the date range.  MAX_PAGES_PER_KEYWORD is a
# safety cap — actual stop is date-driven.
# -----------------------------------------------------------------------
MAX_PAGES_PER_KEYWORD = 50


def extract_date_from_url(url: str):
    """
    Extract date from CNBC article URL.
    CNBC URLs embed timestamp as YYYYMMDDHHMMSS, e.g.:
        /market/20230920125337-17-474036/...
    Returns date object or None.
    """
    if not url:
        return None
    m = re.search(r'/(\d{4})(\d{2})(\d{2})\d{6}', url)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    return None


def _make_session():
    """Build a requests Session with retry logic."""
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    session = requests.Session()
    retry = Retry(
        total=5, connect=5, read=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def _keyword_to_slug(keyword: str) -> str:
    """Convert keyword to CNBC tag slug."""
    slug = keyword.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    return slug


def scrape_cnbc_tag(keyword: str, max_pages: int = MAX_PAGES_PER_KEYWORD):
    """
    Scrape CNBC Indonesia tag pages for one keyword.

    Pages are in reverse-chronological order. We:
      1. Skip pages that are entirely newer than DATE_END.
      2. Collect articles whose date falls in DATE_START..DATE_END.
      3. Stop as soon as a whole page pre-dates DATE_START.

    Returns:
        List of article dicts within DATE_START..DATE_END.
    """
    articles = []
    stock = KEYWORD_STOCK_MAP.get(keyword, 'SECTOR')
    slug  = _keyword_to_slug(keyword)
    url   = CNBC_TAG_URL.format(slug=slug)
    session = _make_session()

    found_in_range = False

    for page in range(1, max_pages + 1):
        try:
            response = session.get(url, params={'page': page},
                                   headers=HEADERS, timeout=20)

            if response.status_code == 404:
                print(f"    [CNBC] 404 — tag '{slug}' page {page} not found")
                break
            if response.status_code != 200:
                print(f"    [CNBC] HTTP {response.status_code} on page {page} for '{keyword}'")
                time.sleep(3)
                continue

            soup = BeautifulSoup(response.text, 'lxml')
            article_elements = soup.select('article')

            if not article_elements:
                print(f"    [CNBC] No articles on page {page} for '{keyword}' — stopping")
                break

            page_dates = []
            page_articles_collected = 0

            for article in article_elements:
                try:
                    # --- URL ---
                    link_el = article.select_one('a[href]')
                    art_url = link_el.get('href', '') if link_el else ''
                    if art_url and not art_url.startswith('http'):
                        art_url = 'https://www.cnbcindonesia.com' + art_url

                    # --- Date from URL (primary — most reliable) ---
                    art_date = extract_date_from_url(art_url)
                    if art_date:
                        page_dates.append(art_date)

                    # --- Range filter ---
                    if art_date is not None:
                        if art_date > _DATE_END:
                            continue   # too new, skip
                        if art_date < _DATE_START:
                            continue   # too old, skip

                    # --- Title ---
                    title_el = (article.select_one('h2') or
                                article.select_one('h3') or
                                article.select_one('h4'))
                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    if not title:
                        continue

                    # --- Date display text (informational) ---
                    date_el = (article.select_one('.text-xs.text-gray') or
                               article.select_one('.date') or
                               article.select_one('time'))
                    date_str = date_el.get_text(strip=True) if date_el else ''

                    # --- Summary ---
                    summary_el = (article.select_one('.desc') or
                                  article.select_one('p') or
                                  article.select_one('.media__desc'))
                    summary = summary_el.get_text(strip=True) if summary_el else ''

                    articles.append({
                        'date':           art_date.strftime('%Y-%m-%d') if art_date else '',
                        'published_at':   date_str,
                        'source':         'CNBC Indonesia',
                        'stock':          stock,
                        'keyword':        keyword,
                        'title':          title,
                        'summary':        summary,
                        'url':            art_url,
                        'is_sector_news': 1 if stock == 'SECTOR' else 0,
                    })
                    page_articles_collected += 1
                    found_in_range = True

                except Exception:
                    continue

            # ---- Pagination control ----
            if page_dates:
                page_max_date = max(page_dates)
                page_min_date = min(page_dates)

                if page_max_date < _DATE_START:
                    # Entire page is older than our window start — nothing more to find
                    print(f"    [CNBC] Page {page} max date {page_max_date} < {DATE_START} — stopping early")
                    break
                # If min_date > DATE_END, the whole page is still too new — keep going deeper

            if page % 5 == 0:
                print(f"    [CNBC] Page {page} | collected so far: {len(articles)} for '{keyword}'")

            time.sleep(1.5)  # polite delay

        except requests.exceptions.RequestException as e:
            print(f"    [CNBC][ERROR] '{keyword}' page {page}: {e}")
            time.sleep(5)
            continue

    return articles


def run_cnbc_scraper():
    """Run CNBC Indonesia scraper for all keywords."""
    ensure_dir(RAW_NEWS_DIR)

    all_keywords = KEYWORDS_BBCA + KEYWORDS_BBRI + KEYWORDS_SECTOR
    all_articles = []

    print(f"\n[INFO] Starting CNBC Indonesia scraper (tag-based, historical)...")
    print(f"[INFO] Target date range: {DATE_START} to {DATE_END}")
    print(f"[INFO] Total keywords: {len(all_keywords)}, max pages each: {MAX_PAGES_PER_KEYWORD}")

    for keyword in all_keywords:
        print(f"\n[INFO] Scraping CNBC for: '{keyword}'")
        articles = scrape_cnbc_tag(keyword, max_pages=MAX_PAGES_PER_KEYWORD)
        print(f"[INFO] Found {len(articles)} in-range articles for '{keyword}'")
        all_articles.extend(articles)
        time.sleep(2)  # inter-keyword delay

    if all_articles:
        df = pd.DataFrame(all_articles)
        # Dedup by URL before saving raw file
        df = df.drop_duplicates(subset=['url'], keep='first')
        filepath = os.path.join(RAW_NEWS_DIR, 'cnbc_raw.csv')
        save_csv(df, filepath)
        print(f"\n[INFO] CNBC scraping complete: {len(df)} unique articles saved to cnbc_raw.csv")
    else:
        print("[WARNING] No articles scraped from CNBC Indonesia")

    return all_articles


if __name__ == '__main__':
    run_cnbc_scraper()
