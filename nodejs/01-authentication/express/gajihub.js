/**
 * Klien API GajiHub untuk dipakai di server (backend) Anda.
 *
 * Praktik keamanan yang diterapkan:
 *  - Token dibaca dari environment variable (file .env), tidak ditulis di dalam kode.
 *  - Token hanya dipakai di server. Jangan pernah kirim token ke browser / aplikasi mobile.
 *  - Aplikasi langsung berhenti saat start jika konfigurasi belum lengkap (fail fast).
 *  - Pesan error tidak memuat token.
 */

const API_HOST = process.env.GAJIHUB_API_HOST;
const ACCESS_TOKEN = process.env.GAJIHUB_ACCESS_TOKEN;

if (!API_HOST || !ACCESS_TOKEN) {
    throw new Error('GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN wajib diisi di file .env');
}

/**
 * Error saat GajiHub membalas status selain 2xx.
 */
export class GajiHubError extends Error {
    constructor(status, message) {
        super(message);
        this.name = 'GajiHubError';
        this.status = status;
    }
}

/**
 * Kirim request ke API GajiHub dan kembalikan isi "data" dari respons.
 *
 * @param {string} method    GET / POST / PUT / PATCH / DELETE
 * @param {string} endpoint  contoh: '/hr/employees/pagination'
 * @param {{ query?: object, body?: object }} opsi
 */
export async function gajihubRequest(method, endpoint, { query = {}, body } = {}) {
    const url = new URL(API_HOST.replace(/\/+$/, '') + endpoint);
    for (const [kunci, nilai] of Object.entries(query)) {
        url.searchParams.append(kunci, nilai);
    }

    const respons = await fetch(url, {
        method,
        headers: {
            Authorization: `Bearer ${ACCESS_TOKEN}`,
            Accept: 'application/json',
            'X-App': 'hr',
            ...(body !== undefined && { 'Content-Type': 'application/json' }),
        },
        body: body !== undefined ? JSON.stringify(body) : undefined,
        signal: AbortSignal.timeout(30_000),
    });

    const hasil = await respons.json().catch(() => null);

    if (!respons.ok) {
        throw new GajiHubError(respons.status, hasil?.message ?? `GajiHub membalas status ${respons.status}`);
    }

    return hasil.data;
}

/**
 * Data user pemilik token (dipakai untuk memastikan token valid).
 */
export function getCurrentUser() {
    return gajihubRequest('GET', '/authentication/user');
}
