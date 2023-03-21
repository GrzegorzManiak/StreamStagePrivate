import { sleep } from "../click_handler";
import { hide_element, show_element } from "./index";

// export function manage_(
//     button: HTMLButtonElement,
//     title: string = 'Pay Now',
//     description: string = 'You will be charged $9.99 USD / month',
//     item_name: string = 'Monthly Subscription',
//     item_price: string = '$9.99 USD / month'
// ) {
//     const on_click = (stop: () => {}) => {
//         const modal = document.createElement('div');
//         let selected_card: SubscriptionMethod,
//             saved_payment: SubscriptionMethod;

//         modal.innerHTML = pay_now(title, description, item_name, item_price);
//         document.body.appendChild(modal);

//         // -- yes / no buttons
//         const yes = modal.querySelector('.yes') as HTMLButtonElement,
//             no = modal.querySelector('.no') as HTMLButtonElement,
//             back = modal.querySelector('.go-back') as HTMLButtonElement;

//         back.style.display = 'none';
//         yes.disabled = true;

//         // -- Saved payments list and new card form readers and the 'save-card' checkbox
//         const reload_saved = saved_payments_dropdown(modal, async(card: PaymentMethod) => {
//             selected_card = card;
//             saved_payment = card;
//             yes.disabled = false;
//         }), read_card = read_card_modal(modal),
//             save_card = modal.querySelector('.save-card') as HTMLInputElement;
//         reload_saved();


//         // -- Grab the main elements .payment-select
//         const payment_select = modal.querySelector('.payment-select'),
//             main_elm = modal.querySelector('.pay-now-modal'),
//             confirm = modal.querySelector('.pay-confirm');

//         // -- Grab the payment mode buttons, .pay-now-slider
//         const pay_now_slider = payment_select.querySelector('.pay-now-slider'),
//             new_card = pay_now_slider.querySelector('.new-card'),
//             saved_card = pay_now_slider.querySelector('.saved-card'),
//             card = modal.querySelector('.final-card');
        

//         // -- Add the event listener to the new card button
//         new_card.addEventListener('click', () => {
//             payment_select.setAttribute('data-mode', 'new');
//             yes.disabled = true;
//             read_card();
//         });

//         saved_card.addEventListener('click', () => {
//             payment_select.setAttribute('data-mode', 'saved');
//             selected_card = saved_payment;
//             if (selected_card) yes.disabled = false;
//             reload_saved();
//         });

            
//         // -- Add the event listener to the yes/no buttons
//         let stage = 0;
//         yes.addEventListener('click', async() => {
//             switch (stage) {
//                 case 0: 
//                     // -- Check the mode of the payment
//                     let mode = payment_select.getAttribute('data-mode');
//                     if (mode === 'new') selected_card = read_card();
//                     main_elm.setAttribute('data-mode', 'confirm');
//                     back.style.display = 'block';

//                     // -- Add the card to the confirm modal
//                     const elm = create_new_card(fit_card(selected_card), false);
//                     card.innerHTML = elm.card.innerHTML;

//                     break;

//                 case 1:
//                     // -- Ask the user to confirm the payment
                    
//                     break;
//             }
//         });

//         back.addEventListener('click', () => {
//             main_elm.setAttribute('data-mode', 'select');
//             back.style.display = 'none';
//             stage = 0;
//         });

//         // -- 'no' event listner
//         no.addEventListener('click', () => {
//             stop()
//         });
//     };


//     // -- Attatch the click function
//     button.addEventListener('click', () => {
//         const stop_spinner = attach(button);

//         // -- Open up the modal
//         on_click(stop_spinner);
//     });
// }


export function manage_override_btn(
    btn: HTMLButtonElement,
    add_review_panel: HTMLElement
) {
    const click = () => {
        show_element(add_review_panel);
        hide_element(btn);
    }

    btn.addEventListener("click", click);
}

export function manage_add_review_btn(
    btn: HTMLButtonElement,
    add_review_panel: HTMLElement
) {
    const click = () => {
        show_element(add_review_panel);
        hide_element(btn);
    }

    btn.addEventListener("click", click);
}

export function manage_add_review_panel(
    panel: HTMLElement,
    can_review: boolean
) {
    
    if (!can_review) {
        hide_element(panel);
        return;
    }

}

