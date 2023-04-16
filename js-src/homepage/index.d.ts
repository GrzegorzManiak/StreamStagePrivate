export interface Streamer {
    id: string;
    name: string;
    pfp: string;
}

export interface Event {
    id: string;
    is_live: boolean;
    title: string;
    views: number;
    views_formatted: string;
    description: string;
    full_url: string;
    start_time: string;
    end_time: string;
    thumbnail: string;
    streamer: Streamer;
}