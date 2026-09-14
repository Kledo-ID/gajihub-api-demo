"""
DEMO: Menambah karyawan baru (data pribadi + karir + payroll sekaligus)

Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
  python 03-create-employee.py

PERHATIAN: demo ini MENAMBAH karyawan di GajiHub Anda.

Kolom yang wajib diisi bisa berbeda di setiap perusahaan, tergantung pengaturan
validasi data karyawan di GajiHub. Jika ada kolom yang kurang, server membalas
status 400 dengan pesan kolom yang perlu diisi, misalnya "Birthplace diperlukan."

ID pilihan (struktur organisasi, jabatan, jenis kelamin, dll) bisa dilihat
di demo folder 03-master-data/.
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

# ============================================================================
# Konfigurasi
# ----------------------------------------------------------------------------
# Isi langsung di sini agar mudah dicoba.
#
# PENTING (keamanan): untuk aplikasi sungguhan, JANGAN tulis token di dalam kode.
# Simpan API_HOST dan ACCESS_TOKEN di file .env / environment variable, dan jangan
# pernah commit token ke Git. Contoh penerapannya ada di folder python/01-authentication/fastapi/
# ============================================================================

API_HOST = 'https://namaperusahaan.api.kledo.com/api/v1'  # alamat API perusahaan Anda, diakhiri /api/v1
ACCESS_TOKEN = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx'  # Personal Access Token (diawali gajihub_pat_)


def main():
    print('=== Tambah Karyawan ===')

    hasil = api_request('POST', '/hr/employees/insert', {

        # ===== 1. Data pribadi =====
        'personal': {
            'name':                 'Budi Santoso',                                 # WAJIB: nama lengkap (4-50 karakter)
            'email':                'budi.' + time.strftime('%H%M%S') + '@contoh.com',  # WAJIB: email (tidak boleh sama dengan karyawan lain)
            'hr_gender_id':         1,             # WAJIB: 1 = laki-laki, 2 = perempuan
            'handphone':            '081234567890',
            'birthplace':           'Yogyakarta',  # tempat lahir
            'birthday':             '1995-05-20',  # tanggal lahir (YYYY-MM-DD)
            'hr_marital_status_id': 2,             # 1 = menikah, 2 = belum menikah, 3 = janda, 4 = duda
            'hr_religion_id':       1,             # lihat demo 03-master-data/06-references.py
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
        print()
        print(f"ID karyawan baru: {hasil['data']['data']['id']}")


# ============================================================================
# Fungsi bantu (tidak perlu diubah)
# ============================================================================

def api_request(method, endpoint, data=None):
    """
    Kirim request ke API GajiHub, lalu kembalikan hasilnya.

    Autentikasi: setiap request membawa header
      Authorization: Bearer <ACCESS_TOKEN>
      Accept: application/json
      X-App: hr

    GET/DELETE     : data dikirim lewat URL (?page=1&per_page=10)
    POST/PUT/PATCH : data dikirim sebagai JSON di body request

    Hasil: {'status': 200, 'sukses': True, 'data': {isi JSON}, 'isi': b'respons mentah', 'header': {...}}
    """
    if 'xxxxxx' in ACCESS_TOKEN:
        print('ERROR: API_HOST dan ACCESS_TOKEN belum diisi. Buka file ini dan isi bagian Konfigurasi.')
        sys.exit(1)

    data = data or {}
    url = API_HOST.rstrip('/') + endpoint

    header = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'Accept': 'application/json',
        'X-App': 'hr',
        'User-Agent': 'gajihub-api-demo',
    }

    body = None
    if method in ('POST', 'PUT', 'PATCH'):
        header['Content-Type'] = 'application/json'
        body = json.dumps(data).encode('utf-8')
    elif data:
        # Nilai berupa list dikirim sebagai kunci[]=1&kunci[]=2
        query = []
        for kunci, nilai in data.items():
            if isinstance(nilai, list):
                query += [(kunci + '[]', isi) for isi in nilai]
            else:
                query.append((kunci, nilai))
        url += '?' + urllib.parse.urlencode(query)

    print(f'{method} {url}')

    request = urllib.request.Request(url, data=body, headers=header, method=method)

    try:
        with urllib.request.urlopen(request, timeout=300) as respons:  # export bisa lama, tunggu maksimal 5 menit
            status, isi, header_respons = respons.status, respons.read(), respons.headers
    except urllib.error.HTTPError as gagal:  # status 4xx / 5xx tetap dibaca isinya (berisi pesan error)
        status, isi, header_respons = gagal.code, gagal.read(), gagal.headers
    except urllib.error.URLError as gagal:
        print(f'ERROR: Gagal terhubung ke server: {gagal.reason}')
        sys.exit(1)

    try:
        data_json = json.loads(isi)
    except ValueError:
        data_json = None  # bukan JSON, misalnya isi file Excel

    return {
        'status': status,
        'sukses': 200 <= status < 300,
        'data': data_json,
        'isi': isi,
        'header': {kunci.lower(): nilai for kunci, nilai in header_respons.items()},
    }


def tampilkan(hasil):
    """Cetak hasil request: status HTTP + isi respons dalam format JSON yang rapi."""
    print(f"Status HTTP: {hasil['status']}" + (' (berhasil)' if hasil['sukses'] else ' (gagal)'))

    # Penjelasan singkat untuk kode status yang sering muncul
    arti = {
        400: 'Artinya: parameter/data yang dikirim tidak valid. Lihat pesan di bawah.',
        401: 'Artinya: token tidak valid atau sudah kedaluwarsa. Periksa ACCESS_TOKEN.',
        403: 'Artinya: user pemilik token tidak punya hak akses ke fitur ini.',
        404: 'Artinya: data atau endpoint tidak ditemukan. Periksa ID / API_HOST.',
        429: 'Artinya: terlalu banyak request. Tunggu sebentar lalu coba lagi.',
    }.get(hasil['status'], 'Artinya: terjadi kesalahan di server. Coba lagi beberapa saat.' if hasil['status'] >= 500 else '')

    if not hasil['sukses'] and arti:
        print(arti)

    if hasil['data'] is not None:
        print(json.dumps(hasil['data'], indent=4, ensure_ascii=False))
    else:
        print(hasil['isi'].decode('utf-8', errors='replace'))


WIB = timezone(timedelta(hours=7))  # zona waktu Asia/Jakarta


def tanggal(tambah_hari=0):
    """Tanggal hari ini (YYYY-MM-DD). tanggal(-1) = kemarin, tanggal(7) = 7 hari lagi."""
    return (datetime.now(WIB) + timedelta(days=tambah_hari)).strftime('%Y-%m-%d')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')  # agar huruf non-ASCII tampil benar di terminal Windows
    main()
