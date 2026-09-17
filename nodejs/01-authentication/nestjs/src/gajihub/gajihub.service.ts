/**
 * Klien API GajiHub untuk dipakai di server (backend) Anda.
 *
 * Praktik keamanan yang diterapkan:
 *  - Token dibaca dari environment variable (file .env), tidak ditulis di dalam kode.
 *  - Token hanya dipakai di server. Jangan pernah kirim token ke browser / aplikasi mobile.
 *  - Aplikasi langsung berhenti saat start jika konfigurasi belum lengkap (fail fast),
 *    lihat validasi di app.module.ts.
 *  - Pesan error tidak memuat token.
 */

import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

import { GajiHubError } from './gajihub.error';

export interface GajiHubRequestOptions {
    query?: Record<string, string | number | boolean>;
    body?: unknown;
}

/** Data user pemilik token (respons aslinya masih berisi permission & menu). */
export interface GajiHubUser {
    id: number;
    name: string;
    email: string;
}

@Injectable()
export class GajiHubService {
    private readonly apiHost: string;
    private readonly accessToken: string;

    constructor(config: ConfigService) {
        this.apiHost = config.getOrThrow<string>('GAJIHUB_API_HOST').replace(/\/+$/, '');
        this.accessToken = config.getOrThrow<string>('GAJIHUB_ACCESS_TOKEN');
    }

    /**
     * Kirim request ke API GajiHub dan kembalikan isi "data" dari respons.
     *
     * @param method    GET / POST / PUT / PATCH / DELETE
     * @param endpoint  contoh: '/hr/employees/pagination'
     */
    async request<T = any>(method: string, endpoint: string, opsi: GajiHubRequestOptions = {}): Promise<T> {
        const { query = {}, body } = opsi;

        const url = new URL(this.apiHost + endpoint);
        for (const [kunci, nilai] of Object.entries(query)) {
            url.searchParams.append(kunci, String(nilai));
        }

        const respons = await fetch(url, {
            method,
            headers: {
                Authorization: `Bearer ${this.accessToken}`,
                Accept: 'application/json',
                'X-App': 'hr',
                ...(body !== undefined && { 'Content-Type': 'application/json' }),
            },
            body: body !== undefined ? JSON.stringify(body) : undefined,
            signal: AbortSignal.timeout(30_000),
        });

        const hasil = await respons.json().catch(() => null);

        if (!respons.ok) {
            throw new GajiHubError(respons.status, hasil?.message ?? `GajiHub membalas status ${respons.status}`);
        }

        return hasil.data;
    }

    /**
     * Data user pemilik token (dipakai untuk memastikan token valid).
     */
    getCurrentUser(): Promise<GajiHubUser> {
        return this.request<GajiHubUser>('GET', '/authentication/user');
    }
}
