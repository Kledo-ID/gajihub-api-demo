/**
 * DEMO: Rekap absensi per karyawan untuk rentang tanggal
 * (jumlah hadir, terlambat, jam kerja, lembur, dll)
 *
 * Jalankan lewat terminal:  node 3-rekap-absensi.mjs
 */

import { apiGet, awalBulan, mulaiDemo, tampilkan, tanggal } from '../../gajihub.mjs';

mulaiDemo('Rekap Absensi per Karyawan');

const hasil = await apiGet('/hr/attendances/summary/pagination', {
    date_started: awalBulan(), // tanggal mulai, format YYYY-MM-DD (contoh: awal bulan ini)
    date_ended: tanggal(),     // tanggal selesai (contoh: hari ini)
    page: 1,
    per_page: 20,

    // --- Filter opsional ---
    // search: 'budi',
    // hr_org_structure_id: 1,
    // hr_job_position_id: 1,
    // is_active: 'active',   // active / not_active / all
    // sort_by: 'name',       // name / lates / working_hours / overtime_hours / ...
    // order_by: 'asc',       // asc / desc
});

tampilkan(hasil);
