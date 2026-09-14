<?php

declare(strict_types=1);

/**
 * DEMO: Daftar struktur organisasi (divisi/departemen)
 *
 * Jalankan lewat terminal:  php 1-struktur-organisasi.php
 *
 * ID struktur organisasi dipakai saat menambah karyawan (hr_org_structure_id)
 * dan sebagai filter di laporan absensi.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Struktur Organisasi');

$hasil = api_get('/hr/orgStructures', [
    // 'is_archive' => 'all', // not_archive (default) / archive / all
]);

if ($hasil['sukses']) {
    foreach ($hasil['data']['data'] as $organisasi) {
        // parent_id = ID organisasi induk (kosong jika organisasi paling atas)
        tulis("ID {$organisasi['id']} : {$organisasi['name']} (induk: " . ($organisasi['parent_id'] ?? '-') . ')');
    }
    tulis('');
}

tampilkan($hasil);
