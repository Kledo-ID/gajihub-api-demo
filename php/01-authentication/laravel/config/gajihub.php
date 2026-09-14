<?php

/**
 * Konfigurasi API GajiHub.
 *
 * Nilainya dibaca dari file .env, tidak ditulis di dalam kode.
 * File .env JANGAN di-commit ke Git.
 */
return [
    // Alamat API perusahaan Anda, diakhiri /api/v1
    'api_host' => env('GAJIHUB_API_HOST'),

    // Personal Access Token dari GajiHub (Pengaturan > API Key), diawali gajihub_pat_
    'access_token' => env('GAJIHUB_ACCESS_TOKEN'),
];
