# PRD Final AI Agent — Sentilytics

**Nama Produk:** Sentilytics  
**Nama Lengkap:** Sentilytics — Sistem Prediksi Harga Saham Perbankan Berbasis Hybrid LSTM dan Sentimen Berita Indonesia  
**Jenis Dokumen:** Product Requirements Document untuk AI Agent Coding  
**Versi:** 3.0 Final Implementable  
**Tujuan Dokumen:** Menjadi acuan utama bagi AI Agent untuk membuat program dari awal sampai selesai  
**Target Pengguna Dokumen:** AI Agent, developer pendamping, mahasiswa pemilik skripsi  
**Mode Pengembangan:** Localhost  
**Hosting:** Opsional setelah versi lokal stabil  
**Status:** Final untuk mulai pengembangan  

---

# 1. Instruksi Utama untuk AI Agent

AI Agent harus membangun aplikasi **Sentilytics** dari awal sampai selesai berdasarkan dokumen ini.

Sentilytics adalah aplikasi web berbasis **Flask** untuk skripsi Informatika / Artificial Intelligence yang membandingkan model **Baseline LSTM** dan **Hybrid LSTM** dalam memprediksi harga penutupan saham perbankan **BBCA** dan **BBRI**.

AI Agent wajib menjaga fokus penelitian sebagai proyek **Artificial Intelligence**, bukan ekonomi, bukan trading, dan bukan rekomendasi investasi.

## 1.1 Aturan Wajib

AI Agent wajib mengikuti aturan berikut:

1. Gunakan nama aplikasi **Sentilytics**.
2. Gunakan **Python 3.10 atau 3.11**.
3. Gunakan **Flask** sebagai web framework.
4. Gunakan UI custom profesional dengan pola **AdminLTE-style**, bukan menyalin template mentah.
5. Buat fitur **login, register, logout, admin account, dan admin panel**.
6. Gunakan **SQLite hanya untuk user/auth**.
7. Simpan dataset dalam **CSV**.
8. Simpan hasil evaluasi dalam **CSV/JSON**.
9. Simpan model dalam format **`.keras`**.
10. Simpan scaler dalam format **`.pkl`** menggunakan `joblib`.
11. Ambil data saham BBCA dan BBRI dari **yfinance/Yahoo Finance**.
12. Scraping berita dilakukan dari nol dari **CNBC Indonesia** dan **Kontan**.
13. Gunakan periode data **1 Januari 2023 sampai 31 Desember 2024**.
14. Gunakan fitur saham **Open, High, Low, Close, Volume (OHLCV)**.
15. Gunakan **Sastrawi** untuk preprocessing teks Bahasa Indonesia.
16. Gunakan **InSet Lexicon** untuk sentiment scoring.
17. Buat **Baseline LSTM** dengan fitur OHLCV.
18. Buat **Hybrid LSTM** dengan fitur OHLCV + skor sentimen berita.
19. Target prediksi utama adalah **Close Price H+1**.
20. Evaluasi utama menggunakan **RMSE, MAE, dan MAPE**.
21. Forecast H+7 hanya fitur simulasi visualisasi dashboard.
22. Untuk forecast Hybrid H+7, gunakan **rata-rata skor sentimen 7 hari perdagangan terakhir**.
23. Jangan melakukan shuffle pada data time-series.
24. Split data harus kronologis.
25. Scaler hanya boleh fit pada data train.
26. Jangan training model langsung dari route Flask.
27. Dashboard hanya membaca file hasil training, prediksi, metrik, dan forecast.
28. Jangan membuat fitur rekomendasi investasi.
29. Jangan membuat fitur trading.
30. Jangan mengklaim hasil “signifikan” tanpa uji statistik.
31. Semua klaim performa harus berdasarkan RMSE, MAE, dan MAPE.
32. Kode harus modular dan mudah dijelaskan saat sidang.

## 1.2 Larangan untuk AI Agent

AI Agent tidak boleh:

1. Mengubah scope utama menjadi aplikasi investasi.
2. Menambahkan fitur buy/sell/hold.
3. Membuat auto trading.
4. Menggunakan LLM untuk sentiment scoring utama.
5. Mengganti InSet Lexicon tanpa izin.
6. Mengganti LSTM sebagai model utama tanpa izin.
7. Menggunakan database besar untuk seluruh dataset jika tidak diperlukan.
8. Menjalankan training model dari tombol dashboard.
9. Menggunakan data test untuk fit scaler.
10. Mengacak urutan data time-series.
11. Menghapus forecast H+7 dari dashboard.
12. Menjadikan forecast H+7 sebagai evaluasi utama.
13. Hardcode password admin di source code.
14. Menyimpan password dalam plain text.
15. Mengandalkan internet saat dashboard demo jika data/model sudah bisa disimpan lokal.

---

# 2. Ringkasan Produk

Sentilytics adalah sistem dashboard analitik untuk memvisualisasikan hasil prediksi harga saham perbankan menggunakan LSTM dan analisis sentimen berita Indonesia.

Sistem memiliki dua alur utama:

1. **Alur Data Science / Machine Learning**
   - Mengambil data saham BBCA dan BBRI.
   - Scraping berita CNBC Indonesia dan Kontan.
   - Preprocessing data saham.
   - Preprocessing teks berita.
   - Menghitung skor sentimen menggunakan InSet Lexicon.
   - Menggabungkan data OHLCV dan skor sentimen.
   - Melatih Baseline LSTM dan Hybrid LSTM.
   - Mengevaluasi model menggunakan RMSE, MAE, dan MAPE.
   - Menyimpan model, scaler, hasil prediksi, hasil evaluasi, dan forecast.

2. **Alur Web Application**
   - User melakukan register/login.
   - User memilih emiten dan model.
   - Dashboard menampilkan prediksi H+1, metrik evaluasi, grafik actual vs predicted, dan simulasi forecast H+7.
   - Admin melihat ringkasan user, dataset, status model, dan evaluasi semua model.

---

# 3. Konsep Final Produk

## 3.1 Konsep Akademik

Sentilytics diposisikan sebagai prototipe sistem skripsi Informatika / Artificial Intelligence.

Kontribusi utama:
1. Pengumpulan dataset saham dan berita.
2. Preprocessing data numerik dan teks.
3. Analisis sentimen berbasis InSet Lexicon.
4. Data fusion antara OHLCV dan skor sentimen.
5. Pembangunan Baseline LSTM dan Hybrid LSTM.
6. Evaluasi model dengan RMSE, MAE, dan MAPE.
7. Visualisasi hasil melalui dashboard Flask.

Sistem tidak memberikan rekomendasi investasi.

## 3.2 Konsep Teknis

Aplikasi terdiri dari tiga bagian utama:

1. **Offline pipeline**
   - Scraping.
   - Preprocessing.
   - Sentiment scoring.
   - Training model.
   - Evaluation.
   - Forecast generation.

2. **File-based result storage**
   - Dataset CSV.
   - Prediction CSV.
   - Metrics CSV/JSON.
   - Forecast CSV.
   - Model `.keras`.
   - Scaler `.pkl`.

3. **Flask dashboard**
   - Auth.
   - User dashboard.
   - Admin panel.
   - API pembacaan hasil.

## 3.3 Konsep UI

UI Sentilytics dibuat custom profesional dengan referensi pola AdminLTE:

- Sidebar kiri.
- Top navigation.
- Metric cards.
- Chart panels.
- Data tables.
- Badge status.
- Breadcrumb.
- Login/register cards.
- Admin panel.

UI tidak perlu menggunakan AdminLTE secara mentah. Yang diikuti adalah pola desain dashboard profesionalnya.

---

# 4. Tujuan Produk

Produk harus mampu:

1. Menyediakan aplikasi web bernama Sentilytics.
2. Menyediakan sistem login/register/logout.
3. Menyediakan admin account dan admin panel.
4. Mengambil data harga saham BBCA dan BBRI periode 2023–2024.
5. Scraping berita CNBC Indonesia dan Kontan dari nol.
6. Membersihkan dan menormalisasi data saham.
7. Membersihkan teks berita Bahasa Indonesia.
8. Melakukan stemming menggunakan Sastrawi.
9. Menghasilkan skor sentimen menggunakan InSet Lexicon.
10. Menghasilkan skor sentimen harian per emiten.
11. Menggabungkan data OHLCV dan skor sentimen.
12. Membangun dataset baseline dan hybrid.
13. Melatih Baseline LSTM dan Hybrid LSTM.
14. Mengevaluasi model dengan RMSE, MAE, dan MAPE.
15. Menghasilkan grafik actual vs predicted.
16. Menghasilkan simulasi forecast H+7.
17. Menampilkan semua hasil ke dashboard.
18. Menyediakan dokumentasi cara menjalankan sistem.
19. Menyediakan hasil pengujian black-box.

---

# 5. Non-Tujuan Produk

Produk ini tidak bertujuan untuk:

1. Menjadi aplikasi rekomendasi investasi.
2. Memberi saran beli/jual/tahan saham.
3. Menjamin keuntungan finansial.
4. Menjadi sistem trading otomatis.
5. Menjadi aplikasi produksi publik berskala besar.
6. Menggunakan data intraday.
7. Menggunakan LLM untuk sentiment scoring utama.
8. Menggunakan transformer sebagai model utama.
9. Mengoptimalkan portofolio.
10. Menjadi aplikasi mobile.
11. Menyediakan notifikasi real-time.
12. Menjalankan scraping dan training live dari dashboard.

---

# 6. Stack Program Final

## 6.1 Backend dan Web

| Komponen | Stack |
|---|---|
| Bahasa utama | Python 3.10 / 3.11 |
| Web framework | Flask |
| Template engine | Jinja2 |
| Session login | Flask-Login |
| ORM | Flask-SQLAlchemy |
| Database auth | SQLite |
| Password hashing | Werkzeug |
| Environment | python-dotenv |

## 6.2 Data Science dan Machine Learning

| Komponen | Stack |
|---|---|
| Dataframe | pandas |
| Numerik | numpy |
| Data saham | yfinance |
| Scaling | scikit-learn MinMaxScaler |
| Metrics | scikit-learn / custom function |
| Model | TensorFlow/Keras |
| Model type | LSTM |
| Save model | `.keras` |
| Save scaler | joblib `.pkl` |

## 6.3 NLP dan Sentiment

| Komponen | Stack |
|---|---|
| Cleaning | regex / string |
| Tokenisasi | custom tokenizer sederhana |
| Stopword | Sastrawi StopWordRemover / custom stopword |
| Stemming | Sastrawi Stemmer |
| Lexicon | InSet Lexicon |
| Output | sentiment_score, sentiment_label |

## 6.4 Scraping

| Komponen | Stack |
|---|---|
| HTTP request | requests |
| HTML parsing | BeautifulSoup4 |
| RSS optional | feedparser |
| Output | CSV raw news |

## 6.5 Frontend

| Komponen | Stack |
|---|---|
| Markup | HTML |
| Styling | CSS custom |
| Interactivity | JavaScript |
| Chart | Chart.js atau Plotly.js |
| Layout style | AdminLTE-style custom |

## 6.6 Testing

| Komponen | Stack |
|---|---|
| Unit test | pytest |
| UI test | Black-box manual |
| Dokumentasi test | Markdown / CSV |

---

# 7. Scope Produk

## 7.1 In Scope

| Area | Detail |
|---|---|
| Saham | BBCA dan BBRI |
| Ticker | BBCA.JK dan BBRI.JK |
| Periode | 1 Januari 2023–31 Desember 2024 |
| Data harga | OHLCV harian |
| Sumber harga | Yahoo Finance/yfinance |
| Sumber berita | CNBC Indonesia dan Kontan |
| Akuisisi berita | Scraping dari nol |
| Sentimen | InSet Lexicon |
| NLP | Sastrawi |
| Model baseline | LSTM OHLCV |
| Model hybrid | LSTM OHLCV + sentiment_score |
| Target | Close Price H+1 |
| Evaluasi | RMSE, MAE, MAPE |
| Forecast | Simulasi H+7 |
| Web app | Flask |
| Auth | Login, register, logout |
| Admin | Admin account + admin panel |
| UI | Custom AdminLTE-style |
| Penyimpanan dataset | CSV |
| Penyimpanan hasil | CSV/JSON |
| Penyimpanan model | `.keras` |
| Penyimpanan scaler | `.pkl` |
| Testing | Unit test dan black-box testing |

## 7.2 Out of Scope

| Area | Keterangan |
|---|---|
| Multi-emiten besar | Tidak dikerjakan |
| Data intraday | Tidak digunakan |
| Trading signal | Tidak dibuat |
| Auto trading | Tidak dibuat |
| Portfolio optimization | Tidak dibuat |
| LLM sentiment | Tidak digunakan |
| Transformer forecasting | Tidak digunakan |
| Live training via dashboard | Tidak dibuat |
| Payment/subscription | Tidak dibuat |
| Mobile app | Tidak dibuat |
| Role kompleks | Tidak dibuat |
| Production-scale deployment | Opsional, bukan prioritas |

---

# 8. User Role

## 8.1 Guest

Guest adalah pengguna yang belum login.

Hak akses:
- Membuka login page.
- Membuka register page.

Tidak boleh:
- Membuka dashboard.
- Membuka admin panel.
- Mengakses API hasil model.

## 8.2 User

User adalah pengguna yang sudah register dan login.

Hak akses:
- Dashboard.
- Prediction Result.
- Model Evaluation.
- Forecast Simulation.
- Logout.

Fitur:
- Pilih emiten BBCA/BBRI.
- Pilih model Baseline/Hybrid.
- Lihat prediksi Close H+1.
- Lihat RMSE, MAE, MAPE.
- Lihat grafik actual vs predicted.
- Lihat forecast H+7.
- Lihat disclaimer.

## 8.3 Admin

Admin adalah user dengan role `admin`.

Hak akses:
- Semua fitur User.
- Admin Panel.
- Dataset Summary.
- Model Status.
- User Summary.
- Evaluation Summary.

Admin tidak perlu menjalankan training dari dashboard.

---

# 9. User Stories

## 9.1 Authentication

1. Sebagai guest, saya ingin register agar dapat mengakses dashboard.
2. Sebagai user, saya ingin login agar dapat melihat hasil prediksi.
3. Sebagai user, saya ingin logout agar session saya berakhir.
4. Sebagai admin, saya ingin login ke admin panel agar dapat melihat ringkasan sistem.

## 9.2 Dashboard

1. Sebagai user, saya ingin memilih emiten BBCA atau BBRI.
2. Sebagai user, saya ingin memilih model Baseline LSTM atau Hybrid LSTM.
3. Sebagai user, saya ingin melihat prediksi Close Price H+1.
4. Sebagai user, saya ingin melihat RMSE, MAE, dan MAPE.
5. Sebagai user, saya ingin melihat grafik actual vs predicted.
6. Sebagai user, saya ingin melihat simulasi forecast H+7.
7. Sebagai user, saya ingin melihat disclaimer bahwa sistem bukan rekomendasi investasi.

## 9.3 Admin

1. Sebagai admin, saya ingin melihat jumlah user.
2. Sebagai admin, saya ingin melihat jumlah data saham dan berita.
3. Sebagai admin, saya ingin melihat status file model.
4. Sebagai admin, saya ingin melihat hasil evaluasi semua model.

---

# 10. Functional Requirements

## 10.1 Authentication

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-AUTH-01 | Sistem menyediakan register | Must | User dapat membuat akun baru |
| FR-AUTH-02 | Sistem menyediakan login | Must | User dapat login dengan email dan password |
| FR-AUTH-03 | Sistem menyediakan logout | Must | Session berakhir setelah logout |
| FR-AUTH-04 | Password di-hash | Must | Password tidak tersimpan plain text |
| FR-AUTH-05 | Role user/admin | Must | Admin dapat membuka admin panel, user biasa tidak |
| FR-AUTH-06 | Admin seed | Must | Admin account dibuat dari `.env` |
| FR-AUTH-07 | Proteksi route | Must | Guest diarahkan ke login jika membuka dashboard |

## 10.2 Data Collection

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-DATA-01 | Download BBCA.JK | Must | `data/raw/stock/BBCA_raw.csv` tersedia |
| FR-DATA-02 | Download BBRI.JK | Must | `data/raw/stock/BBRI_raw.csv` tersedia |
| FR-DATA-03 | Scrape CNBC Indonesia | Must | CSV berita CNBC tersedia |
| FR-DATA-04 | Scrape Kontan | Must | CSV berita Kontan tersedia |
| FR-DATA-05 | Mapping emiten | Must | Berita diberi label BBCA/BBRI/sektor |
| FR-DATA-06 | Deduplikasi berita | Must | Duplikat URL/judul dihapus |
| FR-DATA-07 | Simpan raw data | Must | Data mentah tersedia untuk audit |

## 10.3 Preprocessing

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-PREP-01 | Bersihkan data saham | Must | Data urut tanggal dan valid |
| FR-PREP-02 | Buat target Close H+1 | Must | `target_close_h1` tersedia |
| FR-PREP-03 | Case folding | Must | Teks menjadi lowercase |
| FR-PREP-04 | Cleaning teks | Must | URL/simbol tidak relevan hilang |
| FR-PREP-05 | Stopword removal | Must | Stopword umum dihapus |
| FR-PREP-06 | Tokenisasi | Must | Token tersedia |
| FR-PREP-07 | Stemming Sastrawi | Must | Stemmed text tersedia |
| FR-PREP-08 | Simpan processed text | Must | CSV berita processed tersedia |

## 10.4 Sentiment Scoring

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-SENT-01 | Load InSet Lexicon | Must | Positive dan negative lexicon terbaca |
| FR-SENT-02 | Hitung skor berita | Must | `sentiment_score` per berita tersedia |
| FR-SENT-03 | Label sentimen | Must | positif/netral/negatif tersedia |
| FR-SENT-04 | Agregasi harian | Must | daily sentiment per emiten tersedia |
| FR-SENT-05 | Missing sentiment | Must | Tanggal tanpa berita diisi 0 saat fusion |

## 10.5 Data Fusion

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-FUS-01 | Buat baseline dataset | Must | OHLCV + target tersedia |
| FR-FUS-02 | Buat hybrid dataset | Must | OHLCV + sentiment + target tersedia |
| FR-FUS-03 | Merge berdasarkan tanggal | Must | Data saham dan sentimen align |
| FR-FUS-04 | Simpan dataset final | Must | CSV fusion tersedia |

## 10.6 Modeling

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-ML-01 | Split kronologis | Must | 80% awal train, 20% akhir test |
| FR-ML-02 | Fit scaler train only | Must | Tidak data leakage |
| FR-ML-03 | Sequence window 30 | Must | Shape `(samples, 30, features)` |
| FR-ML-04 | Train BBCA Baseline | Must | Model `.keras` dan prediksi CSV tersedia |
| FR-ML-05 | Train BBCA Hybrid | Must | Model `.keras` dan prediksi CSV tersedia |
| FR-ML-06 | Train BBRI Baseline | Must | Model `.keras` dan prediksi CSV tersedia |
| FR-ML-07 | Train BBRI Hybrid | Must | Model `.keras` dan prediksi CSV tersedia |
| FR-ML-08 | Save scaler | Must | File `.pkl` tersedia |
| FR-ML-09 | Save training history | Should | History CSV tersedia |

## 10.7 Evaluation

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-EVAL-01 | Hitung RMSE | Must | Nilai RMSE tersedia |
| FR-EVAL-02 | Hitung MAE | Must | Nilai MAE tersedia |
| FR-EVAL-03 | Hitung MAPE | Must | Nilai MAPE tersedia |
| FR-EVAL-04 | Simpan metrics | Must | `evaluation_metrics.csv` tersedia |
| FR-EVAL-05 | Grafik actual vs predicted | Must | PNG/CSV/chart data tersedia |
| FR-EVAL-06 | Perbandingan model | Must | Baseline vs Hybrid dapat dibandingkan |

## 10.8 Forecast H+7

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-FC-01 | Forecast H+7 tersedia | Must | 7 baris forecast per model/emiten |
| FR-FC-02 | Hybrid pakai rata-rata sentimen 7 hari | Must | Nilai asumsi dicatat |
| FR-FC-03 | Forecast diberi label simulasi | Must | Dashboard menampilkan disclaimer |
| FR-FC-04 | Forecast tidak masuk evaluasi utama | Must | Metrics tetap hanya dari test H+1 |

## 10.9 Dashboard

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-UI-01 | UI branding Sentilytics | Must | Nama Sentilytics muncul |
| FR-UI-02 | Layout AdminLTE-style custom | Must | Sidebar, topbar, cards, charts, tables |
| FR-UI-03 | Pilih emiten | Must | Dropdown BBCA/BBRI |
| FR-UI-04 | Pilih model | Must | Dropdown Baseline/Hybrid |
| FR-UI-05 | Card prediksi H+1 | Must | Prediksi tampil |
| FR-UI-06 | Card RMSE/MAE/MAPE | Must | Metrik tampil |
| FR-UI-07 | Grafik actual vs predicted | Must | Grafik tampil |
| FR-UI-08 | Forecast H+7 | Must | Grafik/tabel tampil |
| FR-UI-09 | Tabel hasil prediksi | Should | Data prediksi tampil |
| FR-UI-10 | Disclaimer | Must | Bukan rekomendasi investasi |

## 10.10 Admin Panel

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| FR-ADM-01 | Ringkasan user | Must | Total user/admin tampil |
| FR-ADM-02 | Ringkasan dataset | Should | Jumlah data saham/berita tampil |
| FR-ADM-03 | Status model | Should | Tersedia/belum tersedia tampil |
| FR-ADM-04 | Evaluasi semua model | Must | Tabel metrics tampil |
| FR-ADM-05 | Daftar user | Should | Tabel user tampil |

---

# 11. Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Portability | Berjalan di Windows 10/11 localhost |
| NFR-02 | Dashboard loading | < 5 detik pada localhost |
| NFR-03 | Result loading | < 10 detik karena membaca file |
| NFR-04 | Training separation | Training tidak berada di route Flask |
| NFR-05 | Password security | Password hash |
| NFR-06 | Maintainability | Kode modular |
| NFR-07 | Reproducibility | Raw, processed, model, scaler, metrics disimpan |
| NFR-08 | Offline demo | Dashboard bisa jalan tanpa internet jika hasil sudah tersedia |
| NFR-09 | Error handling | Pesan error jelas jika file belum tersedia |
| NFR-10 | Scope control | Admin/auth sederhana saja |

---

# 12. Data Specification

## 12.1 Data Saham Raw

Path:
```text
data/raw/stock/BBCA_raw.csv
data/raw/stock/BBRI_raw.csv
```

Schema:
```csv
date,stock,open,high,low,close,volume
```

Contoh:
```csv
2023-01-02,BBCA,8550,8650,8500,8600,12345600
```

## 12.2 Data Berita Raw

Path:
```text
data/raw/news/news_raw.csv
```

Schema:
```csv
date,published_at,source,stock,keyword,title,summary,url,is_sector_news
```

## 12.3 Data Berita Processed

Path:
```text
data/processed/sentiment/news_processed.csv
```

Schema:
```csv
date,published_at,source,stock,title,summary,raw_text,clean_text,tokens,stemmed_text,sentiment_score,sentiment_label,url
```

## 12.4 Daily Sentiment

Path:
```text
data/processed/sentiment/BBCA_daily_sentiment.csv
data/processed/sentiment/BBRI_daily_sentiment.csv
```

Schema:
```csv
date,stock,total_news,avg_sentiment_score,total_sentiment_score,positive_count,neutral_count,negative_count
```

## 12.5 Baseline Dataset

Path:
```text
data/processed/fusion/BBCA_baseline_dataset.csv
data/processed/fusion/BBRI_baseline_dataset.csv
```

Schema:
```csv
date,stock,open,high,low,close,volume,target_close_h1
```

## 12.6 Hybrid Dataset

Path:
```text
data/processed/fusion/BBCA_hybrid_dataset.csv
data/processed/fusion/BBRI_hybrid_dataset.csv
```

Schema:
```csv
date,stock,open,high,low,close,volume,sentiment_score,target_close_h1
```

## 12.7 Prediction Result

Path:
```text
results/predictions/BBCA_baseline_predictions.csv
results/predictions/BBCA_hybrid_predictions.csv
results/predictions/BBRI_baseline_predictions.csv
results/predictions/BBRI_hybrid_predictions.csv
```

Schema:
```csv
date,stock,model,actual_close,predicted_close,error,absolute_error,absolute_percentage_error
```

## 12.8 Evaluation Metrics

Path:
```text
results/metrics/evaluation_metrics.csv
```

Schema:
```csv
stock,model,features,rmse,mae,mape,window_size,epochs,batch_size
```

## 12.9 Forecast H+7

Path:
```text
results/forecast/BBCA_baseline_forecast_h7.csv
results/forecast/BBCA_hybrid_forecast_h7.csv
results/forecast/BBRI_baseline_forecast_h7.csv
results/forecast/BBRI_hybrid_forecast_h7.csv
```

Schema:
```csv
step,stock,model,predicted_close,sentiment_assumption,forecast_type
```

---

# 13. Scraping Specification

## 13.1 Target Sumber

1. CNBC Indonesia.
2. Kontan.

## 13.2 Keyword

BBCA:
- BBCA
- Bank Central Asia
- BCA
- saham BBCA
- emiten BBCA

BBRI:
- BBRI
- Bank Rakyat Indonesia
- BRI
- saham BBRI
- emiten BBRI

Sektor:
- saham bank
- perbankan
- bank big cap
- suku bunga
- kredit perbankan
- NPL
- dividen bank

## 13.3 Output Minimal Scraper

Scraper harus menghasilkan:
- tanggal berita,
- jam publikasi jika tersedia,
- sumber,
- keyword pencarian,
- stock mapping,
- judul,
- ringkasan jika tersedia,
- URL.

## 13.4 Deduplikasi

Aturan:
1. Duplikat URL dihapus.
2. Duplikat judul setelah lowercase dan cleaning dihapus.
3. Jika berita sama muncul di dua keyword, simpan satu saja.
4. Jumlah sebelum dan sesudah deduplikasi dicatat.

## 13.5 Mitigasi Jika Scraping Sulit

Jika scraping historis 2023–2024 sulit:
1. Simpan hasil scraping yang berhasil.
2. Buat format CSV manual yang mengikuti schema.
3. Data tetap berasal dari CNBC/Kontan.
4. Dashboard dan training tetap menggunakan CSV lokal.
5. Jangan membuat dashboard bergantung pada live scraping.

---

# 14. Sentiment Scoring Specification

## 14.1 Preprocessing Teks

Pipeline:
1. Gabungkan `title` + `summary`.
2. Case folding.
3. Cleaning URL, angka tidak relevan, simbol, emoji.
4. Tokenisasi.
5. Stopword removal.
6. Stemming Sastrawi.
7. Simpan hasil.

## 14.2 Scoring

Gunakan InSet Lexicon.

Rumus sederhana:
```text
sentiment_score = jumlah bobot seluruh token yang ditemukan di kamus InSet
```

Rumus rata-rata:
```text
avg_sentiment_score = sentiment_score / jumlah_token_valid
```

Gunakan `avg_sentiment_score` sebagai fitur model agar skor tidak bias terhadap panjang teks.

## 14.3 Label

```text
score > 0  = positif
score = 0  = netral
score < 0  = negatif
```

## 14.4 Aggregation

Agregasi per tanggal dan emiten:
- total_news,
- avg_sentiment_score,
- total_sentiment_score,
- positive_count,
- neutral_count,
- negative_count.

---

# 15. Data Fusion Specification

Proses:
1. Load stock processed.
2. Load daily sentiment.
3. Merge berdasarkan `date` dan `stock`.
4. Gunakan left join dari data saham.
5. Jika sentiment kosong, isi 0.
6. Buat `target_close_h1 = close.shift(-1)`.
7. Hapus baris terakhir.
8. Simpan baseline dataset.
9. Simpan hybrid dataset.

Catatan:
- Baseline tidak memakai sentiment_score.
- Hybrid memakai sentiment_score.
- Data harus urut tanggal.

---

# 16. Model Specification

## 16.1 Baseline LSTM

Input:
```text
open, high, low, close, volume
```

Target:
```text
target_close_h1
```

Input shape:
```text
(samples, 30, 5)
```

## 16.2 Hybrid LSTM

Input:
```text
open, high, low, close, volume, sentiment_score
```

Target:
```text
target_close_h1
```

Input shape:
```text
(samples, 30, 6)
```

## 16.3 Hyperparameter Awal

| Parameter | Nilai |
|---|---:|
| Window size | 30 |
| LSTM units | 64 |
| Dropout | 0.2 |
| Dense output | 1 |
| Optimizer | Adam |
| Loss function | MSE |
| Epoch | 50 |
| Batch size | 32 |
| Split | 80:20 kronologis |

## 16.4 Arsitektur Minimal

```text
Input
→ LSTM(64)
→ Dropout(0.2)
→ Dense(1)
```

Opsional jika hasil buruk:
```text
Input
→ LSTM(64, return_sequences=True)
→ Dropout(0.2)
→ LSTM(32)
→ Dropout(0.2)
→ Dense(1)
```

AI Agent harus mulai dari arsitektur minimal dulu.

---

# 17. Evaluation Specification

Metrik:
1. RMSE.
2. MAE.
3. MAPE.

Rumus implementasi:
```python
rmse = sqrt(mean_squared_error(actual, predicted))
mae = mean_absolute_error(actual, predicted)
mape = mean(abs((actual - predicted) / actual)) * 100
```

Aturan interpretasi:
- Semakin kecil RMSE, semakin kecil error.
- Semakin kecil MAE, semakin kecil rata-rata error absolut.
- Semakin kecil MAPE, semakin kecil persentase error.
- Model Hybrid hanya boleh disebut lebih baik jika nilai error lebih rendah.
- Jangan menggunakan kata "signifikan" tanpa uji statistik.

---

# 18. Forecast H+7 Specification

## 18.1 Tujuan

Forecast H+7 digunakan hanya untuk visualisasi tambahan pada dashboard.

## 18.2 Hybrid Forecast

Karena sentimen masa depan tidak diketahui:
```text
future_sentiment = mean(sentiment_score 7 hari perdagangan terakhir)
```

Proses:
1. Ambil 30 hari terakhir.
2. Hitung rata-rata sentimen 7 hari terakhir.
3. Prediksi H+1.
4. Masukkan hasil prediksi ke sequence berikutnya.
5. Ulangi sampai H+7.
6. Simpan hasil forecast.
7. Tampilkan disclaimer.

## 18.3 Disclaimer

Tampilkan di dashboard:

> Forecast H+7 merupakan simulasi visualisasi berdasarkan model dan asumsi data terakhir. Hasil ini tidak digunakan sebagai dasar evaluasi akurasi utama dan bukan rekomendasi investasi.

---

# 19. UI/UX Specification

## 19.1 Branding

Nama:
```text
Sentilytics
```

Tagline:
```text
Hybrid LSTM Stock Prediction with Indonesian News Sentiment
```

## 19.2 Style

Gaya:
- Custom.
- Profesional.
- Mengikuti pola AdminLTE.
- Sidebar + topbar.
- Clean, modern, mudah dibaca.

## 19.3 Halaman

| Route | Halaman | Role |
|---|---|---|
| `/login` | Login | Guest |
| `/register` | Register | Guest |
| `/dashboard` | Dashboard utama | User/Admin |
| `/prediction` | Prediction Result | User/Admin |
| `/evaluation` | Model Evaluation | User/Admin |
| `/forecast` | Forecast Simulation | User/Admin |
| `/dataset-summary` | Dataset Summary | Admin |
| `/admin` | Admin Panel | Admin |
| `/logout` | Logout | User/Admin |

## 19.4 Sidebar User

```text
Dashboard
Prediction Result
Model Evaluation
Forecast Simulation
Logout
```

## 19.5 Sidebar Admin

```text
Dashboard
Prediction Result
Model Evaluation
Forecast Simulation
Dataset Summary
Admin Panel
Logout
```

## 19.6 Dashboard Components

1. Filter emiten.
2. Filter model.
3. Button tampilkan hasil.
4. Card prediksi H+1.
5. Card RMSE.
6. Card MAE.
7. Card MAPE.
8. Chart actual vs predicted.
9. Chart forecast H+7.
10. Tabel prediksi.
11. Disclaimer.

---

# 20. API Specification

## 20.1 User API

```http
GET /api/results?stock=BBCA&model=hybrid
```

Response:
```json
{
  "stock": "BBCA",
  "model": "Hybrid LSTM",
  "metrics": {
    "rmse": 123.45,
    "mae": 98.76,
    "mape": 1.23
  },
  "predictions": [
    {
      "date": "2024-10-01",
      "actual": 9500,
      "predicted": 9480
    }
  ]
}
```

```http
GET /api/forecast?stock=BBCA&model=hybrid
```

Response:
```json
{
  "stock": "BBCA",
  "model": "Hybrid LSTM",
  "forecast_type": "simulation",
  "sentiment_assumption": "7-day average sentiment",
  "data": [
    {
      "step": "H+1",
      "predicted_close": 9500
    }
  ]
}
```

## 20.2 Admin API

```http
GET /api/metrics
```

```http
GET /api/dataset-summary
```

```http
GET /api/model-status
```

---

# 21. Database Auth Specification

## 21.1 Table `users`

| Field | Type | Constraint |
|---|---|---|
| id | Integer | primary key |
| name | String | not null |
| email | String | unique, not null |
| password_hash | String | not null |
| role | String | user/admin |
| is_active | Boolean | default true |
| created_at | DateTime | default current timestamp |

## 21.2 Admin Seed

`.env`:
```env
SECRET_KEY=change-this-secret-key
ADMIN_EMAIL=admin@sentilytics.local
ADMIN_PASSWORD=ChangeThisPassword123
```

AI Agent harus:
1. Membaca admin email/password dari `.env`.
2. Membuat admin jika belum ada.
3. Tidak membuat duplikat admin.
4. Tidak hardcode password di source.

---

# 22. Struktur Folder Final

```text
sentilytics/
│
├── README.md
├── requirements.txt
├── .env.example
├── config.yaml
│
├── data/
│   ├── raw/
│   │   ├── stock/
│   │   └── news/
│   ├── processed/
│   │   ├── stock/
│   │   ├── sentiment/
│   │   └── fusion/
│   └── external/
│       └── inset_lexicon/
│
├── notebooks/
│   ├── 01_data_collection_stock.ipynb
│   ├── 02_data_collection_news.ipynb
│   ├── 03_text_preprocessing_sentiment.ipynb
│   ├── 04_data_fusion.ipynb
│   ├── 05_train_baseline_lstm.ipynb
│   ├── 06_train_hybrid_lstm.ipynb
│   └── 07_evaluation_visualization.ipynb
│
├── src/
│   ├── config.py
│   ├── data_collection/
│   │   ├── stock_downloader.py
│   │   ├── cnbc_scraper.py
│   │   └── kontan_scraper.py
│   ├── preprocessing/
│   │   ├── stock_preprocessing.py
│   │   ├── text_preprocessing.py
│   │   └── sequence_builder.py
│   ├── sentiment/
│   │   ├── inset_loader.py
│   │   └── sentiment_scorer.py
│   ├── modeling/
│   │   ├── lstm_model.py
│   │   ├── train_baseline.py
│   │   ├── train_hybrid.py
│   │   └── forecast.py
│   ├── evaluation/
│   │   ├── metrics.py
│   │   └── plots.py
│   └── utils/
│       ├── date_utils.py
│       └── file_utils.py
│
├── models/
│   ├── trained/
│   └── scalers/
│
├── results/
│   ├── predictions/
│   ├── metrics/
│   ├── forecast/
│   └── figures/
│
├── app/
│   ├── app.py
│   ├── models_db.py
│   ├── auth/
│   │   ├── routes.py
│   │   └── decorators.py
│   ├── admin/
│   │   └── routes.py
│   ├── dashboard/
│   │   └── routes.py
│   ├── services/
│   │   ├── prediction_service.py
│   │   ├── chart_service.py
│   │   ├── dataset_service.py
│   │   └── user_service.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── prediction.html
│   │   ├── evaluation.html
│   │   ├── forecast.html
│   │   └── admin_dashboard.html
│   └── static/
│       ├── css/
│       │   └── sentilytics.css
│       ├── js/
│       │   └── dashboard.js
│       └── img/
│
├── tests/
│   ├── test_text_preprocessing.py
│   ├── test_sentiment.py
│   ├── test_metrics.py
│   ├── test_sequence_builder.py
│   └── blackbox_test_plan.md
│
└── docs/
    ├── PRD_FINAL_AI_AGENT.md
    ├── TECHNICAL_SPEC.md
    ├── DATA_PIPELINE_SPEC.md
    ├── ML_EXPERIMENT_PLAN.md
    ├── UI_UX_SPEC.md
    └── TEST_PLAN.md
```

---

# 23. Implementation Milestones

## Milestone 1 — Project Setup

Deliverables:
- Struktur folder.
- Virtual environment.
- `requirements.txt`.
- `.env.example`.
- `config.yaml`.
- README awal.

Acceptance:
- Project dapat di-install.
- Folder utama tersedia.

## Milestone 2 — Flask Auth dan Layout

Deliverables:
- Flask app.
- Login page.
- Register page.
- Logout.
- SQLite users table.
- Admin seed.
- Base layout custom AdminLTE-style.

Acceptance:
- User dapat register/login/logout.
- Admin dapat login.
- Guest tidak bisa membuka dashboard.

## Milestone 3 — Stock Data Pipeline

Deliverables:
- `stock_downloader.py`.
- Raw stock CSV.
- Processed stock CSV.

Acceptance:
- BBCA dan BBRI periode 2023–2024 tersedia.

## Milestone 4 — News Scraping Pipeline

Deliverables:
- `cnbc_scraper.py`.
- `kontan_scraper.py`.
- Raw news CSV.
- Deduplicated news CSV.

Acceptance:
- Berita memiliki tanggal, judul, sumber, URL, stock mapping.

## Milestone 5 — Text Preprocessing dan Sentiment

Deliverables:
- `text_preprocessing.py`.
- `inset_loader.py`.
- `sentiment_scorer.py`.
- News processed CSV.
- Daily sentiment CSV.

Acceptance:
- Skor sentimen per berita dan harian tersedia.

## Milestone 6 — Data Fusion

Deliverables:
- Baseline dataset.
- Hybrid dataset.
- Target Close H+1.

Acceptance:
- Dataset siap untuk sequence LSTM.

## Milestone 7 — Modeling

Deliverables:
- LSTM model builder.
- Train baseline.
- Train hybrid.
- Empat model `.keras`.
- Empat scaler `.pkl`.

Acceptance:
- BBCA/BBRI baseline dan hybrid berhasil training.

## Milestone 8 — Evaluation

Deliverables:
- Prediction CSV.
- Metrics CSV.
- Actual vs predicted figures.

Acceptance:
- RMSE, MAE, MAPE tersedia untuk semua model.

## Milestone 9 — Forecast H+7

Deliverables:
- Forecast CSV.
- Forecast logic.
- Sentiment assumption record.

Acceptance:
- Forecast H+7 tersedia untuk dashboard.

## Milestone 10 — Dashboard Integration

Deliverables:
- Dashboard page.
- Prediction page.
- Evaluation page.
- Forecast page.
- Admin panel.
- API results/forecast/metrics.

Acceptance:
- User dapat melihat semua hasil dari dashboard.

## Milestone 11 — Testing dan Documentation

Deliverables:
- Unit tests.
- Black-box test plan.
- Black-box test result.
- README final.
- Screenshot dashboard.

Acceptance:
- Sistem siap demo lokal.

---

# 24. Black-Box Test Cases

| ID | Skenario | Input | Expected Result |
|---|---|---|---|
| TC-01 | Guest buka dashboard | `/dashboard` | Redirect login |
| TC-02 | Register user | name/email/password | Akun dibuat |
| TC-03 | Login user | email/password valid | Dashboard tampil |
| TC-04 | Login gagal | password salah | Error tampil |
| TC-05 | Logout | klik logout | Session berakhir |
| TC-06 | User buka admin | `/admin` | Access denied |
| TC-07 | Admin buka admin | admin login | Admin panel tampil |
| TC-08 | Pilih BBCA Baseline | BBCA + baseline | Metrik/grafik tampil |
| TC-09 | Pilih BBCA Hybrid | BBCA + hybrid | Metrik/grafik tampil |
| TC-10 | Pilih BBRI Baseline | BBRI + baseline | Metrik/grafik tampil |
| TC-11 | Pilih BBRI Hybrid | BBRI + hybrid | Metrik/grafik tampil |
| TC-12 | Forecast H+7 | pilih emiten/model | 7 data forecast tampil |
| TC-13 | File tidak ada | hapus file result | Pesan error ramah tampil |
| TC-14 | Disclaimer | buka dashboard | Disclaimer tampil |

---

# 25. Acceptance Criteria Final

Program dianggap selesai jika:

1. Project dapat dijalankan dari localhost.
2. Login/register/logout berjalan.
3. Admin account dapat dibuat dan digunakan.
4. Dashboard terlindungi login.
5. Admin panel terlindungi role admin.
6. Data saham BBCA dan BBRI tersedia.
7. Data berita CNBC/Kontan tersedia dari proses scraping atau CSV hasil scraping.
8. Preprocessing teks berjalan.
9. Sentiment scoring InSet berjalan.
10. Daily sentiment per emiten tersedia.
11. Dataset baseline dan hybrid tersedia.
12. Empat model LSTM berhasil dilatih.
13. RMSE, MAE, MAPE tersedia.
14. Actual vs predicted tersedia.
15. Forecast H+7 tersedia.
16. Dashboard menampilkan hasil sesuai filter emiten/model.
17. Dashboard menampilkan disclaimer bukan rekomendasi investasi.
18. Admin panel menampilkan ringkasan sistem.
19. Black-box testing terdokumentasi.
20. README menjelaskan cara install dan run.

---

# 26. Prompt Final untuk AI Agent Coding

Gunakan prompt berikut saat mulai membangun di IDE AI Agent:

```text
Kamu adalah AI Agent pengembang aplikasi skripsi Informatika/Artificial Intelligence.

Bangun aplikasi bernama Sentilytics dari awal sampai selesai.

Deskripsi:
Sentilytics adalah sistem prediksi harga saham perbankan berbasis Hybrid LSTM dan sentimen berita Indonesia. Sistem membandingkan Baseline LSTM dan Hybrid LSTM untuk memprediksi Close Price H+1 saham BBCA dan BBRI. Sistem memiliki dashboard Flask dengan login, register, admin account, grafik actual vs predicted, metrik RMSE/MAE/MAPE, dan simulasi forecast H+7.

Stack:
- Python 3.10/3.11
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite untuk auth
- HTML/CSS/JavaScript custom AdminLTE-style
- pandas, numpy
- yfinance
- requests, BeautifulSoup4, feedparser
- Sastrawi
- InSet Lexicon
- scikit-learn
- TensorFlow/Keras LSTM
- Chart.js atau Plotly.js
- joblib
- pytest

Scope:
- Saham: BBCA.JK dan BBRI.JK
- Periode: 1 Januari 2023 sampai 31 Desember 2024
- Data saham: OHLCV harian
- Data berita: CNBC Indonesia dan Kontan, scraping dari nol
- Preprocessing teks: case folding, cleaning, stopword removal, tokenisasi, stemming Sastrawi
- Sentiment scoring: InSet Lexicon
- Baseline LSTM: OHLCV
- Hybrid LSTM: OHLCV + sentiment_score
- Target: Close H+1
- Evaluasi: RMSE, MAE, MAPE
- Forecast H+7: simulasi visualisasi, bukan evaluasi utama
- Hybrid forecast sentiment: rata-rata sentiment_score tujuh hari perdagangan terakhir
- Dashboard: localhost
- Hosting: opsional setelah lokal stabil

Aturan:
- Jangan membuat fitur rekomendasi investasi.
- Jangan membuat buy/sell/hold signal.
- Jangan training model dari route Flask.
- Simpan dataset sebagai CSV.
- Simpan model sebagai .keras.
- Simpan scaler sebagai .pkl.
- Split data secara kronologis.
- Jangan shuffle time-series.
- Fit scaler hanya pada train.
- Dashboard harus membaca file hasil training.
- UI harus custom profesional mengikuti pola AdminLTE, bukan template mentah.
- Tambahkan disclaimer bahwa hasil bukan rekomendasi investasi.

Mulai dari:
1. Buat struktur folder final.
2. Setup Flask + auth + admin seed.
3. Buat layout Sentilytics custom.
4. Buat pipeline yfinance.
5. Buat scraper CNBC/Kontan.
6. Buat preprocessing teks dan sentiment scoring.
7. Buat data fusion.
8. Buat training baseline/hybrid.
9. Buat evaluasi dan forecast.
10. Integrasikan ke dashboard.
11. Buat testing dan README.
```

---

# 27. Penutup

Dokumen ini adalah acuan final untuk AI Agent. Semua implementasi harus mengacu pada dokumen ini agar program Sentilytics tetap konsisten dengan kebutuhan skripsi, fokus pada Artificial Intelligence, dan tidak melebar menjadi aplikasi investasi.