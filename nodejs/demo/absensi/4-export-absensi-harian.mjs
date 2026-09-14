/**
 * DEMO: Unduh file Excel absensi harian (1 tanggal)
 *
 * Jalankan lewat terminal:  node 4-export-absensi-harian.mjs
 * File tersimpan di folder hasil-unduhan/
 *
 * Ganti "xls" di alamat endpoint menjadi "csv" untuk format CSV.
 * Catatan: format "xls" menghasilkan file .xlsx (Excel modern).
 */

import { mulaiDemo, tanggal, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Export Absensi Harian (Excel)');

await unduhFile('/hr/attendances/daily/export/xls', {
    date: tanggal(), // tanggal, format YYYY-MM-DD. Jika dikosongkan = hari ini

    // --- Filter opsional ---
    // search: 'budi',
    // hr_org_structure_id: 1,
    // is_active: 'active',
});
