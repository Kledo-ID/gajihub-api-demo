"""
DEMO: Unduh file Excel data lembur

Jalankan lewat terminal:  python 3-export-lembur.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import akhir_bulan, awal_bulan, mulai_demo, unduh_file

mulai_demo('Export Lembur (Excel)')

unduh_file('/hr/overtimes/export/xls', {
    'date_started': awal_bulan(),   # tanggal mulai (YYYY-MM-DD)
    'date_ended':   akhir_bulan(),  # tanggal selesai (YYYY-MM-DD)

    # --- Filter opsional ---
    # 'hr_employee_id':      1,
    # 'hr_org_structure_id': 1,
})
