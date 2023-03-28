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

export interface Configuration {
    admin: boolean, 
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
}