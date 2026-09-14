/**
 * DEMO: Menghapus jabatan
 *
 * Jalankan lewat terminal:  node 9-hapus-jabatan.mjs
 *
 * PERHATIAN: demo ini MENGHAPUS data jabatan di GajiHub Anda.
 * Jabatan yang masih dipakai karyawan tidak bisa dihapus.
 */

import { apiDelete, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Hapus Jabatan');

const idJabatan = 0; // ganti dengan ID jabatan (lihat hasil demo 7-tambah-jabatan.mjs)

const hasil = await apiDelete('/hr/jobPositions/' + idJabatan);

tampilkan(hasil);
