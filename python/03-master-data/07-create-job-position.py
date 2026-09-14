"""
DEMO: Menambah jabatan baru

Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
  python 07-create-job-position.py

PERHATIAN: demo ini MENAMBAH data jabatan di GajiHub Anda.
Struktur organisasi (/hr/orgStructures) dan level jabatan (/hr/jobLevels)
bisa ditambah dengan cara yang sama.
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

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
    print('=== Tambah Jabatan ===')

    hasil = api_request('POST', '/hr/jobPositions', {
        'name':      'Staff Gudang ' + time.strftime('%H%M%S'),  # WAJIB: nama jabatan (2-45 karakter, tidak boleh sama)
        'parent_id': None,                                       # opsional: ID jabatan atasan
    })

    tampilkan(hasil)

    if hasil['sukses']:
        print()
        print(f"ID jabatan baru: {hasil['data']['data']['id']} (pakai ID ini di demo ubah / hapus)")


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


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')  # agar huruf non-ASCII tampil benar di terminal Windows
    main()
