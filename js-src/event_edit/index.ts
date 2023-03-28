import { handle_ticket_section } from "./edit_tickets";
import { build_configuration, Type } from "../api/config";

// -- Get the global configuration
export const configuration = build_configuration<{
        event_id: string,

        get_listings: string,
        add_listing: string,
        del_listing: string,

        csrf_token: string,
    }>({
        event_id: new Type('data-event-id', 'string'),

        get_listings: new Type('data-get-ticket-listings', 'string'),
        add_listing: new Type('data-add-ticket-listing', 'string'),
        del_listing: new Type('data-del-ticket-listing', 'string'),

        csrf_token: new Type('data-csrf-token', 'string'),
    });

var listings_panel = document.querySelector('#ticket-listings-panel');


if (listings_panel) {
    handle_ticket_section(listings_panel as HTMLElement);
}