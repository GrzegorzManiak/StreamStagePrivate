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
    login_history: Array<LoginHistory>
}

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

export type SubscriptionMethod = Card | PaymentMethod;

interface SubscriptionIntent {
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

export type AddCardSuccess = DefaultResponseData & { data: PaymentMethod }
export type AddCardResponse = AddCardSuccess | DefaultResponse;

export type GetCardsSuccess = DefaultResponseData & { data: Array<PaymentMethod> }
export type GetCardsResponse = GetCardsSuccess | DefaultResponse;

export type StartSubscriptionSuccess = DefaultResponseData & { data: SubscriptionIntent }
export type StartSubscriptionResponse = StartSubscriptionSuccess | DefaultResponse;