# Demo API GajiHub (Node.js)

Setiap file berdiri sendiri: **tanpa `npm install`**, tanpa file bantu lain. Hanya memakai fitur bawaan Node.js (`fetch`).

## Persiapan

**Node.js 18 atau lebih baru.** Cek dengan `node --version`.

## Menjalankan Demo

1. Buka file demo, lalu isi 2 baris di bagian **Konfigurasi**:

   ```js
   const API_HOST = 'https://namaperusahaan.api.kledo.com/api/v1';
   const ACCESS_TOKEN = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx';
   ```

2. Jalankan lewat terminal:

   ```bash
   cd nodejs/01-authentication
   node 01-check-token.mjs
   ```

Mulailah dari `01-authentication/01-check-token.mjs` untuk memastikan token sudah benar.
File Excel hasil export tersimpan di folder `hasil-unduhan/` di sebelah file demo.

Filter tambahan sudah disiapkan dalam bentuk komentar `//`. Hapus tanda `//` untuk mengaktifkannya.

> File memakai akhiran `.mjs` agar bisa langsung memakai `await` tanpa konfigurasi tambahan.

> Menulis token langsung di file hanya untuk mencoba. Untuk aplikasi sungguhan, simpan token di `.env`,
> lihat contoh NestJS di [01-authentication/nestjs/](01-authentication/nestjs/).

## Daftar Demo

Lihat [README utama](../README.md#daftar-demo). Nama file sama untuk semua bahasa, dengan akhiran `.mjs`.

## Unduh Laporan Otomatis

```bash
# Laporan kemarin
node nodejs/11-scheduled-download/download-attendance-reports.mjs

# Laporan rentang tanggal tertentu
node nodejs/11-scheduled-download/download-attendance-reports.mjs 2026-09-01 2026-09-30
```

**Windows (Task Scheduler)** — buat **Basic Task** harian, pilih **Start a program**, lalu isi:

- **Program/script**: `node` (atau `C:\Program Files\nodejs\node.exe`)
- **Add arguments**: `download-attendance-reports.mjs`
- **Start in**: folder tempat file tersebut, contoh `C:\gajihub-api-demo\nodejs\11-scheduled-download`

**Linux / macOS (cron)** — jalankan `crontab -e`, lalu tambahkan (setiap hari jam 06:00):

```text
0 6 * * * node /lokasi/gajihub-api-demo/nodejs/11-scheduled-download/download-attendance-reports.mjs >> /var/log/unduh-absensi.log 2>&1
```

## Kendala Khusus Node.js

Kendala umum (401, 403, dll) ada di [README utama](../README.md#jika-terjadi-kendala).

| Pesan | Solusi |
|---|---|
| `fetch is not defined` / `AbortSignal.timeout is not a function` | Versi Node.js terlalu lama. Gunakan Node.js 18 atau lebih baru. |
| `Cannot use import statement outside a module` / `await is only valid...` | Pastikan akhiran file `.mjs`, bukan `.js`. |
| `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` / `UNABLE_TO_VERIFY_LEAF_SIGNATURE` / `unable to verify the first certificate` | Sertifikat server tidak dikenali Node.js. Node.js punya daftar CA sendiri, jadi sertifikat yang sudah dipercaya Windows/macOS belum tentu dipercaya Node.js. Jalankan dengan `node --use-system-ca` (Node.js 22+) agar memakai daftar CA sistem, atau arahkan environment variable `NODE_EXTRA_CA_CERTS` ke file sertifikat CA Anda. |
