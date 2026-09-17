// Klien API GajiHub untuk dipakai di server (backend) Anda.
//
// Praktik keamanan yang diterapkan:
//   - Token dibaca dari environment variable (file .env), tidak ditulis di dalam kode.
//   - Token hanya dipakai di server. Jangan pernah kirim token ke browser / aplikasi mobile.
//   - Aplikasi langsung berhenti saat start jika konfigurasi belum lengkap (fail fast),
//     lihat pemanggilan NewGajiHubClient di main.go.
//   - Pesan error tidak memuat token.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

// GajiHubError terjadi saat GajiHub membalas status selain 2xx.
type GajiHubError struct {
	Status int
	Pesan  string
}

func (gagal *GajiHubError) Error() string {
	return fmt.Sprintf("status %d: %s", gagal.Status, gagal.Pesan)
}

// GajiHubClient adalah klien API GajiHub yang dibuat sekali lalu dipakai ulang
// di seluruh aplikasi. Aman dipakai bersamaan oleh banyak request.
type GajiHubClient struct {
	apiHost     string
	accessToken string
	klien       *http.Client
}

// NewGajiHubClient membaca konfigurasi dari environment variable.
func NewGajiHubClient() (*GajiHubClient, error) {
	apiHost := os.Getenv("GAJIHUB_API_HOST")
	accessToken := os.Getenv("GAJIHUB_ACCESS_TOKEN")

	if apiHost == "" || accessToken == "" {
		return nil, errors.New("GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN wajib diisi di file .env")
	}

	return &GajiHubClient{
		apiHost:     strings.TrimRight(apiHost, "/"),
		accessToken: accessToken,
		klien:       &http.Client{Timeout: 30 * time.Second},
	}, nil
}

// Request mengirim request ke API GajiHub dan mengembalikan isi "data" dari respons.
//
//	endpoint  contoh: "/hr/employees/pagination"
//	parameter data untuk GET/DELETE, dikirim lewat URL (boleh nil)
//	body      data untuk POST/PUT/PATCH, dikirim sebagai JSON (boleh nil)
func (klien *GajiHubClient) Request(ctx context.Context, method, endpoint string, parameter url.Values, body any) (json.RawMessage, error) {
	alamat := klien.apiHost + endpoint
	if len(parameter) > 0 {
		alamat += "?" + parameter.Encode()
	}

	var isiBody io.Reader
	if body != nil {
		bodyJSON, gagal := json.Marshal(body)
		if gagal != nil {
			return nil, fmt.Errorf("gagal menyusun data menjadi JSON: %w", gagal)
		}
		isiBody = bytes.NewReader(bodyJSON)
	}

	request, gagal := http.NewRequestWithContext(ctx, method, alamat, isiBody)
	if gagal != nil {
		return nil, gagal
	}

	// Header autentikasi GajiHub
	request.Header.Set("Authorization", "Bearer "+klien.accessToken)
	request.Header.Set("Accept", "application/json")
	request.Header.Set("X-App", "hr")
	if body != nil {
		request.Header.Set("Content-Type", "application/json")
	}

	respons, gagal := klien.klien.Do(request)
	if gagal != nil {
		return nil, fmt.Errorf("gagal menghubungi GajiHub: %w", gagal)
	}
	defer respons.Body.Close()

	// Semua respons GajiHub berbentuk {"success": ..., "data": ..., "message": ...}
	var isi struct {
		Data    json.RawMessage `json:"data"`
		Message string          `json:"message"`
	}
	_ = json.NewDecoder(respons.Body).Decode(&isi) // respons error bisa saja bukan JSON

	if respons.StatusCode < 200 || respons.StatusCode >= 300 {
		pesan := isi.Message
		if pesan == "" {
			pesan = respons.Status
		}
		return nil, &GajiHubError{Status: respons.StatusCode, Pesan: pesan}
	}

	return isi.Data, nil
}

// User adalah data user pemilik token.
// Respons aslinya masih berisi banyak data lain (permission, menu, dll).
type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// CurrentUser mengambil data user pemilik token (dipakai untuk memastikan token valid).
func (klien *GajiHubClient) CurrentUser(ctx context.Context) (*User, error) {
	isi, gagal := klien.Request(ctx, http.MethodGet, "/authentication/user", nil, nil)
	if gagal != nil {
		return nil, gagal
	}

	var user User
	if gagal := json.Unmarshal(isi, &user); gagal != nil {
		return nil, fmt.Errorf("respons GajiHub tidak sesuai: %w", gagal)
	}

	return &user, nil
}
