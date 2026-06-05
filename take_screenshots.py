# -*- coding: utf-8 -*-
"""
Script otomatis untuk mengambil screenshot tampilan terbaru Sentilytics.
Jalankan Flask terlebih dahulu (python run.py), lalu jalankan script ini.
"""
import sys
from pathlib import Path
import urllib.request

SCREENSHOT_DIR = Path("docs/screenshots")
BASE_URL = "http://127.0.0.1:5000"

ADMIN_EMAIL = "admin@sentilytics.local"
ADMIN_PASSWORD = "Admin123!Secure"


def take_screenshots():
    from playwright.sync_api import sync_playwright

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 01: Login Page
        print("[1/8] Login Page...")
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENSHOT_DIR / "01_login_page.png"), full_page=False)
        print("      -> Saved 01_login_page.png")

        # 02: Register Page
        print("[2/8] Register Page...")
        page.goto(f"{BASE_URL}/register", wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENSHOT_DIR / "02_register_page.png"), full_page=False)
        print("      -> Saved 02_register_page.png")

        # Login as Admin
        print("      Logging in as Admin...")
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        page.fill("#email", ADMIN_EMAIL)
        page.fill("#password", ADMIN_PASSWORD)
        page.click("#loginBtn")
        page.wait_for_url(f"{BASE_URL}/dashboard*", timeout=10000)
        page.wait_for_timeout(3000)

        # 03: Dashboard Utama
        print("[3/8] Dashboard Utama (BBCA Baseline)...")
        page.goto(f"{BASE_URL}/dashboard?stock=BBCA&model=baseline", wait_until="networkidle")
        page.wait_for_timeout(4000)
        page.screenshot(path=str(SCREENSHOT_DIR / "03_dashboard_utama.png"), full_page=False)
        print("      -> Saved 03_dashboard_utama.png")

        # 04: Evaluation Page
        print("[4/8] Evaluation Page...")
        page.goto(f"{BASE_URL}/evaluation?stock=BBCA&model=baseline", wait_until="networkidle")
        page.wait_for_timeout(4000)
        page.screenshot(path=str(SCREENSHOT_DIR / "04_evaluation_page.png"), full_page=False)
        print("      -> Saved 04_evaluation_page.png")

        # 05: Forecast H+7
        print("[5/8] Forecast H+7...")
        page.goto(f"{BASE_URL}/forecast?stock=BBCA&model=hybrid", wait_until="networkidle")
        page.wait_for_timeout(4000)
        page.screenshot(path=str(SCREENSHOT_DIR / "05_forecast_h7.png"), full_page=False)
        print("      -> Saved 05_forecast_h7.png")

        # 06: Dataset Summary
        print("[6/8] Dataset Summary...")
        page.goto(f"{BASE_URL}/dataset-summary", wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENSHOT_DIR / "06_dataset_summary.png"), full_page=False)
        print("      -> Saved 06_dataset_summary.png")

        # 07: Admin Panel
        print("[7/8] Admin Panel...")
        page.goto(f"{BASE_URL}/admin", wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENSHOT_DIR / "07_admin_panel.png"), full_page=False)
        print("      -> Saved 07_admin_panel.png")

        # 08: Access Denied - logout then try /admin
        print("[8/8] Access Denied (403)...")
        page.goto(f"{BASE_URL}/logout", wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.goto(f"{BASE_URL}/admin", wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENSHOT_DIR / "08_access_denied.png"), full_page=False)
        print("      -> Saved 08_access_denied.png")

        browser.close()

    print("")
    print("DONE! All screenshots saved to: " + str(SCREENSHOT_DIR.resolve()))


if __name__ == "__main__":
    print("=" * 60)
    print("  Sentilytics - Auto Screenshot Tool")
    print("=" * 60)
    print("")

    try:
        urllib.request.urlopen(f"{BASE_URL}/login", timeout=5)
        print("Flask detected at http://127.0.0.1:5000")
        print("")
    except Exception:
        print("ERROR: Flask not running. Run: python run.py first.")
        sys.exit(1)

    take_screenshots()
