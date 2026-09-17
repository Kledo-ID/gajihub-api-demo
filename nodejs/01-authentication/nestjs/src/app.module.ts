import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

import { GajiHubController } from './gajihub/gajihub.controller';
import { GajiHubModule } from './gajihub/gajihub.module';

@Module({
    imports: [
        ConfigModule.forRoot({
            isGlobal: true,
            envFilePath: '.env',
            // Fail fast: aplikasi menolak start jika konfigurasi belum lengkap
            validate: (env) => {
                for (const kunci of ['GAJIHUB_API_HOST', 'GAJIHUB_ACCESS_TOKEN']) {
                    if (!env[kunci]) {
                        throw new Error(`${kunci} wajib diisi di file .env`);
                    }
                }
                return env;
            },
        }),
        GajiHubModule,
    ],
    controllers: [GajiHubController],
})
export class AppModule {}
