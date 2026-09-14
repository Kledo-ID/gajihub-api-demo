/**
 * DEMO: Unduh file Excel data karyawan
 *
 * Jalankan lewat terminal:  node 4-export-karyawan.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { mulaiDemo, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Data Karyawan (Excel)');

await unduhFile('/hr/employees/export/xls', {
    // --- Filter opsional ---
    // is_active: 'all',              // active (default) / not_active / all
    // hr_org_structure_ids: [1, 2],  // hanya struktur organisasi tertentu
    // hr_job_position_ids: [3],      // hanya jabatan tertentu
});
