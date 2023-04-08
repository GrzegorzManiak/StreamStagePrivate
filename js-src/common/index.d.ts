import { DefaultResponse, DefaultResponseData } from '../api/index.d';
export type ToastType = 'error' | 'success' | 'warning' | 'info';

export interface Card {
    card: string,
    exp_month: number,
    exp_year: number,
    cvc: string,
    name: string
}

export interface PaymentMethod {
    brand: string;
    exp_month: number;
    exp_year: number;
    id: string;
    last4: string;
    created: number;
}

export type PaymentIntentMethod = Card | PaymentMethod;
export type FilterOrder = 'asc' | 'desc';

interface PaymentIntent {
    id: string,
    start: number,
    end: number,
    created: number,
    invoice_id: string,
    payment_intent_id: string,
    payment_intent_secret: string,
    requires_action: boolean,
    next_action?: {
        type: string,
        [key: string]: string
    }
}

export type AddCardSuccess = DefaultResponseData & { data: PaymentMethod }
export type AddCardResponse = AddCardSuccess | DefaultResponse;

export type GetCardsSuccess = DefaultResponseData & { data: Array<PaymentMethod> }
export type GetCardsResponse = GetCardsSuccess | DefaultResponse;

export type report_type = 'event' | 'review' | 'user' | 'broadcaster';

export interface Review {
    id: string,
    event: string,
    event_name: string,
    rating: number,
    body: string,
    title: string,
    created: number,
    likes: number,
    username: string,
}

export type GetReviewsSuccess = DefaultResponseData & { data: {
    reviews: Array<Review>,
    total: number,
    per_page: number,
    page: number,
    pages: number
}}
export type GetReviewsResponse = GetReviewsSuccess | DefaultResponse;