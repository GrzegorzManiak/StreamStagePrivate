import { configuration } from "./index";
import { DefaultResponse, DefaultResponseData, GetTicketListingsResponse, AddTicketListingResponse, GetShowingsResponse, AddShowingResponse, Showing, TicketListing, GetMediaResponse, AddMediaResponse } from "./index.d";

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
                "ss-CSRF-token": configuration.csrf_token,
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
    stock: number = 0,
    showing_id: string = null
): Promise<AddTicketListingResponse> => base_request(
    'POST',
    configuration.add_listing,
    {
        event_id: event_id,
        ticket_type: ticket_type,
        price: price,
        detail: detail,
        stock: stock,
        showing_id: showing_id
    }
);

export const del_ticket_listing = async (
    event_id: string,
    lid: number
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.del_listing,
    { event_id: event_id, listing_id: lid }
);


export const get_evt_showings = async (
    event_id: string
): Promise<GetShowingsResponse> => base_request(
    'POST',
    configuration.get_showings,
    { event_id: event_id }
);
    
export const add_evt_showing = async (
    event_id: string,
    country: string,
    city: string,
    venue: string,
    time: string
): Promise<AddShowingResponse> => base_request(
    'POST',
    configuration.add_showing,
    {
        event_id: event_id,
        country: country,
        city: city,
        venue: venue,
        time: time
    }
);

export const del_evt_showing = async (
    event_id: string,
    sid: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.del_showing,
    { event_id: event_id, showing_id: sid }
);



export const get_evt_media = async (
    event_id: string
): Promise<GetMediaResponse> => base_request(
    'POST',
    configuration.get_media,
    { event_id: event_id }
);

export const add_evt_media = async (
    event_id: string,
    picture: string,
    description: string
): Promise<AddMediaResponse> => base_request(
    'POST',
    configuration.add_media,
    {
        event_id: event_id,
        picture: picture,
        description: description
    }
);

export const del_evt_media = async (
    event_id: string,
    media_id: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.del_media,
    { event_id: event_id, media_id: media_id }
);
