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

}