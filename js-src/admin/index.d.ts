import { DefaultResponseData, DefaultResponse } from '../api/index.d';

export type PanelType = 
    'accounts' |
    'server' |
    'cash_flow' |
    'tickets' |
    'reviews' |
    'subscriptions' |
    'statistics' |
    'viewers' |
    'reports' |
    'users' |
    'streamers' |
    'broadcasters' |
    'venues' |
    'categories' |
    'events' |
    'reviews';

export interface Panel {
    element: Element;
    type: PanelType;
}

export interface Pod {
    element: Element,
    panel: Panel,
    type: PanelType
}


export type Frame = 'seconds' | 'minute' | 'hour' | 'day' | 'week' | 'month' | 'year';
export interface Statistics {
    data: number[],
    labels: string[],
}

export type StatisticsSuccess = DefaultResponseData & { data: Statistics }
export type StatisticsResponse = StatisticsSuccess | DefaultResponse;


export interface Configuration {
    statistics: string,
    users: string,
}


export type FilterPosition = 'all' | 'user' | 'admin' | 'streamer';
export type FilterSort = 'updated' | 'created' | 'username' | 'email' | 'position' | 'country';
export type FilterOrder = 'asc' | 'desc';

export interface FilterdUser {
    username: string,
    cased_username: string,
    email: string,
    streamer: boolean,
    over_18: boolean,
    is_staff: boolean,
    profile_picture: string,
    profile_banner: string,
    updated: string,
    created: string,
    first_name: string,
    last_name: string,
    description: string,
    id: string,
}

export interface FilterdUsers {
    users: Array<FilterdUser>,
    page: number,
    per_page: number,
    total: number,
    pages: number,
}

export type FilterdUsersSuccess = DefaultResponseData & { data: FilterdUsers }
export type FilterdUsersResponse = FilterdUsersSuccess | DefaultResponse;