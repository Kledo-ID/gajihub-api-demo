"""
DEMO: Unduh file Excel data reimbursement

Jalankan lewat terminal:  python 2-export-reimbursement.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import mulai_demo, unduh_file

mulai_demo('Export Reimbursement (Excel)')

unduh_file('/hr/reimbursements/export/xls', {
    # --- Filter opsional ---
    # 'date_request_started': '2026-09-01',
    # 'date_request_ended':   '2026-09-30',
})
