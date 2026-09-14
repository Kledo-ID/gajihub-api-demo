/**
 * Contoh server Express yang memakai API GajiHub dengan aman.
 *
 * Jalankan:  npm install  lalu  npm start
 * Coba:      http://localhost:3000/gajihub/me
 */

import express from 'express';
import { GajiHubError, getCurrentUser } from './gajihub.js';

const app = express();

// Cek koneksi & token GajiHub: siapa pemilik token yang dipakai server ini?
app.get('/gajihub/me', async (req, res) => {
    const user = await getCurrentUser();

    // Kirim hanya data yang dibutuhkan (respons asli juga berisi permission & menu)
    res.json({ id: user.id, name: user.name, email: user.email });
});

// Error dari GajiHub: catat detailnya di log server, balas pesan umum ke pemanggil
app.use((error, req, res, next) => {
    if (!(error instanceof GajiHubError)) {
        return next(error);
    }

    // 401/403 dari GajiHub = token di server salah/kedaluwarsa, bukan kesalahan pemanggil
    console.error(`[GajiHub] status ${error.status}: ${error.message}`);
    res.status(502).json({ message: 'Gagal mengambil data dari GajiHub.' });
});

const port = process.env.PORT ?? 3000;
app.listen(port, () => {
    console.log(`Server berjalan di http://localhost:${port}`);
});
