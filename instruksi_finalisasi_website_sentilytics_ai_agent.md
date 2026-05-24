# Instruksi Detail untuk AI Agent — Finalisasi Website Sentilytics Sebelum Bab 4

## Konteks Project

Project ini adalah aplikasi skripsi Informatika peminatan Artificial Intelligence bernama **Sentilytics**. Sistem digunakan untuk memprediksi harga saham perbankan BBCA dan BBRI menggunakan:

1. **Baseline LSTM**
   - Fitur input: Open, High, Low, Close, Volume (OHLCV)
   - Target: Close Price H+1

2. **Hybrid LSTM**
   - Fitur input: Open, High, Low, Close, Volume, dan skor sentimen berita
   - Target: Close Price H+1

Evaluasi utama model menggunakan:
- RMSE
- MAE
- MAPE

Dashboard web dibuat menggunakan Flask dan Chart.js. Forecast sampai H+7 hanya digunakan sebagai fitur simulasi visualisasi, bukan evaluasi utama akurasi model.

## Status Saat Ini

Website/prototype sudah aman sebagai dasar skripsi dan sudah dapat dipakai untuk mulai menyusun Bab 4. Namun, sebelum dianggap final untuk sidang, masih ada 3 hal wajib yang perlu diselesaikan:

1. Perbaiki bagian forecast Hybrid H+7.
2. Isi black-box testing.
3. Ambil screenshot website untuk Bab 4 dan lampiran.

---

# 1. Perbaikan Forecast Hybrid H+7

## Masalah

Pada file:

```text
src/modeling/forecast.py
```

masih terdapat bagian kode:

```python
pass  # Keep last known scaled sentiment value
```

Masalahnya adalah sistem sudah menghitung `sentiment_assumption`, yaitu rata-rata skor sentimen 7 hari terakhir, tetapi nilai tersebut belum benar-benar dimasukkan ke fitur `sentiment_score` pada sequence input model Hybrid LSTM.

Dengan kondisi ini, secara tampilan forecast terlihat menggunakan rata-rata sentimen 7 hari terakhir, tetapi secara teknis input model masih mempertahankan nilai sentimen terakhir yang sudah ada pada sequence.

## Tujuan Perbaikan

Pastikan pada mode Hybrid LSTM, nilai rata-rata sentimen 7 hari terakhir benar-benar masuk ke fitur `sentiment_score` pada setiap step forecast H+1 sampai H+7.

## Instruksi Teknis

Cari bagian di `src/modeling/forecast.py` yang berisi:

```python
pass  # Keep last known scaled sentiment value
```

Ganti dengan kode berikut:

```python
if model_type == "hybrid" and sentiment_assumption is not None:
    sent_idx = feature_columns.index("sentiment_score")

    sent_min = scaler.data_min_[sent_idx]
    sent_max = scaler.data_max_[sent_idx]

    if sent_max != sent_min:
        scaled_sentiment = (sentiment_assumption - sent_min) / (sent_max - sent_min)
    else:
        scaled_sentiment = 0

    new_row[sent_idx] = scaled_sentiment
```

## Catatan Penting

1. Pastikan nama kolom pada `feature_columns` benar-benar `sentiment_score`.
2. Jika pada project nama kolomnya `Sentiment_Score`, sesuaikan kode menjadi:

```python
sent_idx = feature_columns.index("Sentiment_Score")
```

3. Jangan mengubah logika evaluasi utama H+1.
4. Forecast H+7 tetap hanya fitur simulasi visualisasi.
5. Jangan menghitung RMSE/MAE/MAPE untuk forecast H+7 kecuali tersedia data aktual masa depan.

## Setelah Perbaikan

Jalankan ulang forecast:

```bash
python -m src.modeling.forecast
```

atau jika project menggunakan command lain:

```bash
python run_pipeline.py --forecast-only
```

Jika command `--forecast-only` tidak tersedia, cukup jalankan module forecast sesuai struktur project.

## Output yang Diharapkan

Pastikan file forecast diperbarui, misalnya:

```text
results/forecast/BBCA_baseline_forecast_h7.csv
results/forecast/BBCA_hybrid_forecast_h7.csv
results/forecast/BBRI_baseline_forecast_h7.csv
results/forecast/BBRI_hybrid_forecast_h7.csv
```

atau sesuai struktur folder project yang sudah ada.

## Validasi

Cek file forecast Hybrid dan pastikan ada informasi asumsi sentimen, misalnya:

```text
sentiment_assumption
```

atau kolom sejenis yang menunjukkan rata-rata sentimen 7 hari terakhir.

## Narasi Metodologi untuk Bab 4

Gunakan narasi berikut:

> Pada fitur simulasi forecast sampai H+7, skor sentimen untuk hari perdagangan masa depan pada Model Hybrid LSTM diasumsikan menggunakan rata-rata skor sentimen tujuh hari perdagangan terakhir. Asumsi ini digunakan karena data berita pada tanggal masa depan belum tersedia saat prediksi dilakukan. Forecast H+7 hanya digunakan sebagai fitur visualisasi tambahan pada dashboard Flask, sedangkan evaluasi akurasi utama tetap dilakukan pada prediksi H+1 menggunakan data uji historis.

---

# 2. Pengisian Black-Box Testing

## Masalah

File:

```text
tests/blackbox_test_plan.md
```

masih belum diisi hasil pengujiannya. Status masih:

```text
Total: 14
Passed: 0
Failed: 0
Not Tested: 14
```

Ini belum bisa dipakai untuk Bab 4 karena belum menunjukkan hasil pengujian sistem.

## Tujuan

Isi seluruh test case black-box berdasarkan pengujian langsung pada website Flask.

## Instruksi Pengujian

Jalankan aplikasi:

```bash
python run.py
```

Buka browser:

```text
http://127.0.0.1:5000
```

Lakukan pengujian satu per satu terhadap fitur berikut:

## Daftar Test Case yang Perlu Diuji

### TC-01 — Membuka Halaman Login

- Input: akses halaman login.
- Expected result: halaman login tampil.
- Status: Passed jika halaman login tampil normal.

### TC-02 — Register User Baru

- Input: isi form register dengan data valid.
- Expected result: akun berhasil dibuat atau sistem menampilkan pesan sukses.
- Status: Passed jika register berhasil.

### TC-03 — Login User

- Input: email/username dan password valid.
- Expected result: user berhasil masuk ke dashboard.
- Status: Passed jika dashboard tampil setelah login.

### TC-04 — Login dengan Data Salah

- Input: username/password salah.
- Expected result: sistem menampilkan pesan error.
- Status: Passed jika akses ditolak.

### TC-05 — Menampilkan Dashboard Utama

- Input: akses dashboard setelah login.
- Expected result: dashboard utama tampil.
- Status: Passed jika dashboard tampil lengkap.

### TC-06 — Memilih Emiten BBCA

- Input: pilih BBCA.
- Expected result: sistem menampilkan data/grafik BBCA.
- Status: Passed jika data BBCA tampil.

### TC-07 — Memilih Emiten BBRI

- Input: pilih BBRI.
- Expected result: sistem menampilkan data/grafik BBRI.
- Status: Passed jika data BBRI tampil.

### TC-08 — Menampilkan Evaluasi Baseline LSTM

- Input: pilih model Baseline LSTM.
- Expected result: grafik actual vs predicted dan metrik RMSE/MAE/MAPE tampil.
- Status: Passed jika semua output tampil.

### TC-09 — Menampilkan Evaluasi Hybrid LSTM

- Input: pilih model Hybrid LSTM.
- Expected result: grafik actual vs predicted dan metrik RMSE/MAE/MAPE tampil.
- Status: Passed jika semua output tampil.

### TC-10 — Menampilkan Forecast H+7

- Input: akses halaman forecast atau pilih fitur forecast.
- Expected result: tabel/grafik forecast H+1 sampai H+7 tampil.
- Status: Passed jika forecast tampil.

### TC-11 — Menampilkan Dataset Summary

- Input: akses menu dataset summary.
- Expected result: ringkasan jumlah data saham, berita, dan fusion tampil.
- Status: Passed jika informasi dataset muncul.

### TC-12 — Admin Login

- Input: login menggunakan akun admin.
- Expected result: admin berhasil mengakses admin panel.
- Status: Passed jika admin panel tampil.

### TC-13 — User Biasa Mengakses Admin Panel

- Input: user non-admin mencoba akses admin panel.
- Expected result: sistem menolak akses atau menampilkan halaman 403.
- Status: Passed jika akses ditolak.

### TC-14 — Logout

- Input: klik logout.
- Expected result: user keluar dari sistem dan kembali ke halaman login.
- Status: Passed jika sesi login berakhir.

## Format Tabel Black-Box Testing untuk Bab 4

Gunakan format berikut:

| No | Skenario Pengujian | Input | Hasil yang Diharapkan | Hasil Aktual | Status |
|---:|---|---|---|---|---|
| 1 | Membuka halaman login | Akses `/login` | Halaman login tampil | Halaman login tampil | Berhasil |
| 2 | Register user baru | Data user valid | Akun berhasil dibuat | Akun berhasil dibuat | Berhasil |
| 3 | Login user | Akun valid | Dashboard tampil | Dashboard tampil | Berhasil |
| 4 | Login gagal | Password salah | Pesan error tampil | Pesan error tampil | Berhasil |
| 5 | Menampilkan dashboard | Akses `/dashboard` | Dashboard tampil | Dashboard tampil | Berhasil |
| 6 | Memilih BBCA | Pilih BBCA | Data BBCA tampil | Data BBCA tampil | Berhasil |
| 7 | Memilih BBRI | Pilih BBRI | Data BBRI tampil | Data BBRI tampil | Berhasil |
| 8 | Evaluasi Baseline | Pilih Baseline | Grafik dan metrik tampil | Grafik dan metrik tampil | Berhasil |
| 9 | Evaluasi Hybrid | Pilih Hybrid | Grafik dan metrik tampil | Grafik dan metrik tampil | Berhasil |
| 10 | Forecast H+7 | Akses forecast | Forecast tampil | Forecast tampil | Berhasil |
| 11 | Dataset summary | Akses summary | Ringkasan dataset tampil | Ringkasan dataset tampil | Berhasil |
| 12 | Login admin | Akun admin | Admin panel tampil | Admin panel tampil | Berhasil |
| 13 | Akses admin oleh user biasa | Akun non-admin | Akses ditolak | Akses ditolak | Berhasil |
| 14 | Logout | Klik logout | Sesi berakhir | Sesi berakhir | Berhasil |

## Setelah Testing

Update file:

```text
tests/blackbox_test_plan.md
```

Isi:
- tanggal pengujian,
- nama tester,
- status setiap test case,
- catatan jika ada error,
- ringkasan total Passed/Failed.

Contoh ringkasan:

```text
Total Test Case: 14
Passed: 14
Failed: 0
Not Tested: 0
```

---

# 3. Screenshot Website untuk Bab 4 dan Lampiran

## Tujuan

Screenshot diperlukan sebagai bukti visual bahwa sistem benar-benar sudah diimplementasikan dan berjalan.

## Screenshot Wajib untuk Bab 4

Minimal masukkan screenshot berikut ke Bab 4:

### 1. Halaman Login

File disarankan:

```text
docs/screenshots/01_login_page.png
```

Tujuan:
- membuktikan sistem memiliki autentikasi pengguna.

### 2. Dashboard Utama

File disarankan:

```text
docs/screenshots/02_dashboard_utama.png
```

Tujuan:
- menunjukkan tampilan utama sistem setelah login.

### 3. Halaman Evaluasi Model

File disarankan:

```text
docs/screenshots/03_evaluation_page.png
```

Harus terlihat:
- pilihan emiten,
- model Baseline/Hybrid,
- grafik actual vs predicted,
- RMSE,
- MAE,
- MAPE.

### 4. Halaman Forecast H+7

File disarankan:

```text
docs/screenshots/04_forecast_h7.png
```

Harus terlihat:
- hasil forecast H+1 sampai H+7,
- grafik forecast,
- keterangan bahwa forecast adalah simulasi.

### 5. Dataset Summary

File disarankan:

```text
docs/screenshots/05_dataset_summary.png
```

Harus terlihat:
- jumlah data saham,
- jumlah data berita,
- jumlah data fusion,
- distribusi emiten/sumber jika tersedia.

### 6. Admin Panel

File disarankan:

```text
docs/screenshots/06_admin_panel.png
```

Tujuan:
- menunjukkan fitur manajemen/admin jika memang ada di sistem.

### 7. Hasil Unit Test

File disarankan:

```text
docs/screenshots/07_unit_test_46_passed.png
```

Jalankan:

```bash
pytest tests/ -v
```

Screenshot terminal yang menunjukkan:

```text
46 passed
```

### 8. Terminal Flask Berjalan

File disarankan:

```text
docs/screenshots/08_flask_running.png
```

Screenshot terminal setelah menjalankan:

```bash
python run.py
```

dan terlihat server berjalan di:

```text
http://127.0.0.1:5000
```

## Screenshot Opsional untuk Lampiran

Masukkan ke lampiran jika ingin lebih lengkap:

1. Register page.
2. Halaman 403 access denied.
3. Dashboard BBCA Baseline.
4. Dashboard BBCA Hybrid.
5. Dashboard BBRI Baseline.
6. Dashboard BBRI Hybrid.
7. Grafik comparison baseline vs hybrid.
8. Struktur folder project.
9. File hasil evaluasi `evaluation_metrics.csv`.

## Struktur Folder Screenshot

Buat folder:

```text
docs/screenshots/
```

atau:

```text
documentation/screenshots/
```

Simpan dengan nama rapi:

```text
01_login_page.png
02_register_page.png
03_dashboard_utama.png
04_evaluation_bbca_hybrid.png
05_evaluation_bbri_hybrid.png
06_forecast_h7.png
07_dataset_summary.png
08_admin_panel.png
09_unit_test_46_passed.png
10_flask_running.png
```

---

# 4. Validasi Akhir Setelah 3 Hal Selesai

Setelah forecast diperbaiki, black-box testing diisi, dan screenshot tersedia, jalankan checklist berikut:

## Checklist Teknis

- [ ] Aplikasi Flask bisa dijalankan dengan `python run.py`.
- [ ] Login berhasil.
- [ ] Register berhasil.
- [ ] Dashboard tampil.
- [ ] Grafik Chart.js tampil.
- [ ] Evaluasi BBCA Baseline tampil.
- [ ] Evaluasi BBCA Hybrid tampil.
- [ ] Evaluasi BBRI Baseline tampil.
- [ ] Evaluasi BBRI Hybrid tampil.
- [ ] Forecast H+7 tampil.
- [ ] Dataset summary tampil.
- [ ] Admin panel tampil untuk admin.
- [ ] Admin panel tidak bisa diakses user biasa.
- [ ] Logout berhasil.
- [ ] Unit test berhasil.
- [ ] Black-box testing selesai.

## Checklist Dokumen Bab 4

- [ ] Tabel jumlah data saham.
- [ ] Tabel jumlah data berita.
- [ ] Tabel preprocessing teks.
- [ ] Tabel skor sentimen.
- [ ] Tabel dataset fusion.
- [ ] Tabel hyperparameter model.
- [ ] Tabel evaluasi RMSE, MAE, MAPE.
- [ ] Grafik actual vs predicted.
- [ ] Screenshot dashboard.
- [ ] Screenshot forecast.
- [ ] Tabel black-box testing.

---

# 5. Catatan Narasi Akademik

## Hindari Kalimat Ini

Jangan gunakan:

> Model Hybrid terbukti signifikan lebih baik.

Kecuali ada uji statistik.

## Gunakan Kalimat Ini

Gunakan:

> Model Hybrid LSTM menunjukkan nilai RMSE, MAE, dan MAPE yang lebih rendah dibandingkan Model Baseline LSTM pada data uji.

## Disclaimer Investasi

Pastikan tertulis:

> Sistem ini tidak dimaksudkan sebagai rekomendasi investasi, melainkan sebagai prototipe visualisasi hasil model prediksi berbasis Artificial Intelligence.

## Forecast H+7

Pastikan tertulis:

> Forecast H+7 digunakan sebagai fitur simulasi visualisasi dan tidak dijadikan dasar utama evaluasi akurasi model.

---

# 6. Output Final yang Diharapkan dari AI Agent

AI Agent harus menghasilkan atau memperbarui:

1. `src/modeling/forecast.py` yang sudah benar memasukkan sentiment assumption ke input Hybrid forecast.
2. File forecast H+7 terbaru.
3. `tests/blackbox_test_plan.md` yang sudah terisi.
4. Folder screenshot website.
5. Ringkasan hasil pengujian.
6. Tidak mengubah evaluasi utama H+1.
7. Tidak mengubah hasil training kecuali memang diperlukan.
8. Tidak menghapus disclaimer bukan rekomendasi investasi.
9. Tidak menambahkan klaim “signifikan” tanpa uji statistik.

---

# 7. Perintah Ringkas untuk AI Agent

Gunakan prompt berikut:

```text
Tolong finalisasi project Sentilytics sebelum penulisan Bab 4.

Fokus pekerjaan:
1. Perbaiki file src/modeling/forecast.py agar forecast Hybrid H+7 benar-benar memasukkan rata-rata skor sentimen 7 hari terakhir ke fitur sentiment_score pada sequence input model. Jangan hanya menampilkan sentiment_assumption di output. Gunakan scaler fitur yang sama agar nilai sentiment_assumption masuk dalam skala yang benar.

2. Jalankan ulang proses forecast H+7 dan pastikan file forecast terbaru tersimpan untuk BBCA dan BBRI, baik Baseline maupun Hybrid.

3. Jalankan unit test dengan pytest tests/ -v dan pastikan hasilnya tetap passed.

4. Jalankan aplikasi Flask dengan python run.py dan pastikan halaman login, register, dashboard, evaluation, forecast, dataset summary, dan admin panel berjalan.

5. Isi tests/blackbox_test_plan.md berdasarkan pengujian manual. Semua test case harus memiliki status Passed atau Failed, tanggal pengujian, tester, dan catatan singkat.

6. Buat folder docs/screenshots/ lalu simpan screenshot:
   - login page,
   - register page,
   - dashboard utama,
   - evaluation page,
   - forecast H+7,
   - dataset summary,
   - admin panel,
   - 403/access denied untuk user biasa jika tersedia,
   - terminal Flask running,
   - hasil unit test 46 passed.

Catatan metodologi:
- Evaluasi utama tetap Close Price H+1.
- Forecast H+7 hanya simulasi visualisasi.
- Jangan menghitung RMSE/MAE/MAPE untuk forecast H+7.
- Jangan mengubah hasil training model kecuali diperlukan.
- Jangan menghapus disclaimer bahwa sistem bukan rekomendasi investasi.
- Hindari klaim “signifikan” karena tidak ada uji statistik.
```
