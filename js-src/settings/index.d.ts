import { PaymentIntent } from "../common/index.d";

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
    'tickets' |
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



export interface Subscription {
    has_subscription: boolean,
    subscription_id: string,
    subscription_start: string,
    subscription_end: string,
    subscription_status: string,
}


export type PurchaseSorts = 'purchase_timestamp' | 'billingAddress1' | 'billingCity' | 'billingPostcode' | 'billingCountry' | 'purchase_id' | 'total_multiplier'

export interface PurchaseItem {
    item_name: string,
    price: string,
    other_data: string
}

export interface Purchase {
    purchase_id: string,
    purchase_timestamp: string,
    billingName: string,
    billingAddress1: string,
    billingCity: string,
    billingPostcode: string,
    billingCountry: string,
    total: number,
    total_multiplier: number,
    stripe_id: string,
    payment_id: string,
    items: Array<PurchaseItem>
}

export interface FilterdPurchases {
    purchases: Array<Purchase>,
    page: number,
    per_page: number,
    total: number,
    pages: number,
}

//
// Custom Responses
//

export type VerifyAccessSuccess = DefaultResponseData & { data: VerifyAccess } 
export type VerifyAccessResponse = VerifyAccessSuccess | DefaultResponse;

export type SecurityInfoSuccess = DefaultResponseData & { data: SecurityInfo }
export type SecurityInfoResponse =SecurityInfoSuccess | DefaultResponse;

export type StartSubscriptionSuccess = DefaultResponseData & { data: PaymentIntent }
export type StartSubscriptionResponse = StartSubscriptionSuccess | DefaultResponse;

export type UpdateProiflePictureSuccess = DefaultResponseData & { data: { image: string } }
export type UpdateProiflePictureResponse = UpdateProiflePictureSuccess | DefaultResponse;

export type GetSubscriptionSuccess = DefaultResponseData & { data: Subscription }
export type GetSubscriptionResponse = GetSubscriptionSuccess | DefaultResponse;

export type GetPurchasesSuccess = DefaultResponseData & { data: FilterdPurchases }
export type GetPurchasesResponse = GetPurchasesSuccess | DefaultResponse;

export interface Configuration {
    admin: boolean, 
    imposter: boolean,
    username: string, 
    userid: string,
    useremail: string, 
    userfirst: string, 
    userlast: string,
    access_level: number, 
    profile_picture: string, 
    banner_picture: string,
    csrf_token: string,
    send_verification: string, 
    resend_verification: string,
    remove_verification: string, 
    recent_verification: string,
    security_info: string, 
    update_profile: string, 
    remove_oauth: string,
    extend_session: string, 
    close_session: string, 
    change_email: string,
    setup_mfa: string, 
    disable_mfa: string,
    start_subscription: string, 
    get_reviews: string,
    update_review: string, 
    delete_review: string, 
    verify_mfa: string,
    change_img: string,
    is_subscribed: boolean,
    get_subscription: string,
    cancel_subscription: string,
    filter_purchases: string,
    get_tickets: string,
}