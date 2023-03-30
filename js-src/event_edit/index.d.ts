import { construct_modal } from "../common";

interface TicketListing {
    id: number;
    detail: string;
    price: number;
    ticket_type: number;
    stock: number;
}

interface Showing {
    showing_id: string;
    event_id: string;
    country: string;
    city: string;
    venue: string;
    time: string;
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

export type GetTicketListingsSuccess = DefaultResponseData & { data: {
    listings: Array<TicketListing>
}}

export type GetTicketListingsResponse = GetTicketListingsSuccess | DefaultResponse;


export type AddTicketListingSuccess = DefaultResponseData & { data: {
    listing: TicketListing
}}

export type AddTicketListingResponse = AddTicketListingSuccess | DefaultResponse;

// Showing Section
