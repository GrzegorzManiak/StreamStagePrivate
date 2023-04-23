import { ResetInitSuccess } from '../index.d';
import { attach, create_toast } from "../../common";
import { authenticate_token } from "../api";
import { show_panel } from '..';
import { email_verification } from './email';

export async function forgot_handler() {
    // -- Get the email input and set the value
    const eom = document.querySelector('input[name="eom"]') as HTMLInputElement,
        submit_button = document.querySelector('#register-btn') as HTMLButtonElement;

    // -- Add the event listners to the inputs
    submit_button.disabled = true;
    eom.addEventListener('input', () => {
        if (eom.value.trim() === '') submit_button.disabled = true;
        else submit_button.disabled = false;
    });

    submit_button.addEventListener('click', async () => {
        
        // -- Attach the loading spinner
        const stop = attach(submit_button);
        
        // -- Send the request
        const res = await authenticate_token(
            eom.value.trim()
        ) as ResetInitSuccess;

        // -- Check if the request was successful
        if (res.code !== 200) {
            create_toast('error', 'Forgot Password', res.message);
            return stop();
        }

        // -- Show the success toast
        create_toast(
            'success', 
            'Forgot Password', 
            'Success! Check your email for the reset link!'
        );

        // -- Remove the spinner
        stop();
        show_panel('email_wait');
        handle_email_wait(
            res.data.verify_token,
            res.data.access_token,
            res.data.resend_token,
        );
    });
}


export async function handle_email_wait(
    verify_token: string,
    access_token: string,
    resend_token: string,
) {
    // -- Get the resned button
    const resend_button = document.querySelector('#resend') as HTMLButtonElement;
    email_verification(
        resend_button,
        verify_token,
        resend_token,
        access_token,
    );
}