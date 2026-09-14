/**
 * DEMO: Daftar pembayaran gaji karyawan dalam 1 periode (bulan)
 *
 * Jalankan lewat terminal:  node 1-daftar-gaji-per-periode.mjs
 */

import { apiGet, bulanLalu, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Daftar Gaji per Periode');

const hasil = await apiGet('/hr/payrollPayments', {
    period: bulanLalu(), // WAJIB: periode gaji YYYY-MM (contoh: bulan lalu)

    // --- Filter opsional ---
    // hr_org_structure_id: 1,
    // hr_job_position_id: 1,
    // is_active: 'all',  // active / not_active / all
});

tampilkan(hasil);
