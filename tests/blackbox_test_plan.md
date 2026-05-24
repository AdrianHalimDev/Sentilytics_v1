# Sentilytics — Black-Box Test Plan

## Overview
Pengujian black-box dilakukan untuk memverifikasi fungsionalitas sistem Sentilytics dari perspektif pengguna tanpa melihat kode internal.

## Environment
- OS: Windows 10/11
- Browser: Chrome / Firefox / Edge
- URL: http://127.0.0.1:5000
- Python: 3.10.11
- Flask: Development Server

---

## Test Cases

| ID | Skenario | Input | Expected Result | Actual Result | Status | Notes |
|------|------|------|------|------|------|------|
| TC-01 | Guest buka dashboard | Akses `/dashboard` tanpa login | Redirect ke halaman login | HTTP 302 redirect ke `/login?next=%2Fdashboard` | ✅ Passed | Redirect berfungsi dengan benar |
| TC-02 | Register user baru | Isi name, email, password valid | Akun berhasil dibuat, redirect ke login | HTTP 302 redirect ke `/login`, akun berhasil dibuat | ✅ Passed | Validasi form berjalan |
| TC-03 | Login user valid | Email dan password valid | Dashboard tampil | Dashboard tampil di `/dashboard`, pesan selamat datang muncul | ✅ Passed | Session berhasil dibuat |
| TC-04 | Login gagal | Password salah | Pesan error "Email atau password salah" | Pesan error "Email atau password salah" tampil | ✅ Passed | Pesan error sesuai |
| TC-05 | Logout user | Klik tombol logout | Session berakhir, redirect ke login | HTTP 302 redirect ke `/login`, session berakhir | ✅ Passed | Session berhasil dihapus |
| TC-06 | User biasa akses admin panel | User non-admin akses `/admin` | Access denied (403) | HTTP 403 Forbidden ditampilkan | ✅ Passed | Proteksi role admin berfungsi |
| TC-07 | Admin buka admin panel | Login sebagai admin, buka `/admin` | Admin panel tampil lengkap | Admin panel tampil dengan data users, model status, dan metrics | ✅ Passed | Semua komponen admin tampil |
| TC-08 | Pilih BBCA Baseline | Dashboard: pilih BBCA + Baseline LSTM | Metrik, grafik, dan tabel tampil | Data BBCA Baseline tampil lengkap dengan RMSE, MAE, MAPE | ✅ Passed | Chart.js grafik render OK |
| TC-09 | Pilih BBCA Hybrid | Dashboard: pilih BBCA + Hybrid LSTM | Metrik, grafik, dan tabel tampil | Data BBCA Hybrid tampil lengkap dengan RMSE, MAE, MAPE | ✅ Passed | Chart.js grafik render OK |
| TC-10 | Pilih BBRI Baseline | Dashboard: pilih BBRI + Baseline LSTM | Metrik, grafik, dan tabel tampil | Data BBRI Baseline tampil lengkap dengan RMSE, MAE, MAPE | ✅ Passed | Chart.js grafik render OK |
| TC-11 | Pilih BBRI Hybrid | Dashboard: pilih BBRI + Hybrid LSTM | Metrik, grafik, dan tabel tampil | Data BBRI Hybrid tampil lengkap dengan RMSE, MAE, MAPE | ✅ Passed | Chart.js grafik render OK |
| TC-12 | Forecast H+7 tampil | Buka halaman forecast, pilih emiten dan model | 7 data forecast tampil di tabel dan grafik | Forecast H+1 sampai H+7 tampil dengan predicted close dan sentiment assumption | ✅ Passed | Forecast adalah simulasi |
| TC-13 | Dataset summary tampil | Akses halaman dataset summary | Ringkasan jumlah data saham, berita, dan fusion tampil | Halaman dataset summary tampil dengan statistik lengkap | ✅ Passed | Semua data summary tersedia |
| TC-14 | Disclaimer tampil | Buka halaman dashboard | Disclaimer "bukan rekomendasi investasi" muncul | Disclaimer terkait investasi ditemukan di halaman dashboard | ✅ Passed | Disclaimer sesuai ketentuan |

---

## Test Result Summary

| Total | Passed | Failed | Not Tested |
|-------|--------|--------|------------|
| 14 | 14 | 0 | 0 |

**Tanggal Pengujian:** 24 Mei 2026

**Tester:** Automated + Manual Verification

---

## Catatan
- Semua test dilakukan pada localhost (http://127.0.0.1:5000)
- Database SQLite hanya berisi data user/auth
- Dashboard membaca file CSV/JSON hasil training
- Sistem tidak memberikan rekomendasi investasi
- Pengujian dilakukan menggunakan automated HTTP requests via Python requests library
- Seluruh 14 test case berhasil passed tanpa error
