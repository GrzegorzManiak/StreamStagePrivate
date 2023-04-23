import { single } from '../common/single';
single('admin');

import { Configuration } from './index.d';
import { Type, build_configuration } from '../api/config';
import { attach_event_listeners, get_pod, set_sidebar_state } from './src/panels';
import { manage_statistical_panels } from './src/satistics';
import { manage_users_panel } from './src/users';
import { manage_category_panel } from './src/categorys';
import { manage_broadcaster_panel } from './src/broadcaster';
import { manage_event_panel } from './src/events';
import { manage_terms_panel } from './src/terms';
import { manage_privacy_panel } from './src/privacy';
import { manage_faq_panel } from './src/faq';
import { manage_reports_panel } from './src/reports';

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

    filter_reports: new Type('data-filter-reports', 'string'),
    update_report: new Type('data-update-report', 'string'),
}); 

// -- Attach the event listeners
attach_event_listeners();
set_sidebar_state('open');

// -- Get the statistics pods
const accounts = get_pod('accounts'),
    server = get_pod('server'),
    cash_flow = get_pod('cash_flow'),
    tickets = get_pod('tickets'),
    subscriptions = get_pod('subscriptions');

// -- Attach to all panels
if (
    accounts && server && 
    cash_flow && tickets && 
    subscriptions
) manage_statistical_panels(
    accounts, server,
    cash_flow, tickets, 
    subscriptions, 
);


try {
    const users = get_pod('users');
    if (users) manage_users_panel(users);
    console.log('users', users);
} catch (e) { console.log(e); }

try {
    const categories = get_pod('categories');
    if (categories) manage_category_panel(categories);
    console.log('categories', categories);
} catch (e) { console.log(e); }

try {
    const broadcasters = get_pod('broadcasters');
    if (broadcasters) manage_broadcaster_panel(broadcasters);
    console.log('broadcasters', broadcasters);
} catch (e) { console.log(e); }

try {
    const events = get_pod('events');
    if (events) manage_event_panel(events);
    console.log('events', events);
} catch (e) { console.log(e); }

try {
    const terms = get_pod('terms');
    if (terms) manage_terms_panel(terms);
    console.log('terms', terms);
} catch (e) { console.log(e); }

try {
    const privacy = get_pod('privacy');
    if (privacy) manage_privacy_panel(privacy);
    console.log('privacy', privacy);
} catch (e) { console.log(e); }

try {
    const faq = get_pod('faq');
    if (faq) manage_faq_panel(faq);
    console.log('faq', faq);
} catch (e) { console.log(e); }

try {
    const reports = get_pod('reports');
    if (reports) manage_reports_panel(reports);
    console.log('reports', reports);
} catch (e) { console.log(e); }