"""
DEMO: Absensi 1 karyawan selama 1 bulan

Jalankan lewat terminal:  python 2-absensi-bulanan-karyawan.py

ID karyawan bisa dilihat dari demo "karyawan/1-daftar-karyawan.py".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, bulan_ini, mulai_demo, tampilkan

mulai_demo('Absensi Bulanan 1 Karyawan')

hasil = api_get('/hr/attendances/pagination', {
    'hr_employee_id': 1,            # WAJIB: ID karyawan (ganti sesuai data Anda)
    'date':           bulan_ini(),  # bulan, format YYYY-MM (contoh: bulan ini)
    'page':           1,
    'per_page':       31,

    # --- Filter opsional ---
    # 'hr_attendance_status_id': 1,  # hanya status kehadiran tertentu
})

tampilkan(hasil)
