<?php

declare(strict_types=1);

/**
 * DEMO: Daftar level jabatan (golongan)
 *
 * Jalankan lewat terminal:  php 3-level-jabatan.php
 *
 * ID level jabatan dipakai saat menambah karyawan (hr_job_level_id).
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Level Jabatan');

$hasil = api_get('/hr/jobLevels');

if ($hasil['sukses']) {
    foreach ($hasil['data']['data'] as $level) {
        tulis("ID {$level['id']} : {$level['name']}");
    }
    tulis('');
}

tampilkan($hasil);
