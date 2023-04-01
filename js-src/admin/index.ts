import { Configuration } from './index.d';
import { Type, build_configuration } from '../api/config';
import { attach_event_listeners, get_pod } from './src/panels';
import { manage_statistical_panels } from './src/satistics';
import { manage_users_panel } from './src/users';
import { manage_category_panel } from './src/categorys';
import { manage_broadcaster_panel } from './src/broadcaster';

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