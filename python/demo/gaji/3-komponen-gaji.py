"""
DEMO: Daftar komponen gaji (gaji pokok, tunjangan, potongan, dll)

Jalankan lewat terminal:  python 3-komponen-gaji.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan, tulis

mulai_demo('Daftar Komponen Gaji')

hasil = api_get('/hr/salaryComponents/pagination', {
    'page':     1,
    'per_page': 50,
})

if hasil['sukses']:
    for komponen in hasil['data']['data']['data']:
        tulis(f"ID {komponen['id']} : {komponen['name']} ({komponen['hr_component_type']['name']})")
    tulis('')

tampilkan(hasil)
