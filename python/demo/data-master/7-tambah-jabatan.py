"""
DEMO: Menambah jabatan baru

Jalankan lewat terminal:  python 7-tambah-jabatan.py

PERHATIAN: demo ini MENAMBAH data jabatan di GajiHub Anda.
Struktur organisasi (/hr/orgStructures) dan level jabatan (/hr/jobLevels)
bisa ditambah dengan cara yang sama.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_post, mulai_demo, tampilkan, tulis

mulai_demo('Tambah Jabatan')

hasil = api_post('/hr/jobPositions', {
    'name':      'Staff Gudang ' + time.strftime('%H%M%S'),  # WAJIB: nama jabatan (2-45 karakter, tidak boleh sama)
    'parent_id': None,                                       # opsional: ID jabatan atasan
})

tampilkan(hasil)

if hasil['sukses']:
    tulis('')
    tulis(f"ID jabatan baru: {hasil['data']['data']['id']} (pakai ID ini di demo ubah / hapus)")
