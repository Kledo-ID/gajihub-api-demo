// Contoh server net/http (tanpa library tambahan) yang memakai API GajiHub dengan aman.
//
// Jalankan:  go run .
// Coba:      http://localhost:3000/gajihub/me
package main

import (
	"bufio"
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"os"
	"strings"
)

func main() {
	if gagal := muatEnv(".env"); gagal != nil {
		log.Fatalf("Gagal membaca file .env: %v", gagal)
	}

	// Fail fast: server menolak start jika konfigurasi belum lengkap
	gajihub, gagal := NewGajiHubClient()
	if gagal != nil {
		log.Fatal(gagal)
	}

	mux := http.NewServeMux()

	// Cek koneksi & token GajiHub: siapa pemilik token yang dipakai server ini?
	mux.HandleFunc("GET /gajihub/me", func(w http.ResponseWriter, r *http.Request) {
		user, gagal := gajihub.CurrentUser(r.Context())
		if gagal != nil {
			balasError(w, gagal)
			return
		}

		// Kirim hanya data yang dibutuhkan (respons asli juga berisi permission & menu)
		balasJSON(w, http.StatusOK, map[string]any{
			"id":    user.ID,
			"name":  user.Name,
			"email": user.Email,
		})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	log.Printf("Server berjalan di http://localhost:%s", port)
	log.Fatal(http.ListenAndServe(":"+port, mux))
}

// balasJSON mengirim data sebagai JSON ke pemanggil.
func balasJSON(w http.ResponseWriter, status int, data any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(data)
}

// balasError mencatat detail error di log server, lalu membalas pesan umum ke pemanggil.
func balasError(w http.ResponseWriter, gagal error) {
	// 401/403 dari GajiHub = token di server salah/kedaluwarsa, bukan kesalahan pemanggil
	var errGajiHub *GajiHubError
	if errors.As(gagal, &errGajiHub) {
		log.Printf("[GajiHub] %v", errGajiHub)
	} else {
		log.Printf("[GajiHub] %v", gagal)
	}

	balasJSON(w, http.StatusBadGateway, map[string]string{
		"message": "Gagal mengambil data dari GajiHub.",
	})
}

// muatEnv membaca file .env lalu memasukkan isinya ke environment variable proses ini.
// File .env yang tidak ada bukan masalah: di server, konfigurasi biasanya sudah
// diisi lewat environment variable.
func muatEnv(lokasi string) error {
	berkas, gagal := os.Open(lokasi)
	if errors.Is(gagal, os.ErrNotExist) {
		return nil
	}
	if gagal != nil {
		return gagal
	}
	defer berkas.Close()

	pemindai := bufio.NewScanner(berkas)
	for pemindai.Scan() {
		// TrimPrefix membuang penanda BOM yang sering ikut tersimpan
		// saat file .env diedit dengan Notepad di Windows
		baris := strings.TrimSpace(strings.TrimPrefix(pemindai.Text(), "\ufeff"))
		if baris == "" || strings.HasPrefix(baris, "#") {
			continue
		}

		kunci, nilai, ada := strings.Cut(baris, "=")
		if !ada {
			continue
		}

		// Environment variable yang sudah diisi di server tidak ditimpa
		kunci = strings.TrimSpace(kunci)
		if _, sudahAda := os.LookupEnv(kunci); sudahAda {
			continue
		}

		if gagal := os.Setenv(kunci, strings.Trim(strings.TrimSpace(nilai), `"'`)); gagal != nil {
			return gagal
		}
	}

	return pemindai.Err()
}
