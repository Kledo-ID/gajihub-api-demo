/**
 * DEMO: Detail 1 karyawan (data pribadi, karir, payroll)
 *
 * Jalankan lewat terminal:  node 2-detail-karyawan.mjs
 */

import { apiGet, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Detail Karyawan');

const idKaryawan = 1; // ganti dengan ID karyawan (lihat demo 1-daftar-karyawan.mjs)

const hasil = await apiGet('/hr/employees/' + idKaryawan);

tampilkan(hasil);
