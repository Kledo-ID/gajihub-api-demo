//go:build ignore

// DEMO: Cek token (siapa pemilik token ini?)
//
// Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
//
//	go run 01-check-token.go
//
// Jalankan demo ini lebih dulu untuk memastikan API_HOST dan ACCESS_TOKEN sudah benar.
//
// Cara kerja autentikasi API GajiHub:
//   - Tidak ada proses login. Personal Access Token menggantikan email + password.
//   - Setiap request cukup membawa 3 header berikut:
//     Authorization: Bearer <ACCESS_TOKEN>
//     Accept: application/json
//     X-App: hr
//   - Token bekerja atas nama user yang membuatnya, dengan hak akses yang sama.
//
// Contoh penerapan yang aman untuk aplikasi sungguhan (token disimpan di .env):
// lihat folder nethttp/ di sebelah file ini.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

// ============================================================================
// Konfigurasi
// ----------------------------------------------------------------------------
// Isi langsung di sini agar mudah dicoba.
//
// PENTING (keamanan): untuk aplikasi sungguhan, JANGAN tulis token di dalam kode.
// Simpan API_HOST dan ACCESS_TOKEN di file .env / environment variable, dan jangan
// pernah commit token ke Git. Contoh penerapannya ada di folder go/01-authentication/nethttp/
// ============================================================================

const (
	apiHost     = "https://namaperusahaan.api.kledo.com/api/v1" // alamat API perusahaan Anda, diakhiri /api/v1
	accessToken = "gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx"         // Personal Access Token (diawali gajihub_pat_)
)

// responsUser adalah bagian respons yang dipakai demo ini.
// Respons aslinya masih berisi banyak data lain (permission, menu, dll).
type responsUser struct {
	Data struct {
		Name  string `json:"name"`
		Email string `json:"email"`
	} `json:"data"`
}

func main() {
	fmt.Println("=== Cek Token ===")

	hasil := apiRequest("GET", "/authentication/user", nil, nil)

	if !hasil.Sukses {
		tampilkan(hasil)
		return
	}

	var respons responsUser
	if gagal := json.Unmarshal(hasil.Isi, &respons); gagal != nil {
		tampilkan(hasil)
		return
	}

	fmt.Println("Token valid.")
	fmt.Printf("Pemilik token: %s (%s)\n", respons.Data.Name, respons.Data.Email)
	fmt.Println("Semua request API berjalan dengan hak akses user ini.")
}

// ============================================================================
// Fungsi bantu (tidak perlu diubah)
// ============================================================================

// hasilRequest adalah hasil satu kali panggilan ke API GajiHub.
type hasilRequest struct {
	Status int         // kode status HTTP, contoh 200
	Sukses bool        // true jika status 2xx
	JSON   bool        // true jika respons berbentuk JSON (false untuk isi file Excel)
	Isi    []byte      // respons mentah
	Header http.Header // header respons
}

// apiRequest mengirim request ke API GajiHub, lalu mengembalikan hasilnya.
//
// Autentikasi: setiap request membawa header
//
//	Authorization: Bearer <accessToken>
//	Accept: application/json
//	X-App: hr
//
// GET/DELETE     : data dikirim lewat URL (?page=1&per_page=10), isi lewat parameter
// POST/PUT/PATCH : data dikirim sebagai JSON di body request, isi lewat body
func apiRequest(method, endpoint string, parameter url.Values, body any) hasilRequest {
	if strings.Contains(accessToken, "xxxxxx") {
		fmt.Println("ERROR: API_HOST dan ACCESS_TOKEN belum diisi. Buka file ini dan isi bagian Konfigurasi.")
		os.Exit(1)
	}

	alamat := strings.TrimRight(apiHost, "/") + endpoint
	if len(parameter) > 0 {
		alamat += "?" + parameter.Encode()
	}

	var isiBody io.Reader
	if body != nil {
		bodyJSON, gagal := json.Marshal(body)
		if gagal != nil {
			fmt.Println("ERROR: Gagal menyusun data menjadi JSON:", gagal)
			os.Exit(1)
		}
		isiBody = bytes.NewReader(bodyJSON)
	}

	request, gagal := http.NewRequest(method, alamat, isiBody)
	if gagal != nil {
		fmt.Println("ERROR: Alamat API tidak valid:", gagal)
		os.Exit(1)
	}

	request.Header.Set("Authorization", "Bearer "+accessToken)
	request.Header.Set("Accept", "application/json")
	request.Header.Set("X-App", "hr")
	request.Header.Set("User-Agent", "gajihub-api-demo")
	if body != nil {
		request.Header.Set("Content-Type", "application/json")
	}

	fmt.Printf("%s %s\n", method, alamat)

	klien := &http.Client{Timeout: 300 * time.Second} // export bisa lama, tunggu maksimal 5 menit

	respons, gagal := klien.Do(request)
	if gagal != nil {
		fmt.Println("ERROR: Gagal terhubung ke server:", gagal)
		os.Exit(1)
	}
	defer respons.Body.Close()

	// Status 4xx / 5xx tetap dibaca isinya, karena berisi pesan error dari server
	isi, gagal := io.ReadAll(respons.Body)
	if gagal != nil {
		fmt.Println("ERROR: Gagal membaca respons dari server:", gagal)
		os.Exit(1)
	}

	return hasilRequest{
		Status: respons.StatusCode,
		Sukses: respons.StatusCode >= 200 && respons.StatusCode < 300,
		JSON:   json.Valid(isi),
		Isi:    isi,
		Header: respons.Header,
	}
}

// tampilkan mencetak hasil request: status HTTP + isi respons dalam format JSON yang rapi.
func tampilkan(hasil hasilRequest) {
	keterangan := " (berhasil)"
	if !hasil.Sukses {
		keterangan = " (gagal)"
	}
	fmt.Printf("Status HTTP: %d%s\n", hasil.Status, keterangan)

	// Penjelasan singkat untuk kode status yang sering muncul
	arti := map[int]string{
		400: "Artinya: parameter/data yang dikirim tidak valid. Lihat pesan di bawah.",
		401: "Artinya: token tidak valid atau sudah kedaluwarsa. Periksa ACCESS_TOKEN.",
		403: "Artinya: user pemilik token tidak punya hak akses ke fitur ini.",
		404: "Artinya: data atau endpoint tidak ditemukan. Periksa ID / API_HOST.",
		429: "Artinya: terlalu banyak request. Tunggu sebentar lalu coba lagi.",
	}[hasil.Status]
	if arti == "" && hasil.Status >= 500 {
		arti = "Artinya: terjadi kesalahan di server. Coba lagi beberapa saat."
	}

	if !hasil.Sukses && arti != "" {
		fmt.Println(arti)
	}

	if hasil.JSON {
		var rapi bytes.Buffer
		if json.Indent(&rapi, hasil.Isi, "", "    ") == nil {
			fmt.Println(rapi.String())
			return
		}
	}

	fmt.Println(string(hasil.Isi))
}
