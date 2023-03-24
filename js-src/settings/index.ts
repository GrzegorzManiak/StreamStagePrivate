import { attach_event_listeners, get_pod } from './core/panels';
import { manage_security_panel } from './core/security';
import { manage_payments_panel } from './core/payments';
import { manage_subscription_panel } from './core/subscription';
import { manage_profile_panel } from './core/profile';
import { manage_reviews_panel } from './core/reviews';
import { get_or_error } from '../api/config';

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
    change_email: get_or_error<string>(config, 'data-change-email'),

    setup_mfa: get_or_error<string>(config, 'data-mfa-setup'),
    verify_mfa: get_or_error<string>(config, 'data-mfa-verify'),
    disable_mfa: get_or_error<string>(config, 'data-mfa-disable'),

    start_subscription: get_or_error<string>(config, 'data-start-subscription'),
    get_reviews: get_or_error<string>(config, 'data-get-reviews'),
    update_review: get_or_error<string>(config, 'data-update-review'),
    delete_review: get_or_error<string>(config, 'data-delete-review'),
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

const reviews_panel = get_pod('reviews');
if (reviews_panel) manage_reviews_panel(reviews_panel);