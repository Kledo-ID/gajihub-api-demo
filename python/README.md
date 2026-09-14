# Demo API GajiHub (Python)

Versi Python dari demo PHP di folder utama. Isi, endpoint, dan parameternya sama persis.

- **tanpa `pip install`**: hanya memakai library bawaan Python;
- dijalankan **lewat terminal**.

## Persiapan

1. **Python 3.8 atau lebih baru.** Cek dengan `python --version` (di macOS/Linux: `python3 --version`).
2. Buat file `.env` di **folder utama** `gajihub-api-demo/` (bukan di folder `python/`).
   Caranya sama seperti demo PHP, lihat [README utama](../README.md) bagian 3 dan 4.
   Satu file `.env` dipakai bersama oleh demo PHP, Python, dan Node.js.

## Menjalankan Demo

```bash
cd python/demo/absensi
python 1-absensi-harian.py
```

File Excel hasil export tersimpan di folder `gajihub-api-demo/hasil-unduhan/`.

Filter tambahan sudah disiapkan dalam bentuk komentar `#`. Hapus tanda `#` untuk mengaktifkannya.

## Daftar Demo

Sama dengan [README utama bagian 6](../README.md#6-daftar-demo), cukup ganti akhiran `.php` menjadi `.py`.

```
python/
├── gajihub.py          -> fungsi bantu yang dipakai semua demo (tidak perlu diubah)
└── demo/
    ├── absensi/        ├── cuti/         ├── gaji/     ├── kasbon/
    ├── karyawan/       ├── lembur/       ├── reimbursement/
    ├── data-master/    ├── persetujuan/  └── unduh-otomatis/
```

## Unduh Laporan Otomatis

```bash
# Laporan kemarin
python python/demo/unduh-otomatis/unduh-laporan-absensi.py

# Laporan rentang tanggal tertentu
python python/demo/unduh-otomatis/unduh-laporan-absensi.py 2026-09-01 2026-09-30
```

- **Windows (Task Scheduler)**: seperti [README utama bagian 7](../README.md#7-unduh-laporan-otomatis-setiap-hari), dengan
  **Program/script** `python` (atau lokasi lengkap `python.exe`), **Add arguments** `unduh-laporan-absensi.py`,
  **Start in** `...\gajihub-api-demo\python\demo\unduh-otomatis`.
- **Linux / macOS (cron)**:

  ```text
  0 6 * * * python3 /lokasi/gajihub-api-demo/python/demo/unduh-otomatis/unduh-laporan-absensi.py >> /var/log/unduh-absensi.log 2>&1
  ```

## Membuat Program Sendiri

Letakkan file baru di dalam `python/demo/<folder>/`, lalu:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, api_post, unduh_file, tanggal

# Ambil data (GET)
hasil = api_get('/hr/attendances/daily/pagination', {'date': tanggal(), 'per_page': 100})

if hasil['sukses']:
    for absen in hasil['data']['data']['data']:
        pass  # simpan ke database Anda di sini

# Unduh file Excel
unduh_file('/hr/attendances/detail/export/xls', {'date_started': '2026-09-01', 'date_ended': '2026-09-30'})

# Kirim data (POST / PUT / PATCH / DELETE)
hasil = api_post('/hr/overtimes', {})  # isi data di sini
```

Catatan penting dan daftar kendala (401, 403, dll) sama dengan [README utama](../README.md#9-catatan-penting).
Kendala khusus Python:

| Pesan | Solusi |
|---|---|
| `'python' is not recognized` / `command not found` | Python belum terpasang, atau coba perintah `python3` / `py`. |
| `CERTIFICATE_VERIFY_FAILED` (macOS) | Jalankan `Install Certificates.command` di folder instalasi Python. |
