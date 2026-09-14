/**
 * DEMO: Menambah cuti tahunan karyawan (oleh admin)
 *
 * Jalankan lewat terminal:  node 2-tambah-cuti-tahunan.mjs
 *
 * PERHATIAN: demo ini MENAMBAH data cuti di GajiHub Anda.
 * Karyawan harus masih punya sisa kuota cuti tahunan.
 */

import { apiPost, mulaiDemo, tampilkan, tanggal, tulis } from '../../gajihub.mjs';

mulaiDemo('Tambah Cuti Tahunan');

const hasil = await apiPost('/hr/leaves/annualLeaves', {
    hr_employee_id: 1,                             // WAJIB: ID karyawan
    hr_approval_status_id: 1,                      // WAJIB: 1 = menunggu persetujuan, 2 = langsung disetujui, 3 = ditolak
    date_request: tanggal(),                       // WAJIB: tanggal pengajuan (YYYY-MM-DD)
    date_leaves: [tanggal(7)],                     // WAJIB: daftar tanggal cuti (bisa lebih dari 1)
    description: 'Cuti keluarga (dibuat lewat API)', // opsional: keterangan
});

tampilkan(hasil);

if (hasil.sukses) {
    tulis('');
    tulis('ID cuti baru: ' + hasil.data.data.id);
}
