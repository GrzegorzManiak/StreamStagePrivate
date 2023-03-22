import { create_toast } from '../common';
import { DefaultResponse, DefaultResponseData, ResendVerificationResponse } from './index.d';
import { get_config } from './config';

const configuration = get_config();

export async function base_request (
    mehod: string,
    endpoint: string,
    data: any = {},
    headers: any = {},
): Promise<DefaultResponse> {
    const response = await fetch(
        endpoint,
        {
            method: mehod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
                ...headers,
            },
            body: mehod === 'GET' ? undefined : JSON.stringify(data),
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
            message: 'An unknown error has occured, ' + error.message,
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
    configuration.recent_verification,
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
    configuration.resend_verification,
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
