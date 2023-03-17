import { Pod } from '../index.d';
import { load_cards } from './payments';

/**
 * @param pod: Pod - The pod that this panel is attached to
 * 
 * @returns void
 * 
 * @description This function manages the subscriptions panel
 */
export function manage_subscription_panel(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

    // -- Manage the saved payment methods dropdown
    saved_payments_dropdown(panel, (id: string) => {
        console.log(id);
    });
}


export async function saved_payments_dropdown(
    parent: HTMLElement | Element,
    callback: (id: string) => void,
) {
    // -- Load the cards
    await load_cards(parent, false);
    let active = '';

    // -- Get the 'saved-dropdown' element
    const dropdown = parent.querySelector('.saved-dropdown') as HTMLDivElement,
        button = dropdown.querySelector('button') as HTMLButtonElement;
        
    function manage_cards() {
        // -- Get the cards
        const cards = Array.from(dropdown.querySelectorAll('.cards-body'));

        // -- Add the event listener to the cards
        for (const card of cards) { 
            card.addEventListener('click', () => {
                open = false;
                dropdown.setAttribute('dropdown', open.toString());
                card.setAttribute('selected', 'true');
                active = card.getAttribute('payment-id');
                callback(active);

                // -- Remove the selected attribute from the other cards
                for (const c of cards) {
                    if (c === card) continue;
                    c.removeAttribute('selected');
                }
            });

            // -- Check if the card is active
            if (card.getAttribute('payment-id') === active)
                card.setAttribute('selected', 'true');
        }


        // -- Add the event listener to the rest of the document
        document.addEventListener('click', (e) => {
            if (
                e.target === button ||
                button.contains(e.target as Node)
            ) return;
            open = false;
            dropdown.setAttribute('dropdown', open.toString());
        });
    }


    // -- Add the event listener to the button
    let open = false;
    button.addEventListener('click', () => {
        open = !open;
        dropdown.setAttribute('dropdown', open.toString());

        // -- Reload the cards 
        load_cards(parent, false).then(() => manage_cards());
    });

    // -- Manage the cards
    manage_cards();
}