<?php

declare(strict_types=1);

/**
 * DEMO: Riwayat pengajuan kasbon
 *
 * Jalankan lewat terminal:  php 2-riwayat-kasbon.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Riwayat Kasbon');

$hasil = api_get('/hr/cashReceipt/history/pagination', [
    'page'     => 1,
    'per_page' => 20,

    // --- Filter opsional ---
    // 'hr_cash_receipt_status_id' => 2, // 1 = menunggu, 2 = disetujui, 3 = ditolak, 4 = dibayar, 5 = lunas
]);

tampilkan($hasil);
