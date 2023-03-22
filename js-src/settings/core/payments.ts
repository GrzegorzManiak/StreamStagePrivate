import { attach, create_toast } from '../../common';
import { add_card } from '../../common/api';
import { card_modal } from '../../common/card';
import { load_cards, read_card_modal } from '../../common/card_input';
import { Pod } from '../index.d';

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
