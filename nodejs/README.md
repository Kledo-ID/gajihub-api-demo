# Demo API GajiHub (Node.js)

Versi Node.js dari demo PHP di folder utama. Isi, endpoint, dan parameternya sama persis.

- **tanpa `npm install`**: hanya memakai fitur bawaan Node.js (`fetch`);
- dijalankan **lewat terminal**.

## Persiapan

1. **Node.js 18 atau lebih baru.** Cek dengan `node --version`.
2. Buat file `.env` di **folder utama** `gajihub-api-demo/` (bukan di folder `nodejs/`).
   Caranya sama seperti demo PHP, lihat [README utama](../README.md) bagian 3 dan 4.
   Satu file `.env` dipakai bersama oleh demo PHP, Python, dan Node.js.

## Menjalankan Demo

```bash
cd nodejs/demo/absensi
node 1-absensi-harian.mjs
```

File Excel hasil export tersimpan di folder `gajihub-api-demo/hasil-unduhan/`.

Filter tambahan sudah disiapkan dalam bentuk komentar `//`. Hapus tanda `//` untuk mengaktifkannya.

> File memakai akhiran `.mjs` (ES Module) agar bisa langsung memakai `await` tanpa konfigurasi tambahan.

## Daftar Demo

Sama dengan [README utama bagian 6](../README.md#6-daftar-demo), cukup ganti akhiran `.php` menjadi `.mjs`.

```
nodejs/
├── gajihub.mjs         -> fungsi bantu yang dipakai semua demo (tidak perlu diubah)
└── demo/
    ├── absensi/        ├── cuti/         ├── gaji/     ├── kasbon/
    ├── karyawan/       ├── lembur/       ├── reimbursement/
    ├── data-master/    ├── persetujuan/  └── unduh-otomatis/
```

## Unduh Laporan Otomatis

```bash
# Laporan kemarin
node nodejs/demo/unduh-otomatis/unduh-laporan-absensi.mjs

# Laporan rentang tanggal tertentu
node nodejs/demo/unduh-otomatis/unduh-laporan-absensi.mjs 2026-09-01 2026-09-30
```

- **Windows (Task Scheduler)**: seperti [README utama bagian 7](../README.md#7-unduh-laporan-otomatis-setiap-hari), dengan
  **Program/script** `node` (atau `C:\Program Files\nodejs\node.exe`), **Add arguments** `unduh-laporan-absensi.mjs`,
  **Start in** `...\gajihub-api-demo\nodejs\demo\unduh-otomatis`.
- **Linux / macOS (cron)**:

  ```text
  0 6 * * * node /lokasi/gajihub-api-demo/nodejs/demo/unduh-otomatis/unduh-laporan-absensi.mjs >> /var/log/unduh-absensi.log 2>&1
  ```

## Membuat Program Sendiri

Letakkan file `.mjs` baru di dalam `nodejs/demo/<folder>/`, lalu:

```js
import { apiGet, apiPost, unduhFile, tanggal } from '../../gajihub.mjs';

// Ambil data (GET)
const hasil = await apiGet('/hr/attendances/daily/pagination', { date: tanggal(), per_page: 100 });

if (hasil.sukses) {
    for (const absen of hasil.data.data.data) {
        // simpan ke database Anda di sini
    }
}

// Unduh file Excel
await unduhFile('/hr/attendances/detail/export/xls', { date_started: '2026-09-01', date_ended: '2026-09-30' });

// Kirim data (POST / PUT / PATCH / DELETE)
await apiPost('/hr/overtimes', { /* data */ });
```

Catatan penting dan daftar kendala (401, 403, dll) sama dengan [README utama](../README.md#9-catatan-penting).
Kendala khusus Node.js:

| Pesan | Solusi |
|---|---|
| `fetch is not defined` / `AbortSignal.timeout is not a function` | Versi Node.js terlalu lama. Gunakan Node.js 18 atau lebih baru. |
| `Cannot use import statement outside a module` | Pastikan akhiran file `.mjs`, bukan `.js`. |
