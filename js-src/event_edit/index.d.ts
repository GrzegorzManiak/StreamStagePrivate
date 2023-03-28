
import { construct_modal } from "../common";

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

export type GetTicketListingsSuccess = DefaultResponseData & { data: {
    listings: Array<TicketListing>
}}

export type GetTicketListingsResponse = GetTicketListingsSuccess | DefaultResponse;


export type AddTicketListingSuccess = DefaultResponseData & { data: {
    listing: TicketListing
}}

export type AddTicketListingResponse = AddTicketListingSuccess | DefaultResponse;


export type DelTicketListingSuccess = DefaultResponseData & { data: { }}

export type DelTicketListingResponse = DelTicketListingSuccess | DefaultResponse;

interface TicketListing {
    id: number;
    detail: string;
    price: number;
    ticket_type: number;
    stock: number;
}
