/**
 * DEMO: Unduh file Excel sisa kuota cuti tahunan per karyawan
 *
 * Jalankan lewat terminal:  node 4-export-sisa-kuota-cuti.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { mulaiDemo, tanggal, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Sisa Kuota Cuti Tahunan (Excel)');

await unduhFile('/hr/leaves/annualLeaves/export/xls', {
    as_of_date: tanggal(), // sisa kuota per tanggal (YYYY-MM-DD)

    // --- Opsional: hanya karyawan tertentu (ID dipisah koma) ---
    // hr_employee_ids: '1,2,3',
});
