/**
 * DEMO: Daftar data lembur karyawan
 *
 * Jalankan lewat terminal:  node 1-daftar-lembur.mjs
 */

import { akhirBulan, apiGet, awalBulan, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Daftar Lembur');

const hasil = await apiGet('/hr/overtimes/pagination', {
    date_started: awalBulan(), // tanggal mulai (YYYY-MM-DD)
    date_ended: akhirBulan(),  // tanggal selesai (contoh: akhir bulan ini)
    page: 1,
    per_page: 20,

    // --- Filter opsional ---
    // hr_employee_id: 1,
    // hr_org_structure_id: 1,
    // search: 'budi',
});

tampilkan(hasil);
