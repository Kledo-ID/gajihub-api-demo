/**
 * DEMO: Daftar shift kerja
 *
 * Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
 *   node 04-shifts.js
 */

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

(async () => {
    console.log('=== Daftar Shift Kerja ===');

    const hasil = await apiRequest('GET', '/hr/shifts');

    if (hasil.sukses) {
        for (const shift of hasil.data.data) {
            console.log(`ID ${shift.id} : ${shift.name} (${shift.time_started} - ${shift.time_ended})`);
        }
        console.log();
    }

    tampilkan(hasil);
})();

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
