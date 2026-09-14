/**
 * DEMO: Unduh otomatis laporan absensi (untuk dijadwalkan setiap hari)
 *
 * Cara pakai lewat terminal:
 *   node unduh-laporan-absensi.mjs                          -> laporan kemarin
 *   node unduh-laporan-absensi.mjs 2026-09-01 2026-09-30    -> laporan rentang tanggal
 *
 * File tersimpan di folder hasil-unduhan/
 *
 * Agar berjalan otomatis setiap hari, jadwalkan perintah di atas:
 *   - Windows : Task Scheduler (lihat nodejs/README.md)
 *   - Linux   : cron, contoh setiap jam 06:00:
 *               0 6 * * * node /lokasi/gajihub-api-demo/nodejs/demo/unduh-otomatis/unduh-laporan-absensi.mjs
 */

import { mulaiDemo, tanggal, tulis, unduhFile } from '../../gajihub.mjs';

mulaiDemo('Unduh Otomatis Laporan Absensi');

// Tanggal diambil dari perintah terminal. Jika tidak diisi, pakai tanggal kemarin.
const tanggalMulai = process.argv[2] ?? tanggal(-1);
const tanggalSelesai = process.argv[3] ?? tanggalMulai;

tulis(`Periode: ${tanggalMulai} s/d ${tanggalSelesai}`);

const periode = {
    date_started: tanggalMulai,
    date_ended: tanggalSelesai,
};

// 1. Detail absensi per hari per karyawan
await unduhFile('/hr/attendances/detail/export/xls', periode);

// 2. Rekap absensi per karyawan
await unduhFile('/hr/attendances/summary/export/xls', periode);

// Tambahkan laporan lain di sini jika perlu, contoh:
// await unduhFile('/hr/overtimes/export/xls', periode);   // data lembur

tulis('Selesai.');
