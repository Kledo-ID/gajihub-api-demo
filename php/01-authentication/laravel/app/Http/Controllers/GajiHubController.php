<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Services\GajiHub\GajiHubClient;
use Illuminate\Http\JsonResponse;

class GajiHubController extends Controller
{
    /**
     * Cek koneksi & token GajiHub: siapa pemilik token yang dipakai server ini?
     */
    public function me(GajiHubClient $gajihub): JsonResponse
    {
        $user = $gajihub->getCurrentUser();

        // Kirim hanya data yang dibutuhkan (respons asli juga berisi permission & menu)
        return response()->json([
            'id'    => $user['id'],
            'name'  => $user['name'],
            'email' => $user['email'],
        ]);
    }
}
