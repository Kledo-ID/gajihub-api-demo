# Contoh Autentikasi API GajiHub di Express

Contoh penerapan yang aman untuk aplikasi sungguhan: token disimpan di `.env`, dipakai hanya di server,
dan dibungkus dalam satu modul klien yang bisa dipakai ulang.

Diuji dengan Node.js 25 dan Express 5.2.

## Isi Folder

```
express/
├── .env.example   -> contoh konfigurasi (salin menjadi .env)
├── package.json   -> library yang dibutuhkan + perintah npm start
├── gajihub.js     -> klien API GajiHub (header autentikasi ada di sini)
└── server.js      -> server Express dengan contoh endpoint GET /gajihub/me
```

## Cara Menjalankan

Butuh **Node.js 20.6 atau lebih baru** (untuk opsi `--env-file`).

```bash
cd nodejs/01-authentication/express

# 1. Pasang library
npm install

# 2. Salin .env.example menjadi .env, lalu isi GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux

# 3. Jalankan server
npm start
```

Buka `http://localhost:3000/gajihub/me`. Jika token benar, hasilnya:

```json
{"id": 1, "name": "Nama User", "email": "user@perusahaan.com"}
```

- Jika token salah atau kedaluwarsa, hasilnya `502` dengan pesan umum, dan detailnya
  (misalnya `[GajiHub] status 401: Unauthenticated.`) tercatat di log server.
- Jika `GAJIHUB_API_HOST` / `GAJIHUB_ACCESS_TOKEN` belum diisi, server menolak start.

## Memanggil Endpoint Lain

Import `gajihubRequest`, lalu panggil dari route Anda:

```js
import { gajihubRequest } from './gajihub.js';

app.get('/karyawan', async (req, res) => {
    const halaman = await gajihubRequest('GET', '/hr/employees/pagination', { query: { page: 1, per_page: 20 } });
    res.json(halaman.data);
});
```

Untuk `POST`/`PUT`/`PATCH`, kirim data dengan `{ body: {...} }`.
Daftar endpoint ada di [README utama](../../../README.md#daftar-demo).

## Praktik Keamanan yang Diterapkan

- Token hanya ada di `.env` (atau environment variable server), dibaca lewat `node --env-file=.env`.
- Token hanya dipakai di server. Browser / aplikasi mobile memanggil endpoint Express Anda, bukan API GajiHub langsung.
- Respons ke pemanggil hanya berisi data yang dibutuhkan, dan pesan error tidak memuat token.

Praktik lainnya ada di [README utama](../../../README.md#keamanan-token).
