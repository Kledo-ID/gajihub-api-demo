/**
 * DEMO: Mengubah nama jabatan
 *
 * Jalankan lewat terminal:  node 8-ubah-jabatan.mjs
 *
 * PERHATIAN: demo ini MENGUBAH data jabatan di GajiHub Anda.
 */

import { apiPut, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Ubah Jabatan');

const idJabatan = 0; // ganti dengan ID jabatan (lihat hasil demo 7-tambah-jabatan.mjs)

const hasil = await apiPut('/hr/jobPositions/' + idJabatan, {
    name: 'Kepala Gudang', // WAJIB: nama jabatan yang baru
    parent_id: null,       // opsional: ID jabatan atasan
});

tampilkan(hasil);
