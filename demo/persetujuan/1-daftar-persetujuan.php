<?php

declare(strict_types=1);

/**
 * DEMO: Daftar pengajuan yang perlu disetujui
 * (cuti, izin, lembur, reimbursement, kasbon, dll)
 *
 * Jalankan lewat terminal:  php 1-daftar-persetujuan.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Daftar Persetujuan');

$hasil = api_get('/hr/approvals/pagination', [
    'hr_approval_status_id' => 1, // 1 = menunggu persetujuan, 2 = disetujui, 3 = ditolak
    'page'                  => 1,
    'per_page'              => 20,

    // --- Filter opsional ---
    // 'hr_approval_type_id' => 1,            // jenis pengajuan (lihat referensi approvalTypes)
    // 'date_started'        => '2026-09-01', // tanggal pengajuan mulai
    // 'date_ended'          => '2026-09-30', // tanggal pengajuan selesai
    // 'search'              => 'budi',
    // 'sort_by'             => 'request_date', // employee_name / type_name / request_date
    // 'sort_dir'            => 'desc',
]);

if ($hasil['sukses']) {
    foreach ($hasil['data']['data']['data'] as $pengajuan) {
        tulis("ID {$pengajuan['id']} : {$pengajuan['hr_approval_type']['name']} - {$pengajuan['hr_employee']['name']}");
    }
    tulis('');
}

tampilkan($hasil);
