import { Event, Streamer } from './index.d';
import { add_thumbnail, carousel_scroll } from './thumbnail';

// -- #carousel
const carousel = document.querySelector('#carousel') as HTMLElement;

const streamer: Streamer = {
    id: '1',
    name: 'Test Streamer',
    pfp: 'https://via.placeholder.com/300x300'
}

const events: Array<Event> = [
    {
        id: '1',
        is_live: false,
        title: 'Test Title 1',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '2',
        is_live: true,
        title: 'Test Title 2',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '3',
        is_live: true,
        title: 'Test Title 3',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '4',
        is_live: false,
        title: 'Test Title 4',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '5',
        is_live: false,
        title: 'Test Title 5',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '6',
        is_live: true,
        title: 'Test Title 6',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '7',
        is_live: false,
        title: 'Test Title 7',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '8',
        is_live: true,
        title: 'Test Title 8',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '9',
        is_live: false,
        title: 'Test Title 9',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
    {
        id: '10',
        is_live: false,
        title: 'Test Title 0',
        views: 100,
        views_formatted: '100',
        description: 'Test Description',
        start_time: '2020-01-01',
        end_time: '2020-01-01',
        thumbnail: 'https://via.placeholder.com/300x300',
        streamer: streamer
    },
]

let random_event = undefined;

// -- Loop through events and create carousel items
// events.forEach((event: Event) => {
//     const elm = add_thumbnail(event);
//     carousel.appendChild(elm);
//     random_event = elm;
// });

carousel_scroll(
    carousel,
    events
)