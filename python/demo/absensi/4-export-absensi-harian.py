"""
DEMO: Unduh file Excel absensi harian (1 tanggal)

Jalankan lewat terminal:  python 4-export-absensi-harian.py
File tersimpan di folder hasil-unduhan/

Ganti "xls" di alamat endpoint menjadi "csv" untuk format CSV.
Catatan: format "xls" menghasilkan file .xlsx (Excel modern).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import mulai_demo, tanggal, unduh_file

mulai_demo('Export Absensi Harian (Excel)')

unduh_file('/hr/attendances/daily/export/xls', {
    'date': tanggal(),  # tanggal, format YYYY-MM-DD. Jika dikosongkan = hari ini

    # --- Filter opsional ---
    # 'search':              'budi',
    # 'hr_org_structure_id': 1,
    # 'is_active':           'active',
})
