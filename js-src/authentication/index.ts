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
const code = url.searchParams.get('code');


// -- If there are multiple params, reload
let count = 0;
const count_if_exit = (param: string | null) => 
{ if (param) count++; }

count_if_exit(instructions);
count_if_exit(auth_token);
count_if_exit(code);

if (count > 1) window.location.reload();


// -- Handle anything that comes in
if (instructions) instruction_handler(instructions);



