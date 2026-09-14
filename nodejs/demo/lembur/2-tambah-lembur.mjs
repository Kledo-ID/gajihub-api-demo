/**
 * DEMO: Menambah data lembur karyawan (oleh admin)
 *
 * Jalankan lewat terminal:  node 2-tambah-lembur.mjs
 *
 * PERHATIAN: demo ini MENAMBAH data lembur di GajiHub Anda.
 */

import { apiPost, mulaiDemo, tampilkan, tanggal } from '../../gajihub.mjs';

mulaiDemo('Tambah Lembur');

const hasil = await apiPost('/hr/overtimes', {
    hr_employee_id: 1,          // WAJIB: ID karyawan
    date: tanggal(),            // WAJIB: tanggal lembur (YYYY-MM-DD)
    time_started: '18:00',      // WAJIB: jam mulai (JJ:MM)
    time_ended: '20:00',        // WAJIB: jam selesai (JJ:MM)
    time_ended_is_tomorrow: 0,  // WAJIB: 1 jika jam selesai sudah lewat tengah malam, 0 jika tidak
    note: 'Lembur closing bulanan (dibuat lewat API)', // opsional
});

tampilkan(hasil);
