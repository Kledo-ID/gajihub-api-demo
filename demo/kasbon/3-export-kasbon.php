<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel saldo kasbon dan riwayat kasbon
 *
 * Jalankan lewat terminal:  php 3-export-kasbon.php
 * File tersimpan di folder hasil-unduhan/
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Kasbon (Excel)');

unduh_file('/hr/cashReceipt/balance/export/xls');  // saldo kasbon per karyawan
unduh_file('/hr/cashReceipt/history/export/xls');  // riwayat pengajuan kasbon
