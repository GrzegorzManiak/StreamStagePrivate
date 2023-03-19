import { attach_event_listeners, get_pod } from './core/panels';
import { manage_security_panel } from './core/security';
import { create_toast } from '../toasts';
import { manage_payments_panel } from './core/payments';
import { manage_subscription_panel } from './core/subscription';
import { manage_profile_panel } from './core/profile';

export function get_or_error<e>(element: HTMLElement, attribute: string): e {
    const value = element.getAttribute(attribute);
    if (!value) {
        create_toast('error', 'Configuration Error', `No ${attribute} found, please reload the page`);
        // -- Wait 3 seconds and reload the page
        setTimeout(() => {
            window.location.reload();
        }, 3000);
    }
    return value as unknown as e;
}

const config = document.getElementById('config');

export const configuration = {
    admin: get_or_error<string>(config, 'data-admin') === 'True',
    username: get_or_error<string>(config, 'data-username'),
    userid: get_or_error<number>(config, 'data-userid'),
    useremail: get_or_error<string>(config, 'data-useremail'),
    userfirst: get_or_error<string>(config, 'data-userfirst'),
    userlast: get_or_error<string>(config, 'data-userlast'),
    access_level: get_or_error<number>(config, 'data-access-level'),
    profile_picture: get_or_error<string>(config, 'data-profile-picture'),
    csrf_token: get_or_error<string>(config, 'data-csrf-token'),

    send_verification: get_or_error<string>(config, 'data-send-verification'),
    resend_verification: get_or_error<string>(config, 'data-resend-verification'),
    remove_verification: get_or_error<string>(config, 'data-remove-verification'),
    recent_verification: get_or_error<string>(config, 'data-recent-verification'),

    security_info: get_or_error<string>(config, 'data-security-info'),
    update_profile: get_or_error<string>(config, 'data-update-profile'),
    remove_oauth: get_or_error<string>(config, 'data-remove-oauth'),
    extend_session: get_or_error<string>(config, 'data-extend-session'),
    close_session: get_or_error<string>(config, 'data-close-session'),

    setup_mfa: get_or_error<string>(config, 'data-mfa-setup'),
    verify_mfa: get_or_error<string>(config, 'data-mfa-verify'),
    disable_mfa: get_or_error<string>(config, 'data-mfa-disable'),

    add_payment: get_or_error<string>(config, 'data-add-payment'),
    get_payments: get_or_error<string>(config, 'data-get-payments'),
    remove_payment: get_or_error<string>(config, 'data-remove-payment'),

    start_subscription: get_or_error<string>(config, 'data-start-subscription'),
}


// -- Attach the event listeners
attach_event_listeners();


// -- Attach to all panels
const security_panel = get_pod('security');
if (security_panel) manage_security_panel(security_panel);

const payments_panel = get_pod('payment');
if (payments_panel) manage_payments_panel(payments_panel);

const subscription_panel = get_pod('streamstageplus');
if (subscription_panel) manage_subscription_panel(subscription_panel);

const profile_panel = get_pod('profile');
if (profile_panel) manage_profile_panel(profile_panel);