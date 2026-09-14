<?php

declare(strict_types=1);

/**
 * DEMO: Mengubah nama jabatan
 *
 * Jalankan lewat terminal:  php 8-ubah-jabatan.php
 *
 * PERHATIAN: demo ini MENGUBAH data jabatan di GajiHub Anda.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Ubah Jabatan');

$idJabatan = 0; // ganti dengan ID jabatan (lihat hasil demo 7-tambah-jabatan.php)

$hasil = api_put('/hr/jobPositions/' . $idJabatan, [
    'name'      => 'Kepala Gudang', // WAJIB: nama jabatan yang baru
    'parent_id' => null,            // opsional: ID jabatan atasan
]);

tampilkan($hasil);
