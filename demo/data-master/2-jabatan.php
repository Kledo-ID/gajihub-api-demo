<?php

declare(strict_types=1);

/**
 * DEMO: Daftar jabatan
 *
 * Jalankan lewat terminal:  php 2-jabatan.php
 *
 * ID jabatan dipakai saat menambah karyawan (hr_job_position_id).
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Jabatan');

$hasil = api_get('/hr/jobPositions');

if ($hasil['sukses']) {
    foreach ($hasil['data']['data'] as $jabatan) {
        // parent_id = ID jabatan atasan (kosong jika jabatan paling atas)
        tulis("ID {$jabatan['id']} : {$jabatan['name']} (atasan: " . ($jabatan['parent_id'] ?? '-') . ')');
    }
    tulis('');
}

tampilkan($hasil);
