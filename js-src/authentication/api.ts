import { configuration } from '.';
import { DefaultResponse } from '../api/index.d';
import { base_request } from '../api';
import { LoginResponse } from './index.d';



/**
 * @name login
 * @param {string} emailorusername
 * @param {string} password
 * @returns {Promise<LoginResponse>}
 */
export const login = async (
    emailorusername: string,
    password: string,
): Promise<LoginResponse> => base_request(
    'POST',
    configuration.get_token_url,
    {
        emailorusername,
        password,
    },
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