import { construct_modal } from "../common";

interface TicketListing {
    id: number;
    detail: string;
    price: number;
    ticket_type: number;
    stock: number;
}

interface Showing {
    event_id: string;
    showing_id: string;
    country: string;
    city: string;
    venue: string;
    time: string;
}

interface Media {
    media_id: string;
    description: string;
    picture: string;
}

// api stuff (credits to Greg)
export interface DefaultResponseNoData {
    code: number,
    message: string
}

export interface DefaultResponseData {
    data: { 
        message: string
        status: string
    }
    code: number,
    message: string
}

export type DefaultResponse = DefaultResponseNoData;


// Ticket Section

export type GetTicketListingsSuccess = DefaultResponseData & { data: { listings: Array<TicketListing> } }
export type GetTicketListingsResponse = GetTicketListingsSuccess | DefaultResponse;

export type AddTicketListingSuccess = DefaultResponseData & { data: { listing: TicketListing } }
export type AddTicketListingResponse = AddTicketListingSuccess | DefaultResponse;


export type GetShowingsSuccess = DefaultResponseData & { data: { showings: Array<Showing> } }
export type GetShowingsResponse = GetShowingsSuccess | DefaultResponse;

export type AddShowingSuccess = DefaultResponseData & { data: { showing: Showing } }
export type AddShowingResponse = AddShowingSuccess | DefaultResponse;

export type GetMediaSuccess = DefaultResponseData & { data: { media: Array<Media> } }
export type GetMediaResponse = GetMediaSuccess | DefaultResponse;

export type AddMediaSuccess = DefaultResponseData & { data: { media: Media } }
export type AddMediaResponse = AddMediaSuccess | DefaultResponse;

// Showing Section
