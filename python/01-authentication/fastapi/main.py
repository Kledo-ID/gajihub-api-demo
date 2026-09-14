"""
Contoh aplikasi FastAPI yang memakai API GajiHub dengan aman.

Jalankan:  uvicorn main:app --reload
Coba:      http://localhost:8000/gajihub/me
"""

import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from gajihub import GajiHubClient, GajiHubError, Settings

logger = logging.getLogger('uvicorn.error')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Settings() gagal saat start jika GAJIHUB_API_HOST / GAJIHUB_ACCESS_TOKEN belum diisi
    app.state.gajihub = GajiHubClient(Settings())
    yield
    await app.state.gajihub.close()


app = FastAPI(lifespan=lifespan)


def get_gajihub(request: Request) -> GajiHubClient:
    return request.app.state.gajihub


@app.get('/gajihub/me')
async def gajihub_me(gajihub: Annotated[GajiHubClient, Depends(get_gajihub)]):
    """Cek koneksi & token GajiHub: siapa pemilik token yang dipakai server ini?"""
    user = await gajihub.get_current_user()

    # Kirim hanya data yang dibutuhkan (respons asli juga berisi permission & menu)
    return {'id': user['id'], 'name': user['name'], 'email': user['email']}


@app.exception_handler(GajiHubError)
async def gajihub_error_handler(request: Request, error: GajiHubError):
    # 401/403 dari GajiHub = token di server salah/kedaluwarsa, bukan kesalahan pemanggil.
    # Catat detailnya di log server, balas pesan umum ke pemanggil.
    logger.error('[GajiHub] status %s: %s', error.status, error)
    return JSONResponse(status_code=502, content={'message': 'Gagal mengambil data dari GajiHub.'})
