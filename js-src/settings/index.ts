import { single } from '../common/single';
single('settings');

import { attach_event_listeners, get_pod, set_sidebar_state } from './core/panels';
import { manage_security_panel } from './core/security';
import { manage_payments_panel } from './core/payments';
import { manage_subscription_panel } from './core/subscription';
import { manage_profile_panel } from './core/profile';
import { manage_reviews_panel } from './core/reviews';
import { Type, build_configuration } from '../api/config';
import { Configuration } from './index.d';
import { manage_purchases_panel } from './core/pruchases';
import { manage_ticekts_panel } from './core/tickets';

export const configuration = build_configuration<Configuration>({
    admin: new Type('data-admin', 'boolean'),
    imposter: new Type('data-imposter', 'boolean'),
    username: new Type('data-username', 'string'),
    userid: new Type('data-userid', 'string'),
    useremail: new Type('data-useremail', 'string'),
    userfirst: new Type('data-userfirst', 'string'),
    userlast: new Type('data-userlast', 'string'),
    access_level: new Type('data-access-level', 'number'),
    profile_picture: new Type('data-profile-picture', 'string'),
    banner_picture: new Type('data-banner-picture', 'string'),
    csrf_token: new Type('data-csrf-token', 'string'),

    send_verification: new Type('data-send-verification', 'string'),
    resend_verification: new Type('data-resend-verification', 'string'),
    remove_verification: new Type('data-remove-verification', 'string'),
    recent_verification: new Type('data-recent-verification', 'string'),
    
    security_info: new Type('data-security-info', 'string'),
    update_profile: new Type('data-update-profile', 'string'),
    remove_oauth: new Type('data-remove-oauth', 'string'),
    extend_session: new Type('data-extend-session', 'string'),
    close_session: new Type('data-close-session', 'string'),
    change_email: new Type('data-change-email', 'string'),

    setup_mfa: new Type('data-mfa-setup', 'string'),
    verify_mfa: new Type('data-mfa-verify', 'string'),
    disable_mfa: new Type('data-mfa-disable', 'string'),

    start_subscription: new Type('data-start-subscription', 'string'),
    get_reviews: new Type('data-get-reviews', 'string'),
    update_review: new Type('data-update-review', 'string'),
    delete_review: new Type('data-delete-review', 'string'),

    change_img: new Type('data-change-picture', 'string'),

    is_subscribed: new Type('data-is-subscribed', 'boolean'),
    get_subscription: new Type('data-get-subscription', 'string'),
    cancel_subscription: new Type('data-cancel-subscription', 'string'),
    filter_purchases: new Type('data-filter-purchases', 'string'),

    get_tickets: new Type('data-get-tickets', 'string'),
});

// -- Attach the event listeners and open the left panel
attach_event_listeners();
set_sidebar_state('open');

// -- Attach to all panels
try {
    const security_panel = get_pod('security');
    if (security_panel) manage_security_panel(security_panel);
    console.log('security_panel', security_panel);
} catch (e) { console.error(e); }

try {
    const payments_panel = get_pod('payment');
    if (payments_panel) manage_payments_panel(payments_panel);
    console.log('payments_panel', payments_panel);
} catch (e) { console.error(e); }

try {
    const subscription_panel = get_pod('streamstageplus');
    if (subscription_panel) manage_subscription_panel(subscription_panel);
    console.log('subscription_panel', subscription_panel);
} catch (e) { console.error(e); }

try {
    const profile_panel = get_pod('profile');
    if (profile_panel) manage_profile_panel(profile_panel);
    console.log('profile_panel', profile_panel);
} catch (e) { console.error(e); }

try {
    const reviews_panel = get_pod('reviews');
    if (reviews_panel) manage_reviews_panel(reviews_panel);
    console.log('reviews_panel', reviews_panel);
} catch (e) { console.error(e); }

try {
    const purchases_panel = get_pod('purchases');
    if (purchases_panel) manage_purchases_panel(purchases_panel);
    console.log('purchases_panel', purchases_panel);
} catch (e) { console.error(e); }

try {
    const tickets_panel = get_pod('tickets');
    if (tickets_panel) manage_ticekts_panel(tickets_panel);
    console.log('tickets_panel', tickets_panel);
} catch (e) { console.error(e); }