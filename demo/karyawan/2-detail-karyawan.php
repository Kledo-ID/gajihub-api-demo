<?php

declare(strict_types=1);

/**
 * DEMO: Detail 1 karyawan (data pribadi, karir, payroll)
 *
 * Jalankan lewat terminal:  php 2-detail-karyawan.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Detail Karyawan');

$idKaryawan = 1; // ganti dengan ID karyawan (lihat demo 1-daftar-karyawan.php)

$hasil = api_get('/hr/employees/' . $idKaryawan);

tampilkan($hasil);
