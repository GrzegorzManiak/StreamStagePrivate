import { show_panel } from '..';
import { handle_tfa_input } from '../../click_handler';
import { submit_details } from './core';

export async function totp_verification(
    email_or_username: () => string,
    password: () => string,
) {
    // -- get the totp input   
    const totp_input = document.querySelector('#totp-input'),
        totp_submit = document.querySelector('#totp-submit') as HTMLButtonElement;
    
    // -- Handle the input
    let totp_code = '';
    totp_submit.disabled = false;
    handle_tfa_input(
        totp_input,
        (code: string) => {
            totp_code = code;
            totp_submit.disabled = false;
        },
        () => totp_submit.disabled = true
    );

    // -- Handle the submit button
    totp_submit.addEventListener('click', async () => submit_details(
        totp_submit,
        email_or_username(), 
        password(), 
        totp_code
    ));
}
