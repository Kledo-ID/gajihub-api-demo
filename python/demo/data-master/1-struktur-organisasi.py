"""
DEMO: Daftar struktur organisasi (divisi/departemen)

Jalankan lewat terminal:  python 1-struktur-organisasi.py

ID struktur organisasi dipakai saat menambah karyawan (hr_org_structure_id)
dan sebagai filter di laporan absensi.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan, tulis

mulai_demo('Daftar Struktur Organisasi')

hasil = api_get('/hr/orgStructures', {
    # 'is_archive': 'all',  # not_archive (default) / archive / all
})

if hasil['sukses']:
    for organisasi in hasil['data']['data']:
        # parent_id = ID organisasi induk (kosong jika organisasi paling atas)
        induk = organisasi.get('parent_id')
        tulis(f"ID {organisasi['id']} : {organisasi['name']} (induk: {'-' if induk is None else induk})")
    tulis('')

tampilkan(hasil)
