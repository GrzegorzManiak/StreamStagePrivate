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


export type Frame = 'minute' | 'hour' | 'day' | 'week' | 'month' | 'year';
export interface Statistics {
    data: number[],
    labels: string[],
}

export type StatisticsSuccess = DefaultResponseData & { data: Statistics }
export type StatisticsResponse = StatisticsSuccess | DefaultResponse;


export interface Configuration {
    statistics: string
}