"""
Daftar demo yang diuji.

Nama file demo sama persis di semua bahasa, hanya akhirannya yang berbeda
(.php / .py / .mjs / .go). Jadi satu daftar ini dipakai untuk keempat bahasa.
"""


class Kasus:
    def __init__(self, jalur, mengubah=False, butuh_id=(), harus_memuat=(), menghasilkan=None):
        self.jalur = jalur          # jalur tanpa akhiran, contoh '02-employees/01-list-employees'
        self.mengubah = mengubah    # True jika demo ini menambah/mengubah/menghapus data
        self.butuh_id = butuh_id    # ID khusus tenant yang perlu diisi saat menguji BE sungguhan
        # Teks yang wajib muncul di keluaran saat diuji dengan stub. Dipakai untuk
        # memastikan demo benar-benar membaca isi respons, bukan sekadar tidak error.
        self.harus_memuat = harus_memuat
        # ID yang diambil dari keluaran demo ini untuk dipakai demo berikutnya:
        # {jenis_id: regex dengan 1 grup}
        self.menghasilkan = menghasilkan or {}

    @property
    def nama(self):
        return self.jalur


DAFTAR = [
    Kasus('01-authentication/01-check-token', harus_memuat=('Pemilik token: Budi Santoso (budi@contoh.com)',)),

    Kasus('02-employees/01-list-employees', harus_memuat=('ID 1 : K-001 - Budi Santoso', 'Total karyawan: 2')),
    Kasus('02-employees/02-employee-detail', butuh_id=('karyawan',)),
    Kasus('02-employees/03-create-employee', mengubah=True, harus_memuat=('ID karyawan baru: 99',)),
    Kasus('02-employees/04-export-employees'),

    Kasus('03-master-data/01-org-structures',
          harus_memuat=('ID 1 : Kantor Pusat (induk: -)', 'ID 2 : Divisi Keuangan (induk: 1)')),
    Kasus('03-master-data/02-job-positions',
          harus_memuat=('ID 1 : Kantor Pusat (atasan: -)', 'ID 2 : Divisi Keuangan (atasan: 1)')),
    Kasus('03-master-data/03-job-levels', harus_memuat=('ID 1 : Pilihan Satu', 'ID 2 : Pilihan Dua')),
    Kasus('03-master-data/04-shifts', harus_memuat=('ID 1 : Shift Pagi (08:00 - 17:00)',)),
    Kasus('03-master-data/05-attendance-locations'),
    Kasus('03-master-data/06-references', harus_memuat=('hr_gender_id', '1 = Pilihan Satu')),
    Kasus('03-master-data/07-create-job-position', mengubah=True, harus_memuat=('ID jabatan baru: 99',),
          menghasilkan={'jabatan': r'ID jabatan baru: (\d+)'}),
    Kasus('03-master-data/08-update-job-position', mengubah=True, butuh_id=('jabatan',)),
    Kasus('03-master-data/09-delete-job-position', mengubah=True, butuh_id=('jabatan',)),

    Kasus('04-attendance/01-daily-attendance', harus_memuat=('Total karyawan: 5',)),
    Kasus('04-attendance/02-monthly-attendance-by-employee', butuh_id=('karyawan',)),
    Kasus('04-attendance/03-attendance-summary'),
    Kasus('04-attendance/04-export-daily-attendance'),
    Kasus('04-attendance/05-export-attendance-summary'),
    Kasus('04-attendance/06-export-attendance-detail'),

    Kasus('05-leave/01-list-annual-leaves'),
    Kasus('05-leave/02-create-annual-leave', mengubah=True, butuh_id=('karyawan',)),
    Kasus('05-leave/03-export-leaves'),
    Kasus('05-leave/04-export-annual-leave-balance'),

    Kasus('06-overtime/01-list-overtimes'),
    Kasus('06-overtime/02-create-overtime', mengubah=True, butuh_id=('karyawan',)),
    Kasus('06-overtime/03-export-overtimes'),

    Kasus('07-approvals/01-list-approvals', harus_memuat=('ID 11 : Cuti Tahunan - Budi Santoso',),
          menghasilkan={'pengajuan': r'^ID (\d+) :'}),
    Kasus('07-approvals/02-approve-requests', mengubah=True, butuh_id=('pengajuan',)),

    Kasus('08-payroll/01-list-payroll-by-period'),
    Kasus('08-payroll/02-export-payroll-by-period'),
    Kasus('08-payroll/03-salary-components', harus_memuat=('ID 11 : Gaji Pokok (Pendapatan)',)),

    Kasus('09-reimbursement/01-list-reimbursements'),
    Kasus('09-reimbursement/02-export-reimbursements'),

    Kasus('10-cash-advance/01-cash-advance-balances'),
    Kasus('10-cash-advance/02-cash-advance-history'),
    Kasus('10-cash-advance/03-export-cash-advances'),

    Kasus('11-scheduled-download/download-attendance-reports'),
]


# Bahasa yang diuji: folder, akhiran file, dan perintah menjalankannya.
class Bahasa:
    def __init__(self, folder, akhiran, perintah, alat):
        self.folder = folder        # folder bahasa di dalam repo
        self.akhiran = akhiran      # akhiran file demo
        self.perintah = perintah    # perintah untuk menjalankan 1 file
        self.alat = alat            # program yang harus terpasang


BAHASA = {
    'php':    Bahasa('php', '.php', ['php'], 'php'),
    'python': Bahasa('python', '.py', [None], 'python'),   # None = interpreter Python yang sedang jalan
    'nodejs': Bahasa('nodejs', '.mjs', ['node'], 'node'),
    'go':     Bahasa('go', '.go', ['go', 'run'], 'go'),
}
