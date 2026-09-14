<?php

declare(strict_types=1);

/**
 * DEMO: Daftar lokasi absensi (kantor / titik absen)
 *
 * Jalankan lewat terminal:  php 5-lokasi-absensi.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Lokasi Absensi');

$hasil = api_get('/hr/attendanceLocations', [
    'page'     => 1,
    'per_page' => 20,
]);

tampilkan($hasil);
