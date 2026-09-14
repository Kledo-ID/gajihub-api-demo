"""
DEMO: Mengubah nama jabatan

Jalankan lewat terminal:  python 8-ubah-jabatan.py

PERHATIAN: demo ini MENGUBAH data jabatan di GajiHub Anda.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_put, mulai_demo, tampilkan

mulai_demo('Ubah Jabatan')

id_jabatan = 0  # ganti dengan ID jabatan (lihat hasil demo 7-tambah-jabatan.py)

hasil = api_put(f'/hr/jobPositions/{id_jabatan}', {
    'name':      'Kepala Gudang',  # WAJIB: nama jabatan yang baru
    'parent_id': None,             # opsional: ID jabatan atasan
})

tampilkan(hasil)
