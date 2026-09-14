<?php

declare(strict_types=1);

/**
 * DEMO: Unduh otomatis laporan absensi (untuk dijadwalkan setiap hari)
 *
 * Cara pakai lewat terminal:
 *   php unduh-laporan-absensi.php                          -> laporan kemarin
 *   php unduh-laporan-absensi.php 2026-09-01 2026-09-30    -> laporan rentang tanggal
 *
 * File tersimpan di folder hasil-unduhan/
 *
 * Agar berjalan otomatis setiap hari, jadwalkan perintah di atas:
 *   - Windows : Task Scheduler (lihat README.md bagian "Unduh Otomatis")
 *   - Linux   : cron, contoh setiap jam 06:00:
 *               0 6 * * * php /lokasi/gajihub-api-demo/demo/unduh-otomatis/unduh-laporan-absensi.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Unduh Otomatis Laporan Absensi');

// Tanggal diambil dari perintah terminal. Jika tidak diisi, pakai tanggal kemarin.
$tanggalMulai   = $argv[1] ?? date('Y-m-d', strtotime('-1 day'));
$tanggalSelesai = $argv[2] ?? $tanggalMulai;

tulis("Periode: {$tanggalMulai} s/d {$tanggalSelesai}");

$periode = [
    'date_started' => $tanggalMulai,
    'date_ended'   => $tanggalSelesai,
];

// 1. Detail absensi per hari per karyawan
unduh_file('/hr/attendances/detail/export/xls', $periode);

// 2. Rekap absensi per karyawan
unduh_file('/hr/attendances/summary/export/xls', $periode);

// Tambahkan laporan lain di sini jika perlu, contoh:
// unduh_file('/hr/overtimes/export/xls', $periode);   // data lembur

tulis('Selesai.');
