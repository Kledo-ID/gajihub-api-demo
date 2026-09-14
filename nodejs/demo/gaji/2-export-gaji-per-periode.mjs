/**
 * DEMO: Unduh file Excel rekap gaji 1 periode (bulan)
 *
 * Jalankan lewat terminal:  node 2-export-gaji-per-periode.mjs
 * File tersimpan di folder hasil-unduhan/
 *
 * Periode harus sudah ada data gajinya. Jika belum, server membalas
 * "Period yang dipilih tidak valid."
 */

import { bulanLalu, mulaiDemo, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Gaji per Periode (Excel)');

await unduhFile('/hr/payrolls/perPeriod/export/xls', {
    period: bulanLalu(), // periode gaji YYYY-MM (contoh: bulan lalu)

    // --- Filter opsional ---
    // hr_org_structure_id: 1,
    // hr_job_position_id: 1,
});
