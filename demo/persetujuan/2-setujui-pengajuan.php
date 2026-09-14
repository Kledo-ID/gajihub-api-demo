<?php

declare(strict_types=1);

/**
 * DEMO: Menyetujui (approve) atau menolak (decline) pengajuan
 *
 * Jalankan lewat terminal:  php 2-setujui-pengajuan.php
 *
 * PERHATIAN: demo ini MENGUBAH status pengajuan di GajiHub Anda.
 * ID pengajuan diambil dari demo 1-daftar-persetujuan.php
 */

require __DIR__ . '/../../gajihub.php';

mulai_demo('Setujui Pengajuan');

$idPengajuan = [0]; // ganti dengan ID pengajuan, bisa lebih dari 1: [12, 13]

$hasil = api_patch('/hr/approvals/approve', [   // untuk menolak, ganti menjadi /hr/approvals/decline
    'ids'         => $idPengajuan,
    'description' => 'Disetujui lewat API',   // opsional: catatan
]);

tampilkan($hasil);
