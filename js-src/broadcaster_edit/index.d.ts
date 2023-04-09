
export interface BroadcasterDetails {
    id: string,
    handle: string,
    name: string,
    biography: string,
    profile: string,
    banner: string,

    profile_updated: boolean,
    banner_updated: boolean
}

export interface Config {
    csrf_token:string,

    get_broadcaster_details: string,
    update_broadcaster_details: string,
    broadcaster_ids: string
}


// api stuff (credits to Greg)
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

export type DefaultResponse = DefaultResponseNoData;


// Ticket Section

export type GetBroadcasterDetailsSuccess = DefaultResponseData & { data: { details: BroadcasterDetails } }
export type GetBroadcasterDetailsResponse = GetBroadcasterDetailsSuccess | DefaultResponse;

export type UpdateBroadcasterDetailsSuccess = DefaultResponseData & { data: { details: BroadcasterDetails } }
export type UpdateBroadcasterDetailsResponse = UpdateBroadcasterDetailsSuccess | DefaultResponse;
