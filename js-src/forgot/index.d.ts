import { 
    DefaultResponse, 
    DefaultResponseData 
} from '../api/index.d';

export type ResetInit = {
    verify_token: string,
    access_token: string,
    resend_token: string
}

export type ResetInitSuccess = DefaultResponseData & { data: ResetInit }
export type ResetInitResponse = ResetInitSuccess | DefaultResponse;
