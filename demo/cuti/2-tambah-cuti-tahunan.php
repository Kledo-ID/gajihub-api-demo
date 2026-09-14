<?php

declare(strict_types=1);

/**
 * DEMO: Menambah cuti tahunan karyawan (oleh admin)
 *
 * Jalankan lewat terminal:  php 2-tambah-cuti-tahunan.php
 *
 * PERHATIAN: demo ini MENAMBAH data cuti di GajiHub Anda.
 * Karyawan harus masih punya sisa kuota cuti tahunan.
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Tambah Cuti Tahunan');

$hasil = api_post('/hr/leaves/annualLeaves', [
    'hr_employee_id'        => 1,                                // WAJIB: ID karyawan
    'hr_approval_status_id' => 1,                                // WAJIB: 1 = menunggu persetujuan, 2 = langsung disetujui, 3 = ditolak
    'date_request'          => date('Y-m-d'),                    // WAJIB: tanggal pengajuan (YYYY-MM-DD)
    'date_leaves'           => [date('Y-m-d', strtotime('+7 days'))], // WAJIB: daftar tanggal cuti (bisa lebih dari 1)
    'description'           => 'Cuti keluarga (dibuat lewat API)',  // opsional: keterangan
]);

tampilkan($hasil);

if ($hasil['sukses']) {
    tulis('');
    tulis('ID cuti baru: ' . $hasil['data']['data']['id']);
}
