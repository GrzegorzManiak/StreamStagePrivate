import { construct_modal } from '../../click_handler';
import { PaymentMethod } from '../index.d';

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
    cardBody.className = `cards-body d-flex justify-content-between align-items-center`;
    cardBody.setAttribute('payment-id', card.id);
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
  

    <div class="ms-3">
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
  


export const card_modal = construct_modal(
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