"""
DEMO: Unduh file Excel sisa kuota cuti tahunan per karyawan

Jalankan lewat terminal:  python 4-export-sisa-kuota-cuti.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import mulai_demo, tanggal, unduh_file

mulai_demo('Export Sisa Kuota Cuti Tahunan (Excel)')

unduh_file('/hr/leaves/annualLeaves/export/xls', {
    'as_of_date': tanggal(),  # sisa kuota per tanggal (YYYY-MM-DD)

    # --- Opsional: hanya karyawan tertentu (ID dipisah koma) ---
    # 'hr_employee_ids': '1,2,3',
})
