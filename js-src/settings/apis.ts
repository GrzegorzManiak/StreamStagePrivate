import { PaymentIntentMethod } from "../common/index.d";
import { configuration } from "./";
import { 
    DefaultResponse, 
    SecurityInfoResponse, 
    StartSubscriptionResponse, 
    UpdateProiflePictureResponse, 
    VerifyAccessResponse 
} from "./index.d";
import { base_request } from "../api";


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
 * @name update_profile
 * @param token - PAK token
 * @param data - Profile data
 * @returns Promise<DefaultResponse>
 * @description Update the profile of the user
 *             (name, email, etc)
*/
export const update_profile = async (
    data: { [key: string]: any },
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.update_profile,
    data
);



/**
 * @name start_subscription
 * @param method - PaymentIntentMethod
 * @returns Promise<StartSubscriptionResponse>
 * @description Start a subscription for the user
 */
export const start_subscription = async (
    method: PaymentIntentMethod
): Promise<StartSubscriptionResponse> => {
    // -- If the method is a string
    if (typeof method === 'string') return base_request(
        'POST',
        configuration.start_subscription,
        { payment_method: method }
    );

}



/**
 * @name change_email
 * @param token - PAK token
 * @param email - New email
 * @returns Promise<VerifyAccessResponse>
 * @description Change the email of the user (Sends verification code)
 */
export const change_email = async (
    token: string,
    email: string
): Promise<VerifyAccessResponse> => base_request(
    'POST',
    configuration.change_email,
    { token, email }
);



/**
 * @name update_review
 * @param id - Review id
 * @param rating - Rating
 * @param title - Title
 * @param body - Body
 */
export const update_review = async (
    id: string,
    rating: number,
    title: string,
    body: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.update_review,
    { id, rating, title, body }
);



/**
 * @name delete_review
 * @param id - Review id
 * @returns Promise<DefaultResponse>
 */
export const delete_review = async (
    id: string
): Promise<DefaultResponse> => base_request(
    'POST',
    configuration.delete_review,
    { id }
);



/**
 * @name change_image
 * @param {string} base64 - Base64 image
 * @param {string} type - 'pfp' or 'banner'
 * @returns Promise<UpdateProiflePictureResponse>
 */
export const change_image = async (
    base64: string,
    type: 'pfp' | 'banner'
): Promise<UpdateProiflePictureResponse> => base_request(
    'POST',
    configuration.change_img,
    { image: base64, type }
);