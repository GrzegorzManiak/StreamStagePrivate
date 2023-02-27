import { configuration } from "..";
import { DefaultResponse, DefaultResponseData } from "../index.d";

export default async (
    mehod: string,
    endpoint: string,
    data: any,
): Promise<DefaultResponse> => {
    const response = await fetch(
        endpoint,
        {
            method: mehod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
            },
            body: JSON.stringify(data),
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