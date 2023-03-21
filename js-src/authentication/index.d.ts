import { DefaultResponseData, DefaultResponse } from '../api/index.d'


type CSRF_Token = string;
type OAUTH_Error = string;


export interface Instructions {
    has_account: boolean;
    email_verified: boolean;
    oauth_type: 0;
    can_authenticate: boolean;
    needs_password: boolean;
    needs_username: boolean;
    needs_email: boolean;
}

export interface GoogleUser {
    id: string;
    email: string;
    verified_email: boolean;
    name: string;
    given_name: string;
    picture: string;
}

export type User = GoogleUser;
export type Token = string;
export type Message = string;    

export interface Response {
    user: User;
    token: Token;
    message: Message;
    instructions: Instructions;
}

export interface ParsedHeaders {
    csrf_token: CSRF_Token;
    oauth_error: OAUTH_Error | null;
}


export type PanelType = 'defualt' | 'tfa' | 'oauth' | 'register' | 'email-wait';
export type PageType = 'login' | 'register';

export interface Panel {
    type: PanelType;
    element: HTMLDivElement;
}



//
// Response types
//
export type LoginTOTP = { mode: 'totp' }
export type LoginMFA = { 
    mode: 'mfa',
    resend: string,
    verify: string,
    token: string
}
export type LoginNone = { 
    mode: 'none',
    token: string
}

export type LoginSuccess = DefaultResponseData & { 
    data: LoginTOTP | LoginMFA | LoginNone }
export type LoginResponse = LoginSuccess | DefaultResponse;
