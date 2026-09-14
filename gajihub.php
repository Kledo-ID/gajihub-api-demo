<?php

declare(strict_types=1);

/**
 * ============================================================================
 *  gajihub.php — Fungsi bantu yang dipakai oleh semua demo
 * ============================================================================
 *
 *  File ini di-"require" oleh setiap file demo. Anda TIDAK perlu mengubahnya.
 *  Alamat API dan token diatur di file .env (salin dari .env.example).
 *
 *  Daftar fungsi:
 *    mulai_demo('Judul')                  -> tampilkan judul demo
 *    api_get('/endpoint', [parameter])    -> ambil data            (GET)
 *    api_post('/endpoint', [data])        -> tambah data           (POST)
 *    api_put('/endpoint', [data])         -> ubah data             (PUT)
 *    api_delete('/endpoint')              -> hapus data            (DELETE)
 *    unduh_file('/endpoint', [parameter]) -> unduh file Excel/CSV ke folder hasil-unduhan/
 *    tampilkan($hasil)                    -> cetak hasil request ke layar
 *    tulis('teks')                        -> cetak satu baris teks
 *
 *  Setiap fungsi api_* mengembalikan array:
 *    [
 *      'status' => 200,          // kode HTTP (200 = berhasil)
 *      'sukses' => true,         // true jika status 2xx
 *      'data'   => [...],        // isi respons JSON yang sudah diubah jadi array PHP
 *      'isi'    => '...',        // isi respons mentah (teks / isi file)
 *    ]
 * ============================================================================
 */

/** Folder tempat file hasil export disimpan. */
const FOLDER_UNDUHAN = __DIR__ . '/hasil-unduhan';

date_default_timezone_set('Asia/Jakarta');

// ----------------------------------------------------------------------------
// 1. Konfigurasi dari file .env
// ----------------------------------------------------------------------------

/**
 * Ambil nilai konfigurasi dari file .env, misalnya konfigurasi('API_HOST').
 */
function konfigurasi(string $nama): string
{
    static $isiEnv = null;

    if ($isiEnv === null) {
        $fileEnv = __DIR__ . '/.env';

        if (!is_file($fileEnv)) {
            berhenti('File .env belum ada. Salin .env.example menjadi .env, lalu isi API_HOST dan ACCESS_TOKEN.');
        }

        $isiEnv = [];
        foreach (file($fileEnv, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $baris) {
            $baris = trim($baris);

            // Lewati komentar (#) dan baris tanpa tanda =
            if ($baris === '' || $baris[0] === '#' || !str_contains($baris, '=')) {
                continue;
            }

            [$kunci, $nilai] = explode('=', $baris, 2);
            $isiEnv[trim($kunci)] = trim(trim($nilai), '"\'');
        }
    }

    if (empty($isiEnv[$nama])) {
        berhenti("{$nama} belum diisi di file .env");
    }

    return $isiEnv[$nama];
}

// ----------------------------------------------------------------------------
// 2. Mengirim request ke API GajiHub
// ----------------------------------------------------------------------------

function api_get(string $endpoint, array $parameter = []): array
{
    return kirim_request('GET', $endpoint, $parameter);
}

function api_post(string $endpoint, array $data = []): array
{
    return kirim_request('POST', $endpoint, $data);
}

function api_put(string $endpoint, array $data = []): array
{
    return kirim_request('PUT', $endpoint, $data);
}

function api_patch(string $endpoint, array $data = []): array
{
    return kirim_request('PATCH', $endpoint, $data);
}

function api_delete(string $endpoint, array $parameter = []): array
{
    return kirim_request('DELETE', $endpoint, $parameter);
}

/**
 * Inti dari semua request. Semua endpoint GajiHub diawali /hr,
 * jadi $endpoint cukup ditulis mulai dari /hr/...
 */
function kirim_request(string $method, string $endpoint, array $data = []): array
{
    $url = rtrim(konfigurasi('API_HOST'), '/') . $endpoint;

    $header = [
        'Accept: application/json',
        'Authorization: Bearer ' . konfigurasi('ACCESS_TOKEN'),
    ];

    // GET/DELETE: parameter dikirim lewat URL (?page=1&per_page=10)
    // POST/PUT/PATCH: data dikirim sebagai JSON di body request
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

    // Simpan header respons untuk membaca nama file export
    $headerRespons = [];
    curl_setopt($curl, CURLOPT_HEADERFUNCTION, function ($curl, string $baris) use (&$headerRespons): int {
        if (str_contains($baris, ':')) {
            [$kunci, $nilai] = explode(':', $baris, 2);
            $headerRespons[strtolower(trim($kunci))] = trim($nilai);
        }

        return strlen($baris);
    });

    curl_setopt($curl, CURLOPT_HTTPHEADER, $header);

    tulis("{$method} {$url}");

    $isi = curl_exec($curl);

    if ($isi === false) {
        berhenti('Gagal terhubung ke server: ' . curl_error($curl));
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

// ----------------------------------------------------------------------------
// 3. Mengunduh file export (Excel / CSV)
// ----------------------------------------------------------------------------

/**
 * Unduh file export lalu simpan ke folder hasil-unduhan/.
 * Mengembalikan lokasi file, atau null jika gagal / tidak ada data.
 */
function unduh_file(string $endpoint, array $parameter = []): ?string
{
    $hasil = api_get($endpoint, $parameter);

    // Jika server membalas JSON, berarti ada pesan error (misalnya format tanggal salah)
    if (!$hasil['sukses'] || $hasil['data'] !== null) {
        tampilkan($hasil);
        return null;
    }

    // Respons kosong = tidak ada data pada periode/filter tersebut
    if ($hasil['isi'] === '') {
        tulis('Tidak ada data untuk diexport pada periode/filter tersebut.');
        return null;
    }

    // Ambil nama file dari header "Content-Disposition: attachment; filename=..."
    $namaFile = 'export_' . date('Ymd_His');
    if (preg_match('/filename="?([^";]+)"?/i', $hasil['header']['content-disposition'] ?? '', $cocok)) {
        $namaFile = basename($cocok[1]);
    }

    if (!is_dir(FOLDER_UNDUHAN)) {
        mkdir(FOLDER_UNDUHAN, 0777, true);
    }

    $lokasiFile = FOLDER_UNDUHAN . '/' . $namaFile;
    file_put_contents($lokasiFile, $hasil['isi']);

    tulis('Berhasil! File disimpan di: ' . $lokasiFile . ' (' . strlen($hasil['isi']) . ' bytes)');

    return $lokasiFile;
}

// ----------------------------------------------------------------------------
// 4. Menampilkan hasil (bisa dijalankan lewat terminal maupun browser)
// ----------------------------------------------------------------------------

function jalan_di_terminal(): bool
{
    return PHP_SAPI === 'cli';
}

/**
 * Tampilkan judul demo.
 * Di browser: tampilkan kode demo + tombol "Jalankan Request" (request baru dikirim setelah tombol diklik).
 * Di terminal: langsung jalan.
 */
function mulai_demo(string $judul): void
{
    if (jalan_di_terminal()) {
        echo PHP_EOL . '=== ' . $judul . ' ===' . PHP_EOL;
        return;
    }

    $sudahDiklik = isset($_GET['jalankan']);

    echo '<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width, initial-scale=1">'
        . '<title>' . htmlspecialchars($judul) . '</title>'
        . '<style>
            body{font-family:system-ui,sans-serif;max-width:960px;margin:24px auto;padding:0 16px;color:#1f2937}
            a{color:#2563eb} h1{font-size:22px}
            .tombol{display:inline-block;background:#16a34a;color:#fff;padding:8px 16px;border-radius:6px;text-decoration:none}
            .kotak{background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;overflow:auto;font-size:13px}
            pre{white-space:pre-wrap;word-break:break-word;margin:0}
          </style></head><body>'
        . '<p><a href="../../index.php">&larr; Kembali ke daftar demo</a></p>'
        . '<h1>' . htmlspecialchars($judul) . '</h1>';

    echo '<h3>Kode</h3><div class="kotak">';
    highlight_file($_SERVER['SCRIPT_FILENAME']);
    echo '</div>';

    if (!$sudahDiklik) {
        echo '<p><a class="tombol" href="?jalankan=1">Jalankan Request</a></p></body></html>';
        exit;
    }

    echo '<h3>Hasil</h3><div class="kotak"><pre>';

    // Tutup tag HTML setelah semua kode demo selesai dijalankan
    register_shutdown_function(function (): void {
        echo '</pre></div><p><a class="tombol" href="?jalankan=1">Jalankan Lagi</a></p></body></html>';
    });
}

/**
 * Cetak hasil request: status HTTP + isi respons dalam format JSON yang rapi.
 */
function tampilkan(array $hasil): void
{
    tulis('Status HTTP: ' . $hasil['status'] . ($hasil['sukses'] ? ' (berhasil)' : ' (gagal)'));

    if (!$hasil['sukses']) {
        tulis(arti_status($hasil['status']));
    }

    $teks = $hasil['data'] !== null
        ? json_encode($hasil['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
        : $hasil['isi'];

    tulis($teks);
}

/**
 * Cetak satu baris teks (aman untuk terminal maupun browser).
 */
function tulis(string $teks): void
{
    echo (jalan_di_terminal() ? $teks : htmlspecialchars($teks)) . PHP_EOL;
}

/**
 * Penjelasan singkat untuk kode status HTTP yang sering muncul.
 */
function arti_status(int $status): string
{
    return match ($status) {
        400     => 'Artinya: parameter/data yang dikirim tidak valid. Lihat pesan di bawah.',
        401     => 'Artinya: token tidak valid atau sudah kedaluwarsa. Periksa ACCESS_TOKEN di file .env.',
        403     => 'Artinya: user pemilik token tidak punya hak akses ke fitur ini.',
        404     => 'Artinya: data atau endpoint tidak ditemukan. Periksa ID / alamat endpoint.',
        429     => 'Artinya: terlalu banyak request. Tunggu sebentar lalu coba lagi.',
        default => $status >= 500 ? 'Artinya: terjadi kesalahan di server. Coba lagi beberapa saat.' : '',
    };
}

/**
 * Tampilkan pesan lalu hentikan program.
 */
function berhenti(string $pesan): never
{
    tulis('ERROR: ' . $pesan);
    exit(1);
}
