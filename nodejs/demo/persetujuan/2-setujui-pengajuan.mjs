/**
 * DEMO: Menyetujui (approve) atau menolak (decline) pengajuan
 *
 * Jalankan lewat terminal:  node 2-setujui-pengajuan.mjs
 *
 * PERHATIAN: demo ini MENGUBAH status pengajuan di GajiHub Anda.
 * ID pengajuan diambil dari demo 1-daftar-persetujuan.mjs
 */

import { apiPatch, mulaiDemo, tampilkan } from '../../gajihub.mjs';

mulaiDemo('Setujui Pengajuan');

const idPengajuan = [0]; // ganti dengan ID pengajuan, bisa lebih dari 1: [12, 13]

const hasil = await apiPatch('/hr/approvals/approve', { // untuk menolak, ganti menjadi /hr/approvals/decline
    ids: idPengajuan,
    description: 'Disetujui lewat API', // opsional: catatan
});

tampilkan(hasil);
