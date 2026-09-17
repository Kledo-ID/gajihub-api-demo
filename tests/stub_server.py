"""
Stub API GajiHub untuk pengujian offline.

Meniru bentuk respons API GajiHub secukupnya agar seluruh demo bisa dijalankan
tanpa token dan tanpa koneksi internet. Hanya memakai library bawaan Python.

Jalankan sendiri (untuk mencoba):
  python tests/stub_server.py 8101
"""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# ============================================================================
# Contoh data
# ============================================================================

HALAMAN_KARYAWAN = {
    'total': 2, 'current_page': 1, 'last_page': 1,
    'data': [
        {'id': 1, 'code': 'K-001', 'name': 'Budi Santoso'},
        {'id': 2, 'code': 'K-002', 'name': 'Siti Aminah'},
    ],
}
DAFTAR_NAMA = [{'id': 1, 'name': 'Pilihan Satu'}, {'id': 2, 'name': 'Pilihan Dua'}]
DAFTAR_INDUK = [
    {'id': 1, 'name': 'Kantor Pusat', 'parent_id': None},
    {'id': 2, 'name': 'Divisi Keuangan', 'parent_id': 1},
]
DAFTAR_SHIFT = [{'id': 1, 'name': 'Shift Pagi', 'time_started': '08:00', 'time_ended': '17:00'}]
HALAMAN_KOSONG = {'total': 5, 'current_page': 1, 'last_page': 1, 'data': []}
DATA_BARU = {'id': 99}

# Bentuk halaman untuk endpoint approvals & salaryComponents.
# Sama seperti halaman lain: data (envelope) -> paginator -> data (daftar isi).
HALAMAN_BERSARANG = {'total': 1, 'current_page': 1, 'last_page': 1, 'data': [{
    'id': 11,
    'hr_approval_type': {'name': 'Cuti Tahunan'},
    'hr_employee': {'name': 'Budi Santoso'},
    'name': 'Gaji Pokok',
    'hr_component_type': {'name': 'Pendapatan'},
}]}

# ============================================================================
# Daftar endpoint: (metode, pola jalur, data balasan)
# Jalur memakai {} untuk bagian yang bebas, contoh /hr/employees/{id}
# ============================================================================

ENDPOINT = [
    ('GET', '/authentication/user', {'id': 7, 'name': 'Budi Santoso', 'email': 'budi@contoh.com'}),

    ('GET', '/hr/employees/pagination', HALAMAN_KARYAWAN),
    ('POST', '/hr/employees/insert', DATA_BARU),
    ('GET', '/hr/employees/{id}', {'id': 1, 'name': 'Budi Santoso'}),

    ('GET', '/hr/orgStructures', DAFTAR_INDUK),
    ('GET', '/hr/jobPositions', DAFTAR_INDUK),
    ('POST', '/hr/jobPositions', DATA_BARU),
    ('PUT', '/hr/jobPositions/{id}', DATA_BARU),
    ('DELETE', '/hr/jobPositions/{id}', None),
    ('GET', '/hr/jobLevels', DAFTAR_NAMA),
    ('GET', '/hr/shifts', DAFTAR_SHIFT),
    ('GET', '/hr/attendanceLocations', HALAMAN_KOSONG),
    ('GET', '/hr/references/{jenis}', DAFTAR_NAMA),

    ('GET', '/hr/attendances/daily/pagination', HALAMAN_KOSONG),
    ('GET', '/hr/attendances/pagination', HALAMAN_KOSONG),
    ('GET', '/hr/attendances/summary/pagination', HALAMAN_KOSONG),

    ('GET', '/hr/leaves/annualLeaves/pagination', HALAMAN_KOSONG),
    ('POST', '/hr/leaves/annualLeaves', DATA_BARU),

    ('GET', '/hr/overtimes/pagination', HALAMAN_KOSONG),
    ('POST', '/hr/overtimes', DATA_BARU),

    ('GET', '/hr/approvals/pagination', HALAMAN_BERSARANG),
    ('PATCH', '/hr/approvals/approve', {'approved': 1}),
    ('PATCH', '/hr/approvals/decline', {'declined': 1}),

    ('GET', '/hr/payrollPayments', []),
    ('GET', '/hr/salaryComponents/pagination', HALAMAN_BERSARANG),

    ('GET', '/hr/reimbursements/pagination', HALAMAN_KOSONG),

    ('GET', '/hr/cashReceipt/balance/pagination', HALAMAN_KOSONG),
    ('GET', '/hr/cashReceipt/history/pagination', HALAMAN_KOSONG),
]

# Endpoint export: (pola jalur, nama file yang dikirim)
EKSPOR = [
    ('/hr/employees/export/{jenis}', 'Data Karyawan.xlsx'),
    ('/hr/attendances/daily/export/{jenis}', 'Absensi Harian.xlsx'),
    ('/hr/attendances/summary/export/{jenis}', 'Rekap Absensi.xlsx'),
    ('/hr/attendances/detail/export/{jenis}', 'Detail Absensi.xlsx'),
    ('/hr/leaves/export/{jenis}', 'Data Cuti.xlsx'),
    ('/hr/leaves/annualLeaves/export/{jenis}', 'Sisa Kuota Cuti.xlsx'),
    ('/hr/overtimes/export/{jenis}', 'Data Lembur.xlsx'),
    ('/hr/payrolls/perPeriod/export/{jenis}', 'Gaji per Periode.xlsx'),
    ('/hr/reimbursements/export/{jenis}', 'Reimbursement.xlsx'),
    ('/hr/cashReceipt/balance/export/{jenis}', 'Saldo Kasbon.xlsx'),
    ('/hr/cashReceipt/history/export/{jenis}', 'Riwayat Kasbon.xlsx'),
]

AWALAN = '/api/v1'


def jadikan_pola(jalur):
    """Ubah '/hr/employees/{id}' menjadi regex yang cocok dengan 1 ruas bebas."""
    return re.compile('^' + re.escape(AWALAN + jalur).replace(r'\{id\}', '[^/]+')
                      .replace(r'\{jenis\}', '[^/]+') + '$')


POLA_ENDPOINT = [(m, jadikan_pola(j), d) for m, j, d in ENDPOINT]
POLA_EKSPOR = [(jadikan_pola(j), n) for j, n in EKSPOR]


class Penangan(BaseHTTPRequestHandler):
    """Menjawab request dari file demo."""

    protocol_version = 'HTTP/1.1'
    catatan = None  # file untuk mencatat request yang masuk

    def log_message(self, *args):
        pass  # matikan log bawaan agar keluaran pengujian tetap bersih

    def handle_one_request(self):
        # Program demo sering menutup koneksi begitu selesai membaca respons.
        # Itu wajar, jadi error koneksi terputus tidak perlu dicetak.
        try:
            BaseHTTPRequestHandler.handle_one_request(self)
        except (ConnectionError, OSError):
            self.close_connection = True

    def handle_error(self, *args):
        pass

    # --- semua metode HTTP diarahkan ke satu tempat ---
    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = lambda self: self.layani()

    def layani(self):
        jalur = urlparse(self.path).path
        panjang = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(panjang).decode('utf-8', 'replace') if panjang else ''

        self.rekam(body)

        # Token wajib ada. Tanpa token, balas 401 seperti API sungguhan.
        if not (self.headers.get('Authorization') or '').startswith('Bearer '):
            return self.balas_json(401, {'success': False, 'data': None,
                                         'message': 'Unauthenticated.'})

        # Header X-App: hr wajib untuk endpoint autentikasi
        if jalur.endswith('/authentication/user') and self.headers.get('X-App') != 'hr':
            return self.balas_json(401, {'success': False, 'data': None,
                                         'message': 'Header X-App: hr tidak dikirim.'})

        for pola, nama_file in POLA_EKSPOR:
            if pola.match(jalur):
                return self.balas_berkas(nama_file)

        for metode, pola, data in POLA_ENDPOINT:
            if metode == self.command and pola.match(jalur):
                return self.balas_json(200, {'success': True, 'data': data, 'message': 'ok'})

        # Endpoint tidak dikenal -> 404, supaya salah alamat langsung ketahuan
        self.balas_json(404, {'success': False, 'data': None,
                              'message': 'Endpoint tidak dikenal oleh stub.'})

    def rekam(self, body):
        if not Penangan.catatan:
            return
        Penangan.catatan.write('%s %s\n' % (self.command, self.path))
        if body:
            Penangan.catatan.write('    BODY %s\n' % body)
        Penangan.catatan.flush()

    def balas_json(self, status, isi):
        data = json.dumps(isi, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def balas_berkas(self, nama_file):
        # Isi file Excel palsu: cukup untuk menguji penyimpanan file, bukan isinya
        data = b'PK\x03\x04' + b'x' * 100
        self.send_response(200)
        self.send_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.send_header('Content-Disposition', 'attachment; filename="%s"' % nama_file)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def jalankan(port, lokasi_catatan=None):
    if lokasi_catatan:
        Penangan.catatan = open(lokasi_catatan, 'w', encoding='utf-8')

    server = ThreadingHTTPServer(('127.0.0.1', port), Penangan)
    server.daemon_threads = True
    server.serve_forever()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8101
    print('Stub API GajiHub siap di http://127.0.0.1:%d/api/v1' % port)
    try:
        jalankan(port)
    except KeyboardInterrupt:
        pass
