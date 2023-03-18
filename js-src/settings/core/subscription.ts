import { card_modal } from '../elements/card';
import { PaymentMethod, Pod } from '../index.d';
import { load_cards, read_card_modal } from './payments';

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
    saved_payments_dropdown(panel, (card: PaymentMethod) => {
        console.log(card);
    });



    // -- Get the 'subscription' element
    const subscription = panel.querySelector('.payment-plan') as HTMLDivElement,
        annualy = subscription.querySelector('.annualy') as HTMLDivElement,
        monthly = subscription.querySelector('.monthly') as HTMLDivElement;

    // -- Add the event listener to the annualy button
    annualy.addEventListener('click', () => {
        monthly.classList.remove('selected');
        annualy.classList.add('selected');
    });

    // -- Add the event listener to the monthly button
    monthly.addEventListener('click', () => {
        annualy.classList.remove('selected');
        monthly.classList.add('selected');
    });



    const new_card_button = panel.querySelector('.new-card') as HTMLButtonElement;
    new_card_button.addEventListener('click', () => {
        // -- Add the modal to the body
        const modal_div = document.createElement('div');
        modal_div.innerHTML = card_modal(true, 'New Card', 
            'Pay with a new card, you can add it to your saved cards for later purcahses.');
        document.body.appendChild(modal_div);

        const submit_button = modal_div.querySelector('.yes') as HTMLButtonElement,
            save_card = modal_div.querySelector('#save-card') as HTMLInputElement;
            
        const card_manager = read_card_modal(modal_div);
        submit_button.addEventListener('click', async () => {

            console.log(card_manager(), save_card.checked)
        });
    });
}



/**
 * @name saved_payments_dropdown
 * @description This function manages the saved payments dropdown
 *              Look for '<!-- Saved Cards -->' for the HTML, this
 *              is a reusable component, so you can use it for other
 *              payments related stuff.
 * @param parent: HTMLElement | Element - The parent element
 * @param callback: (id: PaymentMethod) => void - The callback function
 *                  that will be called when a card is selected, it returns
 *                  the full card object
 */
export async function saved_payments_dropdown(
    parent: HTMLElement | Element,
    callback: (id: PaymentMethod) => void,
) {
    // -- Load the cards
    await load_cards(parent, true);
    let active = '';

    // -- Get the 'saved-dropdown' element
    const dropdown = parent.querySelector('.saved-dropdown') as HTMLDivElement,
        button = dropdown.querySelector('button') as HTMLButtonElement,
        cards = dropdown.querySelector('.cards') as HTMLDivElement;
        
    const manage_cards = () => {
        // -- Get the cards
        const cards = Array.from(dropdown.querySelectorAll('.cards-body'));

        // -- Add the event listener to the cards
        for (const card of cards) { 
            card.addEventListener('click', () => {
                // -- Set this card as active
                open = false;
                dropdown.setAttribute('dropdown', open.toString());
                card.setAttribute('selected', 'true');
                active = card.getAttribute('card-id');

                // -- Call the callback
                callback({ 
                    id: card.getAttribute('card-id'),
                    exp_month: Number(card.getAttribute('card-exp-month')),
                    exp_year: Number(card.getAttribute('card-exp-year')),
                    last4: card.getAttribute('card-last4'),
                    brand: card.getAttribute('card-brand'),
                    created: Number(card.getAttribute('card-created')),
                });

                // -- Remove the selected attribute from the other cards
                for (const c of cards) {
                    if (c === card) continue;
                    c.removeAttribute('selected');
                }
            });

            // -- Check if the card is active (this is for 
            //    when the cards get reloaded)
            if (card.getAttribute('card-id') === active)
                card.setAttribute('selected', 'true');
        }
    }


    // -- Add the event listener to the button
    let open = false;
    button.addEventListener('click', () => {
        // -- Toggle the dropdown
        open = !open;
        dropdown.setAttribute('dropdown', open.toString());

        // -- Reload the cards 
        load_cards(parent, true).then(() => manage_cards());
    });


    // -- Add an event listener to the window to close the dropdown
    //    whenever the user clicks outside of the dropdown
    cards.parentElement.addEventListener('click', (e) => {
        if (e.target === button || cards.contains(e.target as Node)) return;
        open = false;
        dropdown.setAttribute('dropdown', open.toString());
    });


    // -- Manage the cards
    manage_cards();
}