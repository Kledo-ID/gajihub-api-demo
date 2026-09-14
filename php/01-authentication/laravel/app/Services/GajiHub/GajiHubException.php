<?php

declare(strict_types=1);

namespace App\Services\GajiHub;

use Illuminate\Http\JsonResponse;
use RuntimeException;

/**
 * Error saat GajiHub membalas status selain 2xx.
 *
 * Laravel otomatis mencatat detailnya di log (storage/logs), lalu memanggil render()
 * untuk membalas pesan umum ke pemanggil.
 */
class GajiHubException extends RuntimeException
{
    public function __construct(public readonly int $status, string $message)
    {
        parent::__construct("[GajiHub] status {$status}: {$message}");
    }

    /**
     * 401/403 dari GajiHub = token di server salah/kedaluwarsa, bukan kesalahan pemanggil.
     */
    public function render(): JsonResponse
    {
        return response()->json(['message' => 'Gagal mengambil data dari GajiHub.'], 502);
    }
}
