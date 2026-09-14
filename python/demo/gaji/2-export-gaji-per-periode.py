"""
DEMO: Unduh file Excel rekap gaji 1 periode (bulan)

Jalankan lewat terminal:  python 2-export-gaji-per-periode.py
File tersimpan di folder hasil-unduhan/

Periode harus sudah ada data gajinya. Jika belum, server membalas
"Period yang dipilih tidak valid."
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import bulan_lalu, mulai_demo, unduh_file

mulai_demo('Export Gaji per Periode (Excel)')

unduh_file('/hr/payrolls/perPeriod/export/xls', {
    'period': bulan_lalu(),  # periode gaji YYYY-MM (contoh: bulan lalu)

    # --- Filter opsional ---
    # 'hr_org_structure_id': 1,
    # 'hr_job_position_id':  1,
})
