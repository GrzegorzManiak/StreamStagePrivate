import { attach_event_listeners, get_pod } from './core/panels';
import { manage_security_panel } from './core/security';
import { manage_payments_panel } from './core/payments';
import { manage_subscription_panel } from './core/subscription';
import { manage_profile_panel } from './core/profile';
import { manage_reviews_panel } from './core/reviews';
import { Type, build_configuration } from '../api/config';
import { Configuration } from './index.d';

export const configuration = build_configuration<Configuration>({
    admin: new Type('data-admin', 'boolean'),
    username: new Type('data-username', 'string'),
    userid: new Type('data-userid', 'string'),
    useremail: new Type('data-useremail', 'string'),
    userfirst: new Type('data-userfirst', 'string'),
    userlast: new Type('data-userlast', 'string'),
    access_level: new Type('data-access-level', 'number'),
    profile_picture: new Type('data-profile-picture', 'string'),
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

    change_pfp: new Type('data-change-profile-picture', 'string')
});

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