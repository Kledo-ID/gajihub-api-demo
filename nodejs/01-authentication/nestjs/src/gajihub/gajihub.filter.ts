/**
 * Mengubah GajiHubError menjadi respons 502 yang aman untuk pemanggil.
 */

import { ArgumentsHost, Catch, ExceptionFilter, Logger } from '@nestjs/common';
import { Response } from 'express';

import { GajiHubError } from './gajihub.error';

@Catch(GajiHubError)
export class GajiHubExceptionFilter implements ExceptionFilter<GajiHubError> {
    private readonly logger = new Logger('GajiHub');

    catch(error: GajiHubError, host: ArgumentsHost) {
        // 401/403 dari GajiHub = token di server salah/kedaluwarsa, bukan kesalahan pemanggil.
        // Catat detailnya di log server, balas pesan umum ke pemanggil.
        this.logger.error(`status ${error.status}: ${error.message}`);

        host.switchToHttp()
            .getResponse<Response>()
            .status(502)
            .json({ message: 'Gagal mengambil data dari GajiHub.' });
    }
}
