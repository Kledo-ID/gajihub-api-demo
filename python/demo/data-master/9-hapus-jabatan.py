"""
DEMO: Menghapus jabatan

Jalankan lewat terminal:  python 9-hapus-jabatan.py

PERHATIAN: demo ini MENGHAPUS data jabatan di GajiHub Anda.
Jabatan yang masih dipakai karyawan tidak bisa dihapus.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_delete, mulai_demo, tampilkan

mulai_demo('Hapus Jabatan')

id_jabatan = 0  # ganti dengan ID jabatan (lihat hasil demo 7-tambah-jabatan.py)

hasil = api_delete(f'/hr/jobPositions/{id_jabatan}')

tampilkan(hasil)
