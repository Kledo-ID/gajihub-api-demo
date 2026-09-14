# Demo API GajiHub (PHP)

Setiap file berdiri sendiri: **tanpa Composer**, tanpa file bantu lain. Cukup PHP dengan ekstensi `curl`.

## Persiapan

| Kebutuhan | Keterangan |
|---|---|
| **PHP 8.1 atau lebih baru** | Paling mudah pakai [XAMPP](https://www.apachefriends.org/download.html) (sudah berisi PHP). Cek dengan `php --version`. |
| **Ekstensi curl aktif** | Cek dengan `php -m`, pastikan ada tulisan `curl`. |

## Menjalankan Demo

1. Buka file demo, lalu isi 2 baris di bagian **Konfigurasi**:

   ```php
   const API_HOST     = 'https://namaperusahaan.api.kledo.com/api/v1';
   const ACCESS_TOKEN = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx';
   ```

2. Jalankan lewat terminal:

   ```bash
   cd php/01-authentication
   php 01-check-token.php
   ```

Mulailah dari `01-authentication/01-check-token.php` untuk memastikan token sudah benar.
File Excel hasil export tersimpan di folder `hasil-unduhan/` di sebelah file demo.

Filter tambahan sudah disiapkan dalam bentuk komentar `//`. Hapus tanda `//` untuk mengaktifkannya.

> Menulis token langsung di file hanya untuk mencoba. Untuk aplikasi sungguhan, simpan token di `.env`,
> lihat contoh Laravel di [01-authentication/laravel/](01-authentication/laravel/).

## Daftar Demo

Lihat [README utama](../README.md#daftar-demo). Nama file sama untuk semua bahasa, dengan akhiran `.php`.

## Unduh Laporan Otomatis

```bash
# Laporan kemarin
php php/11-scheduled-download/download-attendance-reports.php

# Laporan rentang tanggal tertentu
php php/11-scheduled-download/download-attendance-reports.php 2026-09-01 2026-09-30
```

**Windows (Task Scheduler)**

1. Buka **Task Scheduler**, lalu klik **Create Basic Task**.
2. Isi nama, contoh `Unduh Absensi GajiHub`, lalu pilih **Daily** dan tentukan jam (contoh `06:00`).
3. Pilih **Start a program**, lalu isi:
   - **Program/script**: `C:\xampp\php\php.exe`
   - **Add arguments**: `download-attendance-reports.php`
   - **Start in**: folder tempat file tersebut, contoh `C:\gajihub-api-demo\php\11-scheduled-download`
4. Klik **Finish**.

**Linux / macOS (cron)** — jalankan `crontab -e`, lalu tambahkan (setiap hari jam 06:00):

```text
0 6 * * * php /lokasi/gajihub-api-demo/php/11-scheduled-download/download-attendance-reports.php >> /var/log/unduh-absensi.log 2>&1
```

## Kendala Khusus PHP

Kendala umum (401, 403, dll) ada di [README utama](../README.md#jika-terjadi-kendala).

| Pesan | Solusi |
|---|---|
| `'php' is not recognized` / `command not found` | PHP belum ada di PATH. Pakai lokasi lengkap, contoh `C:\xampp\php\php.exe 01-check-token.php`. |
| `Call to undefined function curl_init()` | Ekstensi curl belum aktif. Buka `php.ini`, hapus tanda `;` di depan `extension=curl`. |
| `SSL certificate problem: unable to get local issuer certificate` | PHP belum punya sertifikat CA. Unduh [cacert.pem](https://curl.se/ca/cacert.pem) ke `C:\xampp\php\cacert.pem`, lalu isi `curl.cainfo = "C:\xampp\php\cacert.pem"` di `php.ini`. |
| `syntax error, unexpected ...` | Versi PHP terlalu lama. Gunakan PHP 8.1 atau lebih baru. |
