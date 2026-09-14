"""
DEMO: Daftar jabatan

Jalankan lewat terminal:  python 2-jabatan.py

ID jabatan dipakai saat menambah karyawan (hr_job_position_id).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan, tulis

mulai_demo('Daftar Jabatan')

hasil = api_get('/hr/jobPositions')

if hasil['sukses']:
    for jabatan in hasil['data']['data']:
        # parent_id = ID jabatan atasan (kosong jika jabatan paling atas)
        atasan = jabatan.get('parent_id')
        tulis(f"ID {jabatan['id']} : {jabatan['name']} (atasan: {'-' if atasan is None else atasan})")
    tulis('')

tampilkan(hasil)
