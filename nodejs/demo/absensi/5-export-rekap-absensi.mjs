/**
 * DEMO: Unduh file Excel rekap absensi (rentang tanggal)
 *
 * Jalankan lewat terminal:  node 5-export-rekap-absensi.mjs
 * File tersimpan di folder hasil-unduhan/
 */

import { awalBulan, mulaiDemo, tanggal, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Rekap Absensi (Excel)');

await unduhFile('/hr/attendances/summary/export/xls', {
    date_started: awalBulan(), // tanggal mulai (YYYY-MM-DD)
    date_ended: tanggal(),     // tanggal selesai (YYYY-MM-DD)
});
