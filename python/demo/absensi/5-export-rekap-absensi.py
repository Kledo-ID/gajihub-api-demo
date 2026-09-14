"""
DEMO: Unduh file Excel rekap absensi (rentang tanggal)

Jalankan lewat terminal:  python 5-export-rekap-absensi.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import awal_bulan, mulai_demo, tanggal, unduh_file

mulai_demo('Export Rekap Absensi (Excel)')

unduh_file('/hr/attendances/summary/export/xls', {
    'date_started': awal_bulan(),  # tanggal mulai (YYYY-MM-DD)
    'date_ended':   tanggal(),     # tanggal selesai (YYYY-MM-DD)
})
