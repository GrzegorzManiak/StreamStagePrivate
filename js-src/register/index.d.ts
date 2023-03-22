//
// Response types
//
import { 
    DefaultResponse, 
    DefaultResponseData 
} from '../api/index.d';

export type Register = { 
    type: 'not_verified',
    resend_token: string,
    verify_token: string,
}

export type RegisterEmailVerified = {
    type: 'verified',
    token: string,
}

export type RegisterSuccess = DefaultResponseData & { data: Register | RegisterEmailVerified }
export type RegisterResponse = RegisterSuccess | DefaultResponse;
