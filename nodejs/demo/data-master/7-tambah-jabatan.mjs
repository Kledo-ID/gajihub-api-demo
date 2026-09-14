/**
 * DEMO: Menambah jabatan baru
 *
 * Jalankan lewat terminal:  node 7-tambah-jabatan.mjs
 *
 * PERHATIAN: demo ini MENAMBAH data jabatan di GajiHub Anda.
 * Struktur organisasi (/hr/orgStructures) dan level jabatan (/hr/jobLevels)
 * bisa ditambah dengan cara yang sama.
 */

import { apiPost, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Tambah Jabatan');

const jamSekarang = new Date().toTimeString().slice(0, 8).replaceAll(':', ''); // contoh: 142530

const hasil = await apiPost('/hr/jobPositions', {
    name: 'Staff Gudang ' + jamSekarang, // WAJIB: nama jabatan (2-45 karakter, tidak boleh sama)
    parent_id: null,                     // opsional: ID jabatan atasan
});

tampilkan(hasil);

if (hasil.sukses) {
    tulis('');
    tulis('ID jabatan baru: ' + hasil.data.data.id + ' (pakai ID ini di demo ubah / hapus)');
}
