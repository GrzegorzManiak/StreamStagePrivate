import { Configuration } from './index.d';
import { Type, build_configuration } from '../api/config';
import { attach_event_listeners, get_pod } from './src/panels';
import { manage_statistical_panels } from './src/satistics';
import { manage_users_panel } from './src/users';
import { manage_category_panel } from './src/categorys';
import { manage_broadcaster_panel } from './src/broadcaster';
import { manage_event_panel } from './src/events';
import { manage_terms_panel } from './src/terms';
import { manage_privacy_panel } from './src/privacy';
import { manage_faq_panel } from './src/faq';

// -- Build the configuration
export const configuration = build_configuration<Configuration>({
    statistics: new Type('data-statistics', 'string'),
    users: new Type('data-users', 'string'),
    get_user: new Type('data-get-user', 'string'),
    delete_user: new Type('data-delete-user', 'string'),
    update_email: new Type('data-update-email', 'string'),
    update_streamer_status: new Type('data-update-streamer-status', 'string'),

    category: new Type('data-category', 'string'),
    get_category: new Type('data-get-category', 'string'),
    create_category: new Type('data-create-category', 'string'),
    delete_category: new Type('data-delete-category', 'string'),
    update_category: new Type('data-update-category', 'string'),
    set_category_image: new Type('data-set-category-image', 'string'),

    broadcaster: new Type('data-broadcaster', 'string'),
    get_broadcaster: new Type('data-get-broadcaster', 'string'),
    update_broadcaster: new Type('data-update-broadcaster', 'string'),
    delete_broadcaster: new Type('data-delete-broadcaster', 'string'),

    event: new Type('data-event', 'string'),
    get_event: new Type('data-get-event', 'string'),
    delete_event: new Type('data-delete-event', 'string'),
    update_event: new Type('data-update-event', 'string'),

    latest_privacy: new Type('data-latest-privacy', 'string'),
    create_privacy: new Type('data-create-privacy', 'string'),
    filter_privacy: new Type('data-filter-privacy', 'string'),
    render_privacy: new Type('data-render-privacy', 'string'),

    latest_terms: new Type('data-latest-terms', 'string'),
    create_terms: new Type('data-create-terms', 'string'),
    filter_terms: new Type('data-filter-terms', 'string'),
    render_terms: new Type('data-render-terms', 'string'),

    faq_create: new Type('data-faq-create', 'string'),
    faq_filter: new Type('data-faq-filter', 'string'),
    faq_delete: new Type('data-faq-delete', 'string'),
    faq_update: new Type('data-faq-update', 'string'),
}); 

// -- Attach the event listeners
attach_event_listeners();


// -- Get the statistics pods
const accounts = get_pod('accounts'),
    server = get_pod('server'),
    cash_flow = get_pod('cash_flow'),
    tickets = get_pod('tickets'),
    reviews = get_pod('reviews'),
    subscriptions = get_pod('subscriptions'),
    viewers = get_pod('viewers');

// -- Attach to all panels
if (
    accounts && server && 
    cash_flow && tickets && 
    reviews && subscriptions && 
    viewers
) manage_statistical_panels(
    accounts, server,
    cash_flow, tickets, 
    reviews, subscriptions, 
    viewers
);


const users = get_pod('users');
if (users) manage_users_panel(users);

const categories = get_pod('categories');
if (categories) manage_category_panel(categories);

const broadcasters = get_pod('broadcasters');
if (broadcasters) manage_broadcaster_panel(broadcasters);

const events = get_pod('events');
if (events) manage_event_panel(events);

const terms = get_pod('terms');
if (terms) manage_terms_panel(terms);

const privacy = get_pod('privacy');
if (privacy) manage_privacy_panel(privacy);

const faq = get_pod('faq');
if (faq) manage_faq_panel(faq);