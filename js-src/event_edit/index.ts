import { build_configuration, Type } from "../api/config";
import { construct_modal, create_toast } from "../common";
import { get_ticket_listings } from "./apis";
import { GetTicketListingsSuccess, TicketListing } from "./index.d"

// -- Get the global configuration
export const configuration = build_configuration<{
        get_listings: string,
        csrf_token: string,
    }>({
        get_listings: new Type('data-get-ticket-listings', 'string'),
        csrf_token: new Type('data-csrf-token', 'string'),
    });

var listings_panel = document.querySelector('#ticket-listings-panel');


if (listings_panel) {
    var add_listing_btn = document.querySelector('#add-ticket-listing-btn') as HTMLElement;

    if (add_listing_btn)
        manage_add_listing_btn(add_listing_btn);
}


function manage_add_listing_btn(
    btn: HTMLElement
) {

    btn.addEventListener("click", () => {
        const modal = construct_modal("Add Ticket Listing", "What kind of ticket listing would you like to add?", true, 'success', `
            STREAMING / IN PERSON?
        `);

        // -- Create a div element
        const modal_wrap = document.createElement('div');

        // -- Set the innerHTML of the div to the modal
        modal_wrap.innerHTML = modal;

        // -- Get the buttons
        const yes_btn = modal_wrap.querySelector('.yes') as HTMLButtonElement,
            no_btn = modal_wrap.querySelector('.no') as HTMLButtonElement;

        // -- Add the event listeners
        yes_btn.addEventListener('click', async() => {
            // -- Call the yes function
            //yes();

            // -- Remove the modal
            modal_wrap.remove();
        });

        no_btn.addEventListener('click', async() => {
            // -- Call the no function
            //no();

            // -- Remove the modal
            modal_wrap.remove();
        });

        // -- Append the modal to the body
        document.body.appendChild(modal_wrap);
    });

}

query_listings('myevnt');


function add_listings(listings: TicketListing[]) {
    listings_panel.innerHTML = "";

    for (var listing of listings) {
        listings_panel.innerHTML += ticket_listing_html(listing);
    }
}


async function query_listings(event_id: string) {
    // -- Get the reviews
    const listings = await get_ticket_listings(
        "myevnt"
    );

    // -- Check if the request was successful
    if (listings.code !== 200) return create_toast(
        'error', 'Oops!', 'There was an error while trying to get ticket listings, please try again later.')

    const data = (listings as GetTicketListingsSuccess).data
    
    console.log(data.listings);

    add_listings(data.listings);

    //renderd_reviews = create_reviews(data.reviews);

}


function ticket_listing_html(
    listing: TicketListing
) : string {
    return `
    <div class="row border m-1">
        <div class="col-6">
            <div class="b">${listing.detail}</div>
            <span>€${listing.price}</span>
        </div>
    </div>
    `;
}