# Contoh Autentikasi API GajiHub di Laravel

Contoh penerapan yang aman untuk aplikasi sungguhan: token disimpan di `.env`, dipakai hanya di server,
dan dibungkus dalam satu class klien yang bisa dipakai ulang.

Diuji dengan Laravel 13 dan PHP 8.4.

## Isi Folder

```
laravel/
├── .env.example                                  -> baris yang ditambahkan ke .env
├── config/gajihub.php                            -> membaca GAJIHUB_API_HOST & GAJIHUB_ACCESS_TOKEN dari .env
├── app/Services/GajiHub/GajiHubClient.php        -> klien API GajiHub (header autentikasi ada di sini)
├── app/Services/GajiHub/GajiHubException.php     -> error jika GajiHub membalas selain 2xx
└── app/Http/Controllers/GajiHubController.php    -> contoh endpoint GET /gajihub/me
```

## Cara Pasang

1. Salin folder `config/` dan `app/` ke project Laravel Anda (struktur foldernya sama).
2. Tambahkan isi `.env.example` ke file `.env` project Anda, lalu isi nilainya.
3. Tambahkan route berikut ke `routes/web.php` (atau `routes/api.php`):

   ```php
   use App\Http\Controllers\GajiHubController;

   Route::get('/gajihub/me', [GajiHubController::class, 'me']);
   ```

4. Jalankan:

   ```bash
   php artisan config:clear
   php artisan serve
   ```

5. Buka `http://localhost:8000/gajihub/me`. Jika token benar, hasilnya:

   ```json
   {"id": 1, "name": "Nama User", "email": "user@perusahaan.com"}
   ```

   Jika token salah atau kedaluwarsa, hasilnya `502` dengan pesan umum,
   dan detailnya (misalnya `[GajiHub] status 401: Unauthenticated.`) tercatat di `storage/logs/laravel.log`.

## Memanggil Endpoint Lain

Inject `GajiHubClient` ke controller / job / command, lalu panggil `request()`:

```php
public function index(GajiHubClient $gajihub)
{
    $halaman = $gajihub->request('GET', '/hr/employees/pagination', ['page' => 1, 'per_page' => 20]);

    return $halaman['data'];
}
```

`GET`/`DELETE` mengirim data lewat URL, `POST`/`PUT`/`PATCH` mengirim data sebagai JSON.
Daftar endpoint ada di [README utama](../../../README.md#daftar-demo).

## Praktik Keamanan yang Diterapkan

- Token hanya ada di `.env`, dibaca lewat `config/gajihub.php`, sehingga tetap berfungsi setelah `php artisan config:cache`.
- Token hanya dipakai di server. Browser / aplikasi mobile memanggil route Laravel Anda, bukan API GajiHub langsung.
- Respons ke pemanggil hanya berisi data yang dibutuhkan, dan pesan error tidak memuat token.

Praktik lainnya ada di [README utama](../../../README.md#keamanan-token).
