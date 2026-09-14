"""
DEMO: Rekap absensi per karyawan untuk rentang tanggal
(jumlah hadir, terlambat, jam kerja, lembur, dll)

Jalankan lewat terminal:  python 3-rekap-absensi.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, awal_bulan, mulai_demo, tampilkan, tanggal

mulai_demo('Rekap Absensi per Karyawan')

hasil = api_get('/hr/attendances/summary/pagination', {
    'date_started': awal_bulan(),  # tanggal mulai, format YYYY-MM-DD (contoh: awal bulan ini)
    'date_ended':   tanggal(),     # tanggal selesai (contoh: hari ini)
    'page':         1,
    'per_page':     20,

    # --- Filter opsional ---
    # 'search':              'budi',
    # 'hr_org_structure_id': 1,
    # 'hr_job_position_id':  1,
    # 'is_active':           'active',   # active / not_active / all
    # 'sort_by':             'name',     # name / lates / working_hours / overtime_hours / ...
    # 'order_by':            'asc',      # asc / desc
})

tampilkan(hasil)
