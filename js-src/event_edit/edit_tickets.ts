import { construct_modal, create_toast } from "../common";
import { add_ticket_listing, del_ticket_listing, get_ticket_listings } from "./apis";
import { GetTicketListingsSuccess, AddTicketListingSuccess, TicketListing } from "./index.d"
import { configuration } from "./index"

let listings_panel;

export function handle_ticket_section(panel: HTMLElement) {
    listings_panel = panel;

    var add_listing_btn = document.querySelector('#add-ticket-listing-btn') as HTMLElement;

    if (add_listing_btn)
        manage_add_listing_btn(add_listing_btn);
        
    query_listings();

}

function manage_add_listing_btn(
    btn: HTMLElement
) {

    btn.addEventListener("click", () => {
        const modal = construct_modal("Add Ticket Listing", "What kind of ticket listing would you like to add?", true, 'success', add_stream_ticket_form);

        // -- Create a div element
        const modal_wrap = document.createElement('div');

        // -- Set the innerHTML of the div to the modal
        modal_wrap.innerHTML = modal;

        // Set up price formatting

        var detail_field = modal_wrap.querySelector("#id_ticket_detail") as HTMLInputElement;
        var price_field = modal_wrap.querySelector("#id_ticket_price") as HTMLInputElement;

        // -- Get the buttons
        const yes_btn = modal_wrap.querySelector('.yes') as HTMLButtonElement,
            no_btn = modal_wrap.querySelector('.no') as HTMLButtonElement;

        // -- Add the event listeners
        yes_btn.addEventListener('click', async() => {
            // -- Call the yes function
            //yes();

            add_listing(detail_field.value, price_field.valueAsNumber);

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

// Functions managing physical list of ticket listings.

function set_listings(listings: TicketListing[]) {
    listings_panel.innerHTML = "";

    for (var listing of listings) {
        append_listing(listing);
    }
}

function remove_listing(lid: number) {
    listings_panel.querySelector(".listing-row[data-lid=\"" + lid + "\"]").remove();
}

function append_listing(listing: TicketListing) {
    listings_panel.appendChild(ticket_listing_html(listing));

    console.log(listings_panel.querySelector(`.remove-listing-btn[data-lid="${listing.id}"]`));

    listings_panel.querySelector(`.remove-listing-btn[data-lid="${listing.id}"]`)
            .addEventListener("click", () => {
                del_listing(listing.id);
            });
    console.log("added event listener for " + listing.id);
}

// API calls

async function query_listings() {
    const listings = await get_ticket_listings(configuration.event_id);

    // -- Check if the request was successful
    if (listings.code !== 200)
        return create_toast(
            'error', 'Oops!',
            'There was an error while trying to get ticket listings, please try again later.'
        )

    const data = (listings as GetTicketListingsSuccess).data

    set_listings(data.listings);
}

async function add_listing(
    detail: string,
    price: number
) {
    const request = await add_ticket_listing(configuration.event_id, 0, price, detail, 0);

    // -- Check if the request was successful
    if (request.code !== 200)
        return create_toast(
            'error', 'Oops!',
            'There was an error while trying to add ticket listing, please try again later.'
        )

    const data = (request as AddTicketListingSuccess).data

    append_listing(data.listing);

    create_toast(
        'success', 'Ticketing',
        'Added new ticket listing successfully.'
    )
}

async function del_listing(lid: number) {
    const request = await del_ticket_listing(configuration.event_id, lid);

    // -- Check if the request was successful
    if (request.code !== 200)
        return create_toast(
            'error', 'Oops!',
            'There was an error while trying to remove ticket listing, please try again later.'
        )

    remove_listing(lid);

    create_toast(
        'success', 'Ticketing',
        'Removed ticket listing.'
    )
}


// HTML generation

function ticket_listing_html(
    listing: TicketListing
) : HTMLElement {
    var row = document.createElement('div');
    row.className = "row border m-1 listing-row";
    row.setAttribute("data-lid", listing.id.toString());

    row.innerHTML = `
        <div class="col-6">
            <div class="b">${listing.detail}</div>
            <span>€${listing.price}</span>
        </div>
        <div class="remove-listing-btn btn btn-danger" data-lid="${listing.id}">
            Remove Listing
        </div>
    `

    return row;
}

const add_stream_ticket_form = `
    <form>
        <div class="mb-3">
            <label for="id_ticket_detail" class="form-label requiredField">
                Ticket Detail<span class="asteriskField">*</span>
            </label>
            <input name="detail" maxlength="100" class="textarea form-control" required="" id="id_ticket_detail" value="Streaming Ticket"></input>
        </div>

        <div class="mb-3">
            <label for="id_price" class="form-label requiredField">
                Price<span class="asteriskField">*</span>
            </label>
            <input name="price" type="number" min="0" max="100" class="form-control" required="" id="id_ticket_price" value="10.99"></input>
        </div>
    </form>
`;
