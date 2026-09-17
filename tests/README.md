# Pengujian Otomatis Demo API GajiHub

Menjalankan **seluruh file demo** (38 demo x 4 bahasa = 152 pengujian) lalu memeriksa hasilnya.

Hanya butuh **Python 3.8+**. Tidak ada library tambahan. Bahasa yang programnya belum
terpasang otomatis dilewati, jadi suite tetap bisa jalan walau hanya ada sebagian bahasa.

## Cara Menjalankan

```bash
# Semua bahasa, memakai server tiruan (stub). Tanpa token, tanpa internet.
python tests/run.py

# Ikut menjalankan 7 demo yang mengubah data
python tests/run.py --izinkan-ubah-data

# Hanya bahasa tertentu
python tests/run.py --bahasa go --bahasa python

# Hanya demo tertentu
python tests/run.py --hanya 02-employees
```

Kode keluar `0` jika semua lulus, `1` jika ada yang gagal. Cocok dipakai di CI.

## Isi Folder

```
tests/
├── run.py           -> menjalankan demo dan menilai hasilnya
├── stub_server.py   -> server tiruan API GajiHub (bisa dijalankan sendiri)
└── kasus.py         -> daftar 38 demo + penanda "mengubah data" dan asersi keluaran
```

## Dua Sasaran Pengujian

### 1. `stub` (bawaan)

Server tiruan di komputer sendiri. **Tanpa token, tanpa internet, tanpa menyentuh data siapa pun.**
Semua 38 demo dijalankan, termasuk yang mengubah data (yang "diubah" hanya data tiruan).

Stub juga menolak request tanpa header `Authorization` dan tanpa `X-App: hr`, serta membalas
`404` untuk alamat yang tidak dikenal, sehingga salah alamat langsung ketahuan.

### 2. `real` — API GajiHub sungguhan

```bash
# Linux / macOS
export GAJIHUB_API_HOST="https://namaperusahaan.api.kledo.com/api/v1"
export GAJIHUB_ACCESS_TOKEN="gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx"

# Windows PowerShell
$env:GAJIHUB_API_HOST="https://namaperusahaan.api.kledo.com/api/v1"
$env:GAJIHUB_ACCESS_TOKEN="gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx"

python tests/run.py --sasaran real
```

Agar token tidak tersimpan di riwayat perintah, simpan token di sebuah file lalu tunjuk
file itu dengan `GAJIHUB_ACCESS_TOKEN_FILE` (dipakai bila `GAJIHUB_ACCESS_TOKEN` kosong):

```bash
export GAJIHUB_ACCESS_TOKEN_FILE=/lokasi/aman/token.txt
```

Secara bawaan, **7 demo yang mengubah data tidak dijalankan**. Tambahkan `--izinkan-ubah-data`
hanya jika token menunjuk ke perusahaan percobaan:

```bash
python tests/run.py --sasaran real --izinkan-ubah-data
```

> **PERHATIAN.** Dengan `--izinkan-ubah-data`, suite akan benar-benar menambah karyawan,
> menambah/mengubah/menghapus jabatan, menambah cuti, menambah lembur, dan menyetujui pengajuan.
> Jangan dijalankan pada perusahaan yang dipakai sungguhan.

### ID khusus tenant

Beberapa demo memakai ID contoh (`idKaryawan = 1`, `idJabatan = 0`, `idPengajuan = [0]`)
yang belum tentu ada di perusahaan Anda. Runner menambal ID tersebut sebelum demo dijalankan.

**ID karyawan** diisi lewat environment variable. Boleh beberapa ID dipisah koma: bahasa
pertama memakai ID pertama, bahasa kedua ID kedua, dan seterusnya. Dengan begitu keempat
bahasa tidak berebut jatah cuti atau jam lembur karyawan yang sama.

```bash
export GAJIHUB_TEST_EMPLOYEE_ID=3,4,5,7
```

Pilih karyawan aktif yang sudah punya jatah cuti tahunan (biasanya sudah bekerja lebih dari 1 tahun).

**ID jabatan dan ID pengajuan** diambil otomatis dari demo sebelumnya:

- demo ubah / hapus jabatan memakai jabatan yang **baru saja dibuat** oleh `07-create-job-position`,
  sehingga tidak ada jabatan lama yang ikut terubah atau terhapus;
- demo setujui pengajuan memakai pengajuan pertama dari hasil `01-list-approvals`.

Jika ID yang dibutuhkan tidak tersedia (misalnya tidak ada pengajuan yang menunggu), demo itu
dilewati dan dilaporkan `WARN`, bukan dijalankan dengan ID contoh.

### Menguji server lokal dengan sertifikat sendiri

Server percobaan di komputer sendiri (misalnya `https://app.kledo.test`) biasanya memakai
sertifikat yang dibuat sendiri. PHP, Python, dan Go mengikuti daftar sertifikat milik sistem,
jadi biasanya langsung jalan. **Node.js punya daftar CA sendiri**, sehingga perlu diberi tahu:

```bash
# Linux / macOS
export NODE_OPTIONS=--use-system-ca          # Node.js 22+

# Windows PowerShell
$env:NODE_OPTIONS="--use-system-ca"
```

Tanpa itu, demo Node.js berhenti dengan `unable to verify the first certificate`.

## Cara Menilai Hasil

File demo aslinya tidak pernah diubah. Runner menyalinnya ke folder sementara,
mengisi bagian **Konfigurasi**, menjalankannya, lalu menilai keluarannya:

| Hasil | Artinya |
|---|---|
| `OK` | Demo berjalan normal dan mencetak isi respons dengan benar |
| `WARN` | Berjalan, tapi datanya tidak ada (`Tidak ada data untuk diexport`) atau ditolak validasi (`400`). Wajar di data sungguhan |
| `GAGAL` | Program error, tidak bisa terhubung, status `401/403/404/5xx`, status `400` yang berisi exception dari server, atau keluarannya tidak sesuai |

Selain memeriksa demo tidak error, 12 demo yang membaca isi respons juga diperiksa
**keluarannya** (lihat `harus_memuat` di `kasus.py`). Tanpa pemeriksaan ini, demo yang salah
membaca struktur JSON bisa lolos begitu saja karena kebetulan tidak error.

## Mencoba Stub Sendiri

```bash
python tests/stub_server.py 8101
curl "http://127.0.0.1:8101/api/v1/authentication/user" \
  -H "Authorization: Bearer token-apa-saja" -H "X-App: hr"
```
