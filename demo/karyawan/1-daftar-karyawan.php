<?php

declare(strict_types=1);

/**
 * DEMO: Daftar karyawan
 *
 * Jalankan lewat terminal:  php 1-daftar-karyawan.php
 *
 * Gunakan demo ini untuk mengetahui ID karyawan (hr_employee_id)
 * yang dibutuhkan demo lain.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Karyawan');

$hasil = api_get('/hr/employees/pagination', [
    'page'     => 1,
    'per_page' => 20,

    // --- Filter opsional ---
    // 'search'    => 'budi',     // cari nama / NIK karyawan
    // 'is_active' => 'active',   // active (default) / not_active / all
    // 'sort_by'   => 'name',     // code / name
    // 'order_by'  => 'asc',      // asc / desc
]);

if ($hasil['sukses']) {
    $halaman = $hasil['data']['data'];

    tulis("Total karyawan: {$halaman['total']} (halaman {$halaman['current_page']} dari {$halaman['last_page']})");
    foreach ($halaman['data'] as $karyawan) {
        tulis("ID {$karyawan['id']} : {$karyawan['code']} - {$karyawan['name']}");
    }
    tulis('');
}

tampilkan($hasil);
