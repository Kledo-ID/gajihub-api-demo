# Demo API GajiHub (Python)

Setiap file berdiri sendiri: **tanpa `pip install`**, tanpa file bantu lain. Hanya memakai library bawaan Python.

## Persiapan

**Python 3.8 atau lebih baru.** Cek dengan `python --version` (di macOS/Linux: `python3 --version`).

## Menjalankan Demo

1. Buka file demo, lalu isi 2 baris di bagian **Konfigurasi**:

   ```python
   API_HOST = 'https://namaperusahaan.api.kledo.com/api/v1'
   ACCESS_TOKEN = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx'
   ```

2. Jalankan lewat terminal:

   ```bash
   cd python/01-authentication
   python 01-check-token.py
   ```

Mulailah dari `01-authentication/01-check-token.py` untuk memastikan token sudah benar.
File Excel hasil export tersimpan di folder `hasil-unduhan/` di sebelah file demo.

Filter tambahan sudah disiapkan dalam bentuk komentar `#`. Hapus tanda `#` untuk mengaktifkannya.

> Menulis token langsung di file hanya untuk mencoba. Untuk aplikasi sungguhan, simpan token di `.env`,
> lihat contoh FastAPI di [01-authentication/fastapi/](01-authentication/fastapi/).

## Daftar Demo

Lihat [README utama](../README.md#daftar-demo). Nama file sama untuk semua bahasa, dengan akhiran `.py`.

## Unduh Laporan Otomatis

```bash
# Laporan kemarin
python python/11-scheduled-download/download-attendance-reports.py

# Laporan rentang tanggal tertentu
python python/11-scheduled-download/download-attendance-reports.py 2026-09-01 2026-09-30
```

**Windows (Task Scheduler)** — buat **Basic Task** harian, pilih **Start a program**, lalu isi:

- **Program/script**: `python` (atau lokasi lengkap `python.exe`)
- **Add arguments**: `download-attendance-reports.py`
- **Start in**: folder tempat file tersebut, contoh `C:\gajihub-api-demo\python\11-scheduled-download`

**Linux / macOS (cron)** — jalankan `crontab -e`, lalu tambahkan (setiap hari jam 06:00):

```text
0 6 * * * python3 /lokasi/gajihub-api-demo/python/11-scheduled-download/download-attendance-reports.py >> /var/log/unduh-absensi.log 2>&1
```

## Kendala Khusus Python

Kendala umum (401, 403, dll) ada di [README utama](../README.md#jika-terjadi-kendala).

| Pesan | Solusi |
|---|---|
| `'python' is not recognized` / `command not found` | Python belum terpasang, atau coba perintah `python3` / `py`. |
| `CERTIFICATE_VERIFY_FAILED` (macOS) | Jalankan `Install Certificates.command` di folder instalasi Python. |
| `SyntaxError` | Versi Python terlalu lama. Gunakan Python 3.8 atau lebih baru. |
