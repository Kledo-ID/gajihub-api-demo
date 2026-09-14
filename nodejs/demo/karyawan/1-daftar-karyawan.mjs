/**
 * DEMO: Daftar karyawan
 *
 * Jalankan lewat terminal:  node 1-daftar-karyawan.mjs
 *
 * Gunakan demo ini untuk mengetahui ID karyawan (hr_employee_id)
 * yang dibutuhkan demo lain.
 */

import { apiGet, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Daftar Karyawan');

const hasil = await apiGet('/hr/employees/pagination', {
    page: 1,
    per_page: 20,

    // --- Filter opsional ---
    // search: 'budi',       // cari nama / NIK karyawan
    // is_active: 'active',  // active (default) / not_active / all
    // sort_by: 'name',      // code / name
    // order_by: 'asc',      // asc / desc
});

if (hasil.sukses) {
    const halaman = hasil.data.data;

    tulis(`Total karyawan: ${halaman.total} (halaman ${halaman.current_page} dari ${halaman.last_page})`);
    for (const karyawan of halaman.data) {
        tulis(`ID ${karyawan.id} : ${karyawan.code} - ${karyawan.name}`);
    }
    tulis('');
}

tampilkan(hasil);
