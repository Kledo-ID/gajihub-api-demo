"""
DEMO: Menambah data lembur karyawan (oleh admin)

Jalankan lewat terminal:  python 2-tambah-lembur.py

PERHATIAN: demo ini MENAMBAH data lembur di GajiHub Anda.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_post, mulai_demo, tampilkan, tanggal

mulai_demo('Tambah Lembur')

hasil = api_post('/hr/overtimes', {
    'hr_employee_id':         1,          # WAJIB: ID karyawan
    'date':                   tanggal(),  # WAJIB: tanggal lembur (YYYY-MM-DD)
    'time_started':           '18:00',    # WAJIB: jam mulai (JJ:MM)
    'time_ended':             '20:00',    # WAJIB: jam selesai (JJ:MM)
    'time_ended_is_tomorrow': 0,          # WAJIB: 1 jika jam selesai sudah lewat tengah malam, 0 jika tidak
    'note':                   'Lembur closing bulanan (dibuat lewat API)',  # opsional
})

tampilkan(hasil)
