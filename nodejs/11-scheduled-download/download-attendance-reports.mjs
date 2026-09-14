/**
 * DEMO: Unduh otomatis laporan absensi (untuk dijadwalkan setiap hari)
 *
 * Cara pakai (isi dulu API_HOST dan ACCESS_TOKEN di bagian Konfigurasi):
 *   node download-attendance-reports.mjs                          -> laporan kemarin
 *   node download-attendance-reports.mjs 2026-09-01 2026-09-30    -> laporan rentang tanggal
 *
 * File tersimpan di folder hasil-unduhan/ di sebelah file ini
 *
 * Agar berjalan otomatis setiap hari, jadwalkan perintah di atas:
 *   - Windows : Task Scheduler (lihat nodejs/README.md)
 *   - Linux   : cron, contoh setiap jam 06:00:
 *               0 6 * * * node /lokasi/gajihub-api-demo/nodejs/11-scheduled-download/download-attendance-reports.mjs
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// ============================================================================
// Konfigurasi
// ----------------------------------------------------------------------------
// Isi langsung di sini agar mudah dicoba.
//
// PENTING (keamanan): untuk aplikasi sungguhan, JANGAN tulis token di dalam kode.
// Simpan API_HOST dan ACCESS_TOKEN di file .env / environment variable, dan jangan
// pernah commit token ke Git. Contoh penerapannya ada di folder nodejs/01-authentication/express/
// ============================================================================

const API_HOST = 'https://namaperusahaan.api.kledo.com/api/v1'; // alamat API perusahaan Anda, diakhiri /api/v1
const ACCESS_TOKEN = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx'; // Personal Access Token (diawali gajihub_pat_)

console.log('=== Unduh Otomatis Laporan Absensi ===');

// Tanggal diambil dari perintah terminal. Jika tidak diisi, pakai tanggal kemarin.
const tanggalMulai = process.argv[2] ?? tanggal(-1);
const tanggalSelesai = process.argv[3] ?? tanggalMulai;

console.log(`Periode: ${tanggalMulai} s/d ${tanggalSelesai}`);

const periode = {
    date_started: tanggalMulai,
    date_ended: tanggalSelesai,
};

// 1. Detail absensi per hari per karyawan
await unduhFile('/hr/attendances/detail/export/xls', periode);

// 2. Rekap absensi per karyawan
await unduhFile('/hr/attendances/summary/export/xls', periode);

// Tambahkan laporan lain di sini jika perlu, contoh:
// await unduhFile('/hr/overtimes/export/xls', periode);   // data lembur

console.log('Selesai.');

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
 * GET/DELETE     : data dikirim lewat URL (?page=1&per_page=10)
 * POST/PUT/PATCH : data dikirim sebagai JSON di body request
 *
 * Hasil: { status: 200, sukses: true, data: {isi JSON}, isi: Buffer (respons mentah), header: Headers }
 */
async function apiRequest(method, endpoint, data = {}) {
    if (ACCESS_TOKEN.includes('xxxxxx')) {
        console.log('ERROR: API_HOST dan ACCESS_TOKEN belum diisi. Buka file ini dan isi bagian Konfigurasi.');
        process.exit(1);
    }

    let url = API_HOST.replace(/\/+$/, '') + endpoint;

    const header = {
        Authorization: 'Bearer ' + ACCESS_TOKEN,
        Accept: 'application/json',
        'X-App': 'hr',
        'User-Agent': 'gajihub-api-demo',
    };

    let body;
    if (['POST', 'PUT', 'PATCH'].includes(method)) {
        header['Content-Type'] = 'application/json';
        body = JSON.stringify(data);
    } else if (Object.keys(data).length > 0) {
        // Nilai berupa array dikirim sebagai kunci[]=1&kunci[]=2
        const query = new URLSearchParams();
        for (const [kunci, nilai] of Object.entries(data)) {
            if (Array.isArray(nilai)) {
                nilai.forEach((isi) => query.append(`${kunci}[]`, isi));
            } else {
                query.append(kunci, nilai);
            }
        }
        url += '?' + query.toString();
    }

    console.log(`${method} ${url}`);

    let respons;
    try {
        respons = await fetch(url, {
            method,
            headers: header,
            body,
            signal: AbortSignal.timeout(300_000), // export bisa lama, tunggu maksimal 5 menit
        });
    } catch (gagal) {
        console.log('ERROR: Gagal terhubung ke server: ' + (gagal.cause?.message ?? gagal.message));
        process.exit(1);
    }

    const isi = Buffer.from(await respons.arrayBuffer());

    let dataJson = null;
    try {
        dataJson = JSON.parse(isi.toString('utf8'));
    } catch {
        // bukan JSON, misalnya isi file Excel
    }

    return { status: respons.status, sukses: respons.ok, data: dataJson, isi, header: respons.headers };
}

/**
 * Unduh file export (Excel/CSV) lalu simpan ke folder hasil-unduhan/ di sebelah file ini.
 * Mengembalikan lokasi file, atau null jika gagal / tidak ada data.
 */
async function unduhFile(endpoint, parameter = {}) {
    const hasil = await apiRequest('GET', endpoint, parameter);

    // Jika server membalas JSON, berarti ada pesan error (misalnya format tanggal salah)
    if (!hasil.sukses || hasil.data !== null) {
        tampilkan(hasil);
        return null;
    }

    // Respons kosong = tidak ada data pada periode/filter tersebut
    if (hasil.isi.length === 0) {
        console.log('Tidak ada data untuk diexport pada periode/filter tersebut.');
        return null;
    }

    // Ambil nama file dari header "Content-Disposition: attachment; filename=..."
    let namaFile = 'export_' + Date.now();
    const cocok = /filename="?([^";]+)"?/i.exec(hasil.header.get('content-disposition') ?? '');
    if (cocok) {
        namaFile = path.basename(cocok[1]);
    }

    const folder = path.join(path.dirname(fileURLToPath(import.meta.url)), 'hasil-unduhan');
    fs.mkdirSync(folder, { recursive: true });

    const lokasiFile = path.join(folder, namaFile);
    fs.writeFileSync(lokasiFile, hasil.isi);

    console.log(`Berhasil! File disimpan di: ${lokasiFile} (${hasil.isi.length} bytes)`);

    return lokasiFile;
}

/**
 * Cetak hasil request: status HTTP + isi respons dalam format JSON yang rapi.
 */
function tampilkan(hasil) {
    console.log(`Status HTTP: ${hasil.status}` + (hasil.sukses ? ' (berhasil)' : ' (gagal)'));

    // Penjelasan singkat untuk kode status yang sering muncul
    const arti = {
        400: 'Artinya: parameter/data yang dikirim tidak valid. Lihat pesan di bawah.',
        401: 'Artinya: token tidak valid atau sudah kedaluwarsa. Periksa ACCESS_TOKEN.',
        403: 'Artinya: user pemilik token tidak punya hak akses ke fitur ini.',
        404: 'Artinya: data atau endpoint tidak ditemukan. Periksa ID / API_HOST.',
        429: 'Artinya: terlalu banyak request. Tunggu sebentar lalu coba lagi.',
    }[hasil.status] ?? (hasil.status >= 500 ? 'Artinya: terjadi kesalahan di server. Coba lagi beberapa saat.' : '');

    if (!hasil.sukses && arti) {
        console.log(arti);
    }

    console.log(hasil.data !== null ? JSON.stringify(hasil.data, null, 4) : hasil.isi.toString('utf8'));
}

/** Tanggal hari ini di Asia/Jakarta (YYYY-MM-DD). tanggal(-1) = kemarin, tanggal(7) = 7 hari lagi. */
function tanggal(tambahHari = 0) {
    const waktu = waktuJakarta(tambahHari);
    return `${waktu.getUTCFullYear()}-${duaDigit(waktu.getUTCMonth() + 1)}-${duaDigit(waktu.getUTCDate())}`;
}

/** Waktu sekarang di Asia/Jakarta (UTC+7), dibaca dengan getUTC...() */
function waktuJakarta(tambahHari = 0) {
    return new Date(Date.now() + (7 * 3600 + tambahHari * 86400) * 1000);
}

function duaDigit(angka) {
    return String(angka).padStart(2, '0');
}
