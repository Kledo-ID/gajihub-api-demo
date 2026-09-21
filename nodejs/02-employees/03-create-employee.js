/**
 * DEMO: Menambah karyawan baru (data pribadi + karir + payroll sekaligus)
 *
 * Cara pakai: isi API_HOST dan ACCESS_TOKEN di bagian Konfigurasi, lalu jalankan:
 *   node 03-create-employee.js
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
// pernah commit token ke Git. Contoh penerapannya ada di folder nodejs/01-authentication/express/
// ============================================================================

const API_HOST = 'https://namaperusahaan.api.kledo.com/api/v1'; // alamat API perusahaan Anda, diakhiri /api/v1
const ACCESS_TOKEN = 'gajihub_pat_xxxxxx_xxxxxxxxxxxxxxxx'; // Personal Access Token (diawali gajihub_pat_)

(async () => {
    console.log('=== Tambah Karyawan ===');

    const jamSekarang = new Date().toTimeString().slice(0, 8).replaceAll(':', ''); // contoh: 142530

    const hasil = await apiRequest('POST', '/hr/employees/insert', {

        // ===== 1. Data pribadi =====
        personal: {
            name: 'Budi Santoso',                           // WAJIB: nama lengkap (4-50 karakter)
            email: 'budi.' + jamSekarang + '@contoh.com',   // WAJIB: email (tidak boleh sama dengan karyawan lain)
            hr_gender_id: 1,                                // WAJIB: 1 = laki-laki, 2 = perempuan
            handphone: '081234567890',
            birthplace: 'Yogyakarta',                       // tempat lahir
            birthday: '1995-05-20',                         // tanggal lahir (YYYY-MM-DD)
            hr_marital_status_id: 2,                        // 1 = menikah, 2 = belum menikah, 3 = janda, 4 = duda
            hr_religion_id: 1,                              // lihat demo 03-master-data/06-references.js
            hr_citizenship_id: 1,                           // 1 = WNI

            // Kartu identitas
            hr_id_card_type_id: 1,                          // 1 = KTP
            id_card_number: '3404012005950001',

            // Alamat sesuai KTP
            address: 'Jl. Contoh No. 1',
            country_id: 1,                                  // 1 = Indonesia
            province_id: 18,                                // ID provinsi
            city_id: 250,                                   // ID kota/kabupaten

            // Alamat domisili
            residence_address: 'Jl. Contoh No. 1',
            residence_country_id: 1,
            residence_province_id: 18,
            residence_city_id: 250,

            // Kontak darurat
            emergency_contact: 'Siti (Istri)',
            emergency_contact_phone: '081298765432',
        },

        // ===== 2. Data karir =====
        career: {
            hr_employee_status_id: 1,     // WAJIB: 1 = tetap, 2 = percobaan, 3 = PKWT (kontrak), dll
            hr_org_structure_id: 2,       // WAJIB: ID struktur organisasi
            hr_job_position_id: 11,       // WAJIB: ID jabatan
            hr_job_level_id: 5,           // WAJIB: ID level jabatan
            hr_schedule_pattern_id: 1,    // ID pola jadwal kerja
            date_started_work: tanggal(), // WAJIB: tanggal mulai bekerja (YYYY-MM-DD)
            // date_ended: '2027-09-13',  // WAJIB untuk karyawan tidak tetap: tanggal kontrak berakhir
        },

        // ===== 3. Data payroll =====
        payroll: {
            hr_pph21_withholder_id: 1,    // ID pemotong PPh 21 (perusahaan)
            hr_taxpayer_status_id: 1,     // status PTKP: 1 = TK0, 2 = TK1, dst (lihat referensi taxpayerStatuses)
            // npwp: '12.345.678.9-012.345',
            // bpjs_healthcare_number: '0001234567890',
        },
    });

    tampilkan(hasil);

    if (hasil.sukses) {
        console.log();
        console.log('ID karyawan baru: ' + hasil.data.data.id);
    }
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
