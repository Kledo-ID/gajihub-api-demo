"""
DEMO: Daftar data lembur karyawan

Jalankan lewat terminal:  python 1-daftar-lembur.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import akhir_bulan, api_get, awal_bulan, mulai_demo, tampilkan

mulai_demo('Daftar Lembur')

hasil = api_get('/hr/overtimes/pagination', {
    'date_started': awal_bulan(),   # tanggal mulai (YYYY-MM-DD)
    'date_ended':   akhir_bulan(),  # tanggal selesai (contoh: akhir bulan ini)
    'page':         1,
    'per_page':     20,

    # --- Filter opsional ---
    # 'hr_employee_id':      1,
    # 'hr_org_structure_id': 1,
    # 'search':              'budi',
})

tampilkan(hasil)
