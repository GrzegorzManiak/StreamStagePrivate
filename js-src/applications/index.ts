import { DefaultResponse, DefaultResponseData } from "./index.d";
import { create_toast } from "../common";
import { Type, build_configuration } from "../api/config";

// -- Get the global configuration
export const configuration = build_configuration<{
    csrf_token: string,
}>({
    csrf_token: new Type('data-csrf-token', 'string'),
});

export const get_applications = async (
): Promise<DefaultResponse> => base_request(
    'POST',
    "api/get_applications",
);

get();

async function get() {
    const response = await get_applications();

    // -- Check if the request was successful
    if (response.code !== 200)
        return create_toast(
            'error', 'Oops!',
            'There was an error while trying to get ticket listings, please try again later.'
        )

    const data = (response as DefaultResponseData).data
    
    console.log(data);
}


export async function base_request (
    mehod: string,
    endpoint: string,
    data: any = {},
    headers: any = {},
): Promise<DefaultResponse> {
    const response = await fetch(
        endpoint,
        {
            method: mehod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
                ...headers,
            },
            body: mehod === 'GET' ? undefined : JSON.stringify(data),
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