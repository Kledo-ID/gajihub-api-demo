"""
DEMO: Riwayat pengajuan kasbon

Jalankan lewat terminal:  python 2-riwayat-kasbon.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan

mulai_demo('Riwayat Kasbon')

hasil = api_get('/hr/cashReceipt/history/pagination', {
    'page':     1,
    'per_page': 20,

    # --- Filter opsional ---
    # 'hr_cash_receipt_status_id': 2,  # 1 = menunggu, 2 = disetujui, 3 = ditolak, 4 = dibayar, 5 = lunas
})

tampilkan(hasil)
