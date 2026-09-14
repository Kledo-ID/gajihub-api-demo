# Demo API GajiHub (PHP)

Kumpulan contoh program PHP sederhana untuk mengambil dan mengirim data ke GajiHub lewat API, memakai **Personal Access Token**.

Semua contoh:

- **tanpa Composer** dan tanpa library tambahan, cukup PHP dengan ekstensi `curl`;
- berupa **1 file pendek per contoh**, dengan penjelasan di setiap baris penting;
- bisa dijalankan **lewat terminal** maupun **lewat browser**.

---

## Daftar Isi

1. [Isi Folder](#1-isi-folder)
2. [Persiapan](#2-persiapan)
3. [Membuat Personal Access Token](#3-membuat-personal-access-token)
4. [Konfigurasi](#4-konfigurasi)
5. [Menjalankan Demo](#5-menjalankan-demo)
6. [Daftar Demo](#6-daftar-demo)
7. [Unduh Laporan Otomatis Setiap Hari](#7-unduh-laporan-otomatis-setiap-hari)
8. [Membuat Program Sendiri](#8-membuat-program-sendiri)
9. [Catatan Penting](#9-catatan-penting)
10. [Jika Terjadi Kendala](#10-jika-terjadi-kendala)

---

## 1. Isi Folder

```
gajihub-api-demo/
├── .env.example        -> contoh konfigurasi (salin menjadi .env)
├── gajihub.php         -> fungsi bantu yang dipakai semua demo (tidak perlu diubah)
├── index.php           -> halaman daftar demo (untuk browser)
├── hasil-unduhan/      -> tempat file Excel hasil export (dibuat otomatis)
├── python/             -> demo yang sama dalam Python (lihat python/README.md)
├── nodejs/             -> demo yang sama dalam Node.js (lihat nodejs/README.md)
└── demo/
    ├── absensi/        -> absensi harian, bulanan, rekap, export Excel
    ├── karyawan/       -> daftar, detail, tambah, export karyawan
    ├── data-master/    -> struktur organisasi, jabatan, level, shift, lokasi, referensi
    ├── cuti/           -> daftar, tambah, export cuti & sisa kuota
    ├── lembur/         -> daftar, tambah, export lembur
    ├── persetujuan/    -> daftar pengajuan & menyetujui pengajuan
    ├── gaji/           -> daftar gaji per periode, export gaji, komponen gaji
    ├── reimbursement/  -> daftar & export reimbursement
    ├── kasbon/         -> saldo, riwayat, export kasbon
    └── unduh-otomatis/ -> script unduh laporan absensi untuk dijadwalkan
```

---

## 2. Persiapan

| Kebutuhan | Keterangan |
|---|---|
| **PHP 8.1 atau lebih baru** | Paling mudah pakai [XAMPP](https://www.apachefriends.org/download.html) (sudah berisi PHP). |
| **Ekstensi curl aktif** | Di XAMPP biasanya sudah aktif. Cek dengan perintah `php -m`, pastikan ada tulisan `curl`. |

Cek versi PHP:

```bash
php --version
```

---

## 3. Membuat Personal Access Token

1. Login ke GajiHub sebagai admin.
2. Buka menu **Pengaturan → API Key**.
3. Tambahkan token baru: isi nama token dan masa berlakunya.
4. **Salin token** yang muncul (diawali `gajihub_pat_`), lalu simpan di tempat aman.
   Token hanya ditampilkan **satu kali**.

> **Penting:**
> - Token bekerja atas nama user yang membuatnya. Hak aksesnya sama dengan hak akses user tersebut.
>   Jika user tidak punya akses ke menu tertentu, API untuk menu itu akan membalas `403`.
> - Jangan bagikan token ke orang lain dan jangan simpan token di Git.

---

## 4. Konfigurasi

1. Salin file `.env.example` menjadi `.env`:

   ```bash
   # Windows
   copy .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```

2. Buka file `.env`, lalu isi:

   ```text
   API_HOST=https://namaperusahaan.api.kledo.com/api/v1
   ACCESS_TOKEN="gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx"
   ```

   - `API_HOST`: alamat API perusahaan Anda, diakhiri `/api/v1`. Tanyakan ke tim GajiHub jika belum tahu.
   - `ACCESS_TOKEN`: Personal Access Token dari langkah 3, diapit tanda petik dua.

---

## 5. Menjalankan Demo

### Cara 1: Lewat terminal

Masuk ke folder demo, lalu jalankan file-nya:

```bash
cd demo/absensi
php 1-absensi-harian.php
```

Hasil request (status dan data JSON) langsung tampil di layar.

### Cara 2: Lewat browser

1. Letakkan folder `gajihub-api-demo` di dalam folder `htdocs` XAMPP (contoh: `C:\xampp\htdocs\gajihub-api-demo`).
2. Jalankan **Apache** dari XAMPP Control Panel.
3. Buka `http://localhost/gajihub-api-demo/`.
4. Pilih demo. Halaman menampilkan kode programnya dulu.
   Klik **Jalankan Request** untuk mengirim request dan melihat hasilnya.

> Setiap demo cukup diubah di bagian parameternya (tanggal, ID karyawan, filter).
> Filter tambahan sudah disiapkan dalam bentuk komentar `//`. Hapus tanda `//` untuk mengaktifkannya.

---

## 6. Daftar Demo

Demo bertanda ✏️ **mengubah data** di GajiHub (menambah, mengubah, menghapus, atau menyetujui).
Coba demo tersebut dengan hati-hati.

### Absensi (`demo/absensi/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-absensi-harian.php` | Absensi semua karyawan pada 1 tanggal | `GET /hr/attendances/daily/pagination` |
| `2-absensi-bulanan-karyawan.php` | Absensi 1 karyawan selama 1 bulan | `GET /hr/attendances/pagination` |
| `3-rekap-absensi.php` | Rekap absensi per karyawan (hadir, terlambat, lembur, dll) | `GET /hr/attendances/summary/pagination` |
| `4-export-absensi-harian.php` | File Excel absensi harian | `GET /hr/attendances/daily/export/xls` |
| `5-export-rekap-absensi.php` | File Excel rekap absensi | `GET /hr/attendances/summary/export/xls` |
| `6-export-detail-absensi.php` | File Excel detail absensi per hari per karyawan | `GET /hr/attendances/detail/export/xls` |

### Karyawan (`demo/karyawan/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-daftar-karyawan.php` | Daftar karyawan beserta ID-nya | `GET /hr/employees/pagination` |
| `2-detail-karyawan.php` | Detail 1 karyawan | `GET /hr/employees/{id}` |
| `3-tambah-karyawan.php` ✏️ | Tambah karyawan (data pribadi, karir, payroll) | `POST /hr/employees/insert` |
| `4-export-karyawan.php` | File Excel data karyawan | `GET /hr/employees/export/xls` |

### Data Master (`demo/data-master/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-struktur-organisasi.php` | Daftar struktur organisasi | `GET /hr/orgStructures` |
| `2-jabatan.php` | Daftar jabatan | `GET /hr/jobPositions` |
| `3-level-jabatan.php` | Daftar level jabatan | `GET /hr/jobLevels` |
| `4-shift.php` | Daftar shift kerja | `GET /hr/shifts` |
| `5-lokasi-absensi.php` | Daftar lokasi absensi | `GET /hr/attendanceLocations` |
| `6-referensi.php` | Kode pilihan (jenis kelamin, agama, status karyawan, dll) | `GET /hr/references/...` |
| `7-tambah-jabatan.php` ✏️ | Tambah jabatan | `POST /hr/jobPositions` |
| `8-ubah-jabatan.php` ✏️ | Ubah jabatan | `PUT /hr/jobPositions/{id}` |
| `9-hapus-jabatan.php` ✏️ | Hapus jabatan | `DELETE /hr/jobPositions/{id}` |

### Cuti (`demo/cuti/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-daftar-cuti-tahunan.php` | Daftar pengajuan cuti tahunan | `GET /hr/leaves/annualLeaves/pagination` |
| `2-tambah-cuti-tahunan.php` ✏️ | Tambah cuti tahunan | `POST /hr/leaves/annualLeaves` |
| `3-export-cuti.php` | File Excel data cuti | `GET /hr/leaves/export/xls` |
| `4-export-sisa-kuota-cuti.php` | File Excel sisa kuota cuti tahunan | `GET /hr/leaves/annualLeaves/export/xls` |

### Lembur (`demo/lembur/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-daftar-lembur.php` | Daftar data lembur | `GET /hr/overtimes/pagination` |
| `2-tambah-lembur.php` ✏️ | Tambah data lembur | `POST /hr/overtimes` |
| `3-export-lembur.php` | File Excel data lembur | `GET /hr/overtimes/export/xls` |

### Persetujuan (`demo/persetujuan/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-daftar-persetujuan.php` | Pengajuan yang menunggu persetujuan | `GET /hr/approvals/pagination` |
| `2-setujui-pengajuan.php` ✏️ | Setujui / tolak pengajuan | `PATCH /hr/approvals/approve` (atau `/decline`) |

### Gaji (`demo/gaji/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-daftar-gaji-per-periode.php` | Daftar gaji karyawan dalam 1 bulan | `GET /hr/payrollPayments` |
| `2-export-gaji-per-periode.php` | File Excel rekap gaji 1 bulan | `GET /hr/payrolls/perPeriod/export/xls` |
| `3-komponen-gaji.php` | Daftar komponen gaji | `GET /hr/salaryComponents/pagination` |

### Reimbursement (`demo/reimbursement/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-daftar-reimbursement.php` | Daftar pengajuan reimbursement | `GET /hr/reimbursements/pagination` |
| `2-export-reimbursement.php` | File Excel reimbursement | `GET /hr/reimbursements/export/xls` |

### Kasbon (`demo/kasbon/`)

| File | Keterangan | Endpoint |
|---|---|---|
| `1-saldo-kasbon.php` | Saldo kasbon per karyawan | `GET /hr/cashReceipt/balance/pagination` |
| `2-riwayat-kasbon.php` | Riwayat pengajuan kasbon | `GET /hr/cashReceipt/history/pagination` |
| `3-export-kasbon.php` | File Excel saldo & riwayat kasbon | `GET /hr/cashReceipt/{balance,history}/export/xls` |

### Unduh Otomatis (`demo/unduh-otomatis/`)

| File | Keterangan |
|---|---|
| `unduh-laporan-absensi.php` | Unduh file Excel detail & rekap absensi kemarin (atau rentang tanggal tertentu) |

---

## 7. Unduh Laporan Otomatis Setiap Hari

Script `demo/unduh-otomatis/unduh-laporan-absensi.php` mengunduh laporan absensi ke folder `hasil-unduhan/`.

```bash
# Laporan kemarin
php demo/unduh-otomatis/unduh-laporan-absensi.php

# Laporan rentang tanggal tertentu
php demo/unduh-otomatis/unduh-laporan-absensi.php 2026-09-01 2026-09-30
```

Agar berjalan otomatis, jadwalkan perintah di atas.

### Windows (Task Scheduler)

1. Buka **Task Scheduler**, lalu klik **Create Basic Task**.
2. Isi nama, contoh `Unduh Absensi GajiHub`, lalu pilih **Daily** dan tentukan jam (contoh `06:00`).
3. Pilih **Start a program**, lalu isi:
   - **Program/script**: `C:\xampp\php\php.exe`
   - **Add arguments**: `unduh-laporan-absensi.php`
   - **Start in**: `C:\xampp\htdocs\gajihub-api-demo\demo\unduh-otomatis`
4. Klik **Finish**.

### Linux / macOS (cron)

Jalankan `crontab -e`, lalu tambahkan baris berikut (setiap hari jam 06:00):

```text
0 6 * * * php /var/www/html/gajihub-api-demo/demo/unduh-otomatis/unduh-laporan-absensi.php >> /var/log/unduh-absensi.log 2>&1
```

---

## 8. Membuat Program Sendiri

Salin salah satu demo, lalu ubah endpoint dan parameternya. Pola dasarnya:

```php
<?php
require __DIR__ . '/../../gajihub.php';

// Ambil data (GET)
$hasil = api_get('/hr/attendances/daily/pagination', [
    'date'     => '2026-09-14',
    'per_page' => 100,
]);

if ($hasil['sukses']) {
    foreach ($hasil['data']['data']['data'] as $absen) {
        // simpan ke database Anda di sini
    }
}

// Unduh file Excel
unduh_file('/hr/attendances/detail/export/xls', [
    'date_started' => '2026-09-01',
    'date_ended'   => '2026-09-30',
]);

// Kirim data (POST / PUT / PATCH / DELETE)
$hasil = api_post('/hr/overtimes', [ /* data */ ]);
```

Jika tidak memakai PHP, setiap request cukup mengirim 2 header berikut:

```text
Authorization: Bearer <ACCESS_TOKEN>
Accept: application/json
```

Contoh dengan curl:

```bash
curl -G "https://namaperusahaan.api.kledo.com/api/v1/hr/attendances/daily/pagination" \
  -H "Authorization: Bearer gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx" \
  -H "Accept: application/json" \
  --data-urlencode "date=2026-09-14"
```

---

## 9. Catatan Penting

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

## 10. Jika Terjadi Kendala

| Pesan / Kondisi | Penyebab & Solusi |
|---|---|
| `File .env belum ada` | Salin `.env.example` menjadi `.env` (lihat bagian 4). |
| `401` | Token salah, terpotong, atau kedaluwarsa. Periksa `ACCESS_TOKEN` di `.env`, atau buat token baru. |
| `403` | User pembuat token tidak punya hak akses ke fitur tersebut. |
| `400` | Parameter tidak valid (misalnya format tanggal salah). Baca pesan error yang ditampilkan. |
| `404` | ID data atau alamat endpoint salah. Pastikan `API_HOST` diakhiri `/api/v1`. |
| `429` | Terlalu banyak request dalam waktu singkat. Tunggu sebentar lalu coba lagi. |
| `Call to undefined function curl_init()` | Ekstensi curl belum aktif. Buka `php.ini`, hapus tanda `;` di depan `extension=curl`, lalu restart Apache. |
| `SSL certificate problem: unable to get local issuer certificate` | PHP belum punya sertifikat CA. Unduh [cacert.pem](https://curl.se/ca/cacert.pem) ke `C:\xampp\php\cacert.pem`, lalu isi `curl.cainfo = "C:\xampp\php\cacert.pem"` di `php.ini`, kemudian restart Apache. |
| `syntax error, unexpected ...` / `never` | Versi PHP terlalu lama. Gunakan PHP 8.1 atau lebih baru. |
