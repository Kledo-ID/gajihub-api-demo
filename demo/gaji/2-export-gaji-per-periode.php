<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel rekap gaji 1 periode (bulan)
 *
 * Jalankan lewat terminal:  php 2-export-gaji-per-periode.php
 * File tersimpan di folder hasil-unduhan/
 *
 * Periode harus sudah ada data gajinya. Jika belum, server membalas
 * "Period yang dipilih tidak valid."
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Gaji per Periode (Excel)');

unduh_file('/hr/payrolls/perPeriod/export/xls', [
    'period' => date('Y-m', strtotime('first day of last month')), // periode gaji YYYY-MM (contoh: bulan lalu)

    // --- Filter opsional ---
    // 'hr_org_structure_id' => 1,
    // 'hr_job_position_id'  => 1,
]);
