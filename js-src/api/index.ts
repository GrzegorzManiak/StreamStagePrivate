import { create_toast } from '../common';
import { DefaultResponse, DefaultResponseData, ResendVerificationResponse } from './index.d';
import { configuration } from './config';

// -- Check if we have a 'impersonate' query string
//    If we do, then we need to set the 'Impersonate' header
//    to the value of the query string
const COOKIE_NAME = 'streamstage-token';


/**
 * @name get_session_cookie
 * @returns string | undefined
 */
export function get_session_cookie(): string | undefined {
    // -- Get all cookies
    const cookies = document.cookie.split(';');

    // -- Loop through the cookies
    for (const cookie of cookies) {
        const cookie_name = cookie.split('=')[0].trim();
        if (cookie_name === COOKIE_NAME) return cookie.split('=')[1];
    }
}

const url = new URL(window.location.href);
let impersonate = url.searchParams.get('impersonate');
if (impersonate) console.log('Impersonating: ' + impersonate);

/**
 * @name base_request
 * @param method - Method (GET, POST, PUT, DELETE)
 * @param endpoint - Endpoint to make the request to
 * @param data - Data to send with the request (if any)
 * @param headers - Headers to send with the request (if any)
 * @returns Promise<DefaultResponse>
 */
export async function base_request (
    mehod: string,
    endpoint: string,
    data: any = {},
    headers: any = {},
): Promise<DefaultResponse> {
    // -- Get the session cookie
    const session_cookie = get_session_cookie();

    const new_url = new URL(window.location.href);
    let new_impersonate = new_url.searchParams.get('impersonate');
    if (new_impersonate) {
        impersonate = new_impersonate;
        console.log('Impersonating: ' + impersonate);
    }

    // -- If the request is a GET request, then
    //    we need to convert the data to a query string
    let query = '';
    if (mehod === 'GET') query = Object.keys(data).map(key => {
        return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
    }).join('&');


    // -- Make sure that if any data is undefined/null, then
    //    we remove it from the data object
    let clean_data = {};
    for (let key in data) {
        if (data[key] !== undefined && data[key] !== null) 
            clean_data[key] = data[key];
    }
        
    headers['Impersonate'] = impersonate;
    headers[COOKIE_NAME] = session_cookie;
    let clean_headers = {};
    for (let key in headers) {
        if (headers[key] !== undefined && headers[key] !== null)
            clean_headers[key] = headers[key];
    }

    const response = await fetch(
        endpoint + (mehod === 'GET' ? '?' + query : ''),
        {
            method: mehod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration().csrf_token,
                "ss-CSRF-token": configuration().csrf_token,
                ...clean_headers,
            },
            body: mehod === 'GET' ? undefined : JSON.stringify(clean_data),
        },
    );

    try {
        const data = await response.json();

        return {
            data: data.data as any,
            code: response.status,
            message: data.message as string,
        } as DefaultResponseData;
    }
    catch (error) {
        return {
            code: response.status,
            message: 'Oops! It appears that our servers dont want to talk to us right now. Please try again later.'
        };
    }
}



/**
 * @name recent
 * @param token - Recent email verification token
 * @returns Promise<DefaultResponse>
 * @description Check if the email has been verified
 *             recently
 */
export const recent = async (
    token: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration().recent_verification,
    { token }
);


/**
 * @name resend_verification
 * @param {string} token
 * @param {string} email (optional)
 * @returns {Promise<ResendVerificationResponse>}
 */
export const resend_verification = async (
    token: string,
    email?: string,
): Promise<ResendVerificationResponse> => base_request(
    'POST',
    configuration().resend_verification,
    { token, email },
);


//
// AUXILIARY FUNCTIONS
//

/**
 * 
 * @param verify_token: () => string  - A function that returns the token 
 *                                      That is used to check if the email has been verified
 * @param interval: ?number            - The interval to check if the email has been verified    
 * @param timeout: ?number            - The timeout to stop checking if the email has been verified
 * @param message: ?string            - The message to show when the email has been verified successfully
 * @returns Promise<boolean>          - A promise that resolves to true if
 *                                      the email has been verified, false
 *                                      otherwise
 * 
 * @description This function will check if the email has been verified
 *              every x seconds, if the email has been verified, it will
 *              resolve the promise, if the email has not been verified
 *              after x ammount of time, it will reject the promise.
 */
export async function check_email_verification(
    verify_token: () => string,
    interval: number = 3000,
    timeout: number = 15 * 60 * 1000, // -- 15 minutes
    message: string = 'Your email has been verified, you\'ll be given access to your account in a few seconds.'
): Promise<boolean> {
    return new Promise(async (resolve, reject) => {
        let verified = false;
        const int = setInterval(async () => {
            const response = await recent(verify_token());
    
            // -- If the email has been verified
            if (response.code === 404) {} // -- Do nothing
            else if (response.code === 200) {
                // -- Login the user
                create_toast('success', 'Congratulations!', message);
                clearInterval(int);
                verified = true;
                return resolve(true);
            }

            // -- Server error
            else {
                // -- Show the error
                create_toast('error', 'Error', response.message);
                clearInterval(int);
                return reject(false);
            }
        }, interval);
        
        // -- Stop the interval after 15 minutes
        setTimeout(() => {
            clearInterval(int);
            reject(false);
            if (!verified) create_toast('error', 'Error', 'The verification email has expired');
        }, timeout);
    });
}
