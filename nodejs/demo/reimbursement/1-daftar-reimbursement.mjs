/**
 * DEMO: Daftar pengajuan reimbursement
 *
 * Jalankan lewat terminal:  node 1-daftar-reimbursement.mjs
 */

import { apiGet, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Daftar Reimbursement');

const hasil = await apiGet('/hr/reimbursements/pagination', {
    page: 1,
    per_page: 20,

    // --- Filter opsional ---
    // date_request_started: '2026-09-01', // tanggal pengajuan mulai
    // date_request_ended: '2026-09-30',   // tanggal pengajuan selesai
    // hr_reimbursement_status_id: 2,      // status reimbursement
    // search: 'bensin',
    // sort_by: 'request_date',            // nomor / employee_name / title / request_date / total / status
    // sort_dir: 'desc',                   // asc / desc
});

tampilkan(hasil);
