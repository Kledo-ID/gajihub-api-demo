"""
DEMO: Detail 1 karyawan (data pribadi, karir, payroll)

Jalankan lewat terminal:  python 2-detail-karyawan.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan

mulai_demo('Detail Karyawan')

id_karyawan = 1  # ganti dengan ID karyawan (lihat demo 1-daftar-karyawan.py)

hasil = api_get(f'/hr/employees/{id_karyawan}')

tampilkan(hasil)
