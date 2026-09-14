"""
Klien API GajiHub untuk dipakai di server (backend) Anda.

Praktik keamanan yang diterapkan:
 - Token dibaca dari environment variable (file .env), tidak ditulis di dalam kode.
 - Token hanya dipakai di server. Jangan pernah kirim token ke browser / aplikasi mobile.
 - Aplikasi langsung berhenti saat start jika konfigurasi belum lengkap (fail fast).
 - Token disimpan sebagai SecretStr, sehingga tidak ikut tercetak di log / pesan error.
"""

import httpx
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Dibaca dari environment variable GAJIHUB_API_HOST dan GAJIHUB_ACCESS_TOKEN, atau dari file .env."""

    model_config = SettingsConfigDict(env_file='.env', env_prefix='GAJIHUB_', extra='ignore')

    api_host: str
    access_token: SecretStr


class GajiHubError(Exception):
    """Error saat GajiHub membalas status selain 2xx."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


class GajiHubClient:
    """Satu klien dipakai bersama untuk semua request, sehingga koneksi ke GajiHub dipakai ulang."""

    def __init__(self, settings: Settings):
        self._http = httpx.AsyncClient(
            base_url=settings.api_host.rstrip('/'),
            headers={
                'Authorization': f'Bearer {settings.access_token.get_secret_value()}',
                'Accept': 'application/json',
                'X-App': 'hr',
            },
            timeout=30,
        )

    async def request(self, method: str, endpoint: str, **opsi) -> dict:
        """
        Kirim request ke API GajiHub dan kembalikan isi "data" dari respons.

        Contoh: await gajihub.request('GET', '/hr/employees/pagination', params={'page': 1})
        """
        respons = await self._http.request(method, endpoint, **opsi)

        try:
            hasil = respons.json()
        except ValueError:
            hasil = {}

        if respons.is_error:
            raise GajiHubError(respons.status_code, hasil.get('message') or f'GajiHub membalas status {respons.status_code}')

        return hasil['data']

    async def get_current_user(self) -> dict:
        """Data user pemilik token (dipakai untuk memastikan token valid)."""
        return await self.request('GET', '/authentication/user')

    async def close(self) -> None:
        await self._http.aclose()
