import { handle_ticket_section } from "./edit_tickets";
import { handle_showings_panel } from "./edit_showings";
import { build_configuration, Type } from "../api/config";
import { handle_media_panel } from "./edit_media";
import { single } from "../common/single";

single('event_edit');

// -- Get the global configuration
export const configuration = build_configuration<{
        event_id: string,

        get_listings: string,
        add_listing: string,
        del_listing: string,

        get_showings: string,
        add_showing: string,
        del_showing: string,

        get_media: string,
        add_media: string,
        del_media: string,

        csrf_token: string,
    }>({
        event_id: new Type('data-event-id', 'string'),

        get_listings: new Type('data-get-ticket-listings', 'string'),
        add_listing: new Type('data-add-ticket-listing', 'string'),
        del_listing: new Type('data-del-ticket-listing', 'string'),

        get_showings: new Type('data-get-showings', 'string'),
        add_showing: new Type('data-add-showing', 'string'),
        del_showing: new Type('data-del-showing', 'string'),

        get_media: new Type('data-get-media', 'string'),
        add_media: new Type('data-add-media', 'string'),
        del_media: new Type('data-del-media', 'string'),

        csrf_token: new Type('data-csrf-token', 'string'),
    });

var listings_panel = document.querySelector('#ticket-listings-panel');
var showings_panel = document.querySelector('#showings-panel')
var media_panel = document.querySelector('#media-panel')

var trailer_panel = document.querySelector('#trailer-panel')


if (listings_panel) {
    handle_ticket_section(listings_panel as HTMLElement);
}

if (showings_panel) {
    handle_showings_panel(showings_panel as HTMLElement);
}

if (media_panel) {
    handle_media_panel(media_panel as HTMLElement);
}
// if (trailer_panel) {
//     handle_trailer_panel(trailer_panel as HTMLElement);
// }