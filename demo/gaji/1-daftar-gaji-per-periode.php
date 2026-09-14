<?php

declare(strict_types=1);

/**
 * DEMO: Daftar pembayaran gaji karyawan dalam 1 periode (bulan)
 *
 * Jalankan lewat terminal:  php 1-daftar-gaji-per-periode.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Gaji per Periode');

$hasil = api_get('/hr/payrollPayments', [
    'period' => date('Y-m', strtotime('first day of last month')), // WAJIB: periode gaji YYYY-MM (contoh: bulan lalu)

    // --- Filter opsional ---
    // 'hr_org_structure_id' => 1,
    // 'hr_job_position_id'  => 1,
    // 'is_active'           => 'all',  // active / not_active / all
]);

tampilkan($hasil);
