/**
 * DEMO: Unduh file Excel saldo kasbon dan riwayat kasbon
 *
 * Jalankan lewat terminal:  node 3-export-kasbon.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { mulaiDemo, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Kasbon (Excel)');

await unduhFile('/hr/cashReceipt/balance/export/xls'); // saldo kasbon per karyawan
await unduhFile('/hr/cashReceipt/history/export/xls'); // riwayat pengajuan kasbon
