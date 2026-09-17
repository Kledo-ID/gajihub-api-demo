# Contoh Autentikasi API GajiHub di Go (net/http)

Contoh penerapan yang aman untuk aplikasi sungguhan: token disimpan di `.env`, dipakai hanya di server,
dan dibungkus dalam satu klien yang bisa dipakai ulang.

Hanya memakai library bawaan Go. Diuji dengan Go 1.22.

## Isi Folder

```
nethttp/
├── .env.example   -> contoh konfigurasi (salin menjadi .env)
├── go.mod         -> nama modul + versi Go (tanpa library tambahan)
├── gajihub.go     -> klien API GajiHub (header autentikasi ada di sini)
└── main.go        -> server net/http dengan contoh endpoint GET /gajihub/me
```

## Cara Menjalankan

Butuh **Go 1.22 atau lebih baru** (untuk pola routing `"GET /gajihub/me"`).

```bash
cd go/01-authentication/nethttp

# 1. Salin .env.example menjadi .env, lalu isi GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux

# 2. Jalankan server
go run .
```

Buka `http://localhost:3000/gajihub/me`. Jika token benar, hasilnya:

```json
{"id": 1, "name": "Nama User", "email": "user@perusahaan.com"}
```

- Jika token salah atau kedaluwarsa, hasilnya `502` dengan pesan umum, dan detailnya
  (misalnya `[GajiHub] status 401: Unauthenticated.`) tercatat di log server.
- Jika `GAJIHUB_API_HOST` / `GAJIHUB_ACCESS_TOKEN` belum diisi, server menolak start.

Untuk dijalankan di server sungguhan, kompilasi dulu: `go build -o server .`

## Memanggil Endpoint Lain

Pakai `gajihub.Request` dari handler Anda:

```go
mux.HandleFunc("GET /karyawan", func(w http.ResponseWriter, r *http.Request) {
	halaman, gagal := gajihub.Request(r.Context(), http.MethodGet, "/hr/employees/pagination", url.Values{
		"page":     {"1"},
		"per_page": {"20"},
	}, nil)
	if gagal != nil {
		balasError(w, gagal)
		return
	}

	balasJSON(w, http.StatusOK, json.RawMessage(halaman))
})
```

`Request` mengembalikan isi `data` dari respons dalam bentuk `json.RawMessage`.
Untuk memakai isinya di Go, `json.Unmarshal` ke struct Anda sendiri, seperti `CurrentUser` di `gajihub.go`.

Untuk `POST`/`PUT`/`PATCH`, kirim data lewat argumen terakhir (`body`), misalnya `map[string]any{...}`.
Daftar endpoint ada di [README utama](../../../README.md#daftar-demo).

## Praktik Keamanan yang Diterapkan

- Token hanya ada di `.env` (atau environment variable server), dibaca lewat `os.Getenv`.
- Token hanya dipakai di server. Browser / aplikasi mobile memanggil endpoint Go Anda, bukan API GajiHub langsung.
- Server menolak start jika konfigurasi belum lengkap (`NewGajiHubClient` di `main.go`).
- Respons ke pemanggil hanya berisi data yang dibutuhkan, dan pesan error tidak memuat token.

Praktik lainnya ada di [README utama](../../../README.md#keamanan-token).
