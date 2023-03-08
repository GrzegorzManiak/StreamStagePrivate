import { Event } from './index.d';

/*
    This file handles getting the thumbnail template so we can
    copy it and add it multiple times to the page.
*/

const tn = document.getElementById('thumbnail');
tn.id = '';


/*
    @name add_thumbnail
    @param {Event} event
    @returns {HTMLElement}
*/
export function add_thumbnail(event: Event) {
    // -- Clone TN
    const tn_clone = tn.cloneNode(true) as HTMLElement;
    tn_clone.id = 'thumbnail-' + event.id;

    // -- Is the event live [data-is-live='']
    //    Is the event hidden [data-is-hidden='']
    //    Is the event a skeleton [data-is-skeleton=''] (used for loading)
    tn_clone.setAttribute('data-is-live', event.is_live.toString());
    tn_clone.setAttribute('data-is-hidden', 'false');
    tn_clone.setAttribute('data-is-skeleton', 'false');

    // -- Set the thumbnail image, [data-elm='main-image']
    const tn_img = tn_clone.querySelector('[data-elm="main-image"]') as HTMLImageElement;
    // tn_img.src = event.thumbnail;

    // -- Set the streamer pfp, [data-elm='pfp']
    const tn_pfp = tn_clone.querySelector('[data-elm="pfp"]') as HTMLImageElement;
    // tn_pfp.src = event.streamer.pfp;


    // -- Sreamtitle, [data-elm='title'], [data-elm='view-count'], [data-elm='date-vod']
    const tn_title = tn_clone.querySelector('[data-elm="title"]') as HTMLHeadingElement;
    const tn_view_count = tn_clone.querySelector('[data-elm="view-count"]') as HTMLSpanElement;
    const tn_date_vod = tn_clone.querySelector('[data-elm="date-vod"]') as HTMLSpanElement;

    tn_title.innerText = event.title;
    tn_view_count.innerText = event.views_formatted;
    tn_date_vod.innerText = event.start_time;
    

    // -- Return the cloned thumbnail
    return tn_clone;
}


export function fill_carousel(
    carousel: HTMLElement,
    events: Array<Event>,
): {
    content: Array<Array<Event>>,
    groups: Array<HTMLElement>
} {
// -- Max ammount of thumbnails 
    //    to show on one carousel row
    const MAX_ELMS = 6;
    // -- How many thumbnails to show
    //    per carousel group
    const GROUPS = 3;

    let content: Array<Array<Event>> = [];

    // -- Fill out the group with thumbnails
    //    and repeat some thumbnails if we
    //    don't have enough thumbnails to
    //    by just randomly picking a thumbnail
    //    from the events array
    // -- Fill the group
    for (let i = 0; i < GROUPS; i++) {
        let group: Array<Event> = [];

        for (let i = 0; i < MAX_ELMS; i++) {
            let event = events[Math.floor(Math.random() * events.length)];
            group.push(event);
        }
        
        content.push(group);
    }

    // -- Check for half filled groups
    //    and fill them up with random thumbnails
    for (const element of content) {
        if (element.length < GROUPS) {
            let diff = GROUPS - element.length;

            for (let i = 0; i < diff; i++) {
                let event = events[Math.floor(Math.random() * events.length)];
                content[i].push(event);
            }
        }
    }


    // -- Add the thumbnails to the carousel
    let groups: Array<HTMLElement> = [];

    for (const element of content) {
        let group = document.createElement('div');
        group.classList.add('carousel-group');

        for (const event of element) {
            let tn = add_thumbnail(event);
            group.appendChild(tn);
        }

        groups.push(group);
    }


    // -- Add the groups to the carousel
    for (const element of groups) {
        carousel.appendChild(element);
    }

    return {
        content,
        groups
    };
}


export function carousel_scroll(
    carousel: HTMLElement,
    events: Array<Event>,
) {
    // -- Fill the carousel with thumbnails
    let { content, groups } = fill_carousel(carousel, events);

    
}
  