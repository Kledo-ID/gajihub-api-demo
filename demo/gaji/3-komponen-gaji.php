<?php

declare(strict_types=1);

/**
 * DEMO: Daftar komponen gaji (gaji pokok, tunjangan, potongan, dll)
 *
 * Jalankan lewat terminal:  php 3-komponen-gaji.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Komponen Gaji');

$hasil = api_get('/hr/salaryComponents/pagination', [
    'page'     => 1,
    'per_page' => 50,
]);

if ($hasil['sukses']) {
    foreach ($hasil['data']['data']['data'] as $komponen) {
        tulis("ID {$komponen['id']} : {$komponen['name']} ({$komponen['hr_component_type']['name']})");
    }
    tulis('');
}

tampilkan($hasil);
