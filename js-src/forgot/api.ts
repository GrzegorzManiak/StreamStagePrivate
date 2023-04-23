import { configuration } from '.';
import { DefaultResponse } from '../api/index.d';
import { base_request } from '../api';
import { ResetInitResponse } from './index.d';

/**
 * @name reset_init
 * @param {string} email_or_username
 * @returns {Promise<ResetInitResponse>}
 */
export const authenticate_token = async (
    email_or_username: string,
): Promise<ResetInitResponse> => base_request(
    'POST', configuration.forgot_init, {
        'eom': email_or_username,
    },
);



/**
 * @name change_pass
 * @param {string} token
 * @param {string} password
 * @returns {Promise<DefaultResponse>}
 */
export const change_pass = async (
    token: string,
    password: string,
): Promise<DefaultResponse> => base_request(
    'POST', configuration.change_pass, {
        token, password,
    },
);