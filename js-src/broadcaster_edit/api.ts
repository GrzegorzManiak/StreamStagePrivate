import { configuration } from "./index";
import { DefaultResponse, DefaultResponseData, GetBroadcasterDetailsResponse, UpdateBroadcasterDetailsResponse } from "./index.d";

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

export const get_broadcaster_details = async (
    broadcaster_id: string
): Promise<GetBroadcasterDetailsResponse> => base_request(
    'POST',
    configuration.get_broadcaster_details,
    { id: broadcaster_id }
);
    
export const update_broadcaster_details = async (
    broadcaster_id: string,
    name: string,
    biography: string,
    profile: string = "",
    banner: string = ""
): Promise<UpdateBroadcasterDetailsResponse> => base_request(
    'POST',
    configuration.update_broadcaster_details,
    {
        id: broadcaster_id,
        name: name,
        biography: biography,
        profile: profile,
        banner: banner
    }
);