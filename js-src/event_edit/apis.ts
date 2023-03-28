import { configuration } from "./index";
import { DefaultResponse, DefaultResponseData, GetTicketListingsResponse, AddTicketListingResponse, DelTicketListingResponse, TicketListing } from "./index.d";

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

export const get_ticket_listings = async (
    event_id: string
): Promise<GetTicketListingsResponse> => base_request(
    'POST',
    configuration.get_listings,
    { event_id: event_id }
);
    
export const add_ticket_listing = async (
    event_id: string,
    ticket_type: number,
    price: number,
    detail: string,
    stock: number = 0
): Promise<AddTicketListingResponse> => base_request(
    'POST',
    configuration.add_listing,
    {
        event_id: event_id,
        ticket_type: ticket_type,
        price: price,
        detail: detail,
        stock: stock
    }
);

export const del_ticket_listing = async (
    event_id: string,
    lid: number
): Promise<DelTicketListingResponse> => base_request(
    'POST',
    configuration.del_listing,
    { event_id: event_id, listing_id: lid }
);
    