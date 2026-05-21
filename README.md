# Sentilytics

**Sistem Prediksi Harga Saham Perbankan Berbasis Hybrid LSTM dan Sentimen Berita Indonesia**

> Sentilytics adalah prototipe aplikasi web skripsi Informatika / Artificial Intelligence untuk membandingkan model Baseline LSTM dan Hybrid LSTM dalam memprediksi harga penutupan saham perbankan BBCA dan BBRI.

⚠️ **Disclaimer:** Aplikasi ini bukan rekomendasi investasi. Tidak memberikan sinyal beli/jual/tahan saham. Hasil prediksi hanya untuk tujuan akademis.

---

## 🎯 Fitur Utama

- **Data Pipeline:** Download OHLCV BBCA & BBRI dari Yahoo Finance
- **News Scraping:** Scraping berita dari CNBC Indonesia & Kontan
- **NLP Pipeline:** Preprocessing teks Bahasa Indonesia (Sastrawi) + Sentiment Scoring (InSet Lexicon)
- **Machine Learning:** Baseline LSTM (OHLCV) vs Hybrid LSTM (OHLCV + Sentiment)
- **Evaluasi:** RMSE, MAE, MAPE pada prediksi Close Price H+1
- **Forecast:** Simulasi forecast H+7 (visualisasi only)
- **Dashboard:** Flask web app dengan login/register, admin panel, grafik interaktif
- **UI:** Custom AdminLTE-style profesional

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Backend | Python 3.10, Flask |
| Auth | Flask-Login, Flask-SQLAlchemy, SQLite |
| Data | pandas, numpy, yfinance |
| NLP | Sastrawi, InSet Lexicon |
| ML | TensorFlow/Keras LSTM |
| Scraping | requests, BeautifulSoup4 |
| Frontend | HTML, CSS (custom), JavaScript, Chart.js |
| Testing | pytest |

---

## 📁 Struktur Folder

```
sentilytics/
├── run.py              # Entry point Flask app
├── run_pipeline.py     # Master pipeline runner
├── config.yaml         # Project configuration
├── requirements.txt    # Python dependencies
├── .env                # Secret keys (gitignored)
│
├── app/                # Flask web application
│   ├── app.py          # App factory
│   ├── models_db.py    # SQLAlchemy User model
│   ├── auth/           # Login, register, logout
│   ├── admin/          # Admin panel routes
│   ├── dashboard/      # Dashboard routes & API
│   ├── services/       # Business logic (read-only)
│   ├── templates/      # Jinja2 HTML templates
│   └── static/         # CSS, JS, images
│
├── src/                # Data science modules
│   ├── config.py       # Config loader
│   ├── data_collection/# Stock downloader, news scrapers
│   ├── preprocessing/  # Stock, text, sequence, fusion
│   ├── sentiment/      # InSet loader, scorer
│   ├── modeling/       # LSTM builder, training, forecast
│   ├── evaluation/     # Metrics, plots
│   └── utils/          # Date & file helpers
│
├── data/               # Datasets (CSV)
├── models/             # Trained models (.keras) & scalers (.pkl)
├── results/            # Predictions, metrics, forecasts, figures
├── tests/              # Unit tests & black-box test plan
└── docs/               # Documentation
```

---

## 🚀 Instalasi & Menjalankan

### 1. Clone repository

```bash
git clone <repo-url>
cd Sentilytics_v1
```

### 2. Buat virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment

```bash
copy .env.example .env
# Edit .env sesuai kebutuhan (SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD)
```

### 5. Jalankan pipeline data science (offline)

```bash
# Pipeline lengkap (download data, scraping, training, evaluasi, forecast)
python run_pipeline.py

# Skip scraping jika sudah punya data berita
python run_pipeline.py --skip-scraping

# Skip training jika sudah punya model
python run_pipeline.py --skip-training
```

### 6. Jalankan dashboard

```bash
python run.py
```

Buka browser: **http://127.0.0.1:5000**

---

## 👤 Akun Default

| Role | Email | Password |
|------|-------|----------|
| Admin | (sesuai .env) | (sesuai .env) |

User baru dapat mendaftar melalui halaman Register.

---

## 📊 Alur Penggunaan

1. **Login** dengan akun terdaftar
2. Pilih **Emiten** (BBCA / BBRI) dan **Model** (Baseline / Hybrid)
3. Lihat **Prediksi Close H+1**, **RMSE/MAE/MAPE**, dan **Grafik Actual vs Predicted**
4. Buka **Forecast Simulation** untuk melihat simulasi H+7
5. Admin dapat melihat **Admin Panel** untuk ringkasan sistem

---

## 🧪 Testing

```bash
# Unit tests
pytest tests/ -v

# Spesifik module
pytest tests/test_metrics.py -v
```

Lihat `tests/blackbox_test_plan.md` untuk daftar pengujian black-box.

---

## 📝 Catatan Penting

1. Training model dilakukan **offline** via `run_pipeline.py`, bukan dari dashboard
2. Dashboard hanya **membaca** file hasil training (CSV/JSON)
3. Data saham menggunakan **OHLCV harian** dari Yahoo Finance
4. Sentiment scoring menggunakan **InSet Lexicon** (lexicon-based)
5. Split data dilakukan secara **kronologis** (80:20), tanpa shuffle
6. Scaler hanya di-fit pada **data training**
7. Forecast H+7 adalah **simulasi visualisasi**, bukan evaluasi utama
8. Untuk Hybrid forecast, sentimen masa depan diasumsikan menggunakan rata-rata 7 hari terakhir

---

## 📄 Lisensi

Proyek skripsi — hanya untuk tujuan akademis.
