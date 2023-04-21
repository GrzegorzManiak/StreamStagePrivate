import { Pod } from '../index.d';

/**
 * @param pod: Pod - The pod that this panel is attached to
 * 
 * @returns void
 * 
 * @description This function manages the tickets panel
 */
export function manage_ticekts_panel(pod: Pod) {
    const panel = pod.panel.element;

    const online_tickets = panel.querySelector('#online-tickets') as HTMLDivElement,
        inperson_tickets = panel.querySelector('#inperson-tickets') as HTMLDivElement,
        expired_tickets = panel.querySelector('#expired-tickets') as HTMLDivElement;

    const ot_header = panel.querySelector('#online-tickets-header') as HTMLDivElement,
        ip_header = panel.querySelector('#inperson-tickets-header') as HTMLDivElement,
        et_header = panel.querySelector('#expired-tickets-header') as HTMLDivElement;
    
    // -- Check if theres any tickets, and remove the respective headers if not
    if (online_tickets.children.length === 0) ot_header.remove();
    if (inperson_tickets.children.length === 0) ip_header.remove();
    if (expired_tickets.children.length === 0) et_header.remove();

    // -- Get the ticket template 
    let ticket_template = panel.querySelector('#ticket-template') as HTMLDivElement;
    ticket_template = ticket_template.firstElementChild as HTMLDivElement;

    // -- Loop trough the inperson tickets
    for (const ticket of Array.from(
        inperson_tickets.children
    ) as Array<HTMLElement>) {
        
        // -- Get the ticket data
        const ticket_id = ticket.getAttribute('data-ticket-id') as string,
            title = ticket.getAttribute('data-title') as string,
            date = ticket.getAttribute('data-date') as string,
            start_time = ticket.getAttribute('data-start-time') as string,
            venue = ticket.getAttribute('data-venue') as string,
            price = ticket.getAttribute('data-price') as string;

        // -- Get the 'Ticket' button
        const ticket_button = ticket.querySelector('#view') as HTMLButtonElement;

        // -- Add the event listener
        ticket_button.addEventListener('click', () => {
            // -- Clone the template
            const ticket_clone = ticket_template.cloneNode(true) as HTMLDivElement;

            // -- Get the elements
            const ticket_title = ticket_clone.querySelector("[data-id='ticket-title']") as HTMLDivElement,
                ticket_showing = ticket_clone.querySelector("[data-id='ticket-showing']") as HTMLDivElement,
                ticket_date = ticket_clone.querySelector("[data-id='ticket-date']") as HTMLDivElement,
                ticket_start = ticket_clone.querySelector("[data-id='ticket-gates']") as HTMLDivElement,
                ticket_price = ticket_clone.querySelector("[data-id='ticket-price']") as HTMLDivElement,
                ticket_qr = ticket_clone.querySelector("[data-id='ticket-qr']") as HTMLImageElement,
                ticked_id = ticket_clone.querySelector("[data-id='ticket-id']") as HTMLDivElement;

            const qr = `https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=${ticked_id}&choe=UTF-8`;
            ticket_title.textContent = title;
            ticket_showing.textContent = venue;
            ticket_date.textContent = date;
            ticket_start.textContent = start_time;
            ticket_price.textContent = price;
            ticket_qr.src = qr;

            let formatted_ticket_id = ticket_id.toUpperCase();
            formatted_ticket_id = formatted_ticket_id.slice(0, Math.floor(ticket_id.length / 2)) + ' ' + formatted_ticket_id.slice(Math.floor(ticket_id.length / 2));
            ticked_id.textContent = formatted_ticket_id;

            // -- Get styled-ticket
            const styled_ticket = ticket_clone.querySelector('.styled-ticket') as HTMLDivElement;

            // -- Create the close button
            const close_button = document.createElement('button');
            close_button.textContent = 'Close';
            close_button.classList.add('mfa', 'mt-4', 'btn', 'btn-outline', 'btn-lg', 'loader-btn', 'btn-info', 'info', 'w-100');
            styled_ticket.appendChild(close_button);

            // -- Append this to the body
            const css = `
                <style> body, html { overflow: hidden; scroll-behavior: unset; } </style>
            `;
            styled_ticket.insertAdjacentHTML('beforeend', css);


            // -- Append the ticket to the body 
            ticket_clone.classList.add('fullscreen');
            document.body.appendChild(ticket_clone);

            // -- Add the event listener to the close button
            close_button.addEventListener('click', () => {
                ticket_clone.remove();
            });
        });
    }
}