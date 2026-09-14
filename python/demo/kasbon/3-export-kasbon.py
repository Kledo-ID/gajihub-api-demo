"""
DEMO: Unduh file Excel saldo kasbon dan riwayat kasbon

Jalankan lewat terminal:  python 3-export-kasbon.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import mulai_demo, unduh_file

mulai_demo('Export Kasbon (Excel)')

unduh_file('/hr/cashReceipt/balance/export/xls')  # saldo kasbon per karyawan
unduh_file('/hr/cashReceipt/history/export/xls')  # riwayat pengajuan kasbon
