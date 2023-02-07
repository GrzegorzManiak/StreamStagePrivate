export type PanelType = 
    'profile' |
    'security' |
    'payment' |
    'notifications' |
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