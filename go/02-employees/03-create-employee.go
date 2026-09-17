//go:build ignore

// DEMO: Menambah karyawan baru (data pribadi + karir + payroll sekaligus)
//
// Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
//
//	go run 03-create-employee.go
//
// PERHATIAN: demo ini MENAMBAH karyawan di GajiHub Anda.
//
// Kolom yang wajib diisi bisa berbeda di setiap perusahaan, tergantung pengaturan
// validasi data karyawan di GajiHub. Jika ada kolom yang kurang, server membalas
// status 400 dengan pesan kolom yang perlu diisi, misalnya "Birthplace diperlukan."
//
// ID pilihan (struktur organisasi, jabatan, jenis kelamin, dll) bisa dilihat
// di demo folder 03-master-data/.
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

// responsTambah adalah bagian respons yang dipakai demo ini.
type responsTambah struct {
	Data struct {
		ID int `json:"id"`
	} `json:"data"`
}

func main() {
	fmt.Println("=== Tambah Karyawan ===")

	hasil := apiRequest("POST", "/hr/employees/insert", nil, map[string]any{

		// ===== 1. Data pribadi =====
		"personal": map[string]any{
			"name":                 "Budi Santoso",                                        // WAJIB: nama lengkap (4-50 karakter)
			"email":                "budi." + time.Now().Format("150405") + "@contoh.com", // WAJIB: email (tidak boleh sama dengan karyawan lain)
			"hr_gender_id":         1,                                                     // WAJIB: 1 = laki-laki, 2 = perempuan
			"handphone":            "081234567890",
			"birthplace":           "Yogyakarta", // tempat lahir
			"birthday":             "1995-05-20", // tanggal lahir (YYYY-MM-DD)
			"hr_marital_status_id": 2,            // 1 = menikah, 2 = belum menikah, 3 = janda, 4 = duda
			"hr_religion_id":       1,            // lihat demo 03-master-data/06-references.go
			"hr_citizenship_id":    1,            // 1 = WNI

			// Kartu identitas
			"hr_id_card_type_id": 1, // 1 = KTP
			"id_card_number":     "3404012005950001",

			// Alamat sesuai KTP
			"address":     "Jl. Contoh No. 1",
			"country_id":  1,   // 1 = Indonesia
			"province_id": 18,  // ID provinsi
			"city_id":     250, // ID kota/kabupaten

			// Alamat domisili
			"residence_address":     "Jl. Contoh No. 1",
			"residence_country_id":  1,
			"residence_province_id": 18,
			"residence_city_id":     250,

			// Kontak darurat
			"emergency_contact":       "Siti (Istri)",
			"emergency_contact_phone": "081298765432",
		},

		// ===== 2. Data karir =====
		"career": map[string]any{
			"hr_employee_status_id":  1,          // WAJIB: 1 = tetap, 2 = percobaan, 3 = PKWT (kontrak), dll
			"hr_org_structure_id":    2,          // WAJIB: ID struktur organisasi
			"hr_job_position_id":     11,         // WAJIB: ID jabatan
			"hr_job_level_id":        5,          // WAJIB: ID level jabatan
			"hr_schedule_pattern_id": 1,          // ID pola jadwal kerja
			"date_started_work":      tanggal(0), // WAJIB: tanggal mulai bekerja (YYYY-MM-DD)
			// "date_ended":         "2027-09-13", // WAJIB untuk karyawan tidak tetap: tanggal kontrak berakhir
		},

		// ===== 3. Data payroll =====
		"payroll": map[string]any{
			"hr_pph21_withholder_id": 1, // ID pemotong PPh 21 (perusahaan)
			"hr_taxpayer_status_id":  1, // status PTKP: 1 = TK0, 2 = TK1, dst (lihat referensi taxpayerStatuses)
			// "npwp":                   "12.345.678.9-012.345",
			// "bpjs_healthcare_number": "0001234567890",
		},
	})

	tampilkan(hasil)

	if hasil.Sukses {
		var respons responsTambah
		if json.Unmarshal(hasil.Isi, &respons) == nil {
			fmt.Println()
			fmt.Printf("ID karyawan baru: %d\n", respons.Data.ID)
		}
	}
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

var wib = time.FixedZone("WIB", 7*60*60) // zona waktu Asia/Jakarta

// tanggal mengembalikan tanggal hari ini (YYYY-MM-DD).
// tanggal(-1) = kemarin, tanggal(7) = 7 hari lagi.
func tanggal(tambahHari int) string {
	return time.Now().In(wib).AddDate(0, 0, tambahHari).Format("2006-01-02")
}
