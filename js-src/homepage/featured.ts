/*
    @name: attach_to_showcases
    @description: Attaches a showcase manager to any
        element with the class "showcase".
    @return: void
*/
export function attach_to_showcases() {
    // -- Get all showcase elements
    const showcases = document.getElementsByClassName('showcase');

    // -- Loop through each showcase
    Array.from(showcases).forEach((showcase: HTMLElement) => 
        attach_to_showcase(showcase));
}



/*
    @name: attach_to_showcase
    @description: Attaches a showcase manager to a
        specific element.
    @param: showcase: HTMLElement
    @return: void
*/
export function attach_to_showcase(showcase: HTMLElement) {

    // -- Get all the showcase items
    const showcase_items = showcase.getElementsByClassName('showcase-small-img'),
        big_display = showcase.getElementsByClassName('showcase-big')[0] as HTMLElement;


    // -- Loop through each showcase item
    Array.from(showcase_items).forEach((
        item: HTMLElement, 
        index: number
    ) => item.addEventListener('click', () => {
        // -- Remove the active class from all showcase items
        Array.from(showcase_items).forEach(async(item: HTMLElement) => 
            item.classList.remove('active'));

        // -- Add the active class to the clicked item
        item.classList.add('active');


        // -- Set the big display
        big_display.style.backgroundImage = 'url(' + item.getAttribute('data-stream-big') + ')';
        
        // -- Title [data-sci-elm="title"]
        const title = big_display.querySelector('[data-sci-elm="title"]') as HTMLElement;
        title.innerHTML = item.getAttribute('data-stream-title');

        // -- Description [data-sci-elm="desc"]
        const desc = big_display.querySelector('[data-sci-elm="desc"]') as HTMLElement;
        desc.querySelector('.description').innerHTML = item.getAttribute('data-stream-desc');
        desc.querySelector('[data-skeleton="image"]').setAttribute('src', item.getAttribute('data-stream-pfp'));
        desc.querySelector('[data-elm="view-count"]').innerHTML = item.getAttribute('data-stream-views');
        desc.querySelector('[data-elm="date-vod"]').innerHTML = item.getAttribute('data-stream-date');
        desc.setAttribute('data-is-live', item.getAttribute('data-is-live'));

        // -- Set the tags 
        const tags = item.getAttribute('data-stream-tags').split(','),
            tags_elm = big_display.querySelector('.tags') as HTMLElement;
        
        // -- Clear the tags
        tags_elm.innerHTML = '';

        // -- Add the tags
        tags.forEach(tag => {
            const tag_elm = document.createElement('span');
            tag_elm.classList.add('tag');
            tag_elm.setAttribute('data-tag', 'info');
            tag = tag.trim();
            if (tag === '18+') tag_elm.setAttribute('data-tag', 'error');
            tag_elm.innerHTML = tag;
            tags_elm.appendChild(tag_elm);
        });
    }));


    // -- Click the second item
    (showcase_items[1] as HTMLElement).click();
}