<?php

declare(strict_types=1);

/**
 * DEMO: Data referensi (kode-kode pilihan)
 *
 * Jalankan lewat terminal:  php 6-referensi.php
 *
 * Saat menambah/mengubah karyawan, beberapa kolom diisi dengan ID pilihan,
 * misalnya jenis kelamin (hr_gender_id) atau status karyawan (hr_employee_status_id).
 * Demo ini menampilkan daftar ID tersebut.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Data Referensi');

$daftarReferensi = [
    'genders'          => 'Jenis kelamin      (hr_gender_id)',
    'maritalStatuses'  => 'Status pernikahan  (hr_marital_status_id)',
    'religions'        => 'Agama              (hr_religion_id)',
    'employeeStatuses' => 'Status karyawan    (hr_employee_status_id)',
    'educationLevels'  => 'Pendidikan         (hr_education_level_id)',
];

foreach ($daftarReferensi as $endpoint => $keterangan) {
    $hasil = api_get('/hr/references/' . $endpoint);

    if (!$hasil['sukses']) {
        tampilkan($hasil);
        continue;
    }

    tulis($keterangan . ':');
    foreach ($hasil['data']['data'] as $pilihan) {
        tulis("   {$pilihan['id']} = {$pilihan['name']}");
    }
    tulis('');
}
