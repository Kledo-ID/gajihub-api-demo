# Demo API GajiHub

Kumpulan contoh program untuk mengambil dan mengirim data ke GajiHub lewat API, memakai **Personal Access Token**.
Tersedia dalam **PHP**, **Python**, **Node.js**, dan **Go**, dengan isi yang sama persis.

- **Setiap file berdiri sendiri.** Salin 1 file, isi `API_HOST` dan `ACCESS_TOKEN`, lalu jalankan.
- **Tanpa library tambahan.** Tidak perlu Composer, `pip install`, `npm install`, atau `go get`.
- Ada **contoh penerapan yang aman** untuk aplikasi sungguhan: Laravel, FastAPI, NestJS, dan net/http.

---

## Daftar Isi

1. [Isi Folder](#isi-folder)
2. [Mulai Cepat](#mulai-cepat)
3. [Membuat Personal Access Token](#membuat-personal-access-token)
4. [Cara Kerja Autentikasi](#cara-kerja-autentikasi)
5. [Keamanan Token](#keamanan-token)
6. [Daftar Demo](#daftar-demo)
7. [Pengujian Otomatis](#pengujian-otomatis)
8. [Catatan Penting](#catatan-penting)
9. [Jika Terjadi Kendala](#jika-terjadi-kendala)

---

## Isi Folder

```
gajihub-api-demo/
├── php/                -> demo PHP        (lihat php/README.md)
├── python/             -> demo Python     (lihat python/README.md)
├── nodejs/             -> demo Node.js    (lihat nodejs/README.md)
├── go/                 -> demo Go         (lihat go/README.md)
└── tests/              -> pengujian otomatis semua demo (lihat tests/README.md)

Di dalam setiap folder bahasa (urut dari yang paling dasar):
    ├── 01-authentication/      -> cek token + contoh penerapan aman (laravel/, fastapi/, nestjs/, nethttp/)
    ├── 02-employees/           -> karyawan: daftar, detail, tambah, export
    ├── 03-master-data/         -> struktur organisasi, jabatan, level, shift, lokasi, referensi
    ├── 04-attendance/          -> absensi: harian, bulanan, rekap, export Excel
    ├── 05-leave/               -> cuti: daftar, tambah, export cuti & sisa kuota
    ├── 06-overtime/            -> lembur: daftar, tambah, export
    ├── 07-approvals/           -> persetujuan: daftar pengajuan & menyetujui pengajuan
    ├── 08-payroll/             -> gaji: daftar per periode, export, komponen gaji
    ├── 09-reimbursement/       -> reimbursement: daftar & export
    ├── 10-cash-advance/        -> kasbon: saldo, riwayat, export
    └── 11-scheduled-download/  -> unduh laporan absensi otomatis (untuk dijadwalkan)
```

---

## Mulai Cepat

1. Buat Personal Access Token (lihat [bagian berikut](#membuat-personal-access-token)).
2. Buka file `01-authentication/01-check-token` di folder bahasa pilihan Anda, lalu isi bagian **Konfigurasi** di atas file:
   - `API_HOST`: alamat API perusahaan Anda, diakhiri `/api/v1` (contoh `https://namaperusahaan.api.kledo.com/api/v1`).
     Tanyakan ke tim GajiHub jika belum tahu.
   - `ACCESS_TOKEN`: Personal Access Token Anda (diawali `gajihub_pat_`).
3. Jalankan lewat terminal:

   | Bahasa | Perintah |
   |---|---|
   | PHP 8.1+ | `cd php/01-authentication` lalu `php 01-check-token.php` |
   | Python 3.8+ | `cd python/01-authentication` lalu `python 01-check-token.py` |
   | Node.js 18+ | `cd nodejs/01-authentication` lalu `node 01-check-token.mjs` |
   | Go 1.21+ | `cd go/01-authentication` lalu `go run 01-check-token.go` |

4. Jika muncul `Token valid.`, token sudah benar. Lanjutkan ke demo lain dengan cara yang sama.

Setiap demo cukup diubah di bagian parameternya (tanggal, ID karyawan, filter).
Filter tambahan sudah disiapkan dalam bentuk komentar. Hapus tanda komentarnya untuk mengaktifkan.

---

## Membuat Personal Access Token

1. Login ke GajiHub sebagai admin.
2. Buka menu **Pengaturan → API Key**.
3. Tambahkan token baru: isi nama token dan masa berlakunya.
4. **Salin token** yang muncul (diawali `gajihub_pat_`), lalu simpan di tempat aman.
   Token hanya ditampilkan **satu kali**.

> Token bekerja atas nama user yang membuatnya, dengan hak akses yang sama.
> Jika user tidak punya akses ke menu tertentu, API untuk menu itu akan membalas `403`.

---

## Cara Kerja Autentikasi

Tidak ada proses login. Setiap request cukup membawa header berikut:

```text
Authorization: Bearer <ACCESS_TOKEN>
Accept: application/json
X-App: hr
```

Contoh dengan curl:

```bash
curl "https://namaperusahaan.api.kledo.com/api/v1/authentication/user" \
  -H "Authorization: Bearer gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx" \
  -H "Accept: application/json" \
  -H "X-App: hr"
```

Endpoint `GET /authentication/user` membalas data user pemilik token. Endpoint ini paling cocok untuk memastikan token berfungsi.
Header `X-App: hr` **wajib** untuk endpoint ini. Tanpa header tersebut, server membalas `401`.

---

## Keamanan Token

Demo menulis token langsung di dalam file agar mudah dicoba. **Untuk aplikasi sungguhan, jangan lakukan itu.**

1. **Simpan token di `.env` atau environment variable server**, bukan di kode. Pastikan `.env` masuk `.gitignore`.
2. **Pakai token hanya di server (backend).** Jangan taruh token di JavaScript browser atau aplikasi mobile.
   Aplikasi Anda memanggil server Anda, lalu server Anda yang memanggil API GajiHub.
3. **Buat user khusus integrasi** dengan hak akses seminimal mungkin, karena token mewarisi hak akses user pembuatnya.
4. **Satu token untuk satu aplikasi**, agar bisa dicabut tanpa mengganggu integrasi lain.
5. **Atur masa berlaku** dan ganti token secara berkala. Jika token bocor, segera hapus di **Pengaturan → API Key**.
6. **Jangan mencatat token** di log atau pesan error.
7. **Selalu gunakan HTTPS** (`API_HOST` diawali `https://`).

Contoh penerapannya (token di `.env`, klien yang bisa dipakai ulang, penanganan error yang tidak membocorkan token):

| Framework | Folder |
|---|---|
| Laravel | [php/01-authentication/laravel/](php/01-authentication/laravel/) |
| FastAPI | [python/01-authentication/fastapi/](python/01-authentication/fastapi/) |
| NestJS | [nodejs/01-authentication/nestjs/](nodejs/01-authentication/nestjs/) |
| Go (net/http) | [go/01-authentication/nethttp/](go/01-authentication/nethttp/) |

---

## Daftar Demo

Nama file sama untuk semua bahasa. Akhirannya `.php`, `.py`, `.mjs`, atau `.go`.
Demo bertanda ✏️ **mengubah data** di GajiHub (menambah, mengubah, menghapus, atau menyetujui). Coba dengan hati-hati.

### Autentikasi (`01-authentication/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-check-token` | Cek token valid & siapa pemiliknya | `GET /authentication/user` |

### Karyawan (`02-employees/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-list-employees` | Daftar karyawan beserta ID-nya | `GET /hr/employees/pagination` |
| `02-employee-detail` | Detail 1 karyawan | `GET /hr/employees/{id}` |
| `03-create-employee` ✏️ | Tambah karyawan (data pribadi, karir, payroll) | `POST /hr/employees/insert` |
| `04-export-employees` | File Excel data karyawan | `GET /hr/employees/export/xls` |

### Data Master (`03-master-data/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-org-structures` | Daftar struktur organisasi | `GET /hr/orgStructures` |
| `02-job-positions` | Daftar jabatan | `GET /hr/jobPositions` |
| `03-job-levels` | Daftar level jabatan | `GET /hr/jobLevels` |
| `04-shifts` | Daftar shift kerja | `GET /hr/shifts` |
| `05-attendance-locations` | Daftar lokasi absensi | `GET /hr/attendanceLocations` |
| `06-references` | Kode pilihan (jenis kelamin, agama, status karyawan, dll) | `GET /hr/references/...` |
| `07-create-job-position` ✏️ | Tambah jabatan | `POST /hr/jobPositions` |
| `08-update-job-position` ✏️ | Ubah jabatan | `PUT /hr/jobPositions/{id}` |
| `09-delete-job-position` ✏️ | Hapus jabatan | `DELETE /hr/jobPositions/{id}` |

### Absensi (`04-attendance/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-daily-attendance` | Absensi semua karyawan pada 1 tanggal | `GET /hr/attendances/daily/pagination` |
| `02-monthly-attendance-by-employee` | Absensi 1 karyawan selama 1 bulan | `GET /hr/attendances/pagination` |
| `03-attendance-summary` | Rekap absensi per karyawan (hadir, terlambat, lembur, dll) | `GET /hr/attendances/summary/pagination` |
| `04-export-daily-attendance` | File Excel absensi harian | `GET /hr/attendances/daily/export/xls` |
| `05-export-attendance-summary` | File Excel rekap absensi | `GET /hr/attendances/summary/export/xls` |
| `06-export-attendance-detail` | File Excel detail absensi per hari per karyawan | `GET /hr/attendances/detail/export/xls` |

### Cuti (`05-leave/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-list-annual-leaves` | Daftar pengajuan cuti tahunan | `GET /hr/leaves/annualLeaves/pagination` |
| `02-create-annual-leave` ✏️ | Tambah cuti tahunan | `POST /hr/leaves/annualLeaves` |
| `03-export-leaves` | File Excel data cuti | `GET /hr/leaves/export/xls` |
| `04-export-annual-leave-balance` | File Excel sisa kuota cuti tahunan | `GET /hr/leaves/annualLeaves/export/xls` |

### Lembur (`06-overtime/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-list-overtimes` | Daftar data lembur | `GET /hr/overtimes/pagination` |
| `02-create-overtime` ✏️ | Tambah data lembur | `POST /hr/overtimes` |
| `03-export-overtimes` | File Excel data lembur | `GET /hr/overtimes/export/xls` |

### Persetujuan (`07-approvals/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-list-approvals` | Pengajuan yang menunggu persetujuan | `GET /hr/approvals/pagination` |
| `02-approve-requests` ✏️ | Setujui / tolak pengajuan | `PATCH /hr/approvals/approve` (atau `/decline`) |

### Gaji (`08-payroll/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-list-payroll-by-period` | Daftar gaji karyawan dalam 1 bulan | `GET /hr/payrollPayments` |
| `02-export-payroll-by-period` | File Excel rekap gaji 1 bulan | `GET /hr/payrolls/perPeriod/export/xls` |
| `03-salary-components` | Daftar komponen gaji | `GET /hr/salaryComponents/pagination` |

### Reimbursement (`09-reimbursement/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-list-reimbursements` | Daftar pengajuan reimbursement | `GET /hr/reimbursements/pagination` |
| `02-export-reimbursements` | File Excel reimbursement | `GET /hr/reimbursements/export/xls` |

### Kasbon (`10-cash-advance/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `01-cash-advance-balances` | Saldo kasbon per karyawan | `GET /hr/cashReceipt/balance/pagination` |
| `02-cash-advance-history` | Riwayat pengajuan kasbon | `GET /hr/cashReceipt/history/pagination` |
| `03-export-cash-advances` | File Excel saldo & riwayat kasbon | `GET /hr/cashReceipt/{balance,history}/export/xls` |

### Unduh Otomatis (`11-scheduled-download/`)

| File | Keterangan |
|---|---|
| `download-attendance-reports` | Unduh file Excel detail & rekap absensi kemarin (atau rentang tanggal tertentu). Cara menjadwalkannya ada di README tiap bahasa. |

---

## Pengujian Otomatis

Seluruh demo bisa dijalankan sekaligus untuk memastikan semuanya masih berfungsi:

```bash
python tests/run.py
```

Memakai server tiruan di komputer sendiri, jadi **tanpa token, tanpa internet, dan tanpa
mengubah data siapa pun**. Untuk mengujinya terhadap API GajiHub sungguhan, lihat
[tests/README.md](tests/README.md).

---

## Catatan Penting

- **Format respons.** Semua respons JSON berbentuk `{ "success": true, "data": ..., "message": "..." }`.
- **Data per halaman.** Endpoint `.../pagination` mengirim data per halaman.
  Naikkan `page` (1, 2, 3, …) sampai `last_page` untuk mengambil semua data.
- **Format tanggal.** `YYYY-MM-DD` (contoh `2026-09-14`), sedangkan untuk bulan `YYYY-MM` (contoh `2026-09`).
- **Export Excel.**
  - Ganti `xls` di alamat endpoint menjadi `csv` untuk format CSV.
  - Format `xls` menghasilkan file `.xlsx`.
  - Jika tidak ada data pada periode tersebut, tidak ada file yang dibuat.
- **Tambah karyawan.**
  - Kolom yang wajib diisi mengikuti pengaturan validasi data karyawan di GajiHub, sehingga bisa berbeda antar perusahaan.
  - Jika ada kolom yang kurang, pesan error menyebutkan kolom tersebut.
- **Ubah karyawan.**
  - Endpoint yang dipakai: `PUT /hr/employees/{id}`, dengan bagian `personal`, `career`, dan/atau `payroll`.
  - Setiap bagian yang dikirim harus berisi data lengkap bagian tersebut, bukan hanya kolom yang berubah.
- **Export gaji.** Periode harus sudah memiliki data gaji. Jika belum, server membalas `Period yang dipilih tidak valid.`

---

## Jika Terjadi Kendala

| Pesan / Kondisi | Penyebab & Solusi |
|---|---|
| `API_HOST dan ACCESS_TOKEN belum diisi` | Isi bagian **Konfigurasi** di atas file demo. |
| `401` | Token salah, terpotong, atau kedaluwarsa. Periksa `ACCESS_TOKEN`, atau buat token baru. Jika memanggil API sendiri, pastikan header `X-App: hr` ikut dikirim. |
| `403` | User pembuat token tidak punya hak akses ke fitur tersebut. |
| `400` | Parameter tidak valid (misalnya format tanggal salah). Baca pesan error yang ditampilkan. |
| `404` | ID data atau alamat endpoint salah. Pastikan `API_HOST` diakhiri `/api/v1`. |
| `429` | Terlalu banyak request dalam waktu singkat. Tunggu sebentar lalu coba lagi. |
| `Gagal terhubung ke server` | `API_HOST` salah atau tidak ada koneksi internet. |

Kendala khusus tiap bahasa (instalasi, sertifikat SSL, versi) ada di README folder [php/](php/README.md), [python/](python/README.md), [nodejs/](nodejs/README.md), dan [go/](go/README.md).
