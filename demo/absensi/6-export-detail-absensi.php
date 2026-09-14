<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel detail absensi (per hari, per karyawan)
 *
 * Jalankan lewat terminal:  php 6-export-detail-absensi.php
 * File tersimpan di folder hasil-unduhan/
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Detail Absensi (Excel)');

unduh_file('/hr/attendances/detail/export/xls', [
    'date_started' => date('Y-m-01'), // tanggal mulai (YYYY-MM-DD)
    'date_ended'   => date('Y-m-d'),  // tanggal selesai (YYYY-MM-DD)

    // --- Opsional: hanya karyawan tertentu (ID dipisah koma) ---
    // 'hr_employee_ids' => '12,34,56',
]);
