<?php

declare(strict_types=1);

/**
 * DEMO: Menambah jabatan baru
 *
 * Jalankan lewat terminal:  php 7-tambah-jabatan.php
 *
 * PERHATIAN: demo ini MENAMBAH data jabatan di GajiHub Anda.
 * Struktur organisasi (/hr/orgStructures) dan level jabatan (/hr/jobLevels)
 * bisa ditambah dengan cara yang sama.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Tambah Jabatan');

$hasil = api_post('/hr/jobPositions', [
    'name'      => 'Staff Gudang ' . date('His'), // WAJIB: nama jabatan (2-45 karakter, tidak boleh sama)
    'parent_id' => null,                          // opsional: ID jabatan atasan
]);

tampilkan($hasil);

if ($hasil['sukses']) {
    tulis('');
    tulis('ID jabatan baru: ' . $hasil['data']['data']['id'] . ' (pakai ID ini di demo ubah / hapus)');
}
