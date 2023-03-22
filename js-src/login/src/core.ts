import { LoginMFA, LoginNone, LoginSuccess } from '../index.d';
import { create_toast, attach} from '../../common';
import { authenticate_token, login } from '../api';
import { email_verification } from './email';
import { totp_verification } from './totp';
import { Response } from '../index.d';
import { show_panel } from '..';

function manage_instructions(button: HTMLButtonElement) {
    // -- Handle all URL parameters
    const url = new URL(window.location.href);
    const instructions = url.searchParams.get('instructions');
    if (!instructions) return;

    // -- Decode the instructions (base64)
    const decoded = JSON.parse(atob(instructions)) as unknown as Response;

    // -- Check if the user has an account 
    if (!decoded.instructions.has_account) {
        document.location.href = '/register?instructions=' + instructions;
        return new Promise(() => {});
    }

    // -- Authenticate the user
    else submit_auth_token(button, decoded.token);
}

export async function login_handler() {
    // -- Get the login fields
    const emailorname_input = document.querySelector('input[name="emailorusername"]') as HTMLInputElement,
    password_input = document.querySelector('input[name="password"]') as HTMLInputElement,
    button = document.querySelector('#login-btn') as HTMLButtonElement;

    // -- Handle instructions
    await manage_instructions(button);
    show_panel('login');

    // -- Add the event listners to the inputs
    const check_inputs = () => {
    if (emailorname_input.value.trim() === '' || 
        password_input.value.trim() === ''
    ) button.disabled = true; else button.disabled = false; }

    emailorname_input.addEventListener('input', () => check_inputs());
    password_input.addEventListener('input', () => check_inputs());
    check_inputs();


    // -- Init the other panels
    totp_verification(
        () => emailorname_input.value.trim(),
        () => password_input.value.trim()
    );

    // -- Go back buttons 
    const go_back = document.querySelectorAll('.go-back');
    go_back.forEach((go_button) => {
        go_button.addEventListener('click', () => show_panel('login'));
    });


    // -- Attach the event listener
    button.addEventListener('click', async () => submit_details(
        button,
        emailorname_input.value.trim(),
        password_input.value.trim()
    ));
}



export async function submit_details(
    button: HTMLButtonElement,
    email_or_username: string,
    password: string,
    totp_code?: string,
) {
    // -- Start the spinner
    const stop_spinner = attach(button);

    // -- Make sure the values are not empty
    if (email_or_username === '' || password === '') {
        create_toast('error', 'login', "Please fill in all the fields");
        return stop_spinner();
    }

    // -- Make the request
    const response = await login(email_or_username, password, totp_code);
    if (response.code !== 200 && response.code !== 202) {
        create_toast('error', 'login', response.message);
        return stop_spinner();
    }

    // -- A 202 response means that the user has
    //    to fill in some more details
    const data = (response as LoginSuccess);
    if (response.code === 202) {

        // 
        // -- Requires MFA (Email)
        // 
        if (data.data.mode === 'mfa') {
            const mfa_data = (data.data as LoginMFA);
            email_verification(mfa_data.verify, mfa_data.resend, mfa_data.token);
        }

        //
        // -- Requires TOTP
        //
        if (data.data.mode === 'totp') show_panel('totp');
        stop_spinner();
    }

    // -- 200
    else await submit_auth_token(
        button, (data.data as LoginNone).token);
}



/**
 * @name submit_auth_token
 * 
 * @description This function is used to submit the authentication token
 * to the server and attempts to login the user in.
 * 
 * @param button {HTMLButtonElement} The button that was clicked
 * @param token {string} The token that was sent to the user
 * @returns {Promise<void>}
 */
export async function submit_auth_token(
    button: HTMLButtonElement,
    token: string,
) {
    // -- Start the spinner
    const stop_spinner = attach(button);

    // -- Make the request
    const response = await authenticate_token(token);
    if (response.code !== 200) {
        create_toast('error', 'login', response.message);
        return stop_spinner();
    }

    // -- Login was successful
    create_toast('success', 'login', "You have successfully logged in, redirecting you to the dashboard");

    // -- Wait for 3 seconds
    await new Promise(() => setTimeout(() => {
        // -- Redirect the user to the dashboard
        window.location.href = '/';
    }, 3000));
}