import { GetBroadcasterEventsResponse, GetBroadcasterEventsSuccess, Event } from "../index.d";
import { create_toast } from "../../common";
import { get_events } from "../api";
import { configuration } from "..";

function create_events(
    events: Event[]
): Array<HTMLDivElement> {
    const event_elements: Array<HTMLDivElement> = [];
    events.forEach((evt) => event_elements.push(create_event(evt)));
    return event_elements;
}

export function create_event(
    event: Event
): HTMLDivElement {
    const template = `
        <div class="row my-2 px-4 mx-auto">
            <div class="col-md-3 col-sm-12">
                <!-- Event Categories -->
                {% for category in event.categories.all %}
                <span class="badge bg-primary">{{category.name}}</span>
                {% endfor %}
                <!-- Event Broadcaster -->
                <h6 class="my-2">@{{ event.broadcaster.handle }}</h6>
                <!-- Event Cover Picture (if any) -->
                {% if event.get_media_count == 0 %}
                <img class="event-cover" src="{% static 'images/default_event_cover.png' %}" alt="No Event Cover Photo">
                {% else %}
                <img class="event-cover" src="{{ event.get_cover_picture.picture.url }}"
                    alt="{{ event.get_cover_picture.description }}">
                {% endif %}
            </div>
            <a class="col-md-6 col-sm-12" href="{% url 'event_view' event.event_id %}">
                <!-- Event title & description -->
                <h4 class="sub-title">{{ event.title }}</h4>
                <p>{{ event.description | slice:':250'}}...</p>
            </a>
            <!-- Reviews for Event -->
            <div class="col-md-3 col-sm-12">
                <div class="my-4 mx-1">
                    {% if event.get_review_count > 0 %}
                    <h6 class="text-center"><b>Reviews</b></h6>
                    <!-- Review Carousel -->
                    <div class="swiper mySwiper">
                        <div class="swiper-wrapper">
                            {% for review in event.get_short_reviews %}
                            <div class="swiper-slide">
                                {% include 'reviews/review.html' %}
                            </div>
                            {% endfor %}
                        </div>
                        <div class="swiper-pagination"></div>
                        <div class="s-btn swiper-button-prev"></div>
                        <div class="s-btn swiper-button-next"></div>
                    </div>
                    {% else %}
                    <h6 class="text-center"><b>No reviews yet</b></h6>
                    {% endif %}
                </div>
            </div>
        </div>
    `

    const div = document.createElement('div');
    div.classList.add('review', 'd-flex', 'justify-content-between', 'align-items-center', 'w-100', 'gap-2');
    div.innerHTML = template;

    return div;
}

export function manage_events_panel() {
    // -- Get the panel
    const panel = document.querySelector('#events-tab') as HTMLDivElement;

    // -- Get the review container
    const event_container = panel.querySelector('.events') as HTMLDivElement,
        filter = panel.querySelector('#filter') as HTMLSelectElement,
        order = panel.querySelector('#order') as HTMLSelectElement;

    // -- Get the pagenation controlls
    const prev = panel.querySelector('.prev') as HTMLButtonElement,
        next = panel.querySelector('.next') as HTMLButtonElement,
        page_number = panel.querySelector('#review-page') as HTMLInputElement,
        out_of = panel.querySelector('.out-of') as HTMLSpanElement;
    
    let page = 0, toatl_pages = 0;
    async function reload_events() {
        // -- Get the reviews
        const reviews = await get_events(
            filter.value as 'rating',
            order.value as 'asc' | 'desc', page,
            configuration.broadcaster_id
        );
        
        // -- Check if the request was successful
        if (reviews.code !== 200) return create_toast(
            'error', 'Oops!', 'There was an error while trying to load events.')
        
        const data = (reviews as GetBroadcasterEventsSuccess).data,
            rendered_events = create_events(data.events);
        
        // -- Clear the review container
        event_container.innerHTML = '';
        rendered_events.forEach(evt => event_container.appendChild(evt));
        out_of.innerText = 'out of ' + Number(data.pages);
        page_number.value = page + 1 + '';
        toatl_pages = data.pages;


        // -- Update the pagenation controlls
        if (page === 0) prev.disabled = true;
        else prev.disabled = false;

        if (page === toatl_pages -1) next.disabled = true;
        else next.disabled = false;

        // -- Check if there are no reviews
        if (data.events.length === 0) event_container.innerHTML = `
            <div class="no-reviews w-100 h-100 d-flex justify-content-center align-items-center">
                <h3 class="text-center text-muted">@${configuration.handle} has events yet.</h3>
            </div>
        `;
    }


    // -- Add the event listeners
    prev.disabled = true;
    prev.addEventListener('click', () => {
        if (page === 0) return prev.disabled = true;
        page--;
        reload_events();
    });

    next.addEventListener('click', () => {
        if (page === toatl_pages) return
        prev.disabled = false;
        page++;
        reload_events();
    });

    page_number.addEventListener('change', () => {
        const number = parseInt(page_number.value);
        if (number < 1 || number > toatl_pages) return;
        page = number - 1;
        reload_events();
    });

    filter.addEventListener('change', reload_events);
    order.addEventListener('change', reload_events);

    reload_events();
    console.log('Events panel loaded');
}
