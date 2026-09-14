# Contoh Autentikasi API GajiHub di FastAPI

Contoh penerapan yang aman untuk aplikasi sungguhan: token disimpan di `.env`, dipakai hanya di server,
dan dibungkus dalam satu klien yang dipakai bersama oleh semua request.

Diuji dengan Python 3.12, FastAPI 0.141, httpx 0.28, dan pydantic-settings 2.15.

## Isi Folder

```
fastapi/
├── .env.example      -> contoh konfigurasi (salin menjadi .env)
├── requirements.txt  -> library yang dibutuhkan
├── gajihub.py        -> konfigurasi + klien API GajiHub (header autentikasi ada di sini)
└── main.py           -> aplikasi FastAPI dengan contoh endpoint GET /gajihub/me
```

## Cara Menjalankan

```bash
cd python/01-authentication/fastapi

# 1. Buat virtual environment dan pasang library
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt

# 2. Salin .env.example menjadi .env, lalu isi GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux

# 3. Jalankan server
uvicorn main:app --reload
```

Buka `http://localhost:8000/gajihub/me`. Jika token benar, hasilnya:

```json
{"id": 1, "name": "Nama User", "email": "user@perusahaan.com"}
```

- Jika token salah atau kedaluwarsa, hasilnya `502` dengan pesan umum, dan detailnya
  (misalnya `[GajiHub] status 401: Unauthenticated.`) tercatat di log server.
- Jika `GAJIHUB_API_HOST` / `GAJIHUB_ACCESS_TOKEN` belum diisi, server menolak start dengan pesan `Field required`.

## Memanggil Endpoint Lain

Pakai dependency `get_gajihub`, lalu panggil `request()`:

```python
@app.get('/karyawan')
async def karyawan(gajihub: Annotated[GajiHubClient, Depends(get_gajihub)]):
    halaman = await gajihub.request('GET', '/hr/employees/pagination', params={'page': 1, 'per_page': 20})
    return halaman['data']
```

Untuk `POST`/`PUT`/`PATCH`, kirim data dengan `json={...}`.
Daftar endpoint ada di [README utama](../../../README.md#daftar-demo).

## Praktik Keamanan yang Diterapkan

- Token hanya ada di `.env` (atau environment variable server), dibaca dengan `pydantic-settings`.
- Token disimpan sebagai `SecretStr`, sehingga tidak ikut tercetak saat objek konfigurasi di-log.
- Token hanya dipakai di server. Browser / aplikasi mobile memanggil endpoint FastAPI Anda, bukan API GajiHub langsung.
- Respons ke pemanggil hanya berisi data yang dibutuhkan, dan pesan error tidak memuat token.

Praktik lainnya ada di [README utama](../../../README.md#keamanan-token).

> **Jaringan kantor dengan proxy / sertifikat khusus:** httpx memakai daftar sertifikat bawaan `certifi`.
> Jika muncul `CERTIFICATE_VERIFY_FAILED`, arahkan environment variable `SSL_CERT_FILE` ke file sertifikat CA kantor Anda.
