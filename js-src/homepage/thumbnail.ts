import { Event } from './index.d';

/*
    This file handles getting the thumbnail template so we can
    copy it and add it multiple times to the page.
*/

const tn = document.getElementById('thumbnail'),
    cr = document.getElementById('carousel');

tn.id = '';
cr.id = '';



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
    const tn_img = tn_clone.querySelector('.thumbnail-image') as HTMLImageElement;
    tn_img.style.backgroundImage = 'url(' + event.thumbnail + ')';
    tn_img.onclick = () => {
        window.location.href = event.full_url;
    };

    // -- Set the streamer pfp, [data-elm='pfp']
    const tn_pfp = tn_clone.querySelector('[data-elm="pfp"]') as HTMLImageElement;
    tn_pfp.src = event.streamer.pfp;
    tn_pfp.onclick = () => {
        window.location.href = event.streamer.url;
    }

    // -- Sreamtitle, [data-elm='title'], [data-elm='view-count'], [data-elm='date-vod']
    const tn_title = tn_clone.querySelector('[data-elm="title"]') as HTMLHeadingElement;
    const tn_view_count = tn_clone.querySelector('[data-elm="view-count"]') as HTMLSpanElement;
    const tn_date_vod = tn_clone.querySelector('[data-elm="date-vod"]') as HTMLSpanElement;

    tn_title.innerText = event.title;
    tn_title.style.userSelect = 'none';
    tn_title.onclick = () => {
        window.location.href = event.full_url;
    };

    tn_date_vod.innerText = event.start_time;

    tn_view_count.innerText = "@" + event.streamer.name;
    tn_view_count.onclick = () => {
        window.location.href = event.streamer.url;
    }
    

    // -- Return the cloned thumbnail
    return tn_clone;
}


export function fill_carousel(
    carousel: HTMLElement,
    events: Array<Event>,
): {
    parent: HTMLElement,
    children: Array<HTMLElement>,
}
{
    const cr_clone = cr.cloneNode(true) as HTMLElement;
    cr_clone.id = 'carousel-' + events[0].id;
    carousel.appendChild(cr_clone);
    cr_clone.removeAttribute('data-is-hidden');

    // -- The carousel-content element
    const carousel_content = carousel.querySelector('.carousel-content') as HTMLElement;

    // -- The content to show
    let i = 0;
    for (const element of events) {
        const event = element;
        const tn = add_thumbnail(event);
        carousel_content.appendChild(tn);

        // -- Set the tab index
        tn.setAttribute('tabindex', i.toString());
    }
    
    return {
        parent: carousel_content,
        children: Array.from(carousel_content.children) as Array<HTMLElement>,
    };
}




/*
    @name create_carousel
    @description This function creates a carousel and adds it to the parent element
                 it also manages buttons, scroll etc.
    @param {HTMLElement} parent - This is the element that the carousel will be appended to
    @param {Array<Event>} events - The events to show in the carousel
    @returns {void}
*/
export function create_carousel(
    parent: HTMLElement,
    events: Array<Event>,
    category_name: string,
    search_url: string,
) {
    // -- Fill the carousel with thumbnails
    const {
        parent: carousel_content,
        children: carousel_thumbnails,
    } = fill_carousel(parent, events);

    // -- Get the buttons
    const btn_left = parent.querySelector('.carousel-button-left') as HTMLElement;
    const btn_right = parent.querySelector('.carousel-button-right') as HTMLElement;

    const car_header = parent.querySelector('#car-header') as HTMLElement,
        show_more = parent.querySelector('.show-more') as HTMLElement;
    car_header.innerText = category_name;

    // -- Get the Search URL for this carousel
    search_url += '?cat=' + category_name;
    car_header.onclick = () => { window.location.replace(search_url); };
    show_more.onclick = () => { window.location.replace(search_url); };

    // -- Group count
    let hit_left = false;
    let hit_right = false;


    // -- This keeps track of % of total scroll
    const scroll_indicator = parent.querySelector('.scroll-indicator') as HTMLElement;
    const scroll_listener = () => {
        // -- Calculate how much we have scrolled
        const scroll = carousel_content.scrollLeft,
            carousel_width = carousel_content.offsetWidth;

        // -- Calculate the percentage of the scroll
        const percentage = scroll / (carousel_content.scrollWidth - carousel_width);
        scroll_indicator.style.width = (percentage * 100) + '%';
    };


    // -- Add a scroll listener to the carousel
    const scroll_back = () => {
        // -- Get the scroll position and the width of the carousel
        const scroll = carousel_content.scrollLeft,
            carousel_width = carousel_content.offsetWidth,
            tn_width = carousel_thumbnails[0].clientWidth;

        // -- We are at the end of the carousel, move the scroll to the start
        if (scroll + carousel_width >= carousel_content.scrollWidth - tn_width) {
            carousel_content.scrollLeft = 0;
            hit_right = false;
            hit_left = true;
        }

        // -- We are at the start of the carousel, move the scroll to the end
        else if (scroll <= 0) {
            carousel_content.scrollLeft = carousel_content.scrollWidth - carousel_width;
            hit_left = false;
            hit_right = true;
        }
    };


    // -- Add event listeners to the buttons
    btn_left.addEventListener('click', () => {
        // -- Scroll by 1 thumbnail
        const tn_width = carousel_content.children[0].clientWidth;
        carousel_content.scrollLeft -= tn_width; 

        // -- Check if we are at the start of the carousel
        if (hit_left === false && carousel_content.scrollLeft <= tn_width) hit_left = true;
        else if (hit_left) { hit_left = false; scroll_back();}
        else hit_right = false;
    });

    btn_right.addEventListener('click', () => {
        // -- Scroll by 1 thumbnail
        const tn_width = carousel_content.children[0].clientWidth,
            carousel_width = carousel_content.offsetWidth;
        carousel_content.scrollLeft += tn_width;

        // -- Check if we are at the end of the carousel
        if (hit_right === false && carousel_content.scrollLeft + carousel_width >= carousel_content.scrollWidth - tn_width) hit_right = true;
        else if (hit_right) { hit_right = false; scroll_back();}
        else hit_left = false;
    });


    // -- Center the carousel
    carousel_content.scrollLeft = 0;
    hit_left = true;
    hit_right = false;
    carousel_content.addEventListener('scroll', scroll_listener);
}
  