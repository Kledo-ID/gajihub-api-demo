/**
 * DEMO: Daftar jabatan
 *
 * Jalankan lewat terminal:  node 2-jabatan.mjs
 *
 * ID jabatan dipakai saat menambah karyawan (hr_job_position_id).
 */

import { apiGet, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Daftar Jabatan');

const hasil = await apiGet('/hr/jobPositions');

if (hasil.sukses) {
    for (const jabatan of hasil.data.data) {
        // parent_id = ID jabatan atasan (kosong jika jabatan paling atas)
        tulis(`ID ${jabatan.id} : ${jabatan.name} (atasan: ${jabatan.parent_id ?? '-'})`);
    }
    tulis('');
}

tampilkan(hasil);
