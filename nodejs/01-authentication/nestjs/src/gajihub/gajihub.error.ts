/**
 * Error saat GajiHub membalas status selain 2xx.
 */
export class GajiHubError extends Error {
    constructor(
        readonly status: number,
        message: string,
    ) {
        super(message);
        this.name = 'GajiHubError';
    }
}
