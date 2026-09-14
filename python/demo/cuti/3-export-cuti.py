"""
DEMO: Unduh file Excel data cuti (semua jenis cuti)

Jalankan lewat terminal:  python 3-export-cuti.py
File tersimpan di folder hasil-unduhan/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import akhir_bulan, awal_bulan, mulai_demo, unduh_file

mulai_demo('Export Data Cuti (Excel)')

unduh_file('/hr/leaves/export/xls', {
    'date_leave_started': awal_bulan(),   # tanggal cuti mulai (YYYY-MM-DD)
    'date_leave_ended':   akhir_bulan(),  # tanggal cuti selesai (contoh: akhir bulan ini)

    # --- Filter opsional ---
    # 'hr_leave_type_id':      1,  # jenis cuti (lihat referensi leaveTypes)
    # 'hr_approval_status_id': 2,  # 1 = menunggu, 2 = disetujui, 3 = ditolak
})
