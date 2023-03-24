import { PaymentMethod, PaymentIntent } from "../common/index.d";

export type PanelType = 
    'profile' |
    'security' |
    'streamstageplus' |
    'payment' |
    'notifications' |
    'security-verified' |
    'help' |
    'purchases' |
    'events' |
    'reviews' |
    'event-request' |
    'venues' |
    'security-preferences' |
    'security-mfa' |
    'security-linked-accounts' |
    'security-password' |
    'security-email' |
    'security-history' |
    'security-delete';

export interface Panel {
    element: Element;
    type: PanelType;
}

export interface Pod {
    element: Element,
    panel: Panel,
    type: PanelType
}




//
// Success scenarios
//

export type VerifyAccess = {
    access_key: string,
    resend_key: string,
    verify_key: string
}

export interface ServiceProvider {
    id: string,
    oauth_type: string,
    oauth_id: string,
    last_used: string,
    added: string,
}

export interface LoginHistory {
    id: string,
    ip: string,
    time: string,
    date: string,
    method: string,
}

export interface SecurityPreferences {
    [key: string]: {
        value: boolean,
        help_text: string,
        name: string
    }
}

export interface SecurityInfo {
    email: string,
    dob: string,
    tfa: boolean,
    access_level: number,
    max_keys: number,
    is_streamer: boolean,
    is_broadcaster: boolean,
    is_admin: boolean,
    over_18: boolean,
    service_providers: Array<ServiceProvider>,
    login_history: Array<LoginHistory>,
    security_preferences: SecurityPreferences
}


export interface Review {
    id: string,
    event: string,
    event_name: string,
    rating: number,
    body: string,
    title: string,
    created: number,
    likes: number,
}
  
// 
// Default Server response structure
// 
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


export type DefaultResponse = DefaultResponseNoData | DefaultResponseNoData;



//
// Custom Responses
//

export type VerifyAccessSuccess = DefaultResponseData & { data: VerifyAccess } 
export type VerifyAccessResponse = VerifyAccessSuccess | DefaultResponse;

export type SecurityInfoSuccess = DefaultResponseData & { data: SecurityInfo }
export type SecurityInfoResponse =SecurityInfoSuccess | DefaultResponse;

export type StartSubscriptionSuccess = DefaultResponseData & { data: PaymentIntent }
export type StartSubscriptionResponse = StartSubscriptionSuccess | DefaultResponse;

export type GetReviewsSuccess = DefaultResponseData & { data: {
    reviews: Array<Review>,
    total: number,
    per_page: number,
    page: number,
    pages: number
}}
export type GetReviewsResponse = GetReviewsSuccess | DefaultResponse;