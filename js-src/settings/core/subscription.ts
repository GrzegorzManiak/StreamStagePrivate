import { Pod } from '../index.d';

import { manage_paynow } from '../../click_handler';

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

    // -- Pay button
    const pay_button = panel.querySelector('.pay-now') as HTMLButtonElement;
    manage_paynow(pay_button);
}
