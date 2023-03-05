import { DefaultResponse, DefaultResponseData } from './index.d';

export default async function (
    mehod: string,
    endpoint: string,
    csrf_token: string,
    data: any,
): Promise<DefaultResponse> {
    const response = await fetch(
        endpoint,
        {
            method: mehod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            // -- Only if method is not GET
            body: mehod.toUpperCase() !== 'GET' ? JSON.stringify(data) : undefined,
        },
    );

    try {
        const data = await response.json();

        return {
            data: data.data as any,
            code: response.status,
            message: data.message as string,
        } as DefaultResponseData;
    }
    catch (error) {
        return {
            code: response.status,
            message: 'An unknown error has occured, ' + error.message,
        };
    }
}