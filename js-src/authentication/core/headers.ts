import {
    ParsedHeaders,
} from '../index.d';
import { 
    create_toast 
} from '../../toasts';


export function delete_cookies() {
    // -- Delete cookies
    let cookies_to_delete: string[] = ['csrf_token', 'oauth_error', 'instructions', 'code'];
    cookies_to_delete.forEach((cookie) => {
        document.cookie = `${cookie}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    });
}

export function parse_cookies(): ParsedHeaders {
    // -- Parse cookies
    let raw_cookies: string[] = document.cookie.split(';');

    // -- Destructure
    let cookies: { [key: string]: string } = {};
    raw_cookies.forEach((cookie) => {
        let [key, value] = cookie.split('=');
        key = key.trim();
        value = value.trim();
        cookies[key] = value;
    });

    // -- Parse headers
    return {
        csrf_token: cookies['csrftoken'],
        oauth_error: cookies['oauth_error'] || null,
    };
}

// -- Parse cookies
export const { 
    csrf_token, 
    oauth_error 
} = parse_cookies()

export const ensure_tokens = () => {
    if (!csrf_token) {
        console.error('No CSRF token found');
        create_toast('error', 'CSRF', 'No CSRF token found, reloading page');

        delete_cookies();
    
        // -- Refresh page after 3 seconds
        setTimeout(() => {
            window.location.reload();
        }, 3000);
        
    }
}
