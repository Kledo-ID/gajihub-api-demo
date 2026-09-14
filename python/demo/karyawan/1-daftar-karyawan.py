"""
DEMO: Daftar karyawan

Jalankan lewat terminal:  python 1-daftar-karyawan.py

Gunakan demo ini untuk mengetahui ID karyawan (hr_employee_id)
yang dibutuhkan demo lain.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan, tulis

mulai_demo('Daftar Karyawan')

hasil = api_get('/hr/employees/pagination', {
    'page':     1,
    'per_page': 20,

    # --- Filter opsional ---
    # 'search':    'budi',     # cari nama / NIK karyawan
    # 'is_active': 'active',   # active (default) / not_active / all
    # 'sort_by':   'name',     # code / name
    # 'order_by':  'asc',      # asc / desc
})

if hasil['sukses']:
    halaman = hasil['data']['data']

    tulis(f"Total karyawan: {halaman['total']} (halaman {halaman['current_page']} dari {halaman['last_page']})")
    for karyawan in halaman['data']:
        tulis(f"ID {karyawan['id']} : {karyawan['code']} - {karyawan['name']}")
    tulis('')

tampilkan(hasil)
