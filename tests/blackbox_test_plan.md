# Sentilytics — Black-Box Test Plan

## Overview
Pengujian black-box dilakukan untuk memverifikasi fungsionalitas sistem Sentilytics dari perspektif pengguna tanpa melihat kode internal.

## Environment
- OS: Windows 10/11
- Browser: Chrome / Firefox / Edge
- URL: http://127.0.0.1:5000

---

## Test Cases

| ID | Skenario | Input | Expected Result | Status | Notes |
|------|------|------|------|------|------|
| TC-01 | Guest buka dashboard | Akses `/dashboard` tanpa login | Redirect ke halaman login | ☐ | |
| TC-02 | Register user baru | Isi name, email, password valid | Akun berhasil dibuat, redirect ke login | ☐ | |
| TC-03 | Login user valid | Email dan password valid | Dashboard tampil | ☐ | |
| TC-04 | Login gagal | Password salah | Pesan error "Email atau password salah" | ☐ | |
| TC-05 | Logout user | Klik tombol logout | Session berakhir, redirect ke login | ☐ | |
| TC-06 | User buka admin panel | User biasa akses `/admin` | Access denied (403) | ☐ | |
| TC-07 | Admin buka admin panel | Login sebagai admin, buka `/admin` | Admin panel tampil lengkap | ☐ | |
| TC-08 | Pilih BBCA Baseline | Dashboard: pilih BBCA + Baseline LSTM | Metrik, grafik, dan tabel tampil | ☐ | |
| TC-09 | Pilih BBCA Hybrid | Dashboard: pilih BBCA + Hybrid LSTM | Metrik, grafik, dan tabel tampil | ☐ | |
| TC-10 | Pilih BBRI Baseline | Dashboard: pilih BBRI + Baseline LSTM | Metrik, grafik, dan tabel tampil | ☐ | |
| TC-11 | Pilih BBRI Hybrid | Dashboard: pilih BBRI + Hybrid LSTM | Metrik, grafik, dan tabel tampil | ☐ | |
| TC-12 | Forecast H+7 tampil | Buka halaman forecast, pilih emiten dan model | 7 data forecast tampil di tabel dan grafik | ☐ | |
| TC-13 | File tidak ada | Hapus satu file result | Pesan ramah "data belum tersedia" tampil | ☐ | |
| TC-14 | Disclaimer tampil | Buka halaman dashboard | Disclaimer "bukan rekomendasi investasi" muncul | ☐ | |

---

## Test Result Summary

| Total | Passed | Failed | Not Tested |
|-------|--------|--------|------------|
| 14 | 0 | 0 | 14 |

**Tanggal Pengujian:** _________________

**Tester:** _________________

---

## Catatan
- Semua test dilakukan pada localhost
- Database SQLite hanya berisi data user/auth
- Dashboard membaca file CSV/JSON hasil training
- Sistem tidak memberikan rekomendasi investasi
