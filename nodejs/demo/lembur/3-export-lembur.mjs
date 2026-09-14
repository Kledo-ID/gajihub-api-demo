/**
 * DEMO: Unduh file Excel data lembur
 *
 * Jalankan lewat terminal:  node 3-export-lembur.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { akhirBulan, awalBulan, mulaiDemo, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Lembur (Excel)');

await unduhFile('/hr/overtimes/export/xls', {
    date_started: awalBulan(), // tanggal mulai (YYYY-MM-DD)
    date_ended: akhirBulan(),  // tanggal selesai (YYYY-MM-DD)

    // --- Filter opsional ---
    // hr_employee_id: 1,
    // hr_org_structure_id: 1,
});
