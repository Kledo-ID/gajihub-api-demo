"""
DEMO: Daftar lokasi absensi (kantor / titik absen)

Jalankan lewat terminal:  python 5-lokasi-absensi.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan

mulai_demo('Daftar Lokasi Absensi')

hasil = api_get('/hr/attendanceLocations', {
    'page':     1,
    'per_page': 20,
})

tampilkan(hasil)
