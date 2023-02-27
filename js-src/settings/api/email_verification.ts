import { configuration } from "../";
import { create_toast } from "../../toasts";
import { RecentVerificationResponse, VerifyAccessResponse } from "../index.d";

export const send_verification = async (
    mode: 'email' | 'tfa',
    mfa_code?: string,
): Promise<VerifyAccessResponse> => {

    const response = await fetch(
        configuration.send_verification,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
            },
            body: JSON.stringify({
                mode,
                mfa: mfa_code,
            }),
        },
    );

    try {
        const data = await response.json();
        
        // -- Check for code 200
        if (response.status !== 200) {
            return {
                data: data,
                code: response.status,
                message: data.message as string,
            }
        }

        return {
            data: data,
            code: response.status,
            message: data.message as string,
        }
    }
    catch (error) {
        return {
            code: response.status,
            message: 'An unknown error has occured, ' + error.message,
        };
    }
}


export const recent = async (
    token: string,
): Promise<RecentVerificationResponse> => {
    const response = await fetch(
        configuration.recent_verification,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
            },
            body: JSON.stringify({
                token,
            }),
        },
    );

    try {
        const data = await response.json() as {
            status: string,
            message: string,
        };

        return {
            data: data,
            code: response.status,
            message: data.message,
        }
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            code: response.status,
        };
    }
}


export const remove = async (
    token: string,
): Promise<RecentVerificationResponse> => {
    const response = await fetch(
        configuration.remove_verification,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": configuration.csrf_token,
            },
            body: JSON.stringify({
                token,
            }),
        },
    );

    try {
        const data = await response.json() as {
            status: string,
            message: string,
        };

        return {
            code: response.status,
            message: data.message,
        }
    }
    catch (error) {
        return {
            message: 'An unknown error has occured, ' + error.message,
            code: response.status,
        };
    }
}



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
