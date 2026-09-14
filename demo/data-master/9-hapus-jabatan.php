<?php

declare(strict_types=1);

/**
 * DEMO: Menghapus jabatan
 *
 * Jalankan lewat terminal:  php 9-hapus-jabatan.php
 *
 * PERHATIAN: demo ini MENGHAPUS data jabatan di GajiHub Anda.
 * Jabatan yang masih dipakai karyawan tidak bisa dihapus.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Hapus Jabatan');

$idJabatan = 0; // ganti dengan ID jabatan (lihat hasil demo 7-tambah-jabatan.php)

$hasil = api_delete('/hr/jobPositions/' . $idJabatan);

tampilkan($hasil);
