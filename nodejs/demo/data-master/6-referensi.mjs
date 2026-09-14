/**
 * DEMO: Data referensi (kode-kode pilihan)
 *
 * Jalankan lewat terminal:  node 6-referensi.mjs
 *
 * Saat menambah/mengubah karyawan, beberapa kolom diisi dengan ID pilihan,
 * misalnya jenis kelamin (hr_gender_id) atau status karyawan (hr_employee_status_id).
 * Demo ini menampilkan daftar ID tersebut.
 */

import { apiGet, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Data Referensi');

const daftarReferensi = {
    genders: 'Jenis kelamin      (hr_gender_id)',
    maritalStatuses: 'Status pernikahan  (hr_marital_status_id)',
    religions: 'Agama              (hr_religion_id)',
    employeeStatuses: 'Status karyawan    (hr_employee_status_id)',
    educationLevels: 'Pendidikan         (hr_education_level_id)',
};

for (const [endpoint, keterangan] of Object.entries(daftarReferensi)) {
    const hasil = await apiGet('/hr/references/' + endpoint);

    if (!hasil.sukses) {
        tampilkan(hasil);
        continue;
    }

    tulis(keterangan + ':');
    for (const pilihan of hasil.data.data) {
        tulis(`   ${pilihan.id} = ${pilihan.name}`);
    }
    tulis('');
}
