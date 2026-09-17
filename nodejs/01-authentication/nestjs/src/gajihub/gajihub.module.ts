import { Module } from '@nestjs/common';

import { GajiHubService } from './gajihub.service';

@Module({
    providers: [GajiHubService],
    exports: [GajiHubService],
})
export class GajiHubModule {}
