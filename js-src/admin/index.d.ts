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
    'faq' |
    'terms' |
    'privacy' |
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

    broadcaster: string,
    get_broadcaster: string,
    update_broadcaster: string,
    delete_broadcaster: string,

    event: string,
    get_event: string,
    create_event: string,
    delete_event: string,
    update_event: string,

    latest_privacy: string,
    create_privacy: string,
    filter_privacy: string,
    render_privacy: string,

    latest_terms: string,
    create_terms: string,
    filter_terms: string,
    render_terms: string,

    faq_create: string,
    faq_delete: string,
    faq_update: string,
    faq_filter: string,

    filter_reports: string,
    update_report: string,
}


export type FilterPosition = 'all' | 'user' | 'admin' | 'streamer';
export type FilterSort = 'updated' | 'created' | 'username' | 'email' | 'position' | 'country';

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


export type BroadcasterSorts = 'updated' | 'created' | 'handle' | 'over_18' | 'approved';
export interface Broadcaster {
    id: string,
    handle: string,
    over_18: boolean,
    approved: boolean,
    created: string,
    updated: string,
    name: string,
    profile_picture: string,
    profile_banner: string,
    streamer: string,
    biography: string,
}

export interface FilterdBroadcaster {
    broadcasters: Array<Broadcaster>,
    page: number,
    per_page: number,
    total: number,
    pages: number,
}


export type EventSorts = 'updated' | 'created' | 'title' | 'description' | 'over_18' | 'categories' | 'approved';
export interface Event {
    id: string,
    title: string,
    description: string,
    over_18: boolean,
    categories: Array<{
        id: string,
        name: string,
    }>,
    broadcaster: {
        id: string,
        handle: string,
    },
    created: string,
    updated: string,
    contributors: Array<{
        id: string,
        handle: string,
    }>,
    approved: boolean,
    showings: Array<{
        id: string,
    }>,
}

export interface FilterdEvent {
    events: Array<Event>,
    page: number,
    per_page: number,
    total: number,
    pages: number,
}


export type TermsPrivacySorts = 'updated' | 'created' | 'name' | 'content';
export type Filterd = {
    page: number,
    per_page: number,
    total: number,
    pages: number,
}

export interface Terms {
    id: string,
    name: string,
    content: string,
    created: string,
}

export interface Privacy {
    id: string,
    name: string,
    content: string,
    created: string,
}

export type FaqSorts = 'updated' | 'created' | 'question' | 'answer' | 'section';
export interface Faq {
    id: string,
    question: string,
    answer: string,
    section: string,
    created: string,
    updated: string,
}


export interface Ticket {
    ticket_id: string,
    purchase_id: string,
    listing: {
        id: string,
        details: string,
        price: number,
        stock: number,
        ticket_type: string,
    },
    purchase_date: string,
    streaming_ticket: boolean,  
    event: {
        url: string,
        broadcaster_name: string,
        title: string,
        event_id: string,
        splash: string,
    }
}

export interface FilterdReports {
    reports:  Report[];
    page: number;
    per_page: number;
    total: number;
    pages: number;
}

export interface Report {
    id: string;
    reporter: Reporter;
    reason: string;
    time: string;
    date: Date;
    reported: Reported;
    solved: boolean;
    reported_fields: ReportedFields;
    solved_by: null;
    created: string;
    updated: string;
}

export interface Reported {
    user: Reporter;
}

export interface Reporter {
    id: string;
    username: string;
    profile_pic: string;
    url: string;
}

export interface ReportedFields {
    user: boolean;
}

export type ReportSorts = 'id' | 'reason' | 'question' | 'time' | 'date' | 'solved'



export type FilterdFaqs = Filterd & { faq: Array<Faq> }
export type FilterdTerms = Filterd & { terms: Array<Terms> }
export type FilterdPrivacy = Filterd & { privacy: Array<Privacy> }

export type FilterdUsersSuccess = DefaultResponseData & { data: FilterdUsers }
export type FilterdUsersResponse = FilterdUsersSuccess | DefaultResponse;

export type UserSuccess = DefaultResponseData & { data: FilterdUser }
export type UserResponse = UserSuccess | DefaultResponse;

export type FilterdCategoriesSuccess = DefaultResponseData & { data: FilterdCategory }
export type FilterdCategoriesResponse = FilterdCategoriesSuccess | DefaultResponse;

export type CategorySuccess = DefaultResponseData & { data: Category }
export type CategoryResponse = CategorySuccess | DefaultResponse;

export type FilterdBroadcastersSuccess = DefaultResponseData & { data: FilterdBroadcaster }
export type FilterdBroadcastersResponse = FilterdBroadcastersSuccess | DefaultResponse;

export type BroadcasterSuccess = DefaultResponseData & { data: Broadcaster }
export type BroadcasterResponse = BroadcasterSuccess | DefaultResponse;

export type FilterdEventsSuccess = DefaultResponseData & { data: FilterdEvent }
export type FilterdEventsResponse = FilterdEventsSuccess | DefaultResponse;

export type FilterdTermsSuccess = DefaultResponseData & { data: FilterdTerms }
export type FilterdTermsResponse = FilterdTermsSuccess | DefaultResponse;

export type FilterdPrivacySuccess = DefaultResponseData & { data: FilterdPrivacy }
export type FilterdPrivacyResponse = FilterdPrivacySuccess | DefaultResponse;

export type TermsSuccess = DefaultResponseData & { data: Terms }
export type TermsResponse = TermsSuccess | DefaultResponse;

export type PrivacySuccess = DefaultResponseData & { data: Privacy }
export type PrivacyResponse = PrivacySuccess | DefaultResponse;

export type FilterdFaqsSuccess = DefaultResponseData & { data: FilterdFaqs }
export type FilterdFaqsResponse = FilterdFaqsSuccess | DefaultResponse;

export type GetFilteredReportsSuccess = DefaultResponseData & { data: FilterdReports }
export type GetFilteredReportsResponse = GetFilteredReportsSuccess | DefaultResponse;
