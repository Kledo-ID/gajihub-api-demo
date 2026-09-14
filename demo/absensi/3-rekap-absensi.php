<?php

declare(strict_types=1);

/**
 * DEMO: Rekap absensi per karyawan untuk rentang tanggal
 * (jumlah hadir, terlambat, jam kerja, lembur, dll)
 *
 * Jalankan lewat terminal:  php 3-rekap-absensi.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Rekap Absensi per Karyawan');

$hasil = api_get('/hr/attendances/summary/pagination', [
    'date_started' => date('Y-m-01'), // tanggal mulai, format YYYY-MM-DD (contoh: awal bulan ini)
    'date_ended'   => date('Y-m-d'),  // tanggal selesai (contoh: hari ini)
    'page'         => 1,
    'per_page'     => 20,

    // --- Filter opsional ---
    // 'search'              => 'budi',
    // 'hr_org_structure_id' => 1,
    // 'hr_job_position_id'  => 1,
    // 'is_active'           => 'active',   // active / not_active / all
    // 'sort_by'             => 'name',     // name / lates / working_hours / overtime_hours / ...
    // 'order_by'            => 'asc',      // asc / desc
]);

tampilkan($hasil);
