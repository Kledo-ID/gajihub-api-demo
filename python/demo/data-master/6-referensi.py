"""
DEMO: Data referensi (kode-kode pilihan)

Jalankan lewat terminal:  python 6-referensi.py

Saat menambah/mengubah karyawan, beberapa kolom diisi dengan ID pilihan,
misalnya jenis kelamin (hr_gender_id) atau status karyawan (hr_employee_status_id).
Demo ini menampilkan daftar ID tersebut.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_get, mulai_demo, tampilkan, tulis

mulai_demo('Data Referensi')

daftar_referensi = {
    'genders':          'Jenis kelamin      (hr_gender_id)',
    'maritalStatuses':  'Status pernikahan  (hr_marital_status_id)',
    'religions':        'Agama              (hr_religion_id)',
    'employeeStatuses': 'Status karyawan    (hr_employee_status_id)',
    'educationLevels':  'Pendidikan         (hr_education_level_id)',
}

for endpoint, keterangan in daftar_referensi.items():
    hasil = api_get('/hr/references/' + endpoint)

    if not hasil['sukses']:
        tampilkan(hasil)
        continue

    tulis(keterangan + ':')
    for pilihan in hasil['data']['data']:
        tulis(f"   {pilihan['id']} = {pilihan['name']}")
    tulis('')
