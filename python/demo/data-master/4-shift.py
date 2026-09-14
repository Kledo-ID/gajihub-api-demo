"""
DEMO: Daftar shift kerja

Jalankan lewat terminal:  python 4-shift.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan, tulis

mulai_demo('Daftar Shift Kerja')

hasil = api_get('/hr/shifts')

if hasil['sukses']:
    for shift in hasil['data']['data']:
        tulis(f"ID {shift['id']} : {shift['name']} ({shift['time_started']} - {shift['time_ended']})")
    tulis('')

tampilkan(hasil)
