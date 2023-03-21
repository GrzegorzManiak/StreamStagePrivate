import { get_or_error } from '../api/config';
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
const sso_config = document.getElementById('config');
export const token_url = sso_config?.getAttribute('data-token-url'),
    get_token_url = sso_config?.getAttribute('data-get-token-url'),
    register_url = sso_config?.getAttribute('data-register-url'),
    login_url = sso_config?.getAttribute('data-login-url'),
    csrf_token = sso_config?.getAttribute('data-csrf-token');


// -- Email verification
export const email_recent = sso_config?.getAttribute('data-recent-verification'),
    email_verify = sso_config?.getAttribute('data-email-verify'),
    email_resend = sso_config?.getAttribute('data-email-resend');


export const configuration = {
    verify_token_url: get_or_error<string>(sso_config, 'data-token-url'),
    get_token_url: get_or_error<string>(sso_config, 'data-get-token-url'),
    register_url: get_or_error<string>(sso_config, 'data-register-url'),
    login_url: get_or_error<string>(sso_config, 'data-login-url'),
    csrf_token: get_or_error<string>(sso_config, 'data-csrf-token'),
    email_recent: get_or_error<string>(sso_config, 'data-recent-verification'),
    email_verify: get_or_error<string>(sso_config, 'data-email-verify'),
    email_resend: get_or_error<string>(sso_config, 'data-email-resend'),
};



//
// We use this library to handle both, loging in
// and account creation, so we need to know what
// page we are on.
//
const page: PageType = sso_config?.getAttribute('data-page') as PageType;
if (instructions) instruction_handler(instructions);
else if (page === 'login') login_handler();
else if (page === 'register') register_handler();