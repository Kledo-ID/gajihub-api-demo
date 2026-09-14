"""
DEMO: Unduh file Excel detail absensi (per hari, per karyawan)

Jalankan lewat terminal:  python 6-export-detail-absensi.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import awal_bulan, mulai_demo, tanggal, unduh_file

mulai_demo('Export Detail Absensi (Excel)')

unduh_file('/hr/attendances/detail/export/xls', {
    'date_started': awal_bulan(),  # tanggal mulai (YYYY-MM-DD)
    'date_ended':   tanggal(),     # tanggal selesai (YYYY-MM-DD)

    # --- Opsional: hanya karyawan tertentu (ID dipisah koma) ---
    # 'hr_employee_ids': '12,34,56',
})
