/**
 * Contoh aplikasi NestJS yang memakai API GajiHub dengan aman.
 *
 * Jalankan:  npm install  lalu  npm start
 * Coba:      http://localhost:3000/gajihub/me
 */

import { NestFactory } from '@nestjs/core';

import { AppModule } from './app.module';

async function bootstrap() {
    const app = await NestFactory.create(AppModule);

    const port = process.env.PORT ?? 3000;
    await app.listen(port);
    console.log(`Server berjalan di http://localhost:${port}`);
}

bootstrap();
