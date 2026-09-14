/**
 * DEMO: Saldo kasbon (pinjaman) per karyawan
 *
 * Jalankan lewat terminal:  node 1-saldo-kasbon.mjs
 */

import { apiGet, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Saldo Kasbon Karyawan');

const hasil = await apiGet('/hr/cashReceipt/balance/pagination', {
    page: 1,
    per_page: 20,

    // --- Urutan opsional ---
    // sort_by: 'due',    // plafon / due / last_payment_amount / last_payment_date / employee_name
    // order_by: 'desc',  // asc / desc
});

tampilkan(hasil);
