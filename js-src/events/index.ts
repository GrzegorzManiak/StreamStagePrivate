import { manage_paynow } from "../click_handler";
import { create_toast } from "../toasts";

import { manage_add_review_panel, manage_override_btn } from "./reviews"

export function get_or_error<e>(element: HTMLElement, attribute: string): e {
    const value = element.getAttribute(attribute);
    if (!value) {
        create_toast('error', 'Configuration Error', `No ${attribute} found, please reload the page`);
        // -- Wait 3 seconds and reload the page
        setTimeout(() => {
            window.location.reload();
        }, 3000);
    }
    return value as unknown as e;
}

// -- Purchase streaming ticket btn
const purchase_stream_ticket = document.querySelector('#buy-streaming-ticket') as HTMLButtonElement;

manage_paynow(purchase_stream_ticket as HTMLButtonElement, "Purchase Streaming Ticket", "Test", "Ticket", "10.20");

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
        