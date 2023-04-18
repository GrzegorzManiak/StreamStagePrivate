import { GetSubscriptionSuccess, Pod } from '../index.d';
import { instant_paynow } from '../../common/card_input';
import { configuration } from '..';
import { confirmation_modal, create_toast } from '../../common';
import { cancel_subscription, get_subscription } from '../apis';


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
    let subscribed = configuration.is_subscribed;

    // -- Buttons
    const pay_button = panel.querySelector('[name="purchase-stream"]') as HTMLButtonElement,
        monthly_button = panel.querySelector('.monthly') as HTMLButtonElement,
        yearly_button = panel.querySelector('.annualy') as HTMLButtonElement,
        unsubscribe_button = panel.querySelector('[name="unsubscribe"]') as HTMLButtonElement;

    // -- Strip the buttons of the 'selected' class
    monthly_button.classList.remove('selected');
    yearly_button.classList.remove('selected');

    // -- Add the selected class to the Yearly button
    yearly_button.classList.add('selected');
    manage_sub(panel, subscribed, unsubscribe_button);

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


    unsubscribe_button.disabled = true;
    unsubscribe_button.addEventListener('click', () => {
        confirmation_modal(
            async() => {
                const res = await cancel_subscription();
                if (res.code !== 200) return create_toast('error', 'Subscription', res.message);
                create_toast('success', 'Subscription', 'You have successfully unsubscribed from StreamStage+');
                manage_sub(panel, subscribed, unsubscribe_button);
            }, 
            () => {}, 
            'By clicking "Yes" you will be unsubscribed from StreamStage+, you will retain access to StreamStage+ until the end of your current billing cycle. You will not be charged again after this period. Are you sure you want to unsubscribe?',
            'Unsubscribe',
        );
    });


    // -- Add the event listener to the pay now button
    pay_button.addEventListener('click', () => {
        instant_paynow(
            subscription.id, 
            subscription.name,
            subscription.description,
            subscription.item,
            subscription.amount,
            () => {},
            async(success) => {
                // -- Check if the subscription is active
                subscribed = success;
                manage_sub(panel, subscribed, unsubscribe_button);
            }
        );
    });
}



async function manage_sub(
    panel: Element,
    subscribed: boolean,
    button: HTMLButtonElement
) {
    // -- Inform the user
    const subscribed_panel = panel.querySelector('#subscribed') as HTMLDivElement,
        unsubscribed_panel = panel.querySelector('#not-subscribed') as HTMLDivElement;

    // -- Check if the user is subscribed
    subscribed_panel.style.display = subscribed ? 'block' : 'none';
    unsubscribed_panel.style.display = subscribed ? 'none' : 'block';
    
    // -- Sub details
    const sub_on = panel.querySelector('#subscribed-on') as HTMLDivElement,
        sub_ends = panel.querySelector('#subscribed-end') as HTMLDivElement,
        plan = panel.querySelector('#plan') as HTMLDivElement,
        un_subbed = panel.querySelector('#unsubscribed') as HTMLDivElement,
        thank_you = panel.querySelector('#thank-you') as HTMLDivElement;

    // -- Are we subscribed?
    if (!subscribed) return;

    // -- Get the subscription details
    const res = await get_subscription() as GetSubscriptionSuccess;
    if (res.code !== 200) return create_toast('error', 'Subscription', res.message);

    // -- Set the subscription details
    let sub_on_date = new Date(Number(res.data.subscription_start) * 1000);
    sub_on.innerHTML = `${sub_on_date.toLocaleDateString()}`;

    let sub_ends_date = new Date(Number(res.data.subscription_end) * 1000);
    sub_ends.innerHTML = `${sub_ends_date.toLocaleDateString()}`;
    
    plan.innerHTML = `${res.data.subscription_status}`;
    
    // -- Check if the subscription is active
    un_subbed.style.display = res.data.subscription_status === 'none' ? 'block' : 'none';
    thank_you.style.display = res.data.subscription_status === 'none' ? 'none' : 'block';
    button.disabled = res.data.subscription_status === 'none' ? true : false;
}