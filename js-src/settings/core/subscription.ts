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

    // -- Get the 'saved-dropdown' element
    const dropdown = parent.querySelector('.saved-dropdown') as HTMLDivElement,
        button = dropdown.querySelector('button') as HTMLButtonElement,
        cards = Array.from(dropdown.querySelectorAll('.cards-body'));

    let open = false;

    // -- Add the event listener to the button
    button.addEventListener('click', () => {
        open = !open;
        dropdown.setAttribute('dropdown', open.toString());
    });


    // -- Add the event listener to the cards
    for (const card of cards) {
        card.addEventListener('click', () => {
            open = false;
            dropdown.setAttribute('dropdown', open.toString());
            card.setAttribute('selected', 'true');
            callback(card.getAttribute('payment-id'));

            // -- Remove the selected attribute from the other cards
            for (const c of cards) {
                if (c === card) continue;
                c.removeAttribute('selected');
            }
        });
    }


    // // -- Add the event listener to the rest of the document
    // document.addEventListener('click', (e) => {
    //     if (
    //         e.target === button ||
    //         button.contains(e.target as Node)
    //     ) return;
    //     open = false;
    //     dropdown.setAttribute('dropdown', open.toString());
    // });

}