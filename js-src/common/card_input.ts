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


interface PaymentModalObject {
    modal: Element,
    payment_select: Element,
    main_elm: Element,
    pay_now_slider: Element,
    new_card: Element,
    saved_card: Element,
    card: Element,
    continue: HTMLButtonElement,
    back: HTMLButtonElement,
    save_card: HTMLInputElement
    tds_iframe: HTMLIFrameElement,
    order_num_elm: Element,
    loading_pulse: Element,
}

/**
 * @name instant_paynow
 * @description This function creates a modal that allows the user
 *              to pay instantly. This is a reusable component, so
 *              you can use it for other payments related stuff.  
 *              This differs from the other payment modal because
 *              This one doesnt require pre set up buttons or anything
 * @param {string} price_id - The price id (Event ID or 'subscription')
 * @param {string} title - The title of the modal
 * @param {string} description - The description of the modal
 * @param {string} item_name - The name of the item
 * @param {string} item_price - The price of the item
 * @param {() => void} stop - A function that will be called when the
 *                           modal is closed / the user is finished
 */
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

    // -- Get the elements
    const pmo: PaymentModalObject = {
        modal: modal,
        payment_select: modal.querySelector('.payment-select'),
        main_elm: modal.querySelector('.pay-now-modal'),
        pay_now_slider: modal.querySelector('.pay-now-slider'),
        new_card: modal.querySelector('.new-card'),
        saved_card: modal.querySelector('.saved-card'),
        card: modal.querySelector('.final-card'),
        continue: modal.querySelector('.yes') as HTMLButtonElement,
        back: modal.querySelector('.no') as HTMLButtonElement,
        save_card: modal.querySelector('.save-card') as HTMLInputElement,
        tds_iframe: modal.querySelector('.tds-iframe') as HTMLIFrameElement,
        order_num_elm: modal.querySelector('#order-num'),
        loading_pulse: modal.querySelector('.loading-pulse'),
    }

    // -- Hide the back button and disable the yes button
    pmo.continue.disabled = true;
    const payment_details = get_payment_details(pmo);
        
    // -- Add the event listener to the yes/no buttons
    let stage = 0;
    pmo.continue.addEventListener('click', async() => {
        if (stage === 2) { modal.remove(); return stop(); }
        switch_stage(++stage, price_id, pmo, payment_details);
    });


    // -- Event listener for the no button
    pmo.back.addEventListener('click', async() => {
        if (stage === 0) { modal.remove(); return stop(); }
        switch_stage(--stage, price_id, pmo, payment_details);
    });
}



/**
 * @name get_payment_details
 * @description This function adds all the saved cards,
 *              and an event listener to the new card button, this
 *              returns a function that can be called to get the 
 *              selected card
 * @param {PaymentModalObject} pmo - The payment modal object
 * @returns {() => PaymentIntentMethod} - A function that will return
 */
export async function get_payment_details(
    pmo: PaymentModalObject,
) {
    // -- Helper function to reload the saved payments dropdown
    let selected_card: PaymentIntentMethod;
    let saved_payment: PaymentIntentMethod;

    // -- Helper function to reload the saved payments dropdown
    const reload_saved = saved_payments_dropdown(pmo.modal, async (card: PaymentMethod) => {
        selected_card = card; saved_payment = card;
        pmo.continue.disabled = false;
    });

    // -- Helper function to show the new card form and set payment mode
    const read_card = read_card_modal(pmo.modal);
    pmo.new_card.addEventListener('click', () => {
        pmo.payment_select.setAttribute('data-mode', 'new');
        pmo.continue.disabled = true;
        read_card();
    });

    // -- Helper function to show the saved payments and set payment mode
    pmo.saved_card.addEventListener('click', () => {
        pmo.payment_select.setAttribute('data-mode', 'saved');
        selected_card = saved_payment;
        if (selected_card) pmo.continue.disabled = false;
        reload_saved();
    });


    // -- Preload the saved payments
    reload_saved();
    read_card();


    return () => {
        if (pmo.payment_select.getAttribute('data-mode') === 'new')
            return read_card();
        else return saved_payment;
    }
}



export async function switch_stage(
    stage: number,
    price_id: string,
    pmo: PaymentModalObject,
    payment_details: Promise<() => PaymentIntentMethod>,
) {
    let selected_card = (await payment_details)();

    switch (stage) {

        // -- Payment selection
        case 0:
            pmo.back.disabled = false;
            pmo.back.innerHTML = 'Cancel';
            return;


        // -- Payment confirmation
        case 1:
            // -- Check the payment mode and update the modal
            pmo.loading_pulse.setAttribute('loading-state', 'none');
            pmo.main_elm.setAttribute('data-mode', 'confirm');
            pmo.back.disabled = false;
            pmo.back.innerHTML = 'Back';

            // -- Create the card element
            const elm = create_new_card(fit_card(selected_card), false);
            pmo.card.innerHTML = elm.card.innerHTML;
            return;

 
        // -- Payment processing
        case 2:
            // -- Ask the user to confirm the payment
            const stop = attach(pmo.continue);
            pmo.loading_pulse.setAttribute('loading-state', 'loading');
            pmo.back.disabled = true;

            const data = Object.keys(selected_card).includes('id') ? (
            selected_card as PaymentMethod).id : {
                ...selected_card,
                save: pmo.save_card.checked
            } as Card & { save: boolean };

            // -- Create the payment intent
            const intent = await create_intent(price_id, data) as NewPaymentIntentSuccess;

            // -- Check for a 200
            if (intent.code !== 200) {
                pmo.back.disabled = false;
                create_toast('error', 'Oops!', intent.message);
                stop();
                return;
            }

            // -- Start the intent listener
            intent_listiner(intent.data.intent_id, 
                // -- If the intent is successful
                (pid) => {
                    pmo.loading_pulse.setAttribute('loading-state', 'none');
                    pmo.main_elm.setAttribute('data-mode', 'thank-you');
                    pmo.continue.innerHTML = 'Close';
                    pmo.continue.classList.remove('w-75');
                    pmo.continue.classList.add('w-100');
                    pmo.continue.disabled = false;
                    pmo.back.remove();

                    // -- Update the order number
                    pmo.order_num_elm.innerHTML = pid;
                    stop();
                }, 
                
                // -- If the intent is 3DS
                (url) => {
                    pmo.loading_pulse.setAttribute('loading-state', 'none');
                    pmo.main_elm.setAttribute('data-mode', 'tds');
                    pmo.tds_iframe.src = url;
                }, 

                // -- If the intent is an error
                () => {
                    pmo.loading_pulse.setAttribute('loading-state', 'none');
                    pmo.main_elm.setAttribute('data-mode', 'confirm');
                    pmo.back.disabled = false;
                    pmo.back.innerHTML = 'Back';
                    pmo.continue.disabled = false;
                }
            );
            return;
    }
}



async function intent_listiner(
    intent_id: string,
    success: (pid: string) => void,
    threeds: (url: string) => void,
    error: () => void,
    interval: number = 5000,    
) {
    
    let already_threeds = false,
        done = false;


    const check = async() => {
        // -- Check the intent
        const req = await check_intent(intent_id) as CheckPaymentIntentSuccess;


        // -- If the code is not 200, then return an error
        if (req.code !== 200) {
            done = true;
            create_toast('error', 'Oops!', req.message);
            return error();
        }


        // -- Check the progress of the intent
        const status = req.data.status;
        if (status === 'success') {
            done = true;
            create_toast('success', 'Success!', 'Payment verified!');
            return success(req.data.purchase_id);
        }


        // -- Intent requires action
        else if (
            status === 'requires_action' || 
            status === 'requires_confirmation'
        ) {
            if (already_threeds === false) {
                already_threeds = true;
                create_toast('warning', 'Success!', 'Youll have to verify your payment!');
                threeds(req.data.next_action);
            }
            return;
        }


        // -- Intent failed
        else {
            done = true;
            create_toast('error', 'Oops!', 'Payment failed!');
            return error();
        }
    };


    // -- Check the intent every x seconds
    const interval_id = setInterval(() => {
        if (done) return clearInterval(interval_id);
        else check();
    }, interval);
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