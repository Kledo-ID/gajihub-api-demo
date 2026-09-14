<?php

declare(strict_types=1);

/**
 * DEMO: Menambah data lembur karyawan (oleh admin)
 *
 * Jalankan lewat terminal:  php 2-tambah-lembur.php
 *
 * PERHATIAN: demo ini MENAMBAH data lembur di GajiHub Anda.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Tambah Lembur');

$hasil = api_post('/hr/overtimes', [
    'hr_employee_id'         => 1,               // WAJIB: ID karyawan
    'date'                   => date('Y-m-d'),   // WAJIB: tanggal lembur (YYYY-MM-DD)
    'time_started'           => '18:00',         // WAJIB: jam mulai (JJ:MM)
    'time_ended'             => '20:00',         // WAJIB: jam selesai (JJ:MM)
    'time_ended_is_tomorrow' => 0,               // WAJIB: 1 jika jam selesai sudah lewat tengah malam, 0 jika tidak
    'note'                   => 'Lembur closing bulanan (dibuat lewat API)', // opsional
]);

tampilkan($hasil);
