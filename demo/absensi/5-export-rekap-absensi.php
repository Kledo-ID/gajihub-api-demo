<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel rekap absensi (rentang tanggal)
 *
 * Jalankan lewat terminal:  php 5-export-rekap-absensi.php
 * File tersimpan di folder hasil-unduhan/
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Rekap Absensi (Excel)');

unduh_file('/hr/attendances/summary/export/xls', [
    'date_started' => date('Y-m-01'), // tanggal mulai (YYYY-MM-DD)
    'date_ended'   => date('Y-m-d'),  // tanggal selesai (YYYY-MM-DD)
]);
