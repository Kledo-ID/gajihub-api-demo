# Demo API GajiHub (Go)

Setiap file berdiri sendiri: **tanpa `go get`**, tanpa file bantu lain. Hanya memakai library bawaan Go (`net/http`).

## Persiapan

**Go 1.21 atau lebih baru.** Cek dengan `go version`.

## Menjalankan Demo

1. Buka file demo, lalu isi 2 baris di bagian **Konfigurasi**:

   ```go
   const (
       apiHost     = "https://namaperusahaan.api.kledo.com/api/v1"
       accessToken = "gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx"
   )
   ```

2. Jalankan lewat terminal:

   ```bash
   cd go/01-authentication
   go run 01-check-token.go
   ```

Mulailah dari `01-authentication/01-check-token.go` untuk memastikan token sudah benar.
File Excel hasil export tersimpan di folder `hasil-unduhan/` di folder tempat Anda menjalankan perintah.

Filter tambahan sudah disiapkan dalam bentuk komentar `//`. Hapus tanda `//` untuk mengaktifkannya.

> Setiap file diawali `//go:build ignore`. Baris itu membuat file tidak ikut ter-*build* oleh
> `go build ./...`, sehingga banyak file `func main()` bisa berada di satu folder.
> File tetap bisa dijalankan dengan `go run <nama-file>.go` seperti biasa.

> Menulis token langsung di file hanya untuk mencoba. Untuk aplikasi sungguhan, simpan token di `.env`,
> lihat contoh net/http di [01-authentication/nethttp/](01-authentication/nethttp/).

## Daftar Demo

Lihat [README utama](../README.md#daftar-demo). Nama file sama untuk semua bahasa, dengan akhiran `.go`.

## Unduh Laporan Otomatis

```bash
cd go/11-scheduled-download

# Laporan kemarin
go run download-attendance-reports.go

# Laporan rentang tanggal tertentu
go run download-attendance-reports.go 2026-09-01 2026-09-30
```

Untuk penjadwalan, sebaiknya kompilasi dulu agar tidak perlu compile setiap kali jalan:

```bash
go build -o unduh-absensi download-attendance-reports.go     # Linux / macOS
go build -o unduh-absensi.exe download-attendance-reports.go # Windows
```

**Windows (Task Scheduler)** — buat **Basic Task** harian, pilih **Start a program**, lalu isi:

- **Program/script**: `unduh-absensi.exe` (hasil `go build` di atas)
- **Start in**: folder tempat file tersebut, contoh `C:\gajihub-api-demo\go\11-scheduled-download`

**Linux / macOS (cron)** — jalankan `crontab -e`, lalu tambahkan (setiap hari jam 06:00):

```text
0 6 * * * cd /lokasi/gajihub-api-demo/go/11-scheduled-download && ./unduh-absensi >> /var/log/unduh-absensi.log 2>&1
```

> `cd` perlu ditulis karena file hasil unduhan disimpan di folder `hasil-unduhan/`
> relatif terhadap folder tempat perintah dijalankan.

## Kendala Khusus Go

Kendala umum (401, 403, dll) ada di [README utama](../README.md#jika-terjadi-kendala).

| Pesan | Solusi |
|---|---|
| `go: go.mod file not found` | Jalankan perintah dari dalam folder `go/` (file `go/go.mod` sudah disediakan). Jika file demo disalin ke folder lain, jalankan `go mod init demo` lebih dulu. |
| `expected 'package', found 'import'` | File dijalankan dengan `go run *.go`. Sebutkan 1 nama file saja, contoh `go run 01-check-token.go`. |
| `main redeclared in this block` | Sama seperti di atas: jalankan 1 file saja, bukan seluruh folder. |
| `x509: certificate signed by unknown authority` | Jaringan kantor memakai sertifikat khusus. Tambahkan sertifikat CA kantor ke penyimpanan sertifikat sistem, atau arahkan environment variable `SSL_CERT_FILE` ke file sertifikat tersebut. |
| Huruf beraksen tampil aneh di Command Prompt | Jalankan `chcp 65001` sebelum `go run`, atau gunakan Windows Terminal / PowerShell. |
