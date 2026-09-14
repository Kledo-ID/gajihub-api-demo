"""
DEMO: Menyetujui (approve) atau menolak (decline) pengajuan

Jalankan lewat terminal:  python 2-setujui-pengajuan.py

PERHATIAN: demo ini MENGUBAH status pengajuan di GajiHub Anda.
ID pengajuan diambil dari demo 1-daftar-persetujuan.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_patch, mulai_demo, tampilkan

mulai_demo('Setujui Pengajuan')

id_pengajuan = [0]  # ganti dengan ID pengajuan, bisa lebih dari 1: [12, 13]

hasil = api_patch('/hr/approvals/approve', {  # untuk menolak, ganti menjadi /hr/approvals/decline
    'ids':         id_pengajuan,
    'description': 'Disetujui lewat API',  # opsional: catatan
})

tampilkan(hasil)
