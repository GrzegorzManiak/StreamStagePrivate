import { build_configuration, Type } from "../api/config";
import { manage_paynow } from "../common/card_input";
import { manage_add_review_panel, manage_override_btn } from "./reviews"
import { manage_tickets_btn } from "./ticketing";

// -- Purchase streaming ticket btn
//const purchase_stream_ticket = document.querySelector('#buy-streaming-ticket') as HTMLButtonElement;

//manage_paynow(purchase_stream_ticket as HTMLButtonElement, "Purchase Streaming Ticket", "Test", "Ticket", "10.20");

// -- Get the global configuration
export const configuration = build_configuration<{
    event_id: string,
    csrf_token: string,
}>({
    event_id: new Type('data-event-id', 'string'),
    csrf_token: new Type('data-csrf-token', 'string'),


});

manage_tickets();

function manage_tickets() {
    document.querySelectorAll(".purchase-ticket").forEach(btn => {
        manage_paynow(
            btn as HTMLButtonElement,
            "Purchase Ticket",
            btn.getAttribute("data-item-name"),
            btn.getAttribute("data-item-name"),
            btn.getAttribute("data-item-price"),
            btn.getAttribute("data-ticket-id")
        );
        


    });
}


//manage_tickets_btn(document.querySelector('#show-tickets-btn'));




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
        