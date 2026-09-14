/**
 * DEMO: Daftar lokasi absensi (kantor / titik absen)
 *
 * Jalankan lewat terminal:  node 5-lokasi-absensi.mjs
 */

import { apiGet, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Daftar Lokasi Absensi');

const hasil = await apiGet('/hr/attendanceLocations', {
    page: 1,
    per_page: 20,
});

tampilkan(hasil);
