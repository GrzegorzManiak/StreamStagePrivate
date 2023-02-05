
import { ensure_tokens, oauth_error } from './core/headers';
import { instruction_handler } from './methods/instructions';
import { login_handler } from './methods/login';

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
    register_url = sso_config?.getAttribute('data-register-url');


// -- If theres no urls or auth token, error out
if (!token_url || !get_token_url || !register_url) {
    console.error('No token url or get token url or register url found');
    window.location.reload();
};

if (oauth_error) {
    console.error(oauth_error);
}


// -- Handle anything that comes in
if (instructions) instruction_handler(instructions);

// -- Login with just normal details
login_handler();



