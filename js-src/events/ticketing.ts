import { construct_modal } from "../common";
import { show_element, hide_element } from "./index";

export function manage_tickets_btn(
    btn: HTMLElement
) {
    var tickets_panel = create_panel() ;

    const click = () => {
        show_element(tickets_panel);
    }

    console.log(btn);
    btn.addEventListener("click", click);
}

function create_panel(
) : HTMLElement {
    // -- String template for the modal
    const modal = construct_modal("Tickets", "Message blah", false, 'danger');

    // -- Create a div element
    const div = document.createElement('div');

    // -- Set the innerHTML of the div to the modal
    div.innerHTML = modal;

    // -- Append the modal to the body
    document.body.appendChild(div);

    hide_element(div);

    return div;
}