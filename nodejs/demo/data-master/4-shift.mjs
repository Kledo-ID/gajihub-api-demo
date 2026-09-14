/**
 * DEMO: Daftar shift kerja
 *
 * Jalankan lewat terminal:  node 4-shift.mjs
 */

import { apiGet, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Daftar Shift Kerja');

const hasil = await apiGet('/hr/shifts');

if (hasil.sukses) {
    for (const shift of hasil.data.data) {
        tulis(`ID ${shift.id} : ${shift.name} (${shift.time_started} - ${shift.time_ended})`);
    }
    tulis('');
}

tampilkan(hasil);
