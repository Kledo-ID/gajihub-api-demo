<?php

declare(strict_types=1);

/**
 * DEMO: Menambah karyawan baru (data pribadi + karir + payroll sekaligus)
 *
 * Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
 *   php 03-create-employee.php
 *
 * PERHATIAN: demo ini MENAMBAH karyawan di GajiHub Anda.
 *
 * Kolom yang wajib diisi bisa berbeda di setiap perusahaan, tergantung pengaturan
 * validasi data karyawan di GajiHub. Jika ada kolom yang kurang, server membalas
 * status 400 dengan pesan kolom yang perlu diisi, misalnya "Birthplace diperlukan."
 *
 * ID pilihan (struktur organisasi, jabatan, jenis kelamin, dll) bisa dilihat
 * di demo folder 03-master-data/.
 */

// ============================================================================
// Konfigurasi
// ----------------------------------------------------------------------------
// Isi langsung di sini agar mudah dicoba.
//
// PENTING (keamanan): untuk aplikasi sungguhan, JANGAN tulis token di dalam kode.
// Simpan API_HOST dan ACCESS_TOKEN di file .env / environment variable, dan jangan
// pernah commit token ke Git. Contoh penerapannya ada di folder php/01-authentication/laravel/
// ============================================================================

const API_HOST     = 'https://namaperusahaan.api.kledo.com/api/v1'; // alamat API perusahaan Anda, diakhiri /api/v1
const ACCESS_TOKEN = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx'; // Personal Access Token (diawali gajihub_pat_)

date_default_timezone_set('Asia/Jakarta');

echo '=== Tambah Karyawan ===' . PHP_EOL;

$hasil = api_request('POST', '/hr/employees/insert', [

    // ===== 1. Data pribadi =====
    'personal' => [
        'name'                 => 'Budi Santoso',                        // WAJIB: nama lengkap (4-50 karakter)
        'email'                => 'budi.' . date('His') . '@contoh.com', // WAJIB: email (tidak boleh sama dengan karyawan lain)
        'hr_gender_id'         => 1,             // WAJIB: 1 = laki-laki, 2 = perempuan
        'handphone'            => '081234567890',
        'birthplace'           => 'Yogyakarta',  // tempat lahir
        'birthday'             => '1995-05-20',  // tanggal lahir (YYYY-MM-DD)
        'hr_marital_status_id' => 2,             // 1 = menikah, 2 = belum menikah, 3 = janda, 4 = duda
        'hr_religion_id'       => 1,             // lihat demo 03-master-data/06-references.php
        'hr_citizenship_id'    => 1,             // 1 = WNI

        // Kartu identitas
        'hr_id_card_type_id'   => 1,             // 1 = KTP
        'id_card_number'       => '3404012005950001',

        // Alamat sesuai KTP
        'address'              => 'Jl. Contoh No. 1',
        'country_id'           => 1,             // 1 = Indonesia
        'province_id'          => 18,            // ID provinsi
        'city_id'              => 250,           // ID kota/kabupaten

        // Alamat domisili
        'residence_address'     => 'Jl. Contoh No. 1',
        'residence_country_id'  => 1,
        'residence_province_id' => 18,
        'residence_city_id'     => 250,

        // Kontak darurat
        'emergency_contact'       => 'Siti (Istri)',
        'emergency_contact_phone' => '081298765432',
    ],

    // ===== 2. Data karir =====
    'career' => [
        'hr_employee_status_id'  => 1,              // WAJIB: 1 = tetap, 2 = percobaan, 3 = PKWT (kontrak), dll
        'hr_org_structure_id'    => 2,              // WAJIB: ID struktur organisasi
        'hr_job_position_id'     => 11,             // WAJIB: ID jabatan
        'hr_job_level_id'        => 5,              // WAJIB: ID level jabatan
        'hr_schedule_pattern_id' => 1,              // ID pola jadwal kerja
        'date_started_work'      => date('Y-m-d'),  // WAJIB: tanggal mulai bekerja (YYYY-MM-DD)
        // 'date_ended'          => '2027-09-13',   // WAJIB untuk karyawan tidak tetap: tanggal kontrak berakhir
    ],

    // ===== 3. Data payroll =====
    'payroll' => [
        'hr_pph21_withholder_id' => 1,  // ID pemotong PPh 21 (perusahaan)
        'hr_taxpayer_status_id'  => 1,  // status PTKP: 1 = TK0, 2 = TK1, dst (lihat referensi taxpayerStatuses)
        // 'npwp'                => '12.345.678.9-012.345',
        // 'bpjs_healthcare_number' => '0001234567890',
    ],
]);

tampilkan($hasil);

if ($hasil['sukses']) {
    echo PHP_EOL;
    echo 'ID karyawan baru: ' . $hasil['data']['data']['id'] . PHP_EOL;
}

// ============================================================================
// Fungsi bantu (tidak perlu diubah)
// ============================================================================

/**
 * Kirim request ke API GajiHub, lalu kembalikan hasilnya.
 *
 * Autentikasi: setiap request membawa header
 *   Authorization: Bearer <ACCESS_TOKEN>
 *   Accept: application/json
 *   X-App: hr
 *
 * GET/DELETE     : $data dikirim lewat URL (?page=1&per_page=10)
 * POST/PUT/PATCH : $data dikirim sebagai JSON di body request
 *
 * Hasil: ['status' => 200, 'sukses' => true, 'data' => [isi JSON], 'isi' => 'respons mentah', 'header' => [...]]
 */
function api_request(string $method, string $endpoint, array $data = []): array
{
    if (str_contains(ACCESS_TOKEN, 'xxxxxx')) {
        echo 'ERROR: API_HOST dan ACCESS_TOKEN belum diisi. Buka file ini dan isi bagian Konfigurasi.' . PHP_EOL;
        exit(1);
    }

    $url = rtrim(API_HOST, '/') . $endpoint;

    $header = [
        'Authorization: Bearer ' . ACCESS_TOKEN,
        'Accept: application/json',
        'X-App: hr',
        'User-Agent: gajihub-api-demo',
    ];

    $kirimSebagaiJson = in_array($method, ['POST', 'PUT', 'PATCH'], true);

    if (!$kirimSebagaiJson && $data !== []) {
        $url .= '?' . http_build_query($data);
    }

    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_TIMEOUT, 300); // export bisa lama, tunggu maksimal 5 menit

    if ($kirimSebagaiJson) {
        $header[] = 'Content-Type: application/json';
        curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
    }

    curl_setopt($curl, CURLOPT_HTTPHEADER, $header);

    // Simpan header respons (dipakai untuk membaca nama file export)
    $headerRespons = [];
    curl_setopt($curl, CURLOPT_HEADERFUNCTION, function ($curl, string $baris) use (&$headerRespons): int {
        if (str_contains($baris, ':')) {
            [$kunci, $nilai] = explode(':', $baris, 2);
            $headerRespons[strtolower(trim($kunci))] = trim($nilai);
        }

        return strlen($baris);
    });

    echo "{$method} {$url}" . PHP_EOL;

    $isi = curl_exec($curl);

    if ($isi === false) {
        echo 'ERROR: Gagal terhubung ke server: ' . curl_error($curl) . PHP_EOL;
        exit(1);
    }

    $status = (int) curl_getinfo($curl, CURLINFO_HTTP_CODE);

    return [
        'status' => $status,
        'sukses' => $status >= 200 && $status < 300,
        'data'   => json_decode($isi, true),
        'isi'    => $isi,
        'header' => $headerRespons,
    ];
}

/**
 * Cetak hasil request: status HTTP + isi respons dalam format JSON yang rapi.
 */
function tampilkan(array $hasil): void
{
    echo 'Status HTTP: ' . $hasil['status'] . ($hasil['sukses'] ? ' (berhasil)' : ' (gagal)') . PHP_EOL;

    // Penjelasan singkat untuk kode status yang sering muncul
    $arti = match (true) {
        $hasil['sukses']         => '',
        $hasil['status'] === 400 => 'Artinya: parameter/data yang dikirim tidak valid. Lihat pesan di bawah.',
        $hasil['status'] === 401 => 'Artinya: token tidak valid atau sudah kedaluwarsa. Periksa ACCESS_TOKEN.',
        $hasil['status'] === 403 => 'Artinya: user pemilik token tidak punya hak akses ke fitur ini.',
        $hasil['status'] === 404 => 'Artinya: data atau endpoint tidak ditemukan. Periksa ID / API_HOST.',
        $hasil['status'] === 429 => 'Artinya: terlalu banyak request. Tunggu sebentar lalu coba lagi.',
        $hasil['status'] >= 500  => 'Artinya: terjadi kesalahan di server. Coba lagi beberapa saat.',
        default                  => '',
    };

    if ($arti !== '') {
        echo $arti . PHP_EOL;
    }

    echo ($hasil['data'] !== null
        ? json_encode($hasil['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
        : $hasil['isi']) . PHP_EOL;
}
