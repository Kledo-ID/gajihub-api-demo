<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel data lembur
 *
 * Jalankan lewat terminal:  php 3-export-lembur.php
 * File tersimpan di folder hasil-unduhan/
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Lembur (Excel)');

unduh_file('/hr/overtimes/export/xls', [
    'date_started' => date('Y-m-01'), // tanggal mulai (YYYY-MM-DD)
    'date_ended'   => date('Y-m-t'),  // tanggal selesai (YYYY-MM-DD)

    // --- Filter opsional ---
    // 'hr_employee_id'      => 1,
    // 'hr_org_structure_id' => 1,
]);
