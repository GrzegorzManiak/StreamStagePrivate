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
    get_user: string,
    delete_user: string,
    update_email: string,
    update_streamer_status: string,

    category: string,
    get_category: string,
    create_category: string,
    delete_category: string,
    update_category: string,
    set_category_image: string,
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


export type CategorySorts = 'updated' | 'created' | 'name' | 'description' | 'color';


export interface Category {
    id: string,
    name: string,
    description: string,
    created: string,
    updated: string,
    image: string,
    color: string,
}

export interface FilterdCategory {
    categorys: Array<Category>,
    page: number,
    per_page: number,
    total: number,
    pages: number,
}

export type FilterdUsersSuccess = DefaultResponseData & { data: FilterdUsers }
export type FilterdUsersResponse = FilterdUsersSuccess | DefaultResponse;

export type UserSuccess = DefaultResponseData & { data: FilterdUser }
export type UserResponse = UserSuccess | DefaultResponse;

export type FilterdCategoriesSuccess = DefaultResponseData & { data: FilterdCategory }
export type FilterdCategoriesResponse = FilterdCategoriesSuccess | DefaultResponse;

export type CategorySuccess = DefaultResponseData & { data: Category }
export type CategoryResponse = CategorySuccess | DefaultResponse;