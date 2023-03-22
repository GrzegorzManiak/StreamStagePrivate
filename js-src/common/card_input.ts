import { Card, GetCardsSuccess, PaymentIntentMethod, PaymentMethod } from './index.d';
import { card_type, card_type_to_fontawesome, create_new_card, fit_card, pay_now } from "./card";
import { attach, confirmation_modal, create_toast } from '.';
import { get_cards, remove_card } from './api';


export function read_card_modal(
    parent: HTMLElement | Element
): () => Card {
    // -- Get the buttons and inputs
    const submit_button = parent.querySelector('.yes') as HTMLButtonElement,
        cancel_button = parent.querySelector('.no') as HTMLButtonElement,
        card_number = parent.querySelector('#cardnumber') as HTMLInputElement,
        card_expiry = parent.querySelector('#card-expiry') as HTMLInputElement,
        card_cvc = parent.querySelector('#card-cvc') as HTMLInputElement,
        card_name = parent.querySelector('#card-name') as HTMLInputElement;
    cancel_button.addEventListener('click', () => parent.remove());
    
    //
    // -- Add the event listeners to the inputs
    //    checks if the values are valid
    //
    const check = () => {
        // -- Check if the values are valid
        if (card_number.value.length < 13 || card_expiry.value.length < 5 || 
            card_cvc.value.length < 3 || card_name.value.length < 3
        ) return submit_button.disabled = true;
        return submit_button.disabled = false;
    };
    const inputs = [card_number, card_expiry, card_cvc, card_name];
    inputs.forEach(input => input.addEventListener('input', check));
    check();



    //
    // -- Card type
    //
    const card_type_elm = parent.querySelector('.card-type') as HTMLDivElement,
        card_type_icon = card_type_elm.querySelector('i') as HTMLDivElement;

    card_number.addEventListener('input', () => {
        // -- Get the card type
        const type = card_type(card_number.value);
        card_type_icon.className = card_type_to_fontawesome(type) + ' align-self-center';

        // -- Every 4th character, add a space
        const cleaned = card_number.value.replace(/\D/g, '');
        card_number.value = cleaned.replace(/(\d{4})/g, '$1 ').trim();
    });


    //
    // -- Card expiry
    //
    card_expiry.addEventListener('keydown', (e) => {
        // -- Ignore if the key is not a number
        if (e.key.length > 1) return;

        // -- Every 2nd character, add a slash
        const cleaned = card_expiry.value.replace(/\D/g, '');
        card_expiry.value = cleaned.replace(/(^\d{2})/g, '$1/').slice(0, 6);
    });

    

    // -- Return the function
    return () => {
        // -- Check if the values are valid
        check();
        
        // -- Get the expiry date
        const expiry = card_expiry.value.split('/');

        // -- Return the card
        return {
            card: card_number.value,
            exp_month: parseInt(expiry[0]),
            exp_year: parseInt(expiry[1]),
            cvc: card_cvc.value,
            name: card_name.value
        };
    }
}




/**
 * @name saved_payments_dropdown
 * @description This function manages the saved payments dropdown
 *              Look for '<!-- Saved Cards -->' for the HTML, this
 *              is a reusable component, so you can use it for other
 *              payments related stuff.
 * @param {HTMLElement | Element} parent - The parent element
 * @returns {() => void} - A function that will reload the cards
 *                        (useful when the cards get updated)
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
    button: HTMLButtonElement,
    title: string = 'Pay Now',
    description: string = 'You will be charged $9.99 USD / month',
    item_name: string = 'Monthly Subscription',
    item_price: string = '$9.99 USD / month'
) {
    const on_click = (stop: () => {}) => {
        const modal = document.createElement('div');
        let selected_card: PaymentIntentMethod,
            saved_payment: PaymentIntentMethod;
        modal.innerHTML = pay_now(title, description, item_name, item_price);
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




export async function load_cards(
    element: HTMLElement | Element, 
    remove: boolean = true
) {

    // -- Get the cards
    const cards = await get_cards();
    
    // -- Check if the request was successful
    if (cards.code !== 200) {
        // -- Show the error
        return create_toast(
            'error', 
            'verification', 
            'There was an error while trying to get your cards, please try again later.'
        );
    }

    // -- Get the cards object and the cards container
    const cards_object = (cards as GetCardsSuccess).data,
        cards_container = element.querySelector('.cards') as HTMLDivElement;

    // -- Clear the cards container
    cards_container.innerHTML = '';

    // -- Check if there are no cards
    console.log(cards_object.length);
    if (cards_object.length === 0) 
        cards_container.innerHTML = '<div class="no-cards w-100 h-100 d-flex justify-content-center align-items-center"><h3 class="text-center">You have no cards saved</h3></div>';

    // -- Create the cards
    cards_object.forEach(card => {
        const elm = create_new_card(card, remove);
        cards_container.appendChild(elm.card);

        // -- Add the event listener to the remove button
        if (remove)
        elm.button.addEventListener('click', async () => {
            // -- Attach the spinner
            const stop = attach(elm.button);

            confirmation_modal(
                async () => {
                    // -- Remove the card
                    const response = await remove_card(card.id);
                    if (response.code !== 200) create_toast(
                        'error', 
                        'Payments', 
                        'There was an error while trying to remove your card, please try again later.'
                    );
                    
                    else {
                        // -- Remove the card
                        elm.card.remove();
                        elm.card.remove();

                        // -- Show the success toast
                        create_toast(
                            'success',
                            'Payments',
                            'Success! We have removed your card!'
                        );
                    }

                    // -- Stop the spinner
                    stop();
                },
                () => stop(),
                'Are you sure you want to remove this card?'
            )
        });
    });
}