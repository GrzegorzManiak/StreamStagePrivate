//
// This library here is responsible for handling the authentication code
// flow, once a user needs to lets say, verify their email address.
// Theyll recieve an email with a link to the website, which will
// contain a code generated by the server. 
// 
// Once the user clicks the link, the code will be set as a cookie
// and the page will close.
// The page waiting for the code will then check for the code, and
// if it exists, it will send a request to the server to verify the
// code.
// 
// Completing the process.
//

import { csrf_token } from "./header";

export const get_code = (): string | null => {
    // -- Get the code from cookies
    let cookies: string[] = document.cookie.split(';');
    let code: string | null = null;

    // -- Find the code
    cookies.forEach((cookie) => {
        let [key, value] = cookie.split('=');
        key = key.trim();
        value = value.trim();

        if (key === 'code') code = value;
    });

    // -- Return the code
    return code;
}

export const set_code = (code: string) => {
    // -- Set the code
    document.cookie = `code=${code}; path=/;`;
}

export const delete_code = () => {
    // -- Delete the code
    document.cookie = `code=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

