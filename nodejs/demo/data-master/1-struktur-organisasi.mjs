/**
 * DEMO: Daftar struktur organisasi (divisi/departemen)
 *
 * Jalankan lewat terminal:  node 1-struktur-organisasi.mjs
 *
 * ID struktur organisasi dipakai saat menambah karyawan (hr_org_structure_id)
 * dan sebagai filter di laporan absensi.
 */

import { apiGet, mulaiDemo, tampilkan, tulis } from '../../gajihub.mjs';

mulaiDemo('Daftar Struktur Organisasi');

const hasil = await apiGet('/hr/orgStructures', {
    // is_archive: 'all', // not_archive (default) / archive / all
});

if (hasil.sukses) {
    for (const organisasi of hasil.data.data) {
        // parent_id = ID organisasi induk (kosong jika organisasi paling atas)
        tulis(`ID ${organisasi.id} : ${organisasi.name} (induk: ${organisasi.parent_id ?? '-'})`);
    }
    tulis('');
}

tampilkan(hasil);
