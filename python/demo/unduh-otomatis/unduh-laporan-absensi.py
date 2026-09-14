"""
DEMO: Unduh otomatis laporan absensi (untuk dijadwalkan setiap hari)

Cara pakai lewat terminal:
  python unduh-laporan-absensi.py                          -> laporan kemarin
  python unduh-laporan-absensi.py 2026-09-01 2026-09-30    -> laporan rentang tanggal

File tersimpan di folder hasil-unduhan/

Agar berjalan otomatis setiap hari, jadwalkan perintah di atas:
  - Windows : Task Scheduler (lihat python/README.md)
  - Linux   : cron, contoh setiap jam 06:00:
              0 6 * * * python3 /lokasi/gajihub-api-demo/python/demo/unduh-otomatis/unduh-laporan-absensi.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import mulai_demo, tanggal, tulis, unduh_file

mulai_demo('Unduh Otomatis Laporan Absensi')

# Tanggal diambil dari perintah terminal. Jika tidak diisi, pakai tanggal kemarin.
tanggal_mulai = sys.argv[1] if len(sys.argv) > 1 else tanggal(-1)
tanggal_selesai = sys.argv[2] if len(sys.argv) > 2 else tanggal_mulai

tulis(f'Periode: {tanggal_mulai} s/d {tanggal_selesai}')

periode = {
    'date_started': tanggal_mulai,
    'date_ended':   tanggal_selesai,
}

# 1. Detail absensi per hari per karyawan
unduh_file('/hr/attendances/detail/export/xls', periode)

# 2. Rekap absensi per karyawan
unduh_file('/hr/attendances/summary/export/xls', periode)

# Tambahkan laporan lain di sini jika perlu, contoh:
# unduh_file('/hr/overtimes/export/xls', periode)   # data lembur

tulis('Selesai.')
