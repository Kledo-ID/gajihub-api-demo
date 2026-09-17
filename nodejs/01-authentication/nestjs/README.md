# Contoh Autentikasi API GajiHub di NestJS

Contoh penerapan yang aman untuk aplikasi sungguhan: token disimpan di `.env`, dipakai hanya di server,
dan dibungkus dalam satu service yang bisa di-inject ke mana saja.

Diuji dengan Node.js 22 dan NestJS 11.

## Isi Folder

```
nestjs/
├── .env.example              -> contoh konfigurasi (salin menjadi .env)
├── package.json              -> library yang dibutuhkan + perintah npm start
├── nest-cli.json             -> konfigurasi Nest CLI
├── tsconfig.json             -> konfigurasi TypeScript
└── src/
    ├── main.ts               -> titik awal aplikasi
    ├── app.module.ts         -> modul utama + validasi .env (fail fast)
    └── gajihub/
        ├── gajihub.service.ts     -> klien API GajiHub (header autentikasi ada di sini)
        ├── gajihub.error.ts       -> error saat GajiHub membalas selain 2xx
        ├── gajihub.filter.ts      -> ubah error GajiHub jadi respons 502 yang aman
        ├── gajihub.module.ts      -> modul yang meng-export GajiHubService
        └── gajihub.controller.ts  -> contoh endpoint GET /gajihub/me
```

## Cara Menjalankan

Butuh **Node.js 20 atau lebih baru**.

```bash
cd nodejs/01-authentication/nestjs

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
- Jika `GAJIHUB_API_HOST` / `GAJIHUB_ACCESS_TOKEN` belum diisi, aplikasi menolak start.

## Memanggil Endpoint Lain

Inject `GajiHubService` ke controller atau service Anda:

```ts
@Controller('karyawan')
export class KaryawanController {
    constructor(private readonly gajihub: GajiHubService) {}

    @Get()
    async daftar() {
        return this.gajihub.request('GET', '/hr/employees/pagination', {
            query: { page: 1, per_page: 20 },
        });
    }
}
```

Agar `GajiHubService` bisa di-inject, `import` `GajiHubModule` di modul tempat controller itu berada.
Untuk `POST`/`PUT`/`PATCH`, kirim data dengan `{ body: {...} }`.
Daftar endpoint ada di [README utama](../../../README.md#daftar-demo).

Pasang `GajiHubExceptionFilter` di controller baru Anda (`@UseFilters(GajiHubExceptionFilter)`), atau
daftarkan sekali untuk seluruh aplikasi di `main.ts` dengan `app.useGlobalFilters(new GajiHubExceptionFilter())`.

## Praktik Keamanan yang Diterapkan

- Token hanya ada di `.env` (atau environment variable server), dibaca lewat `@nestjs/config`.
- Token hanya dipakai di server. Browser / aplikasi mobile memanggil endpoint NestJS Anda, bukan API GajiHub langsung.
- Aplikasi menolak start jika konfigurasi belum lengkap (validasi di `app.module.ts`).
- Respons ke pemanggil hanya berisi data yang dibutuhkan, dan pesan error tidak memuat token.

Praktik lainnya ada di [README utama](../../../README.md#keamanan-token).
