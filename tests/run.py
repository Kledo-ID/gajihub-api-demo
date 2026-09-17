"""
Menjalankan seluruh file demo dan memeriksa hasilnya.

Dua sasaran pengujian:
  stub  (bawaan) -> server tiruan di komputer sendiri. Tanpa token, tanpa internet,
                    tanpa mengubah data siapa pun. Cocok untuk CI.
  real           -> API GajiHub sungguhan. Butuh GAJIHUB_API_HOST dan
                    GAJIHUB_ACCESS_TOKEN. PERHATIAN: 7 demo mengubah data.

Contoh:
  python tests/run.py                             semua bahasa, sasaran stub
  python tests/run.py --bahasa go                 hanya Go
  python tests/run.py --hanya 02-employees        hanya demo tertentu
  python tests/run.py --sasaran real              API sungguhan (hanya yang membaca)
  python tests/run.py --sasaran real --izinkan-ubah-data   ikut menjalankan 7 demo pengubah data

Hanya memakai library bawaan Python.
"""

import argparse
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import kasus as daftar_kasus
import stub_server

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Nilai contoh di file demo yang diganti sebelum dijalankan
HOST_CONTOH = 'https://namaperusahaan.api.kledo.com/api/v1'
TOKEN_CONTOH = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx'

# ID khusus tenant. Pola cocok untuk keempat bahasa sekaligus:
#   $idKaryawan = 1;   id_karyawan = 1   const idKaryawan = 1;   idKaryawan := 1
POLA_ID = {
    'karyawan': re.compile(r'(\bid_?[Kk]aryawan\b\s*(?::=|=>|=)\s*)\d+'),
    'jabatan': re.compile(r'(\bid_?[Jj]abatan\b\s*(?::=|=>|=)\s*)\d+'),
    # idPengajuan berbentuk daftar: [0] atau []int{0}
    'pengajuan': re.compile(r'(\bid_?[Pp]engajuan\b\s*(?::=|=>|=)\s*(?:\[\]int\{|\[)\s*)\d+'),
}
# hr_employee_id di dalam body POST
POLA_HR_EMPLOYEE_ID = re.compile(r"(['\"]?hr_employee_id['\"]?\s*(?:=>|:)\s*)\d+")

HIJAU, MERAH, KUNING, ABU, NORMAL = '\033[32m', '\033[31m', '\033[33m', '\033[90m', '\033[0m'
if os.name == 'nt' and not os.environ.get('WT_SESSION'):
    HIJAU = MERAH = KUNING = ABU = NORMAL = ''


def port_bebas():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def nyalakan_stub(lokasi_catatan):
    """Jalankan stub di thread terpisah, kembalikan alamat API-nya."""
    port = port_bebas()
    utas = threading.Thread(target=stub_server.jalankan, args=(port, lokasi_catatan), daemon=True)
    utas.start()

    # Tunggu sampai stub siap menerima koneksi
    for _ in range(50):
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.2):
                break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError('Stub tidak kunjung siap.')

    return 'http://127.0.0.1:%d/api/v1' % port


def siapkan_berkas(sumber, tujuan, host, token, kasus, id_tenant):
    """Salin file demo lalu isi bagian Konfigurasi (dan ID tenant bila perlu)."""
    with open(sumber, encoding='utf-8') as f:
        isi = f.read()

    isi = isi.replace(HOST_CONTOH, host).replace(TOKEN_CONTOH, token)

    for jenis in kasus.butuh_id:
        nilai = id_tenant.get(jenis)
        if nilai:
            isi = POLA_ID[jenis].sub(lambda m: m.group(1) + str(nilai), isi)
            if jenis == 'karyawan':
                isi = POLA_HR_EMPLOYEE_ID.sub(lambda m: m.group(1) + str(nilai), isi)

    os.makedirs(os.path.dirname(tujuan), exist_ok=True)
    with open(tujuan, 'w', encoding='utf-8', newline='') as f:
        f.write(isi)


POLA_STATUS = re.compile(r'Status HTTP:\s*(\d{3})')


POLA_EXCEPTION = re.compile(r'([A-Za-z_]+(?:Exception|Error)): ?(.{0,90})')


def ringkas_exception(keluaran):
    """Ambil nama exception + awal pesannya, agar laporan tetap satu baris."""
    cocok = POLA_EXCEPTION.search(keluaran)
    if not cocok:
        return 'lihat keluaran'
    return '%s: %s' % (cocok.group(1), cocok.group(2).split(' in ')[0].strip())


def nilai_hasil(kode_keluar, keluaran, sasaran, kasus=None):
    """Tentukan status kasus: 'ok', 'gagal', atau 'peringatan' + alasannya."""
    # Diperiksa lebih dulu: error sertifikat juga membuat kode keluar 1,
    # padahal penyebab dan cara memperbaikinya jauh lebih spesifik.
    if 'unable to verify the first certificate' in keluaran or 'UNABLE_TO_VERIFY_LEAF_SIGNATURE' in keluaran:
        return 'gagal', 'sertifikat server tidak dipercaya Node.js (set NODE_OPTIONS=--use-system-ca)'

    if kode_keluar != 0:
        return 'gagal', 'keluar dengan kode %s' % kode_keluar

    if 'Traceback' in keluaran or 'panic:' in keluaran or 'Fatal error' in keluaran:
        return 'gagal', 'program error'

    if 'Gagal terhubung ke server' in keluaran:
        return 'gagal', 'tidak bisa terhubung'

    status = [int(s) for s in POLA_STATUS.findall(keluaran)]
    buruk = [s for s in status if s in (401, 403, 404, 405, 429) or s >= 500]
    if buruk:
        return 'gagal', 'status HTTP %s' % buruk[0]

    # Beberapa server membalas 400 untuk error yang tidak tertangani, dengan jejak
    # exception di pesannya. Itu error server, bukan data yang ditolak.
    if any(s == 400 for s in status) and re.search(r'Error Unexpected|Exception:|Stack trace', keluaran):
        return 'gagal', 'error di server (%s)' % ringkas_exception(keluaran)

    # 400 = data/parameter ditolak. Di BE sungguhan ini bisa wajar
    # (aturan validasi tiap perusahaan berbeda), jadi dilaporkan sebagai peringatan.
    if any(s == 400 for s in status):
        if sasaran == 'stub':
            return 'gagal', 'status HTTP 400'
        return 'peringatan', 'status HTTP 400 (validasi perusahaan)'

    if 'Tidak ada data untuk diexport' in keluaran:
        return 'peringatan', 'tidak ada data untuk diexport'

    # Demo yang membaca isi respons harus benar-benar mencetak isinya.
    # Tanpa pemeriksaan ini, demo yang salah membaca struktur JSON bisa lolos
    # begitu saja karena tidak error (misalnya PHP yang hanya mencetak kosong).
    if sasaran == 'stub' and kasus is not None:
        hilang = [t for t in kasus.harus_memuat if t not in keluaran]
        if hilang:
            return 'gagal', 'keluaran tidak memuat %r' % hilang[0]

    return 'ok', ''


def jalankan_kasus(bahasa, kasus, folder_kerja, batas_waktu):
    """Jalankan 1 file demo, kembalikan (kode_keluar, keluaran)."""
    nama_file = os.path.basename(kasus.jalur) + bahasa.akhiran
    folder = os.path.join(folder_kerja, os.path.dirname(kasus.jalur))

    perintah = [sys.executable if b is None else b for b in bahasa.perintah] + [nama_file]

    try:
        hasil = subprocess.run(
            perintah, cwd=folder, capture_output=True, text=True,
            encoding='utf-8', errors='replace', timeout=batas_waktu,
        )
        return hasil.returncode, (hasil.stdout or '') + (hasil.stderr or '')
    except subprocess.TimeoutExpired:
        return 1, 'Melebihi batas waktu %s detik.' % batas_waktu
    except FileNotFoundError as gagal:
        return 1, 'Perintah tidak ditemukan: %s' % gagal


def baca_token():
    """
    Token dari GAJIHUB_ACCESS_TOKEN, atau dari file yang ditunjuk GAJIHUB_ACCESS_TOKEN_FILE.
    Versi _FILE membuat token tidak muncul di riwayat perintah maupun daftar proses.
    """
    token = os.environ.get('GAJIHUB_ACCESS_TOKEN', '').strip()
    lokasi = os.environ.get('GAJIHUB_ACCESS_TOKEN_FILE', '').strip()
    if not token and lokasi:
        with open(lokasi, encoding='utf-8') as f:
            token = f.read().strip()
    return token


def alat_tersedia(alat):
    return alat == 'python' or shutil.which(alat) is not None


def main():
    p = argparse.ArgumentParser(description='Menjalankan seluruh file demo API GajiHub.')
    p.add_argument('--bahasa', action='append', choices=sorted(daftar_kasus.BAHASA),
                   help='bahasa yang diuji (boleh diulang). Default: semua yang terpasang.')
    p.add_argument('--sasaran', choices=('stub', 'real'), default='stub',
                   help='stub = server tiruan lokal (default), real = API GajiHub sungguhan')
    p.add_argument('--hanya', default='', help='hanya jalankan demo yang namanya memuat teks ini')
    p.add_argument('--izinkan-ubah-data', action='store_true',
                   help='ikut menjalankan 7 demo yang mengubah data (wajib untuk sasaran real)')
    p.add_argument('--batas-waktu', type=int, default=180, help='batas waktu per demo (detik)')
    p.add_argument('--tampilkan-keluaran', action='store_true', help='tampilkan keluaran tiap demo')
    argumen = p.parse_args()

    # --- tentukan alamat API dan token ---
    catatan_stub = None
    if argumen.sasaran == 'stub':
        catatan_stub = os.path.join(tempfile.mkdtemp(prefix='gajihub-stub-'), 'requests.log')
        host = nyalakan_stub(catatan_stub)
        token = 'gajihub_pat_stub_untuk_pengujian'
        print('Sasaran : stub lokal (%s)' % host)
    else:
        host = os.environ.get('GAJIHUB_API_HOST', '').strip()
        token = baca_token()
        if not host or not token:
            p.error('sasaran "real" butuh GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN (atau GAJIHUB_ACCESS_TOKEN_FILE)')
        print('Sasaran : API sungguhan (%s)' % host)

    id_tenant = {
        'karyawan': os.environ.get('GAJIHUB_TEST_EMPLOYEE_ID'),
        'jabatan': os.environ.get('GAJIHUB_TEST_JOB_POSITION_ID'),
        'pengajuan': os.environ.get('GAJIHUB_TEST_APPROVAL_ID'),
    }

    # --- pilih bahasa ---
    dipilih = argumen.bahasa or sorted(daftar_kasus.BAHASA)
    bahasa_jalan, bahasa_lewat = [], []
    for nama in dipilih:
        b = daftar_kasus.BAHASA[nama]
        (bahasa_jalan if alat_tersedia(b.alat) else bahasa_lewat).append((nama, b))

    if bahasa_lewat:
        print('Dilewati: %s (program belum terpasang)' % ', '.join(n for n, _ in bahasa_lewat))

    # --- pilih kasus ---
    kasus_dipilih = [k for k in daftar_kasus.DAFTAR if argumen.hanya in k.jalur]
    if not argumen.izinkan_ubah_data:
        dilewati = [k for k in kasus_dipilih if k.mengubah]
        kasus_dipilih = [k for k in kasus_dipilih if not k.mengubah]
        if dilewati:
            print('Dilewati: %d demo yang mengubah data (pakai --izinkan-ubah-data untuk menjalankannya)'
                  % len(dilewati))

    print('Menguji : %d demo x %d bahasa\n' % (len(kasus_dipilih), len(bahasa_jalan)))
    return laporkan(argumen, bahasa_jalan, kasus_dipilih, host, token, id_tenant, catatan_stub)


def laporkan(argumen, bahasa_jalan, kasus_dipilih, host, token, id_tenant, catatan_stub):
    """Jalankan semua kombinasi bahasa x demo, lalu cetak ringkasannya."""
    lencana = {'ok': HIJAU + 'OK  ' + NORMAL,
               'peringatan': KUNING + 'WARN' + NORMAL,
               'gagal': MERAH + 'GAGAL' + NORMAL}
    jumlah = {'ok': 0, 'peringatan': 0, 'gagal': 0}
    kegagalan = []

    for urutan_bahasa, (nama_bahasa, bahasa) in enumerate(bahasa_jalan):
        print('--- %s ---' % nama_bahasa)
        folder_kerja = tempfile.mkdtemp(prefix='gajihub-uji-%s-' % nama_bahasa)

        # ID untuk bahasa ini. Diawali dari environment variable, lalu ditimpa oleh ID
        # yang dicetak demo sebelumnya (misalnya ID jabatan yang baru dibuat), sehingga
        # demo ubah/hapus bekerja pada data buatan pengujian, bukan data yang sudah ada.
        id_bahasa = dict(id_tenant)

        # GAJIHUB_TEST_EMPLOYEE_ID boleh berisi beberapa ID dipisah koma, satu per bahasa,
        # agar bahasa-bahasa tidak berebut jatah cuti / jam lembur karyawan yang sama.
        daftar_karyawan = [x.strip() for x in (id_tenant.get('karyawan') or '').split(',') if x.strip()]
        if daftar_karyawan:
            id_bahasa['karyawan'] = daftar_karyawan[urutan_bahasa % len(daftar_karyawan)]

        try:
            for kasus in kasus_dipilih:
                sumber = os.path.join(AKAR, bahasa.folder, kasus.jalur + bahasa.akhiran)
                if not os.path.exists(sumber):
                    print('  %s %s (file tidak ada)' % (lencana['gagal'], kasus.nama))
                    jumlah['gagal'] += 1
                    kegagalan.append((nama_bahasa, kasus.nama, 'file tidak ada'))
                    continue

                # Tanpa ID yang benar, demo hanya akan ditolak server. Lebih jujur
                # dilaporkan sebagai "tidak ada data" daripada memanggil API dengan ID contoh.
                kosong = [j for j in kasus.butuh_id if not id_bahasa.get(j)]
                if argumen.sasaran == 'real' and kosong:
                    jumlah['peringatan'] += 1
                    print('  %s %s %s' % (lencana['peringatan'], kasus.nama,
                                          ABU + 'dilewati: tidak ada ID %s untuk diuji' % kosong[0] + NORMAL))
                    continue

                tujuan = os.path.join(folder_kerja, kasus.jalur + bahasa.akhiran)
                siapkan_berkas(sumber, tujuan, host, token, kasus, id_bahasa)

                kode, keluaran = jalankan_kasus(bahasa, kasus, folder_kerja, argumen.batas_waktu)
                status, alasan = nilai_hasil(kode, keluaran, argumen.sasaran, kasus)

                for jenis, pola in kasus.menghasilkan.items():
                    cocok = re.search(pola, keluaran, re.M)
                    if cocok:
                        id_bahasa[jenis] = cocok.group(1)

                jumlah[status] += 1
                keterangan = (' ' + ABU + alasan + NORMAL) if alasan else ''
                print('  %s %s%s' % (lencana[status], kasus.nama, keterangan))

                if status == 'gagal':
                    kegagalan.append((nama_bahasa, kasus.nama, alasan))
                if argumen.tampilkan_keluaran or status == 'gagal':
                    for baris in keluaran.strip().splitlines()[:12]:
                        print('       ' + ABU + baris + NORMAL)
        finally:
            shutil.rmtree(folder_kerja, ignore_errors=True)
        print()

    total = sum(jumlah.values())
    print('=' * 60)
    print('Total %d  |  %sOK %d%s  %sWARN %d%s  %sGAGAL %d%s'
          % (total, HIJAU, jumlah['ok'], NORMAL, KUNING, jumlah['peringatan'], NORMAL,
             MERAH, jumlah['gagal'], NORMAL))

    if kegagalan:
        print('\nYang gagal:')
        for bahasa, nama, alasan in kegagalan:
            print('  - [%s] %s: %s' % (bahasa, nama, alasan))

    if catatan_stub and os.path.exists(catatan_stub):
        print('\nCatatan request stub: %s' % catatan_stub)

    return 1 if kegagalan else 0


if __name__ == '__main__':
    sys.exit(main())
