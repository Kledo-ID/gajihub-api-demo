<?php

declare(strict_types=1);

/**
 * Halaman utama: daftar semua demo.
 * Buka lewat browser: http://localhost/gajihub-api-demo/
 *
 * Daftar demo dibaca otomatis dari folder demo/.
 * Judul demo diambil dari baris "DEMO: ..." di bagian atas setiap file.
 */

$daftarFolder = glob(__DIR__ . '/demo/*', GLOB_ONLYDIR);
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Demo API GajiHub</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 960px; margin: 24px auto; padding: 0 16px; color: #1f2937; }
        .kotak { border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px; margin-bottom: 12px; }
        h2 { font-size: 17px; margin: 0 0 8px; text-transform: capitalize; }
        li { margin: 4px 0; }
        a { color: #2563eb; }
        code { background: #f1f5f9; padding: 1px 4px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Demo API GajiHub</h1>

    <div class="kotak">
        Versi PHP: <code><?= PHP_VERSION ?></code><br>
        File konfigurasi .env: <?= is_file(__DIR__ . '/.env') ? '<b style="color:#16a34a">ditemukan</b>' : '<b style="color:#dc2626">belum ada, salin .env.example menjadi .env</b>' ?>
    </div>

    <?php foreach ($daftarFolder as $folder): ?>
        <div class="kotak">
            <h2><?= htmlspecialchars(str_replace('-', ' ', basename($folder))) ?></h2>
            <ul>
                <?php foreach (glob($folder . '/*.php') as $file): ?>
                    <?php
                    // Ambil judul dari baris "DEMO: ..." di komentar atas file
                    preg_match('/DEMO:\s*(.+)/', file_get_contents($file), $cocok);
                    $judul = $cocok[1] ?? basename($file);
                    ?>
                    <li>
                        <a href="demo/<?= basename($folder) ?>/<?= basename($file) ?>"><?= htmlspecialchars($judul) ?></a>
                        <small><code><?= basename($file) ?></code></small>
                    </li>
                <?php endforeach; ?>
            </ul>
        </div>
    <?php endforeach; ?>
</body>
</html>
