import { configuration } from '.';
import { RegisterResponse } from './index.d';
import { base_request } from '../api';



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
    headers?: { [key: string]: string },
): Promise<RegisterResponse> => base_request(
    'POST',
    configuration.register_url,
    { email, username, password },
    headers
);
