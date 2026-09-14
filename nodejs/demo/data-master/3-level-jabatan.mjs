/**
 * DEMO: Daftar level jabatan (golongan)
 *
 * Jalankan lewat terminal:  node 3-level-jabatan.mjs
 *
 * ID level jabatan dipakai saat menambah karyawan (hr_job_level_id).
 */

import { apiGet, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Daftar Level Jabatan');

const hasil = await apiGet('/hr/jobLevels');

if (hasil.sukses) {
    for (const level of hasil.data.data) {
        tulis(`ID ${level.id} : ${level.name}`);
    }
    tulis('');
}

tampilkan(hasil);
