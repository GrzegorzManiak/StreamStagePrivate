import { Review } from "../common/index.d"

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

export interface Event {
    event_id: string,
    rating: number,
    categories: string[],
    cover_pic: string,
    url: string,
    description: string,
    title: string,
    reviews: Review[]
}

export type GetBroadcasterEventsSuccess = DefaultResponseData & { data: {
    events: Event[],
    total: number,
    per_page: number,
    page: number,
    pages: number
}}
export type GetBroadcasterEventsResponse = GetBroadcasterEventsSuccess | DefaultResponse;