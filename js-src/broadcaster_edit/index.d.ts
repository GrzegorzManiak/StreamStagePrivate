export type PanelType = 
    'my_broadcasters' |
    'applications' |
    'invitations';

export interface Panel {
    element: Element;
    type: PanelType;
}

export interface Pod {
    element: Element,
    panel: Panel,
    type: PanelType
}

export interface Contributor {
    username: string,
    url: string,
    profile: string
}

export interface BroadcasterDetails {
    id: string,
    handle: string,
    name: string,
    biography: string,
    profile: string,
    approved: boolean,
    banner: string,
    url: string,
    contributors: Contributor[]

    profile_updated: boolean,
    banner_updated: boolean
}

export interface Config {
    csrf_token:string,

    get_broadcaster_details: string,
    update_broadcaster_details: string,
    broadcaster_ids: string,

    fetch_invites: string,
    send_invite: string,
    remove_contributor: string,
    respond_invite: string
}

export interface Invite {
    id: string
    inviter: string
    broadcaster: string
    bc_profile: string
    bc_url: string
    message: string
}

export interface InviteResponse {
    id: string
    response: "y" | "n"
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

export type GetInvitationsSuccess = DefaultResponseData & { data: { invites: Invite[] } }
export type GetInvitationsResponse = GetInvitationsSuccess | DefaultResponse;

export type RespondToInviteResponse = DefaultResponseData | DefaultResponse;

export type SendInvitationResponse = DefaultResponseData | DefaultResponse

export type RemoveContributorResponse = DefaultResponseData | DefaultResponse;