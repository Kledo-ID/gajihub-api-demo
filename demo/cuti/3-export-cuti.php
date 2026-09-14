<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel data cuti (semua jenis cuti)
 *
 * Jalankan lewat terminal:  php 3-export-cuti.php
 * File tersimpan di folder hasil-unduhan/
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Data Cuti (Excel)');

unduh_file('/hr/leaves/export/xls', [
    'date_leave_started' => date('Y-m-01'), // tanggal cuti mulai (YYYY-MM-DD)
    'date_leave_ended'   => date('Y-m-t'),  // tanggal cuti selesai (contoh: akhir bulan ini)

    // --- Filter opsional ---
    // 'hr_leave_type_id'      => 1, // jenis cuti (lihat demo data-master/6-referensi.php -> leaveTypes)
    // 'hr_approval_status_id' => 2, // 1 = menunggu, 2 = disetujui, 3 = ditolak
]);
