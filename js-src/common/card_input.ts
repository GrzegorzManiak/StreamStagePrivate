import { Card, CheckPaymentIntentSuccess, GetCardsSuccess, NewPaymentIntentSuccess, PaymentIntentMethod, PaymentMethod } from './index.d';
import { card_type, card_type_to_fontawesome, create_new_card, fit_card, pay_now } from "./card";
import { attach, confirmation_modal, create_toast, sleep } from '.';
import { check_intent, create_intent, get_cards, remove_card } from './api';


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



export async function instant_paynow(
    price_id: string,
    title: string = 'Pay Now',
    description: string = 'You will be charged $9.99 USD / month',
    item_name: string = 'Monthly Subscription',
    item_price: string = '$9.99 USD / month',
    stop: () => void = () => {},
) {
    // -- Create the modal and append it to the document body
    const modal = document.createElement('div');
    modal.innerHTML = pay_now(title, description, item_name, item_price);
    document.body.appendChild(modal);

    // -- Initialize payment method and payment confirmation variables
    let selected_card: PaymentIntentMethod;
    let saved_payment: PaymentIntentMethod;

    // -- Initialize modal elements
    const payment_select = modal.querySelector('.payment-select'),
        main_elm = modal.querySelector('.pay-now-modal'),
        pay_now_slider = payment_select.querySelector('.pay-now-slider'),
        new_card = pay_now_slider.querySelector('.new-card'),
        saved_card = pay_now_slider.querySelector('.saved-card'),
        card = modal.querySelector('.final-card'),
        yes = modal.querySelector('.yes') as HTMLButtonElement,
        no = modal.querySelector('.no') as HTMLButtonElement,
        back = modal.querySelector('.go-back') as HTMLButtonElement,
        save_card = modal.querySelector('.save-card') as HTMLInputElement;

    // -- Hide the back button and disable the yes button
    back.style.display = 'none';
    yes.disabled = true;

    // -- Helper function to reload the saved payments dropdown
    const reload_saved = saved_payments_dropdown(modal, async (card: PaymentMethod) => {
        selected_card = card;
        saved_payment = card;
        yes.disabled = false;
    });
    reload_saved();

    // Helper function to show the new card form and set payment mode
    const read_card = read_card_modal(modal);
    new_card.addEventListener('click', () => {
        payment_select.setAttribute('data-mode', 'new');
        yes.disabled = true;
        read_card();
    });

    // Helper function to show the saved payments and set payment mode
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
                // -- Check the payment mode and update the modal
                const mode = payment_select.getAttribute('data-mode');
                if (mode === 'new') selected_card = read_card();
                main_elm.setAttribute('data-mode', 'confirm');
                back.style.display = 'block';
                no.disabled = false;

                // -- Add the selected payment method to the confirm modal
                const elm = create_new_card(fit_card(selected_card), false);
                card.innerHTML = elm.card.innerHTML;
                stage = 1;
                break;

            case 1:
                // -- Ask the user to confirm the payment
                const stop = attach(yes);
                no.disabled = true;
                back.style.display = 'none';

                const data = Object.keys(selected_card).includes('id') ? (
                selected_card as PaymentMethod).id : {
                    ...selected_card,
                    save: save_card.checked
                } as Card & { save: boolean };

                // -- Create the payment intent
                const intent = await create_intent(price_id, data) as NewPaymentIntentSuccess;

                // -- Check for a 200
                if (intent.code !== 200) {
                    create_toast('error', 'Oops!', intent.message);
                    stop();
                    no.disabled = false;
                    back.style.display = 'block';
                    return;
                }

                create_toast('success', 'Success!', 'Payment successful! Checking for verification...');
                let threeds = false;

                while (true) {
                    // -- Check the intent
                    const check = await check_intent(intent.data.intent_id) as CheckPaymentIntentSuccess;

                    if (check.code !== 200) {
                        create_toast('error', 'Oops!', check.message);
                        stop();
                        no.disabled = false;
                        back.style.display = 'block';
                        threeds = false;
                        return;
                    }

                    // -- Check if the intent is verified
                    const status = check.data.status;
                    if (status === 'success') {
                        create_toast('success', 'Success!', 'Payment verified!');
                        modal.remove();
                        stop();
                        return;
                    }

                    // -- Intent requires action
                    else if (status === 'requires_action' && threeds === false) {
                        threeds = true;
                        const action = check.data.next_action;

                        // -- Open the 3DS modal
                        const win = window.open(action, '_blank', 'directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,width=600,height=700');
                        if (win) win.focus();

                        // -- Sleep for 5 seconds
                        await sleep(5000);
                    }

                    if (['success', 'requires_action', 'requires_confirmation'].includes(status) === false) {
                        console.log(status);
                        create_toast('error', 'Oops!', 'Payment failed!');
                        stop();
                        no.disabled = false;
                        threeds = false;
                        back.style.display = 'block';
                        return;
                    }

                    // -- Sleep for 5 seconds
                    await sleep(5000);
                }
        }
    });


    // -- Event listener for the no button
    no.addEventListener('click', () => {
        if (stage === 0) return stop();
        
        // -- If user clicked no at the second stage, go back to the previous stage
        main_elm.setAttribute('data-mode', 'select');
        back.style.display = 'none';
        no.disabled = true;
        yes.disabled = true;
        stage = 0;
    });
    

    // -- Event listener for the back button
    back.addEventListener('click', () => {
        main_elm.setAttribute('data-mode', 'select');
        back.style.display = 'none';
        no.disabled = true;
        yes.disabled = true;
        stage = 0;
    });
}





export function manage_paynow(
    price_id: string,
    button: HTMLButtonElement,
    title: string = 'Pay Now',
    description: string = 'You will be charged $9.99 USD / month',
    item_name: string = 'Monthly Subscription',
    item_price: string = '$9.99 USD / month'
) {
    const on_click = (stop: () => {}) => {
        instant_paynow(price_id, title, description, item_name, item_price, stop);
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