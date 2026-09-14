/**
 * DEMO: Unduh file Excel data reimbursement
 *
 * Jalankan lewat terminal:  node 2-export-reimbursement.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { mulaiDemo, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Reimbursement (Excel)');

await unduhFile('/hr/reimbursements/export/xls', {
    // --- Filter opsional ---
    // date_request_started: '2026-09-01',
    // date_request_ended: '2026-09-30',
});
