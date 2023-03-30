import { Configuration } from './index.d';
import { Type, build_configuration } from '../api/config';
import { attach_event_listeners, get_pod } from './src/panels';
import { manage_statistical_panels } from './src/satistics';
import { manage_users_panel } from './src/users';

// -- Build the configuration
export const configuration = build_configuration<Configuration>({
    statistics: new Type('data-statistics', 'string'),
    users: new Type('data-users', 'string'),
    get_user: new Type('data-get-user', 'string'),
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