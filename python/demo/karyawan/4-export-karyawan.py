"""
DEMO: Unduh file Excel data karyawan

Jalankan lewat terminal:  python 4-export-karyawan.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import mulai_demo, unduh_file

mulai_demo('Export Data Karyawan (Excel)')

unduh_file('/hr/employees/export/xls', {
    # --- Filter opsional ---
    # 'is_active':            'all',     # active (default) / not_active / all
    # 'hr_org_structure_ids': [1, 2],    # hanya struktur organisasi tertentu
    # 'hr_job_position_ids':  [3],       # hanya jabatan tertentu
})
