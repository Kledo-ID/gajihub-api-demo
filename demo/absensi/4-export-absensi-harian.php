<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel absensi harian (1 tanggal)
 *
 * Jalankan lewat terminal:  php 4-export-absensi-harian.php
 * File tersimpan di folder hasil-unduhan/
 *
 * Ganti "xls" di alamat endpoint menjadi "csv" untuk format CSV.
 * Catatan: format "xls" menghasilkan file .xlsx (Excel modern).
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Absensi Harian (Excel)');

unduh_file('/hr/attendances/daily/export/xls', [
    'date' => date('Y-m-d'), // tanggal, format YYYY-MM-DD. Jika dikosongkan = hari ini

    // --- Filter opsional ---
    // 'search'              => 'budi',
    // 'hr_org_structure_id' => 1,
    // 'is_active'           => 'active',
]);
