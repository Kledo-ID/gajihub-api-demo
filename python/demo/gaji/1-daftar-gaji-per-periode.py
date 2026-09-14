"""
DEMO: Daftar pembayaran gaji karyawan dalam 1 periode (bulan)

Jalankan lewat terminal:  python 1-daftar-gaji-per-periode.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, bulan_lalu, mulai_demo, tampilkan

mulai_demo('Daftar Gaji per Periode')

hasil = api_get('/hr/payrollPayments', {
    'period': bulan_lalu(),  # WAJIB: periode gaji YYYY-MM (contoh: bulan lalu)

    # --- Filter opsional ---
    # 'hr_org_structure_id': 1,
    # 'hr_job_position_id':  1,
    # 'is_active':           'all',  # active / not_active / all
})

tampilkan(hasil)
