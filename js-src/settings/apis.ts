import { create_toast } from "../toasts";
import { configuration } from "./";
import { AddCardResponse, Card, DefaultResponse, DefaultResponseData, GetCardsResponse, SecurityInfoResponse, StartSubscriptionResponse, SubscriptionMethod, VerifyAccessResponse } from "./index.d";

export async function base_request (
    mehod: string,
    endpoint: string,
    data: any,
): Promise<DefaultResponse> {
    const response = await fetch(
        endpoint,
        {
            method: mehod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
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


//
// REQUESTS
//


/**
 * @name disable_mfa
 * @param token - PAK token
 * @returns Promise<DefaultResponse>
 * 
 * @description Disable MFA for user
 */
export const disable_mfa = async(
    token: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.disable_mfa,
    { token },
);



/**
 * @name setup_mfa
 * @param token - PAK token
 * @returns Promise<DefaultResponse>
 * 
 * @description Begins the setup of MFA for user
 *              and returns the secret key   
 */
export const setup_mfa = async (
    token: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.setup_mfa,
    { token }
);



/**
 * @name verify_mfa
 * @param token - PAK token
 * @param otp - TFA code
 * @returns Promise<DefaultResponse>
 *  
 * @description Verifies the TFA code and enables MFA
 *              for the user if the code is correct
 */
export const verify_mfa = async (
    token: string,
    otp: string,
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.verify_mfa,
    { token, otp }
);



/**
 * @name send_verification
 * @param mode - 'email' or 'tfa'
 * @param mfa_code - TFA code (optional)
 * @returns Promise<VerifyAccessResponse>
 * @description Send verification code to user by email or TFA
 */ 
export const send_verification = async (
    mode: 'email' | 'tfa', mfa_code?: string
): Promise<VerifyAccessResponse> => base_request(
    'POST',
    configuration.send_verification,
    { mode, mfa: mfa_code }
);



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
 * @name remove
 * 
 * @param token - Recent email verification token
 * @returns Promise<DefaultResponse>
 * @description Remove the email verification request
 */ 
export const remove = async (
    token: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.remove_verification,
    { token }
);



/**
 * @name extend_session
 * @param token - PAK token
 * @returns Promise<DefaultResponse>
 * @description Extends the session of the user
 */
export const extend_session = async (
    token: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.extend_session,
    { token }
);



/**
 * @name close_session
 * @param token - PAK token
 * @returns Promise<DefaultResponse>
 * @description Closes the session of the user (PAK Secure area access)
 */
export const close_session = async (
    token: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.close_session,
    { token }
);



/**
 * @name remove_oauth
 * @param token - PAK token
 * @param oauth_id - Oauth id
 * @returns Promise<DefaultResponse>
 * @description Removes a linked oauth account from the user
 */
export const remove_oauth = async (
    token: string, 
    oauth_id: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.remove_oauth,
    { token, oauth_id }
);



/**
 * @name get_security_info
 * @param token - PAK token
 * @returns Promise<SecurityInfoResponse>
 * @description Get the security info of the user
 *             (2FA, linked oauth accounts, etc)    
 */
export const get_security_info = async (
    token: string,
): Promise<SecurityInfoResponse> => base_request(
    'POST',
    configuration.security_info,
    { token }
);



/**
 * @name add_card
 * @param card - Card: Token, number, exp_month, exp_year, cvc
 * @returns Promise<DefaultResponse>
 */
export const add_card = async (
    card: Card
): Promise<AddCardResponse> => base_request(
    'POST',
    configuration.add_payment,
    card
);


/**
 * @name get_cards
 * @returns Promise<DefaultResponse>
 * @description Get the cards of the user
 */
export const get_cards = async (): Promise<GetCardsResponse> => base_request(
    'GET',
    configuration.get_payments,
    {}
);


/**
 * @name remove_card
 * @param id - Card id
 * @returns Promise<DefaultResponse>
 * @description Remove a card from the user
 */
export const remove_card = async (
    id: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.remove_payment,
    { id }
);


/**
 * @name update_profile
 * @param token - PAK token
 * @param data - Profile data
 * @returns Promise<DefaultResponse>
 * @description Update the profile of the user
 *             (name, email, etc)
*/
export const update_profile = async (
    token: string,
    data: { [key: string]: any }
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.update_profile,
    { token, ...data }
);


/**
 * @name start_subscription
 * @param method - SubscriptionMethod
 * @returns Promise<StartSubscriptionResponse>
 * @description Start a subscription for the user
 */
export const start_subscription = async (
    method: SubscriptionMethod
): Promise<StartSubscriptionResponse> => {
    // -- If the method is a string
    if (typeof method === 'string') return base_request(
        'POST',
        configuration.start_subscription,
        { payment_method: method }
    );

}
    

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
