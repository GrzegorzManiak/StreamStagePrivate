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
    tn_view_count.innerText = event.views_formatted + ' views';
    tn_date_vod.innerText = event.start_time;
    

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
    for (const element of events) {
        const event = element;
        const tn = add_thumbnail(event);
        carousel_content.appendChild(tn);
    }
    
    return {
        parent: carousel_content,
        children: Array.from(carousel_content.children) as Array<HTMLElement>,
    };
}




  
export function carousel_scroll(
    carousel: HTMLElement,
    events: Array<Event>,
) {
    // -- Fill the carousel with thumbnails
    const {
        parent: carousel_content,
        children: carousel_thumbnails,
    } = fill_carousel(carousel, events);

    // -- Get the buttons
    const btn_left = carousel.querySelector('.carousel-button-left') as HTMLElement;
    const btn_right = carousel.querySelector('.carousel-button-right') as HTMLElement;

    // -- Group count
    let hit_left = false;
    let hit_right = false;

    // -- Center the carousel
    const carousel_width = carousel.offsetWidth;
    const tn_width = carousel_thumbnails[0].clientWidth;
    
    // -- Depending on the amount of thumbnails, we we want to
    //    center the carousel differently
    if (carousel_thumbnails.length % 2 === 0) {
        // -- Even amount of thumbnails
        carousel_content.scrollLeft = (carousel_width / 2) - (tn_width / 2) - (tn_width / 2);
    }

    if (carousel_thumbnails.length % 2 === 1) {
        // -- Odd amount of thumbnails
        carousel_content.scrollLeft = (carousel_width / 2) - (tn_width / 2);
    }


    // -- Add a scroll listener to the carousel
    const scroll_back = () => {
        // -- Get the scroll position
        const scroll = carousel_content.scrollLeft;

        // -- Get the size of the thumbnails
        const tn_width = carousel_content.children[0].clientWidth;

        // -- Get the size of the carousel
        const carousel_width = carousel.offsetWidth;

        // -- Check if we are at the end of the carousel
        if (scroll + carousel_width >= carousel_content.scrollWidth) {
            // -- We are at the end of the carousel, move the scroll to the start
            carousel_content.scrollLeft = 0;
        }

        // -- Check if we are at the start of the carousel
        if (scroll <= 0) {
            // -- We are at the start of the carousel, move the scroll to the end
            carousel_content.scrollLeft = carousel_content.scrollWidth;
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
        hit_right = false;
    });

    btn_right.addEventListener('click', () => {
        // -- Scroll by 1 thumbnail
        const tn_width = carousel_content.children[0].clientWidth;
        carousel_content.scrollLeft += tn_width;

        // -- Check if we are at the end of the carousel
        if (hit_right === false && carousel_content.scrollLeft + carousel_width >= carousel_content.scrollWidth - tn_width) hit_right = true;
        else if (hit_right) { hit_right = false; scroll_back();}
        hit_left = false;
    });
}
  