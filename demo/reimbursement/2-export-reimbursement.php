<?php

declare(strict_types=1);

/**
 * DEMO: Unduh file Excel data reimbursement
 *
 * Jalankan lewat terminal:  php 2-export-reimbursement.php
 * File tersimpan di folder hasil-unduhan/
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Export Reimbursement (Excel)');

unduh_file('/hr/reimbursements/export/xls', [
    // --- Filter opsional ---
    // 'date_request_started' => '2026-09-01',
    // 'date_request_ended'   => '2026-09-30',
]);
