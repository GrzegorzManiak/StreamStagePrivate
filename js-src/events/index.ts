import { manage_add_review_panel, manage_override_btn } from "./reviews"
import { build_configuration, Type } from "../api/config";
import { instant_paynow } from "../common/card_input";
import { single } from "../common/single";
import { attach } from "../common";

single('events');


// -- Build the configuration
export const configuration = build_configuration<{
    event_id: string,
    csrf_token: string,
}>({
    event_id: new Type('data-event-id', 'string'),
    csrf_token: new Type('data-csrf-token', 'string'),
});


// -- Get the ticketing buttons
const buttons = Array.from(
    document.querySelectorAll("[data-ticket-id]") as NodeListOf<HTMLButtonElement>
);


// -- Loop trough the buttons and
//    attach the payment handler
buttons.forEach(btn => btn.addEventListener('click', async() => {
    // -- Attach the spinner
    const stop = attach(btn);

    // -- Get the ticket details
    const ticket_id = btn.getAttribute('data-ticket-id') as string,
        item_name = btn.getAttribute('data-item-name') as string,
        item_price = btn.getAttribute('data-item-price') as string;

    // -- Manage the payment
    await instant_paynow(
        ticket_id, 'Event Ticket', 
        'One time payment for "' + item_name + '"',
        item_name, item_price, stop
    );

    // -- Remove the spinner
    stop();
}));







const add_review_panel = document.querySelector("#add-review-panel") as HTMLElement;
if (add_review_panel)
    manage_add_review_panel(add_review_panel, true);

const admin_review_override_btn = document.querySelector("#admin-review-override-btn") as HTMLButtonElement;
if (admin_review_override_btn)
    manage_override_btn(admin_review_override_btn, add_review_panel);

export function hide_element(element: HTMLElement) {
    // -- Set the element to hidden
    element.setAttribute('elem-status', 'hidden');
}

export function show_element(element: HTMLElement) {
    // -- Set the element to shown
    element.setAttribute('elem-status', 'shown');
}
        