import { sleep } from '../common';
import { single } from '../common/single';
import { attach_to_showcases } from './featured';
import { Event, Streamer } from './index.d';
import { create_carousel } from './thumbnail';

single('homepage');

// -- Get all the elements with the 'car' class
const carousels = document.querySelectorAll('.car') as NodeListOf<HTMLElement>,
    showcase = document.querySelector('.showcase-main') as HTMLElement;

// -- Loop through all the carousels
carousels.forEach((carousel) => {
    // -- Get the attributes
    const id = carousel.getAttribute('data-category-id'),
        name = carousel.getAttribute('data-category'),
        search_url = carousel.getAttribute('data-search-url');

    // -- Get the events from within the carousel
    const events_elms = carousel.querySelectorAll('span') as NodeListOf<HTMLElement>;
    let events: Array<Event> = [];
    
    // -- Loop through the events
    events_elms.forEach((event_elm) => {

        // -- id
        const id = event_elm.getAttribute('data-id'),
            is_live = event_elm.getAttribute('data-is-live') === 'true',
            title = event_elm.getAttribute('data-title'),
            description = event_elm.getAttribute('data-description'),
            thumbnail = event_elm.getAttribute('data-thumbnail'),
            streamer_id = event_elm.getAttribute('data-streamer-id'),
            streamer_name = event_elm.getAttribute('data-streamer-name'),
            streamer_pfp = event_elm.getAttribute('data-streamer-pfp'),
            start_time = event_elm.getAttribute('data-earliest-date'),
            full_url = event_elm.getAttribute('data-full-url');

        // -- Create the event
        const event: Event = {
            id: id,
            is_live: is_live,
            title: title,
            views: 0,
            views_formatted: '',
            description: description,
            start_time: start_time,
            end_time: '2020-01-01',
            thumbnail: thumbnail,
            full_url: full_url,
            streamer: {
                id: streamer_id,
                name: streamer_name,
                pfp: streamer_pfp,
            }
        };

        // -- Add the event to the array
        events.push(event);
    });

    if (events.length === 0) return;
    create_carousel(carousel, events, name, search_url);
});

//
// -- Grab the logo SVG 
//
const logo = document.querySelector('#logo-loader') as SVGGeometryElement;

function set_splash_state(
    state: 'loading' | 'finising' | 'finished'
) {
    switch (state) {
        case 'loading': 
            logo.setAttribute('state', 'loading'); 
            document.body.setAttribute('state', 'zoomed-out');
            break;
        case 'finising': logo.setAttribute('state', 'finising'); break;
        case 'finished': 
            logo.setAttribute('state', 'finished'); 
            document.body.setAttribute('state', 'zoomed-in');
            break;
    }
}

// -- Start the splash animation
const load = () => {
    let loaded = false;
    set_splash_state('loading');
    sleep(3000).then(() => {
        if (loaded) return;
        set_splash_state('finising');
        sleep(1500).then(() => { 
            if (loaded) return;
            loaded = true;
            set_splash_state('finished'); 
        });
    });

    window.addEventListener('load', async() => {
        if (loaded) return;
        set_splash_state('finising');
        sleep(1000).then(() => {
            if (loaded) return;
            loaded = true;
            set_splash_state('finished'); 
        });
    });

    attach_to_showcases();
}