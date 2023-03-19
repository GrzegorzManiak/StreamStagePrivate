import { attach } from '../../click_handler';
import { create_new_card, fit_card, pay_now } from '../elements/card';
import { PaymentMethod, Pod, SubscriptionMethod } from '../index.d';
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

    // -- Pay button
    const pay_button = panel.querySelector('.pay-now') as HTMLButtonElement;
    manage_paynow(pay_button);
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
export function saved_payments_dropdown(
    parent: HTMLElement | Element,
    callback: (id: PaymentMethod) => void,
): () => void {
    let active = '';
    const manage_cards = () => {
        // -- Get the cards
        const cards = Array.from(parent.querySelectorAll('.cards-body'));

        // -- Add the event listener to the cards
        for (const card of cards) { 
            card.addEventListener('click', () => {
                // -- Set this card as active
                parent.setAttribute('dropdown', open.toString());
                card.setAttribute('data-selected', 'true');
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
                    c.removeAttribute('data-selected');
                }
            });

            // -- Check if the card is active (this is for 
            //    when the cards get reloaded)
            if (card.getAttribute('card-id') === active)
                card.setAttribute('data-selected', 'true');
        }

        // -- Check if there are no cards
        if (cards.length === 0)
            parent.setAttribute('no-cards', 'true');
        
    }

    return async() => {
        // -- Reload the cards 
        load_cards(parent, true).then(() => manage_cards());
    };
}




export function manage_paynow(
    button: HTMLButtonElement
) {
    const on_click = (stop: () => {}) => {
        const modal = document.createElement('div');
        let selected_card: SubscriptionMethod,
            saved_payment: SubscriptionMethod;
        modal.innerHTML = pay_now();
        document.body.appendChild(modal);

        // -- yes / no buttons
        const yes = modal.querySelector('.yes') as HTMLButtonElement,
            no = modal.querySelector('.no') as HTMLButtonElement,
            back = modal.querySelector('.go-back') as HTMLButtonElement;

        back.style.display = 'none';
        yes.disabled = true;

        // -- Saved payments list and new card form readers and the 'save-card' checkbox
        const reload_saved = saved_payments_dropdown(modal, async(card: PaymentMethod) => {
            selected_card = card;
            saved_payment = card;
            yes.disabled = false;
        }), read_card = read_card_modal(modal),
            save_card = modal.querySelector('.save-card') as HTMLInputElement;
        reload_saved();


        // -- Grab the main elements .payment-select
        const payment_select = modal.querySelector('.payment-select'),
            main_elm = modal.querySelector('.pay-now-modal'),
            confirm = modal.querySelector('.pay-confirm');

        // -- Grab the payment mode buttons, .pay-now-slider
        const pay_now_slider = payment_select.querySelector('.pay-now-slider'),
            new_card = pay_now_slider.querySelector('.new-card'),
            saved_card = pay_now_slider.querySelector('.saved-card'),
            card = modal.querySelector('.final-card');
        

        // -- Add the event listener to the new card button
        new_card.addEventListener('click', () => {
            payment_select.setAttribute('data-mode', 'new');
            yes.disabled = true;
            read_card();
        });

        saved_card.addEventListener('click', () => {
            payment_select.setAttribute('data-mode', 'saved');
            selected_card = saved_payment;
            if (selected_card) yes.disabled = false;
            reload_saved();
        });

            
        // -- Add the event listener to the yes/no buttons
        let stage = 0;
        yes.addEventListener('click', async() => {
            switch (stage) {
                case 0: 
                    // -- Check the mode of the payment
                    let mode = payment_select.getAttribute('data-mode');
                    if (mode === 'new') selected_card = read_card();
                    main_elm.setAttribute('data-mode', 'confirm');
                    back.style.display = 'block';

                    // -- Add the card to the confirm modal
                    const elm = create_new_card(fit_card(selected_card), false);
                    card.innerHTML = elm.card.innerHTML;

                    break;

                case 1:
                    // -- Ask the user to confirm the payment
                    
                    break;
            }
        });

        back.addEventListener('click', () => {
            main_elm.setAttribute('data-mode', 'select');
            back.style.display = 'none';
            stage = 0;
        });

        // -- 'no' event listner
        no.addEventListener('click', () => {
            stop()
        });
    };


    // -- Attatch the click function
    button.addEventListener('click', () => {
        const stop_spinner = attach(button);

        // -- Open up the modal
        on_click(stop_spinner);
    });
}