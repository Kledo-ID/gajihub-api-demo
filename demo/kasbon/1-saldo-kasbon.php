<?php

declare(strict_types=1);

/**
 * DEMO: Saldo kasbon (pinjaman) per karyawan
 *
 * Jalankan lewat terminal:  php 1-saldo-kasbon.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Saldo Kasbon Karyawan');

$hasil = api_get('/hr/cashReceipt/balance/pagination', [
    'page'     => 1,
    'per_page' => 20,

    // --- Urutan opsional ---
    // 'sort_by'  => 'due',   // plafon / due / last_payment_amount / last_payment_date / employee_name
    // 'order_by' => 'desc',  // asc / desc
]);

tampilkan($hasil);
