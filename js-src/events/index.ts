import { manage_paynow } from "../click_handler";
import { create_toast } from "../toasts";


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

manage_paynow(purchase_stream_ticket, "Purchase Streaming Ticket", "Test", "Ticket", "10.20");
