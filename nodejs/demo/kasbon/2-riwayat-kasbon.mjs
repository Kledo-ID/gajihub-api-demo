/**
 * DEMO: Riwayat pengajuan kasbon
 *
 * Jalankan lewat terminal:  node 2-riwayat-kasbon.mjs
 */

import { apiGet, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Riwayat Kasbon');

const hasil = await apiGet('/hr/cashReceipt/history/pagination', {
    page: 1,
    per_page: 20,

    // --- Filter opsional ---
    // hr_cash_receipt_status_id: 2, // 1 = menunggu, 2 = disetujui, 3 = ditolak, 4 = dibayar, 5 = lunas
});

tampilkan(hasil);
