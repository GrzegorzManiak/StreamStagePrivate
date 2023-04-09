import { construct_modal } from './';
import { PaymentMethod, PaymentIntentMethod } from './index.d';


/**
 * @name card_type
 * @description This function returns the type of card
 *             that was passed in. eg 4242 4242 4242 4242 -> Visa
 * @param {string} card - The card number (can contain spaces)
 * @returns {string} - The card type
 */
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



/**
 * @name card_type_to_fontawesome
 * @description This function returns the fontawesome class
 * @param {string} card - The card type
 * @returns {string} - The fontawesome class
 */
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



/**
 * @name create_new_card
 * @description This function creates a new card element
 * @param {PaymentMethod} card - The card object
 * @param {boolean} remove_button - Whether to show the remove button
 * @returns {HTMLDivElement} - The card element
 * @returns {HTMLButtonElement} - The remove button
 */
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
  


/**
 * @name card_input
 * @description This function returns the card input element
 * @param {boolean} save_card - Whether to show the save card checkbox
 * @returns {string} - The card input element
 */
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



/**
 * @name card_modal
 * 
 * @description This function returns the card modal
 * @param {boolean} save_card - Whether to show the save card checkbox
 * @param {string} title - The title of the modal
 * @param {string} body - The body of the modal
 * @returns {string} - The card modal
 */
export const card_modal = (
    save_card: boolean = false,
    title: string = 'Add Card',
    body: string = 'Add a new card to your account',
) => construct_modal(title, body, true, 'primary', card_input(save_card));



/**
 * @name pay_now
 * @description Creates the HTML sting for the pay now modal 
 * TODO: Add callbacks for when the purchase is successful
 * 
 * @param {string} title - Title of the item (Preferrably just 'Pay now')
 * @param {string} body - Description of the item
 * @param {string} item - Name of the item
 * @param {string} cost - Cost of the item (You have to format it yourself)
 * @returns {string} - Returns the HTML for the modal
 */
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
                <div class='w-100 h-100 loading-pulse' loading-state='none'>
                    <i class="fas fs-1 fa-spinner fa-spin"></i>
                </div>
                <div class='w-100 h-100 d-flex flex-column justify-content-between'>
                    <div class='cards cards-slim w-100'><div class='w-100 final-card card-body p-2'></div></div>

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
                </div>
            </span>


            <span class='pay-tds d-flex justify-content-between flex-column'>
                <iframe 
                    class='tds-iframe'
                    id="tds-iframe" 
                    src="" 
                    style="width: 100%; height: 500px;"
                ></iframe>
            </span>

            <span class='pay-thank-you d-flex justify-content-between flex-column'>

                <div class="d-flex align-items-center justify-content-between flex-column h-100">
                    <h1 class="text-center text-success mb-0 d-flex flex-column mt-3">
                        <i class="fas fa-check-circle"></i>
                        Thank you for your purchase!
                    </h1>

                    <p class="
                        text-muted
                        text-center
                        m-0
                    ">
                        A confirmation email has been sent to your email address. 
                        Please take note of the order number for future reference.

                        <hr>

                        <span 
                            class='w-100 text-center text-muted' 
                            id='order-num'
                        ></span>
                    </p>
                </div>
            </span>

        </span>

    `
);



/**
    @name fit_card
    @param {PaymentIntentMethod} card
    @returns {PaymentMethod}

    @description This is a really simple funciton that takes in both 
    a Card object and a PaymentMethod object, and returns a PaymentMethod
    object. This is used to convert a Card object into a PaymentMethod object
    so that it can be used in the payment modal.
*/
export function fit_card(card: PaymentIntentMethod): PaymentMethod {
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