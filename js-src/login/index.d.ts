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
