"""
DEMO: Daftar level jabatan (golongan)

Jalankan lewat terminal:  python 3-level-jabatan.py

ID level jabatan dipakai saat menambah karyawan (hr_job_level_id).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan, tulis

mulai_demo('Daftar Level Jabatan')

hasil = api_get('/hr/jobLevels')

if hasil['sukses']:
    for level in hasil['data']['data']:
        tulis(f"ID {level['id']} : {level['name']}")
    tulis('')

tampilkan(hasil)
