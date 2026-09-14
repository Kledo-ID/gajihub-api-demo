/**
 * DEMO: Unduh file Excel detail absensi (per hari, per karyawan)
 *
 * Jalankan lewat terminal:  node 6-export-detail-absensi.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { awalBulan, mulaiDemo, tanggal, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Detail Absensi (Excel)');

await unduhFile('/hr/attendances/detail/export/xls', {
    date_started: awalBulan(), // tanggal mulai (YYYY-MM-DD)
    date_ended: tanggal(),     // tanggal selesai (YYYY-MM-DD)

    // --- Opsional: hanya karyawan tertentu (ID dipisah koma) ---
    // hr_employee_ids: '12,34,56',
});
