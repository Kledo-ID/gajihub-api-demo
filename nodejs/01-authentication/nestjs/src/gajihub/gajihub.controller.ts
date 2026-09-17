import { Controller, Get, UseFilters } from '@nestjs/common';

import { GajiHubExceptionFilter } from './gajihub.filter';
import { GajiHubService } from './gajihub.service';

@Controller('gajihub')
@UseFilters(GajiHubExceptionFilter)
export class GajiHubController {
    constructor(private readonly gajihub: GajiHubService) {}

    /** Cek koneksi & token GajiHub: siapa pemilik token yang dipakai server ini? */
    @Get('me')
    async me() {
        const user = await this.gajihub.getCurrentUser();

        // Kirim hanya data yang dibutuhkan (respons asli juga berisi permission & menu)
        return { id: user.id, name: user.name, email: user.email };
    }
}
