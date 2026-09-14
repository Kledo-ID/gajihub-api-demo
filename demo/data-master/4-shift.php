<?php

declare(strict_types=1);

/**
 * DEMO: Daftar shift kerja
 *
 * Jalankan lewat terminal:  php 4-shift.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Shift Kerja');

$hasil = api_get('/hr/shifts');

if ($hasil['sukses']) {
    foreach ($hasil['data']['data'] as $shift) {
        tulis("ID {$shift['id']} : {$shift['name']} ({$shift['time_started']} - {$shift['time_ended']})");
    }
    tulis('');
}

tampilkan($hasil);
