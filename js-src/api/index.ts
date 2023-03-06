import { DefaultResponse, DefaultResponseData } from './index.d';

export default async function (
    method: string,
    endpoint: string,
    csrf_token: string | null = null,
    data: { [key: string]: any; } = {},
    headers: { [key: string]: string; } = {},
): Promise<DefaultResponse> {
    // -- Create the request
    const request = new XMLHttpRequest();

    // -- Open the request
    request.open(method.toUpperCase(), endpoint, true);

    // -- Add the headers
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    if (csrf_token) request.setRequestHeader('X-CSRFToken', csrf_token);
    for (const key in headers) request.setRequestHeader(key, headers[key]);

    // -- Handle the response
    return new Promise((resolve, reject) => {
        request.onload = () => {
            try {
                const data = JSON.parse(request.responseText);
                resolve({
                    data: data.data as any,
                    code: request.status,
                    message: data.message as string,
                } as DefaultResponse);
            } 
            
            // -- Handle the error
            catch (error) { reject({
                code: request.status, 
                message: 'An unknown error has occurred, ' + error.message 
            })}
        };

        // -- Handle the error
        request.onerror = () => reject({
            code: request.status,
            message: 'An error has occurred, ' + request.statusText,
        });

        // -- Send the request
        request.send(method.toUpperCase() !== 'GET' ? JSON.stringify(data) : null);
    });
}
