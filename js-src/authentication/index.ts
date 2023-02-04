
import {
    ensure_tokens 
} from './core/header';
import { instruction_handler } from './core/instructions';


// -- Ensure CSRF token
ensure_tokens();

// -- Handle all URL parameters
const url = new URL(window.location.href);

// -- Get URL parameters
const instructions = url.searchParams.get('instructions');
const auth_token = url.searchParams.get('auth_token'); 
const code = url.searchParams.get('code');


// -- If there are multiple params, reload
let count = 0;
const count_if_exit = (param: string | null) => 
{ if (param) count++; }

count_if_exit(instructions);
count_if_exit(auth_token);
count_if_exit(code);

if (count > 1) window.location.reload();



// -- Get configuration
const sso_config = document.getElementById('sso');

export const token_url = sso_config?.getAttribute('data-token-url'),
    get_token_url = sso_config?.getAttribute('data-get-token-url');

// -- If theres no urls or auth token, error out
if (!token_url || !get_token_url) {
    console.error('No token url or get token url or auth token');
};

// -- Handle anything that comes in
if (instructions) instruction_handler(instructions);



