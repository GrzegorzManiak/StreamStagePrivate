import { GetBroadcasterEventsResponse, GetBroadcasterEventsSuccess, Event } from "../index.d";
import { create_toast } from "../../common";
import { get_events } from "../api";
import { configuration } from "..";
import { Review } from "../../common/index.d";

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
    var categories = ""

    console.log(event);
    for (var category of event.categories){
        categories +=`<span class="badge bg-secondary">${category}</span>`
    }

    var reviews_html = "";

    if (event.reviews.length > 0) {
        reviews_html += `
        <h6 class="text-center"><b>Reviews</b></h6>
        <!-- Review Carousel -->
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">`;
        
        for (var review of event.reviews){ 
            reviews_html += create_review_html(review);
        }

        reviews_html += `</div>
            <div class="swiper-pagination"></div>
            <div class="s-btn swiper-button-prev"></div>
            <div class="s-btn swiper-button-next"></div>
        </div>`;

    } else {
        reviews_html = `<h6 class="text-center"><b>No reviews yet</b></h6>`;
    }

    const template = `
        <div class="row my-2 px-4 mx-auto">
            <div class="col-md-3 col-sm-12">
                <!-- Event Categories -->
                ${categories}
                <!-- Event Broadcaster -->
                <h6 class="my-2">@${configuration.handle}</h6>
                <!-- Event Cover Picture (if any) -->
                <img class="event-cover" src="${event.cover_pic}">
            </div>
            <a class="col-md-6 col-sm-12" href="${event.url}">
                <!-- Event title & description -->
                <h4 class="sub-title">${event.title}</h4>
                <p>${event.description}</p>
            </a>
            <!-- Reviews for Event -->
            <div class="col-md-3 col-sm-12">
                <div class="my-4 mx-1">
                   ${reviews_html}
                </div>
            </div>
        </div>
    `

    const div = document.createElement('div');
    div.classList.add('review', 'd-flex', 'justify-content-between', 'align-items-center', 'w-100', 'gap-2');
    div.innerHTML = template;

    return div;
}

function create_review_html(review: Review) {
  return `
  <div class="swiper-slide"><div class="card bg-dark p-3 mb-1">
    <div>
        <b class="card-title">${review.title} </b>
        <span class="float-end">by ${review.username}</span>
    </div>
    
    <p class="card-text">
        ${review.body}
    </p>
    <div>
        <!-- Giving a star rating out of 5 -->
        <ul class="btn btn-light list-inline rating-list">
          <li>
              <i class="fa fa-star {% if review.rating > 4 %} checked {% endif %}" title="Rate 5"></i></li>
          <li>
              <i class="fa fa-star {% if review.rating > 3 %} checked {% endif %}" title="Rate 4"></i></li>
          <li>
              <i class="fa fa-star {% if review.rating > 2 %} checked {% endif %}" title="Rate 3"></i></li>
          <li>
              <i class="fa fa-star {% if review.rating > 1 %} checked {% endif %}" title="Rate 2"></i></li>
          <li>
              <i class="fa fa-star {% if review.rating > 0 %} checked {% endif %}" title="Rate 1"></i></li>
        </ul>

        <a href="#" >
            <span data-id="${review.id}" data-likes="${review.likes}" 
            user-liked="" 
            class="like-button float-end btn btn-primary btn-sm m-1">
                <i class="fa fa-thumbs-o-up" aria-hidden="true">&nbsp;{{ review.likes }}</i>
            </span>
        </a>
    </div>

    {% if review.author == user %}
    <div>
        <a href="{% cross_app_reverse_tag 'events' 'review_delete' event_id=event.event_id review_id=review.review_id %}" class="float-start btn btn-danger btn-sm m-1">Delete</a>
        <a href="{% cross_app_reverse_tag 'events' 'review_update' event_id=event.event_id review_id=review.review_id %}" class="float-start btn btn-primary btn-sm m-1">Update</a>
    </div>

    {% endif %}

</div></div>`
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
        page_number = panel.querySelector('#events-page') as HTMLInputElement,
        out_of = panel.querySelector('.out-of') as HTMLSpanElement;
    
    let page = 0, toatl_pages = 0;
    async function reload_events() {
        // -- Get the events
        const events = await get_events(
            filter.value as 'rating',
            order.value as 'asc' | 'desc', page,
            configuration.broadcaster_id
        );
        
        // -- Check if the request was successful
        if (events.code !== 200) return create_toast(
            'error', 'Oops!', 'There was an error while trying to load events.')
        
        const data = (events as GetBroadcasterEventsSuccess).data,
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
            <div class="no-events w-100 h-100 d-flex justify-content-center align-items-center">
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
