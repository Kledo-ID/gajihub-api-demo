"""
DEMO: Menambah karyawan baru (data pribadi + karir + payroll sekaligus)

Jalankan lewat terminal:  python 3-tambah-karyawan.py

PERHATIAN: demo ini MENAMBAH karyawan di GajiHub Anda.

Kolom yang wajib diisi bisa berbeda di setiap perusahaan, tergantung pengaturan
validasi data karyawan di GajiHub. Jika ada kolom yang kurang, server membalas
status 400 dengan pesan kolom yang perlu diisi, misalnya "Birthplace diperlukan."

ID pilihan (struktur organisasi, jabatan, jenis kelamin, dll) bisa dilihat
di demo folder data-master/.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # agar gajihub.py bisa di-import

from gajihub import api_post, mulai_demo, tampilkan, tanggal, tulis

mulai_demo('Tambah Karyawan')

hasil = api_post('/hr/employees/insert', {

    # ===== 1. Data pribadi =====
    'personal': {
        'name':                 'Budi Santoso',                                 # WAJIB: nama lengkap (4-50 karakter)
        'email':                'budi.' + time.strftime('%H%M%S') + '@contoh.com',  # WAJIB: email (tidak boleh sama dengan karyawan lain)
        'hr_gender_id':         1,             # WAJIB: 1 = laki-laki, 2 = perempuan
        'handphone':            '081234567890',
        'birthplace':           'Yogyakarta',  # tempat lahir
        'birthday':             '1995-05-20',  # tanggal lahir (YYYY-MM-DD)
        'hr_marital_status_id': 2,             # 1 = menikah, 2 = belum menikah, 3 = janda, 4 = duda
        'hr_religion_id':       1,             # lihat demo data-master/6-referensi.py
        'hr_citizenship_id':    1,             # 1 = WNI

        # Kartu identitas
        'hr_id_card_type_id':   1,             # 1 = KTP
        'id_card_number':       '3404012005950001',

        # Alamat sesuai KTP
        'address':              'Jl. Contoh No. 1',
        'country_id':           1,             # 1 = Indonesia
        'province_id':          18,            # ID provinsi
        'city_id':              250,           # ID kota/kabupaten

        # Alamat domisili
        'residence_address':     'Jl. Contoh No. 1',
        'residence_country_id':  1,
        'residence_province_id': 18,
        'residence_city_id':     250,

        # Kontak darurat
        'emergency_contact':       'Siti (Istri)',
        'emergency_contact_phone': '081298765432',
    },

    # ===== 2. Data karir =====
    'career': {
        'hr_employee_status_id':  1,          # WAJIB: 1 = tetap, 2 = percobaan, 3 = PKWT (kontrak), dll
        'hr_org_structure_id':    2,          # WAJIB: ID struktur organisasi
        'hr_job_position_id':     11,         # WAJIB: ID jabatan
        'hr_job_level_id':        5,          # WAJIB: ID level jabatan
        'hr_schedule_pattern_id': 1,          # ID pola jadwal kerja
        'date_started_work':      tanggal(),  # WAJIB: tanggal mulai bekerja (YYYY-MM-DD)
        # 'date_ended':           '2027-09-13',  # WAJIB untuk karyawan tidak tetap: tanggal kontrak berakhir
    },

    # ===== 3. Data payroll =====
    'payroll': {
        'hr_pph21_withholder_id': 1,  # ID pemotong PPh 21 (perusahaan)
        'hr_taxpayer_status_id':  1,  # status PTKP: 1 = TK0, 2 = TK1, dst (lihat referensi taxpayerStatuses)
        # 'npwp':                   '12.345.678.9-012.345',
        # 'bpjs_healthcare_number': '0001234567890',
    },
})

tampilkan(hasil)

if hasil['sukses']:
    tulis('')
    tulis(f"ID karyawan baru: {hasil['data']['data']['id']}")
