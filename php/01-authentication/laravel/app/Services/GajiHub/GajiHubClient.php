<?php

declare(strict_types=1);

namespace App\Services\GajiHub;

use Illuminate\Http\Client\PendingRequest;
use Illuminate\Support\Facades\Http;
use RuntimeException;

/**
 * Klien API GajiHub untuk dipakai di server (backend) Anda.
 *
 * Praktik keamanan yang diterapkan:
 *  - Token dibaca dari config/gajihub.php (sumbernya file .env), tidak ditulis di dalam kode.
 *  - Token hanya dipakai di server. Jangan pernah kirim token ke browser / aplikasi mobile.
 *  - Error langsung muncul jika konfigurasi belum lengkap (fail fast).
 *  - Pesan error tidak memuat token.
 */
class GajiHubClient
{
    private string $apiHost;

    private string $accessToken;

    public function __construct()
    {
        $this->apiHost = (string) config('gajihub.api_host');
        $this->accessToken = (string) config('gajihub.access_token');

        if ($this->apiHost === '' || $this->accessToken === '') {
            throw new RuntimeException('GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN wajib diisi di file .env');
        }
    }

    /**
     * Data user pemilik token (dipakai untuk memastikan token valid).
     */
    public function getCurrentUser(): array
    {
        return $this->request('GET', '/authentication/user');
    }

    /**
     * Kirim request ke API GajiHub dan kembalikan isi "data" dari respons.
     *
     * Contoh: $gajihub->request('GET', '/hr/employees/pagination', ['page' => 1]);
     *
     * @throws \App\Services\GajiHub\GajiHubException
     */
    public function request(string $method, string $endpoint, array $data = []): array
    {
        $opsi = in_array($method, ['GET', 'DELETE'], true) ? ['query' => $data] : ['json' => $data];

        $response = $this->http()->send($method, $endpoint, $opsi);

        if ($response->failed()) {
            throw new GajiHubException(
                $response->status(),
                $response->json('message') ?? "GajiHub membalas status {$response->status()}"
            );
        }

        return $response->json('data');
    }

    private function http(): PendingRequest
    {
        return Http::baseUrl(rtrim($this->apiHost, '/'))
            ->withToken($this->accessToken)
            ->acceptJson()
            ->withHeaders(['X-App' => 'hr'])
            ->timeout(30);
    }
}
