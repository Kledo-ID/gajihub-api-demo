<?php

declare(strict_types=1);

/**
 * DEMO: Daftar jabatan
 *
 * Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
 *   php 02-job-positions.php
 *
 * ID jabatan dipakai saat menambah karyawan (hr_job_position_id).
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

echo '=== Daftar Jabatan ===' . PHP_EOL;

$hasil = api_request('GET', '/hr/jobPositions');

if ($hasil['sukses']) {
    foreach ($hasil['data']['data'] as $jabatan) {
        // parent_id = ID jabatan atasan (kosong jika jabatan paling atas)
        echo "ID {$jabatan['id']} : {$jabatan['name']} (atasan: " . ($jabatan['parent_id'] ?? '-') . ')' . PHP_EOL;
    }
    echo PHP_EOL;
}

tampilkan($hasil);

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
