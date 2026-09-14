"""
DEMO: Saldo kasbon (pinjaman) per karyawan

Jalankan lewat terminal:  python 1-saldo-kasbon.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan

mulai_demo('Saldo Kasbon Karyawan')

hasil = api_get('/hr/cashReceipt/balance/pagination', {
    'page':     1,
    'per_page': 20,

    # --- Urutan opsional ---
    # 'sort_by':  'due',   # plafon / due / last_payment_amount / last_payment_date / employee_name
    # 'order_by': 'desc',  # asc / desc
})

tampilkan(hasil)
