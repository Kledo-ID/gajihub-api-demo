<?php

declare(strict_types=1);

/**
 * DEMO: Absensi harian semua karyawan (untuk 1 tanggal)
 *
 * Jalankan lewat terminal:  php 1-absensi-harian.php
 * Atau buka lewat browser:  http://localhost/gajihub-api-demo/demo/absensi/1-absensi-harian.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Absensi Harian Semua Karyawan');

$hasil = api_get('/hr/attendances/daily/pagination', [
    'date'     => date('Y-m-d'), // tanggal absensi, format YYYY-MM-DD (contoh: hari ini)
    'page'     => 1,             // halaman ke-
    'per_page' => 20,            // jumlah data per halaman

    // --- Filter opsional (hapus tanda // untuk mengaktifkan) ---
    // 'search'                   => 'budi',     // cari nama karyawan
    // 'hr_org_structure_id'      => 1,          // ID struktur organisasi
    // 'hr_job_position_id'       => 1,          // ID jabatan
    // 'hr_attendance_location_id'=> 1,          // ID lokasi absensi
    // 'hr_shift_id'              => 1,          // ID shift
    // 'hr_attendance_status_ids' => [1, 2],     // status kehadiran (lihat daftar di bawah)
    // 'is_late'                  => 'late',     // late = terlambat, not_late = tidak terlambat
    // 'is_active'                => 'active',   // active / not_active / all
    // 'sort_by'                  => 'employee_name',
    // 'sort_dir'                 => 'asc',      // asc / desc
]);

/*
 * Kode status kehadiran (hr_attendance_status_id):
 *  1 = Tanpa status,        2 = Hadir (hari kerja),  3 = Hadir (hari libur),
 *  4 = Mangkir,             5 = Hari libur,          6 = Dinas luar,
 *  7 = Sakit,               8 = Izin,                9 = Cuti,
 *  10 = Cuti setengah hari, 11 = Cuti tidak dibayar, 12 = Cuti bersama
 */

if ($hasil['sukses']) {
    $halaman = $hasil['data']['data'];

    tulis("Total karyawan: {$halaman['total']} (halaman {$halaman['current_page']} dari {$halaman['last_page']})");
    tulis('');
}

tampilkan($hasil);
