import { construct_modal } from '../../click_handler';
import { Card, PaymentMethod, SubscriptionMethod } from '../index.d';

export function card_type(card: string): string {
    // Visa: 4 (starts with 4)
    // Mastercard: 2 (first digit is 5, second digit is between 1 and 5)
    // American Express: 2 (first two digits are 34 or 37)
    // Discover: 4 (starts with 6011, or 65, or range between 622126-622925, 644-649)
    // Diners Club: 2 (first two digits are 30, 36, or 38)
    // JCB: 4 (starts with 2131 or 1800, or range between 3528-3589)
    // UnionPay: 2 (first two digits are 62)
    // Maestro: 4 (starts with 5018, 5020, 5038, 6304, 6759, 6761, 6762, 6763, 0604, or 6390, or range between 56-69)

    // -- Remove all non-digit characters from the card number
    const cleaned = card.replace(/\D/g, '');

    // -- Check the card type
    if (/^4/.test(cleaned)) return 'Visa';
    if (/^5[1-5]/.test(cleaned)) return 'Mastercard';
    if (/^3[47]/.test(cleaned)) return 'American Express';
    if (/^6(?:011|5[0-9])/.test(cleaned)) return 'Discover';
    if (/^3(?:0[0-5]|[68][0-9])/.test(cleaned)) return 'Diners Club';
    if (/^(?:2131|180)/.test(cleaned)) return 'JCB';
    if (/^62/.test(cleaned)) return 'UnionPay';
    if (/^(5018|5020|5038|6304|6759|6761|6762|6763|0604|6390)/.test(cleaned)) return 'Maestro';
    if (/^(56|57|58|59|60|61|62|63|64|65|66|67|68|69)/.test(cleaned)) return 'Maestro';
    return 'unknown';
}


export function card_type_to_fontawesome(card: string): string {
    switch (card) {
        case 'Visa': return 'fa-brands fa-cc-visa';
        case 'Mastercard': return 'fa-brands fa-cc-mastercard';
        case 'American Express': return 'fa-brands fa-cc-amex';
        case 'Discover': return 'fa-brands fa-cc-discover';
        case 'Diners Club': return 'fa-brands fa-cc-diners-club';
        case 'JCB': return 'fa-brands fa-cc-jcb';
        case 'UnionPay': return 'fa-brands fa-cc-jcb';
        case 'Maestro': return 'fa-brands fa-cc-jcb';
        default: return 'fas fa-credit-card';
    }
}


export function create_new_card(
    card: PaymentMethod,
    remove_button: boolean = true,
): {
    card: HTMLDivElement,
    button: HTMLButtonElement,
} {
    const cardBody = document.createElement('div');
    cardBody.className = `cards-body d-flex justify-content-between align-items-center gap-3`;

    cardBody.setAttribute('card-id', card.id);
    cardBody.setAttribute('card-brand', card.brand);
    cardBody.setAttribute('card-exp-month', card.exp_month.toString());
    cardBody.setAttribute('card-exp-year', card.exp_year.toString());
    cardBody.setAttribute('card-last4', card.last4);
    cardBody.setAttribute('card-created', card.created.toString());
    
    cardBody.innerHTML = `
    <div class="d-flex align-items-center main-card-detail">
        <div class="me-3 card-icon" card-type="${card.brand}">
            <i class="fas fa-credit-card" data-card='cartes_bancaires'></i>
            <i class="fas fa-credit-card" data-card='unionpay'></i>
            <i class="fa-brands fa-cc-amex" data-card='amex'></i>
            <i class="fa-brands fa-cc-diners-club" data-card='diners'></i>
            <i class="fa-brands fa-cc-discover" data-card='discover'></i>
            <i class="fa-brands fa-cc-jcb" data-card='jcb'></i>
            <i class="fa-brands fa-cc-mastercard" data-card='mastercard'></i>
            <i class="fa-brands fa-cc-visa" data-card='visa'></i>
        </div>
  
        <div>
            <p class="card-number">**** **** **** ${card.last4}</p>
            <p class="text-muted exp-date">Expires - ${card.exp_month}/${card.exp_year}</p>
        </div>
    </div>
  

    <div>
        <p class="text-muted card-added">Added - 
            ${new Date(card.created * 1000).toLocaleDateString()} at
            ${new Date(card.created * 1000).toLocaleTimeString()}
        </p>
    </div>

    ${remove_button ? `
    <div class="d-flex h-100 align-items-center">
        <button type="submit" id="remove-card" 
            class="mfa btn btn-danger btn-lg loader-btn error" loader-state='default'>
            <span>
                <div class='spinner-border' role='status'>
                    <span class='visually-hidden'>Loading...</span>
                </div>
            </span>
            <p>Remove</p>
        </button>
    </div>
    ` : ''}
    `;
    
    return {
        card: cardBody,
        button: cardBody.querySelector('#remove-card') as HTMLButtonElement,
    }
}
  


const card_input = (
    save_card: boolean = false,
) => `
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

        <div class="mt-3">
            ${save_card ? `
                <div class="form-check">
                    <input class="form-check-input save-card" type="checkbox" value="" id="save-card">
                    <label class="form-check-label" for="save-card">
                        <span class="text-muted">Save this card for future purchases</span>
                    </label>
                </div>
            ` : ''}
        </div>
    </div>
</div>
`


export const card_modal = (
    save_card: boolean = false,
    title: string = 'Add Card',
    body: string = 'Add a new card to your account',
) => construct_modal(title, body, true, 'primary', card_input(save_card));


export const tds_modal = (
    url: string,
) => construct_modal(
    '3D Secure',
    'Please complete the 3D Secure process to continue',
    false,
    'primary',
    `   
    <iframe 
        class='tds-iframe'
        id="tds-iframe" 
        src="${url}" 
        style="width: 100%; height: 500px;"
    ></iframe>

    <!-- Cancel Button -->
    <div class="d-flex h-100 align-items-center">
        <button type="submit" id="3ds-cancel" 
            class="mfa btn btn-danger btn-lg loader-btn error w-100" loader-state='default'>
            <span>
                <div class='spinner-border' role='status'>
                    <span class='visually-hidden'>Loading...</span>
                </div>
            </span>
            <p>Cancel</p>
        </button>
    </div>
    `
);


export const pay_now = (
    title: string = 'Pay now',
    body: string = 'Please enter your card details, or select a saved payment method.',
    item: string = 'StreamStage+',
    cost: string = '$9.99 Per Month',
) => construct_modal(
    title, body, true, 'primary',
    `   
        <span data-mode='select' class='pay-now-modal'>

            <span class='payment-select' data-mode='saved'>
                <div class="d-flex align-items-center justify-content-between pay-now-slider">
                    <h5 class="mb-0 saved-card">Saved Cards</h5>
                    <h5 class="mb-0 new-card">New Card</h5>
                </div>

                <hr>

                <div class="pay-now-body">
                    <div class='new-card'> ${card_input(true)} </div>
                    <div class='saved-card'> <div class='cards cards-slim'></div> </div>
                </div>
            </span>

            <span class='pay-confirm d-flex justify-content-between flex-column'>
                <div class='cards cards-slim'><div class='final-card card-body p-2'></div></div>

                <div class='pay-confirm-body'>
                    <p class='pay-confirm-item'>${item}</p>
                    <p class='pay-confirm-amount'>${cost}</p>
                </div>
                
                <div class="d-flex align-items-center">
                    <hr>
                    <!-- Terms -->
                    <p class="
                        text-muted
                        text-center
                        m-0
                    ">
                        By proceeding with this purchase, you agree to StreamStage's <a href='/terms'>terms and conditions</a>,
                        which includes refund policies, and the <a href='/privacy'>privacy policy</a>.
                        Additionally, you also agree to Stripe's <a href='https://stripe.com/'>terms and conditions</a>.
                    </p>
                </div>
            </span>

        </span>

        <p class='w-100 text-muted text-center go-back'> Go back </p>
    `
);



/*
    @name fit_card
    @param card: SubscriptionMethod 
    @returns PaymentMethod

    @description This is a really simple funciton that takes in both 
    a Card object and a PaymentMethod object, and returns a PaymentMethod
    object. This is used to convert a Card object into a PaymentMethod object
    so that it can be used in the payment modal.
*/
export function fit_card(card: SubscriptionMethod): PaymentMethod {
    if ('id' in card) return card;

    let brand = card_type(card.card),
        last4 = card.card.slice(-4);
        
    return {
        id: 'NEW',
        brand: brand,
        last4: last4,
        exp_month: card.exp_month,
        exp_year: card.exp_year,
        created: Date.now(),
    }
}