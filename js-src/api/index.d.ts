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

export type ResendVerification = DefaultResponseData & {
    data: { token: string, verify: string, }};
export type ResendVerificationResponse = ResendVerification | DefaultResponse;