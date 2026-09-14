<?php

declare(strict_types=1);

/**
 * DEMO: Absensi 1 karyawan selama 1 bulan
 *
 * Jalankan lewat terminal:  php 2-absensi-bulanan-karyawan.php
 *
 * ID karyawan bisa dilihat dari demo "karyawan/1-daftar-karyawan.php".
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Absensi Bulanan 1 Karyawan');

$hasil = api_get('/hr/attendances/pagination', [
    'hr_employee_id' => 1,             // WAJIB: ID karyawan (ganti sesuai data Anda)
    'date'           => date('Y-m'),   // bulan, format YYYY-MM (contoh: bulan ini)
    'page'           => 1,
    'per_page'       => 31,

    // --- Filter opsional ---
    // 'hr_attendance_status_id' => 1,  // hanya status kehadiran tertentu
]);

tampilkan($hasil);
