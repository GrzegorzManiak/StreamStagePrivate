import { Pod } from '../index.d';
import { instant_paynow } from '../../common/card_input';


/**
 * @param pod: Pod - The pod that this panel is attached to
 * 
 * @returns void
 * 
 * @description This function manages the subscriptions panel
 */
export function manage_subscription_panel(pod: Pod) {
    // -- Get the panel
    const panel = pod.panel.element;

    // -- Buttons
    const pay_button = panel.querySelector('[name="purchase-stream"]') as HTMLButtonElement,
        monthly_button = panel.querySelector('.monthly') as HTMLButtonElement,
        yearly_button = panel.querySelector('.annualy') as HTMLButtonElement;

    // -- Strip the buttons of the 'selected' class
    monthly_button.classList.remove('selected');
    yearly_button.classList.remove('selected');

    // -- Add the selected class to the Yearly button
    yearly_button.classList.add('selected');


    const ss_monthly = {
        id: 'ss_monthly',
        name: 'StreamStage+',
        description: 'A recurring monthly subscription to StreamStage+',
        item: 'Monthly Subscription',
        amount: '€9.99 / month',
    }

    const ss_yearly = {
        id: 'ss_yearly',
        name: 'StreamStage+',
        description: 'A recurring yearly subscription to StreamStage+ (Save 20%!)',
        item: 'Yearly Subscription',
        amount: '€99.99 / year',
    }
    


    let subscription = ss_yearly;

    // -- Add the event listeners to the buttons
    monthly_button.addEventListener('click', () => {
        monthly_button.classList.add('selected');
        yearly_button.classList.remove('selected');
        subscription = ss_monthly;
    });

    yearly_button.addEventListener('click', () => {
        yearly_button.classList.add('selected');
        monthly_button.classList.remove('selected');
        subscription = ss_yearly;
    });


    // -- Add the event listener to the pay now button
    pay_button.addEventListener('click', () => {
        instant_paynow(
            subscription.id, 
            subscription.name,
            subscription.description,
            subscription.item,
            subscription.amount
        );
    });
}

