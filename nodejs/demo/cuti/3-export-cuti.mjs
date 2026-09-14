/**
 * DEMO: Unduh file Excel data cuti (semua jenis cuti)
 *
 * Jalankan lewat terminal:  node 3-export-cuti.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { akhirBulan, awalBulan, mulaiDemo, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Data Cuti (Excel)');

await unduhFile('/hr/leaves/export/xls', {
    date_leave_started: awalBulan(), // tanggal cuti mulai (YYYY-MM-DD)
    date_leave_ended: akhirBulan(),  // tanggal cuti selesai (contoh: akhir bulan ini)

    // --- Filter opsional ---
    // hr_leave_type_id: 1,       // jenis cuti (lihat referensi leaveTypes)
    // hr_approval_status_id: 2,  // 1 = menunggu, 2 = disetujui, 3 = ditolak
});
