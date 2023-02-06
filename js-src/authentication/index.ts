
import { create_toast } from '../toasts';
import { PageType } from './index.d';
import { instruction_handler } from './methods/instructions';
import { login_handler } from './methods/login';
import { register_handler } from './methods/register';

export function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


// -- Handle all URL parameters
const url = new URL(window.location.href);
const instructions = url.searchParams.get('instructions');


// -- Get auth configuration
const sso_config = document.getElementById('sso');
export const token_url = sso_config?.getAttribute('data-token-url'),
    get_token_url = sso_config?.getAttribute('data-get-token-url'),
    register_url = sso_config?.getAttribute('data-register-url'),
    login_url = sso_config?.getAttribute('data-login-url'),
    csrf_token = sso_config?.getAttribute('data-csrf-token');


// -- Email verification
export const email_recent = sso_config?.getAttribute('data-email-recent'),
    email_verify = sso_config?.getAttribute('data-email-verify'),
    email_resend = sso_config?.getAttribute('data-email-resend');



//
// We use this library to handle both, loging in
// and account creation, so we need to know what
// page we are on.
//
const page: PageType = sso_config?.getAttribute('data-page') as PageType;

if (!csrf_token) {
    create_toast('error', 'CSRF Error', 'No CSRF token found, please reload the page');
    // -- Wait 3 seconds and reload the page
    setTimeout(() => {
        window.location.reload();
    }, 3000);
}


// -- If theres no urls or auth token, error out
if (
    !token_url || !get_token_url || 
    !register_url || !login_url || 
    !page || !email_recent ||
    !email_verify || !email_resend
) {
    create_toast('error', 'Configuration Error', 'No configuration found, please reload the page');
    // -- Wait 3 seconds and reload the page
    setTimeout(() => {
        window.location.reload();
    }, 3000);
};


// -- Handle PAGES
switch (page) {
    case 'login':
        if (instructions) instruction_handler(instructions);
        else login_handler();
        break;


    case 'register':
        register_handler();
        break;
}


