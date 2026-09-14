<?php

declare(strict_types=1);

/**
 * DEMO: Daftar data lembur karyawan
 *
 * Jalankan lewat terminal:  php 1-daftar-lembur.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Lembur');

$hasil = api_get('/hr/overtimes/pagination', [
    'date_started' => date('Y-m-01'), // tanggal mulai (YYYY-MM-DD)
    'date_ended'   => date('Y-m-t'),  // tanggal selesai (contoh: akhir bulan ini)
    'page'         => 1,
    'per_page'     => 20,

    // --- Filter opsional ---
    // 'hr_employee_id'      => 1,
    // 'hr_org_structure_id' => 1,
    // 'search'              => 'budi',
]);

tampilkan($hasil);
