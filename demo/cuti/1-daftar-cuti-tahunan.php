<?php

declare(strict_types=1);

/**
 * DEMO: Daftar pengajuan cuti tahunan
 *
 * Jalankan lewat terminal:  php 1-daftar-cuti-tahunan.php
 *
 * Jenis cuti lain memakai pola alamat yang sama, cukup ganti "annualLeaves":
 *   /hr/leaves/sickLeaves/pagination     -> sakit
 *   /hr/leaves/specialLeaves/pagination  -> cuti khusus
 *   /hr/leaves/unpaidLeaves/pagination   -> cuti tidak dibayar
 *   /hr/leaves/otherLeaves/pagination    -> izin
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Cuti Tahunan');

$hasil = api_get('/hr/leaves/annualLeaves/pagination', [
    'page'     => 1,
    'per_page' => 20,

    // --- Filter opsional ---
    // 'date_leave_started'    => '2026-09-01', // tanggal cuti mulai
    // 'date_leave_ended'      => '2026-09-30', // tanggal cuti selesai
    // 'hr_approval_status_id' => 2,            // 1 = menunggu, 2 = disetujui, 3 = ditolak
    // 'hr_employee_id'        => 1,            // hanya karyawan tertentu
    // 'search'                => 'budi',
    // 'order_by'              => 'leave_date', // leave_date / date_request / employee_name / ...
    // 'order_type'            => 'desc',       // asc / desc
]);

tampilkan($hasil);
