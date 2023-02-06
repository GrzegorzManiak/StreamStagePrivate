
import { PageType } from './index.d';
import { ensure_tokens } from './core/headers';
import { instruction_handler } from './methods/instructions';
import { login_handler } from './methods/login';
import { register_handler } from './methods/register';

export function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


// -- Ensure CSRF token
ensure_tokens();


// -- Handle all URL parameters
const url = new URL(window.location.href);
const instructions = url.searchParams.get('instructions');


// -- Get auth configuration
const sso_config = document.getElementById('sso');
export const token_url = sso_config?.getAttribute('data-token-url'),
    get_token_url = sso_config?.getAttribute('data-get-token-url'),
    register_url = sso_config?.getAttribute('data-register-url'),
    login_url = sso_config?.getAttribute('data-login-url');


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


// -- If theres no urls or auth token, error out
if (
    !token_url || !get_token_url || 
    !register_url || !login_url || 
    !page || !email_recent ||
    !email_verify || !email_resend
) {
    console.error('Please ensure that you have set the correct urls in the sso config');
    window.location.reload();
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


