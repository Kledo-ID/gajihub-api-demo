"""
============================================================================
 gajihub.py — Fungsi bantu yang dipakai oleh semua demo Python
============================================================================

 File ini di-"import" oleh setiap file demo. Anda TIDAK perlu mengubahnya.
 Alamat API dan token diatur di file .env di folder utama gajihub-api-demo/
 (salin dari .env.example). File .env yang sama dipakai demo PHP & Node.js.

 Hanya memakai library bawaan Python (tanpa pip install).

 Daftar fungsi:
   mulai_demo('Judul')                  -> tampilkan judul demo
   api_get('/endpoint', {parameter})    -> ambil data            (GET)
   api_post('/endpoint', {data})        -> tambah data           (POST)
   api_put('/endpoint', {data})         -> ubah data             (PUT)
   api_patch('/endpoint', {data})       -> ubah sebagian data    (PATCH)
   api_delete('/endpoint')              -> hapus data            (DELETE)
   unduh_file('/endpoint', {parameter}) -> unduh file Excel/CSV ke folder hasil-unduhan/
   tampilkan(hasil)                     -> cetak hasil request ke layar
   tulis('teks')                        -> cetak satu baris teks

 Fungsi tanggal (zona waktu Asia/Jakarta):
   tanggal()      -> hari ini, YYYY-MM-DD   tanggal(-1) = kemarin, tanggal(7) = 7 hari lagi
   awal_bulan()   -> YYYY-MM-01             akhir_bulan() -> tanggal terakhir bulan ini
   bulan_ini()    -> YYYY-MM                bulan_lalu()  -> YYYY-MM bulan lalu

 Setiap fungsi api_* mengembalikan dict:
   {
     'status': 200,       # kode HTTP (200 = berhasil)
     'sukses': True,      # True jika status 2xx
     'data':   {...},     # isi respons JSON yang sudah diubah jadi dict Python
     'isi':    b'...',    # isi respons mentah (bytes / isi file)
     'header': {...},     # header respons (nama header huruf kecil)
   }
============================================================================
"""

import calendar
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Folder utama gajihub-api-demo/ (satu tingkat di atas folder python/)
FOLDER_UTAMA = Path(__file__).resolve().parent.parent

# Folder tempat file hasil export disimpan
FOLDER_UNDUHAN = FOLDER_UTAMA / "hasil-unduhan"

# Zona waktu Asia/Jakarta (WIB, UTC+7)
WIB = timezone(timedelta(hours=7))

# Agar huruf non-ASCII tampil benar di terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ----------------------------------------------------------------------------
# 1. Konfigurasi dari file .env
# ----------------------------------------------------------------------------

_isi_env = None


def konfigurasi(nama):
    """Ambil nilai konfigurasi dari file .env, misalnya konfigurasi('API_HOST')."""
    global _isi_env

    if _isi_env is None:
        file_env = FOLDER_UTAMA / ".env"

        if not file_env.is_file():
            berhenti("File .env belum ada. Salin .env.example menjadi .env, lalu isi API_HOST dan ACCESS_TOKEN.")

        _isi_env = {}
        for baris in file_env.read_text(encoding="utf-8").splitlines():
            baris = baris.strip()

            # Lewati komentar (#) dan baris tanpa tanda =
            if baris == "" or baris.startswith("#") or "=" not in baris:
                continue

            kunci, nilai = baris.split("=", 1)
            _isi_env[kunci.strip()] = nilai.strip().strip("\"'")

    if not _isi_env.get(nama):
        berhenti(f"{nama} belum diisi di file .env")

    return _isi_env[nama]


# ----------------------------------------------------------------------------
# 2. Mengirim request ke API GajiHub
# ----------------------------------------------------------------------------

def api_get(endpoint, parameter=None):
    return kirim_request("GET", endpoint, parameter)


def api_post(endpoint, data=None):
    return kirim_request("POST", endpoint, data)


def api_put(endpoint, data=None):
    return kirim_request("PUT", endpoint, data)


def api_patch(endpoint, data=None):
    return kirim_request("PATCH", endpoint, data)


def api_delete(endpoint, parameter=None):
    return kirim_request("DELETE", endpoint, parameter)


def buat_query(parameter):
    """Ubah dict parameter menjadi teks query URL, contoh: page=1&ids[]=1&ids[]=2"""
    pasangan = []
    for kunci, nilai in parameter.items():
        if nilai is None:
            continue  # nilai kosong tidak dikirim
        if isinstance(nilai, (list, tuple)):
            pasangan += [(f"{kunci}[]", isi) for isi in nilai]
        elif isinstance(nilai, bool):
            pasangan.append((kunci, int(nilai)))
        else:
            pasangan.append((kunci, nilai))
    return urllib.parse.urlencode(pasangan)


def kirim_request(method, endpoint, data=None):
    """
    Inti dari semua request. Semua endpoint GajiHub diawali /hr,
    jadi endpoint cukup ditulis mulai dari /hr/...
    """
    data = data or {}
    url = konfigurasi("API_HOST").rstrip("/") + endpoint

    header = {
        "Accept": "application/json",
        "Authorization": "Bearer " + konfigurasi("ACCESS_TOKEN"),
    }

    # GET/DELETE: parameter dikirim lewat URL (?page=1&per_page=10)
    # POST/PUT/PATCH: data dikirim sebagai JSON di body request
    body = None
    if method in ("POST", "PUT", "PATCH"):
        header["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    elif data:
        url += "?" + buat_query(data)

    tulis(f"{method} {url}")

    request = urllib.request.Request(url, data=body, headers=header, method=method)

    try:
        # Export bisa lama, tunggu maksimal 5 menit
        with urllib.request.urlopen(request, timeout=300) as respons:
            status, isi, header_respons = respons.status, respons.read(), respons.headers
    except urllib.error.HTTPError as gagal:
        # Status 4xx / 5xx tetap dibaca isinya (berisi pesan error dari server)
        status, isi, header_respons = gagal.code, gagal.read(), gagal.headers
    except (urllib.error.URLError, OSError) as gagal:
        berhenti(f"Gagal terhubung ke server: {gagal}")

    try:
        data_json = json.loads(isi)
    except ValueError:
        data_json = None  # bukan JSON, misalnya isi file Excel

    return {
        "status": status,
        "sukses": 200 <= status < 300,
        "data": data_json,
        "isi": isi,
        "header": {kunci.lower(): nilai for kunci, nilai in header_respons.items()},
    }


# ----------------------------------------------------------------------------
# 3. Mengunduh file export (Excel / CSV)
# ----------------------------------------------------------------------------

def unduh_file(endpoint, parameter=None):
    """
    Unduh file export lalu simpan ke folder hasil-unduhan/.
    Mengembalikan lokasi file, atau None jika gagal / tidak ada data.
    """
    hasil = api_get(endpoint, parameter)

    # Jika server membalas JSON, berarti ada pesan error (misalnya format tanggal salah)
    if not hasil["sukses"] or hasil["data"] is not None:
        tampilkan(hasil)
        return None

    # Respons kosong = tidak ada data pada periode/filter tersebut
    if hasil["isi"] == b"":
        tulis("Tidak ada data untuk diexport pada periode/filter tersebut.")
        return None

    # Ambil nama file dari header "Content-Disposition: attachment; filename=..."
    nama_file = "export_" + datetime.now(WIB).strftime("%Y%m%d_%H%M%S")
    cocok = re.search(r'filename="?([^";]+)"?', hasil["header"].get("content-disposition", ""), re.IGNORECASE)
    if cocok:
        nama_file = os.path.basename(cocok.group(1))

    FOLDER_UNDUHAN.mkdir(parents=True, exist_ok=True)

    lokasi_file = FOLDER_UNDUHAN / nama_file
    lokasi_file.write_bytes(hasil["isi"])

    tulis(f"Berhasil! File disimpan di: {lokasi_file} ({len(hasil['isi'])} bytes)")

    return lokasi_file


# ----------------------------------------------------------------------------
# 4. Menampilkan hasil
# ----------------------------------------------------------------------------

def mulai_demo(judul):
    """Tampilkan judul demo."""
    tulis("")
    tulis(f"=== {judul} ===")


def tampilkan(hasil):
    """Cetak hasil request: status HTTP + isi respons dalam format JSON yang rapi."""
    tulis(f"Status HTTP: {hasil['status']}" + (" (berhasil)" if hasil["sukses"] else " (gagal)"))

    if not hasil["sukses"]:
        tulis(arti_status(hasil["status"]))

    if hasil["data"] is not None:
        teks = json.dumps(hasil["data"], indent=4, ensure_ascii=False)
    else:
        teks = hasil["isi"].decode("utf-8", errors="replace")

    tulis(teks)


def tulis(teks):
    """Cetak satu baris teks."""
    print(teks)


def arti_status(status):
    """Penjelasan singkat untuk kode status HTTP yang sering muncul."""
    daftar = {
        400: "Artinya: parameter/data yang dikirim tidak valid. Lihat pesan di bawah.",
        401: "Artinya: token tidak valid atau sudah kedaluwarsa. Periksa ACCESS_TOKEN di file .env.",
        403: "Artinya: user pemilik token tidak punya hak akses ke fitur ini.",
        404: "Artinya: data atau endpoint tidak ditemukan. Periksa ID / alamat endpoint.",
        429: "Artinya: terlalu banyak request. Tunggu sebentar lalu coba lagi.",
    }
    if status in daftar:
        return daftar[status]
    return "Artinya: terjadi kesalahan di server. Coba lagi beberapa saat." if status >= 500 else ""


def berhenti(pesan):
    """Tampilkan pesan lalu hentikan program."""
    tulis("ERROR: " + pesan)
    sys.exit(1)


# ----------------------------------------------------------------------------
# 5. Fungsi tanggal (zona waktu Asia/Jakarta)
# ----------------------------------------------------------------------------

def tanggal(tambah_hari=0):
    """Tanggal hari ini (YYYY-MM-DD). tanggal(-1) = kemarin, tanggal(7) = 7 hari lagi."""
    return (datetime.now(WIB) + timedelta(days=tambah_hari)).strftime("%Y-%m-%d")


def bulan_ini():
    """Bulan ini (YYYY-MM)."""
    return datetime.now(WIB).strftime("%Y-%m")


def awal_bulan():
    """Tanggal pertama bulan ini (YYYY-MM-01)."""
    return bulan_ini() + "-01"


def akhir_bulan():
    """Tanggal terakhir bulan ini (YYYY-MM-DD)."""
    sekarang = datetime.now(WIB)
    return f"{bulan_ini()}-{calendar.monthrange(sekarang.year, sekarang.month)[1]:02d}"


def bulan_lalu():
    """Bulan lalu (YYYY-MM)."""
    return (datetime.now(WIB).replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
