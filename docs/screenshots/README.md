# Screenshot Guide — Sentilytics

Folder `docs/screenshots/` telah dibuat. Berikut panduan untuk mengambil screenshot.

## Cara Mengambil Screenshot

1. Jalankan Flask: `python run.py`
2. Buka browser di `http://127.0.0.1:5000`
3. Gunakan **Windows + Shift + S** (Snipping Tool) untuk capture
4. Simpan ke folder `docs/screenshots/` dengan nama sesuai tabel

## Daftar Screenshot yang Dibutuhkan

| No | File | Halaman/URL | Catatan |
|---|---|---|---|
| 1 | `01_login_page.png` | `/login` | Tampilan form login |
| 2 | `02_register_page.png` | `/register` | Tampilan form register |
| 3 | `03_dashboard_utama.png` | `/dashboard?stock=BBCA&model=baseline` | Dashboard utama setelah login |
| 4 | `04_evaluation_page.png` | `/evaluation` | Halaman evaluasi model — tabel + grafik |
| 5 | `05_forecast_h7.png` | `/forecast?stock=BBCA&model=hybrid` | Forecast H+7 — tabel + grafik |
| 6 | `06_dataset_summary.png` | `/dataset-summary` | Ringkasan dataset |
| 7 | `07_admin_panel.png` | `/admin` (login admin) | Admin panel |
| 8 | `08_access_denied.png` | `/admin` (login user biasa) | Halaman 403 |
| 9 | `09_flask_running.png` | Terminal | Terminal setelah `python run.py` |
| 10 | `10_unit_test_passed.png` | Terminal | Hasil `pytest tests/ -v` (46 passed) |

## Akun untuk Testing

- **Admin**: admin@sentilytics.local / Admin123!Secure
- **User biasa**: testuser@sentilytics.local / TestPass123

## Urutan Screenshot

1. Buka browser, navigasi ke `/login` → screenshot 01
2. Klik Register → screenshot 02
3. Login sebagai admin → screenshot 03 (dashboard)
4. Navigasi ke `/evaluation` → screenshot 04
5. Navigasi ke `/forecast?stock=BBCA&model=hybrid` → screenshot 05
6. Navigasi ke `/dataset-summary` → screenshot 06
7. Navigasi ke `/admin` → screenshot 07
8. Logout, login sebagai user biasa, navigasi ke `/admin` → screenshot 08
9. Terminal Flask running → screenshot 09
10. Terminal pytest output → screenshot 10
