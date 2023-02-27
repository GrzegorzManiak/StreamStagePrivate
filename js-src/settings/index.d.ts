export type PanelType = 
    'profile' |
    'security' |
    'payment' |
    'notifications' |
    'security-verified' |
    'help' |
    'purchases' |
    'events' |
    'event-request' |
    'venues';

export interface Panel {
    element: Element;
    type: PanelType;
}

export interface Pod {
    element: Element,
    panel: Panel,
    type: PanelType
}


export interface VerifyAccessSuccess {
    data: {
        status: 'success',
        message: 'Email sent',
        access_key: string,
        resend_key: string,
        verify_key: string
    },
    code: 200,
    message: 'Email sent'
}

export interface VerifyAccessPartialSuccess {
    data: {
        status: string,
        message: string,
    },
    code: number,
    message: string
}

export interface VerifyAccessError {
    code: number,
    message: string
}

export type VerifyAccessResponse = VerifyAccessSuccess | VerifyAccessPartialSuccess | VerifyAccessError;



export interface RecentVerificationSuccess {
    data: {
        status: string,
        message: string,
    },
    code: number,
    message: string
}

export interface RecentVerificationError {
    code: number,
    message: string
}

export type RecentVerificationResponse = RecentVerificationSuccess | RecentVerificationError;



export interface Form {
    element: Element,
    type: string,
    endpoint: string,
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

export interface SecurityInfoSuccess {
    data: SecurityInfo,
    code: number,
    message: string
}

export interface SecurityInfoError {
    code: number,
    message: string
}

export type SecurityInfoResponse = SecurityInfoSuccess | SecurityInfoError;



export interface DefualtSuccess {
    data: {
        [key: string]: string | number | boolean,
        status: string,
        message: string,
    },
    code: number,
    message: string
}

export interface DefaultError {
    code: number,
    message: string
}

export type DefaultResponse = DefualtSuccess | DefaultError;