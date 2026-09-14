<?php

declare(strict_types=1);

/**
 * DEMO: Daftar pengajuan reimbursement
 *
 * Jalankan lewat terminal:  php 1-daftar-reimbursement.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Reimbursement');

$hasil = api_get('/hr/reimbursements/pagination', [
    'page'     => 1,
    'per_page' => 20,

    // --- Filter opsional ---
    // 'date_request_started'      => '2026-09-01', // tanggal pengajuan mulai
    // 'date_request_ended'        => '2026-09-30', // tanggal pengajuan selesai
    // 'hr_reimbursement_status_id'=> 2,            // status reimbursement
    // 'search'                    => 'bensin',
    // 'sort_by'                   => 'request_date', // nomor / employee_name / title / request_date / total / status
    // 'sort_dir'                  => 'desc',         // asc / desc
]);

tampilkan($hasil);
