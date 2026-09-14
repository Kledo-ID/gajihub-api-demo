/**
 * DEMO: Absensi 1 karyawan selama 1 bulan
 *
 * Jalankan lewat terminal:  node 2-absensi-bulanan-karyawan.mjs
 *
 * ID karyawan bisa dilihat dari demo "karyawan/1-daftar-karyawan.mjs".
 */

import { apiGet, bulanIni, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Absensi Bulanan 1 Karyawan');

const hasil = await apiGet('/hr/attendances/pagination', {
    hr_employee_id: 1,  // WAJIB: ID karyawan (ganti sesuai data Anda)
    date: bulanIni(),   // bulan, format YYYY-MM (contoh: bulan ini)
    page: 1,
    per_page: 31,

    // --- Filter opsional ---
    // hr_attendance_status_id: 1,  // hanya status kehadiran tertentu
});

tampilkan(hasil);
