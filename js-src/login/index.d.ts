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


//
// Response types
//
import { 
    DefaultResponse, 
    DefaultResponseData 
} from '../api/index.d';


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
