import { attach, confirmation_modal, construct_modal } from '../../click_handler';
import { create_toast } from '../../toasts';
import { add_card, get_cards, remove_card } from '../apis';
import { card_type, card_type_to_fontawesome, create_new_card } from '../elements/card';
import { GetCardsSuccess, Pod } from '../index.d';

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
    load_cards(pod);
}

async function load_cards(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

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
        cards_container = panel.querySelector('.cards') as HTMLDivElement;

    // -- Clear the cards container
    cards_container.innerHTML = '';

    // -- Create the cards
    cards_object.forEach(card => {
        const elm = create_new_card(card);
        cards_container.appendChild(elm.card);

        // -- Add the event listener to the remove button
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

function manage_add_card(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

    // -- Get the add card button
    const add_card_button = panel.querySelector('#add-card') as HTMLButtonElement;

    add_card_button.addEventListener('click', async() => {
        
        // -- Construct the form
        const modal = construct_modal(
            'Add Card',
            'Add a new card to your account',
            true,
            'primary',
            `
            <div class="add-card-details">
                <div class="mb-5">
             
             
                    <label class="form-label d-flex" for="card-number">
                        <span class="card-type col-1 d-flex"><i class="fas fa-credit-card align-self-center"></i></span>
                        Card Number
                    </label>

                    <input name="card_number" autocomplete='on' id="cardnumber" placeholder="1234 5678 9101 1123" class="form-control form-control-lg inp">


                    <div class="row mt-3">
                        <div class="col">
                            <label class="form-label" for="card-expiry">Expiry</label>
                            <input name="exp" autocomplete='on' id="card-expiry" placeholder="MM/YY" class="form-control form-control-lg inp">
                        </div>

                        <div class="col">
                            <label class="form-label" for="card-cvc">CVC</label>
                            <input type="password" maxlength="4" name="cvc" autocomplete='on' id="card-cvc" placeholder="***" class="form-control form-control-lg inp">
                        </div>
                    </div>

                    <div class="mt-3">
                        <label class="form-label" for="card-name">Name</label>
                        <input name="name" autocomplete='on' id="card-name" placeholder="John Doe" class="form-control form-control-lg inp">
                    </div>
                </div>
            </div>
            `
        );

        const modal_div = document.createElement('div');
        modal_div.innerHTML = modal;
        document.body.appendChild(modal_div);

        // -- Get the buttons
        const submit_button = modal_div.querySelector('.yes') as HTMLButtonElement,
            cancel_button = modal_div.querySelector('.no') as HTMLButtonElement;

        // -- Get the inputs
        const card_number = modal_div.querySelector('#cardnumber') as HTMLInputElement,
            card_expiry = modal_div.querySelector('#card-expiry') as HTMLInputElement,
            card_cvc = modal_div.querySelector('#card-cvc') as HTMLInputElement,
            card_name = modal_div.querySelector('#card-name') as HTMLInputElement;

        // -- Add the event listeners
        const check = () => {
            // -- Get the values
            const card_number_value = card_number.value,
                card_expiry_value = card_expiry.value,
                card_cvc_value = card_cvc.value,
                card_name_value = card_name.value;

            // -- Check if the values are valid
            if (
                card_number_value.length < 13 ||
                card_expiry_value.length < 5 || 
                card_cvc_value.length < 3 || 
                card_name_value.length < 3
            ) return submit_button.disabled = true;
            return submit_button.disabled = false;
        };
        const inputs = [card_number, card_expiry, card_cvc, card_name];
        inputs.forEach(input => input.addEventListener('input', check));
        check();

        //
        // -- Card type
        //
        const card_type_elm = modal_div.querySelector('.card-type') as HTMLDivElement,
            card_type_icon = card_type_elm.querySelector('i') as HTMLDivElement;

        card_number.addEventListener('input', () => {
            // -- Get the value
            const card_number_value = card_number.value;

            // -- Get the card type
            const type = card_type(card_number_value),
                icon = card_type_to_fontawesome(type);

            // -- Set the icon
            card_type_icon.className = icon + ' align-self-center';


            // -- Every 4th character, add a space
            const cleaned = card_number.value.replace(/\D/g, ''),
                spaced = cleaned.replace(/(\d{4})/g, '$1 ');

            // -- Trim any extra spaces at the end
            card_number.value = spaced.trim();
        });



        //
        // -- Card expiry
        //
        card_expiry.addEventListener('keydown', (e) => {
            // -- Ignore if the key is not a number
            if (e.key.length > 1) return;

            // -- Get the value
            const card_expiry_value = card_expiry.value;

            // -- Every 2nd character, add a slash
            const cleaned = card_expiry_value.replace(/\D/g, '');
            let formatted = cleaned.replace(/(\d{2})/g, '$1/');

            // -- rim any extra digits after the last 4
            card_expiry.value = formatted.slice(0, 6);
        });

        

        // -- Add the event listeners
        cancel_button.addEventListener('click', () => modal_div.remove());
        submit_button.addEventListener('click', async () => {
            // -- Attach the spinner
            const stop = attach(submit_button);
        
            // -- Get the expiry date
            const expiry = card_expiry.value.split('/');

            // -- Add the card
            const response = await add_card({
                card: card_number.value,
                exp_month: parseInt(expiry[0]),
                exp_year: parseInt(expiry[1]),
                cvc: card_cvc.value,
                name: card_name.value
            });

            // -- Check if the request was successful
            if (response.code !== 200) return create_toast(
                'error', 'Payments', response.message);
            
            // -- Show the success toast
            create_toast('success', 'Payments', 'Success! We have added your card!');
            modal_div.remove();
            load_cards(pod);
            stop();
        });

    });
}