/**
 * DEMO: Daftar komponen gaji (gaji pokok, tunjangan, potongan, dll)
 *
 * Jalankan lewat terminal:  node 3-komponen-gaji.mjs
 */

import { apiGet, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Daftar Komponen Gaji');

const hasil = await apiGet('/hr/salaryComponents/pagination', {
    page: 1,
    per_page: 50,
});

if (hasil.sukses) {
    for (const komponen of hasil.data.data.data) {
        tulis(`ID ${komponen.id} : ${komponen.name} (${komponen.hr_component_type.name})`);
    }
    tulis('');
}

tampilkan(hasil);
