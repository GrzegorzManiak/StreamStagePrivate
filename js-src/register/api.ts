import { configuration } from '.';
import { RegisterResponse } from './index.d';
import { base_request } from '../api';
import { DefaultResponse } from '../api/index.d';



/**
 * @name register
 * @param {string} email    
 * @param {string} username
 * @param {string} password
 * @param {string} oauth_token (optional)
 * @returns {Promise<LoginResponse>}
 */
export const register = async (
    email: string,
    username: string,
    password: string,
    headers?: { [key: string]: string | void },
): Promise<RegisterResponse> => base_request(
    'POST',
    configuration.register_url,
    { email, username, password },
    headers
);



/**
 * @name authenticate_token
 * @param {string} token
 * @returns {Promise<DefaultResponse>}
 */
export const authenticate_token = async (
    token: string,
): Promise<DefaultResponse> => base_request(
    'POST', configuration.verify_token_url, {},
    { 'Authorization': token }
);
