import { GetBroadcasterEventsResponse, DefaultResponseData, DefaultResponse } from "./index.d";
import { configuration } from "./index"

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


/**
 * 
 * @name get_reviews
 * @param filter - Filter
 * @param sort - Sort
 * @param page - Page
 * @param username - Username
 */
export const get_events = async (
    sort: 'rating',
    order: 'asc' | 'desc',
    page: number,
    broadcaster_id: string
): Promise<GetBroadcasterEventsResponse> => base_request(
    'POST',
    configuration.get_events,
    { sort, order, page, broadcaster_id }
);
    