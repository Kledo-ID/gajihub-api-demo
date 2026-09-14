<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel sisa kuota cuti tahunan per karyawan
 *
 * Jalankan lewat terminal:  php 4-export-sisa-kuota-cuti.php
 * File tersimpan di folder hasil-unduhan/
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Sisa Kuota Cuti Tahunan (Excel)');

unduh_file('/hr/leaves/annualLeaves/export/xls', [
    'as_of_date' => date('Y-m-d'), // sisa kuota per tanggal (YYYY-MM-DD)

    // --- Opsional: hanya karyawan tertentu (ID dipisah koma) ---
    // 'hr_employee_ids' => '1,2,3',
]);
