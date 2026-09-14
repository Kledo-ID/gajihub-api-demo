/**
 * ============================================================================
 *  gajihub.mjs — Fungsi bantu yang dipakai oleh semua demo Node.js
 * ============================================================================
 *
 *  File ini di-"import" oleh setiap file demo. Anda TIDAK perlu mengubahnya.
 *  Alamat API dan token diatur di file .env di folder utama gajihub-api-demo/
 *  (salin dari .env.example). File .env yang sama dipakai demo PHP & Python.
 *
 *  Tanpa npm install: hanya memakai fitur bawaan Node.js 18 atau lebih baru.
 *
 *  Daftar fungsi (semua fungsi api* dan unduhFile dipanggil dengan await):
 *    mulaiDemo('Judul')                  -> tampilkan judul demo
 *    apiGet('/endpoint', {parameter})    -> ambil data            (GET)
 *    apiPost('/endpoint', {data})        -> tambah data           (POST)
 *    apiPut('/endpoint', {data})         -> ubah data             (PUT)
 *    apiPatch('/endpoint', {data})       -> ubah sebagian data    (PATCH)
 *    apiDelete('/endpoint')              -> hapus data            (DELETE)
 *    unduhFile('/endpoint', {parameter}) -> unduh file Excel/CSV ke folder hasil-unduhan/
 *    tampilkan(hasil)                    -> cetak hasil request ke layar
 *    tulis('teks')                       -> cetak satu baris teks
 *
 *  Fungsi tanggal (zona waktu Asia/Jakarta):
 *    tanggal()     -> hari ini, YYYY-MM-DD   tanggal(-1) = kemarin, tanggal(7) = 7 hari lagi
 *    awalBulan()   -> YYYY-MM-01             akhirBulan() -> tanggal terakhir bulan ini
 *    bulanIni()    -> YYYY-MM                bulanLalu()  -> YYYY-MM bulan lalu
 *
 *  Setiap fungsi api* mengembalikan object:
 *    {
 *      status: 200,      // kode HTTP (200 = berhasil)
 *      sukses: true,     // true jika status 2xx
 *      data:   {...},    // isi respons JSON yang sudah diubah jadi object JavaScript
 *      isi:    Buffer,   // isi respons mentah (isi file)
 *      header: Headers,  // header respons
 *    }
 * ============================================================================
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Folder utama gajihub-api-demo/ (satu tingkat di atas folder nodejs/)
const FOLDER_UTAMA = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

// Folder tempat file hasil export disimpan
const FOLDER_UNDUHAN = path.join(FOLDER_UTAMA, 'hasil-unduhan');

// ----------------------------------------------------------------------------
// 1. Konfigurasi dari file .env
// ----------------------------------------------------------------------------

let isiEnv = null;

/**
 * Ambil nilai konfigurasi dari file .env, misalnya konfigurasi('API_HOST').
 */
function konfigurasi(nama) {
    if (isiEnv === null) {
        const fileEnv = path.join(FOLDER_UTAMA, '.env');

        if (!fs.existsSync(fileEnv)) {
            berhenti('File .env belum ada. Salin .env.example menjadi .env, lalu isi API_HOST dan ACCESS_TOKEN.');
        }

        isiEnv = {};
        for (let baris of fs.readFileSync(fileEnv, 'utf8').split(/\r?\n/)) {
            baris = baris.trim();

            // Lewati komentar (#) dan baris tanpa tanda =
            if (baris === '' || baris.startsWith('#') || !baris.includes('=')) {
                continue;
            }

            const posisi = baris.indexOf('=');
            const kunci = baris.slice(0, posisi).trim();
            const nilai = baris.slice(posisi + 1).trim().replace(/^["']+|["']+$/g, '');
            isiEnv[kunci] = nilai;
        }
    }

    if (!isiEnv[nama]) {
        berhenti(`${nama} belum diisi di file .env`);
    }

    return isiEnv[nama];
}

// ----------------------------------------------------------------------------
// 2. Mengirim request ke API GajiHub
// ----------------------------------------------------------------------------

export const apiGet = (endpoint, parameter = {}) => kirimRequest('GET', endpoint, parameter);
export const apiPost = (endpoint, data = {}) => kirimRequest('POST', endpoint, data);
export const apiPut = (endpoint, data = {}) => kirimRequest('PUT', endpoint, data);
export const apiPatch = (endpoint, data = {}) => kirimRequest('PATCH', endpoint, data);
export const apiDelete = (endpoint, parameter = {}) => kirimRequest('DELETE', endpoint, parameter);

/**
 * Ubah object parameter menjadi teks query URL, contoh: page=1&ids[]=1&ids[]=2
 */
function buatQuery(parameter) {
    const query = new URLSearchParams();
    for (const [kunci, nilai] of Object.entries(parameter)) {
        if (nilai === null || nilai === undefined) {
            continue; // nilai kosong tidak dikirim
        }
        if (Array.isArray(nilai)) {
            nilai.forEach((isi) => query.append(`${kunci}[]`, isi));
        } else if (typeof nilai === 'boolean') {
            query.append(kunci, nilai ? 1 : 0);
        } else {
            query.append(kunci, nilai);
        }
    }
    return query.toString();
}

/**
 * Inti dari semua request. Semua endpoint GajiHub diawali /hr,
 * jadi endpoint cukup ditulis mulai dari /hr/...
 */
async function kirimRequest(method, endpoint, data = {}) {
    let url = konfigurasi('API_HOST').replace(/\/+$/, '') + endpoint;

    const header = {
        Accept: 'application/json',
        Authorization: 'Bearer ' + konfigurasi('ACCESS_TOKEN'),
    };

    // GET/DELETE: parameter dikirim lewat URL (?page=1&per_page=10)
    // POST/PUT/PATCH: data dikirim sebagai JSON di body request
    const kirimSebagaiJson = ['POST', 'PUT', 'PATCH'].includes(method);
    let body;

    if (kirimSebagaiJson) {
        header['Content-Type'] = 'application/json';
        body = JSON.stringify(data);
    } else if (Object.keys(data).length > 0) {
        url += '?' + buatQuery(data);
    }

    tulis(`${method} ${url}`);

    let respons;
    try {
        respons = await fetch(url, {
            method,
            headers: header,
            body,
            signal: AbortSignal.timeout(300_000), // export bisa lama, tunggu maksimal 5 menit
        });
    } catch (gagal) {
        berhenti('Gagal terhubung ke server: ' + (gagal.cause?.message ?? gagal.message));
    }

    const isi = Buffer.from(await respons.arrayBuffer());

    let dataJson = null;
    try {
        dataJson = JSON.parse(isi.toString('utf8'));
    } catch {
        // bukan JSON, misalnya isi file Excel
    }

    return {
        status: respons.status,
        sukses: respons.status >= 200 && respons.status < 300,
        data: dataJson,
        isi,
        header: respons.headers,
    };
}

// ----------------------------------------------------------------------------
// 3. Mengunduh file export (Excel / CSV)
// ----------------------------------------------------------------------------

/**
 * Unduh file export lalu simpan ke folder hasil-unduhan/.
 * Mengembalikan lokasi file, atau null jika gagal / tidak ada data.
 */
export async function unduhFile(endpoint, parameter = {}) {
    const hasil = await apiGet(endpoint, parameter);

    // Jika server membalas JSON, berarti ada pesan error (misalnya format tanggal salah)
    if (!hasil.sukses || hasil.data !== null) {
        tampilkan(hasil);
        return null;
    }

    // Respons kosong = tidak ada data pada periode/filter tersebut
    if (hasil.isi.length === 0) {
        tulis('Tidak ada data untuk diexport pada periode/filter tersebut.');
        return null;
    }

    // Ambil nama file dari header "Content-Disposition: attachment; filename=..."
    let namaFile = 'export_' + tanggal().replaceAll('-', '') + '_' + Date.now();
    const cocok = /filename="?([^";]+)"?/i.exec(hasil.header.get('content-disposition') ?? '');
    if (cocok) {
        namaFile = path.basename(cocok[1]);
    }

    fs.mkdirSync(FOLDER_UNDUHAN, { recursive: true });

    const lokasiFile = path.join(FOLDER_UNDUHAN, namaFile);
    fs.writeFileSync(lokasiFile, hasil.isi);

    tulis(`Berhasil! File disimpan di: ${lokasiFile} (${hasil.isi.length} bytes)`);

    return lokasiFile;
}

// ----------------------------------------------------------------------------
// 4. Menampilkan hasil
// ----------------------------------------------------------------------------

/**
 * Tampilkan judul demo.
 */
export function mulaiDemo(judul) {
    tulis('');
    tulis(`=== ${judul} ===`);
}

/**
 * Cetak hasil request: status HTTP + isi respons dalam format JSON yang rapi.
 */
export function tampilkan(hasil) {
    tulis(`Status HTTP: ${hasil.status}` + (hasil.sukses ? ' (berhasil)' : ' (gagal)'));

    if (!hasil.sukses) {
        tulis(artiStatus(hasil.status));
    }

    tulis(hasil.data !== null ? JSON.stringify(hasil.data, null, 4) : hasil.isi.toString('utf8'));
}

/**
 * Cetak satu baris teks.
 */
export function tulis(teks) {
    console.log(teks);
}

/**
 * Penjelasan singkat untuk kode status HTTP yang sering muncul.
 */
function artiStatus(status) {
    const daftar = {
        400: 'Artinya: parameter/data yang dikirim tidak valid. Lihat pesan di bawah.',
        401: 'Artinya: token tidak valid atau sudah kedaluwarsa. Periksa ACCESS_TOKEN di file .env.',
        403: 'Artinya: user pemilik token tidak punya hak akses ke fitur ini.',
        404: 'Artinya: data atau endpoint tidak ditemukan. Periksa ID / alamat endpoint.',
        429: 'Artinya: terlalu banyak request. Tunggu sebentar lalu coba lagi.',
    };
    return daftar[status] ?? (status >= 500 ? 'Artinya: terjadi kesalahan di server. Coba lagi beberapa saat.' : '');
}

/**
 * Tampilkan pesan lalu hentikan program.
 */
function berhenti(pesan) {
    tulis('ERROR: ' + pesan);
    process.exit(1);
}

// ----------------------------------------------------------------------------
// 5. Fungsi tanggal (zona waktu Asia/Jakarta)
// ----------------------------------------------------------------------------

const duaDigit = (angka) => String(angka).padStart(2, '0');

/** Waktu sekarang di Asia/Jakarta (UTC+7), dibaca dengan getUTC...() */
const waktuJakarta = (tambahHari = 0) => new Date(Date.now() + (7 * 3600 + tambahHari * 86400) * 1000);

/** Tanggal hari ini (YYYY-MM-DD). tanggal(-1) = kemarin, tanggal(7) = 7 hari lagi. */
export function tanggal(tambahHari = 0) {
    const waktu = waktuJakarta(tambahHari);
    return `${waktu.getUTCFullYear()}-${duaDigit(waktu.getUTCMonth() + 1)}-${duaDigit(waktu.getUTCDate())}`;
}

/** Bulan ini (YYYY-MM). */
export const bulanIni = () => tanggal().slice(0, 7);

/** Tanggal pertama bulan ini (YYYY-MM-01). */
export const awalBulan = () => bulanIni() + '-01';

/** Tanggal terakhir bulan ini (YYYY-MM-DD). */
export function akhirBulan() {
    const waktu = waktuJakarta();
    const hariTerakhir = new Date(Date.UTC(waktu.getUTCFullYear(), waktu.getUTCMonth() + 1, 0)).getUTCDate();
    return `${bulanIni()}-${duaDigit(hariTerakhir)}`;
}

/** Bulan lalu (YYYY-MM). */
export function bulanLalu() {
    const waktu = waktuJakarta();
    const awalBulanLalu = new Date(Date.UTC(waktu.getUTCFullYear(), waktu.getUTCMonth() - 1, 1));
    return `${awalBulanLalu.getUTCFullYear()}-${duaDigit(awalBulanLalu.getUTCMonth() + 1)}`;
}
