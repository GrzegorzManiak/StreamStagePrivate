import { attach, confirmation_modal } from '../../click_handler';
import { create_toast } from '../../toasts';
import { add_card, get_cards, remove_card } from '../apis';
import { card_modal, card_type, card_type_to_fontawesome, create_new_card } from '../elements/card';
import { Card, GetCardsSuccess, Pod } from '../index.d';

/**
 * @param pod: Pod - The pod that this panel is attached to
 * 
 * @returns void
 * 
 * @description This function manages the payments panel
 */
export function manage_payments_panel(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

    manage_add_card(pod);
    load_cards(panel);
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

export function manage_add_card(pod: Pod) {
    // -- Get the panel and the add card button
    const panel = pod.panel.element,
        add_card_button = panel.querySelector('#add-card') as HTMLButtonElement;

    // -- Add the event listener to the add card button
    add_card_button.addEventListener('click', async() => {
        // -- Add the modal to the body
        const modal_div = document.createElement('div');
        modal_div.innerHTML = card_modal();
        document.body.appendChild(modal_div);
        
        const submit_button = modal_div.querySelector('.yes') as HTMLButtonElement;
        const card_manager = read_card_modal(modal_div);

        //
        // -- Add the event listeners to the 
        //    submit and cancel buttons
        //
        submit_button.addEventListener('click', async () => {
            // -- Attach the spinner
            const stop = attach(submit_button);

            // -- Add the card
            const response = await add_card(card_manager());

            // -- Check if the request was successful
            if (response.code !== 200) return create_toast(
                'error', 'Payments', response.message);
            
            // -- Show the success toast
            create_toast('success', 'Payments', 'Success! We have added your card!');
            modal_div.remove();
            load_cards(panel);
            stop();
        });
    });
}



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