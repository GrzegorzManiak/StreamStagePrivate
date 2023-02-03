import {
    Response,
} from './index.d';

import {
    oauth_error, 
    ensure_tokens 
} from './header';
import { instruction_handler } from './instructions';


// -- Ensure CSRF token
ensure_tokens();


// -- Handle all URL parameters
const url = new URL(window.location.href);

// -- Get URL parameters
const instructions = url.searchParams.get('instructions');
const auth_token = url.searchParams.get('auth_token'); 

// -- If there are both, reload page
if (instructions && auth_token) {
    window.location.reload();
}


// -- Handle anything that comes in
if (instructions) instruction_handler(instructions);



