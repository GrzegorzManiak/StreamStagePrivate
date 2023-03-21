import { create_toast } from '../../toasts';
import { attach } from "../../click_handler";
import { email_verification } from './email';
import { show_panel } from '..';
import { name_monitor, password_monitor, rp_password_monitor, validate_name, validate_password } from './validation';
import { register } from '../api';
import { Register, RegisterSuccess } from '../index.d';


export function register_handler() {
    // -- Get the email input and set the value
    const email_input = document.querySelector('input[name="email"]') as HTMLInputElement,
        name_input = document.querySelector('input[name="username"]') as HTMLInputElement,
        password_input = document.querySelector('input[name="password"]') as HTMLInputElement,
        rp_password_input = document.querySelector('input[name="rp-password"]') as HTMLInputElement,
        submit_button = document.querySelector('button[type="submit"]') as HTMLButtonElement;

    name_monitor(name_input);
    password_monitor(password_input);
    rp_password_monitor(password_input, rp_password_input);

    // -- Add the event listners to the inputs
    const check_inputs = () => {
        if (email_input.value.trim() === '' || 
            name_input.value.trim() === '' || 
            password_input.value.trim() === '' || 
            rp_password_input.value.trim() === ''
        ) submit_button.disabled = true; 
        else submit_button.disabled = false;
    }

    email_input.addEventListener('input', () => check_inputs());
    name_input.addEventListener('input', () => check_inputs());
    password_input.addEventListener('input', () => check_inputs());
    rp_password_input.addEventListener('input', () => check_inputs());
    check_inputs();

    // -- Add the event listener to the button
    submit_button.addEventListener('click', async () => handle_click(
        submit_button,
        name_input,
        email_input,
        password_input,
        rp_password_input
    ));
}



async function handle_click(
    button: HTMLButtonElement,
    name_input: HTMLInputElement,
    email_input: HTMLInputElement,
    password_input: HTMLInputElement,
    rp_password_input: HTMLInputElement
) {
    // -- Start the spinner
    const stop_spinner = attach(button);


    // -- Validate all inputs
    const name_valid = validate_name(name_input.value);
    const password_valid = validate_password(password_input.value);


    // -- Make sure the passwords match
    if (password_input.value !== rp_password_input.value) {
        create_toast('error', 'Passwords', 'Oops! It looks like your passwords don\'t match.');
        return await stop_spinner();
    }
    
    // -- Make sure the name is valid
    if (name_valid.length > 0) {
        create_toast('error', 'Name', 'Oops! It looks like your name is invalid.');
        return await stop_spinner();
    }

    // -- Make sure the password is valid
    if (password_valid.length > 0) {
        create_toast('error', 'Password', 'Oops! It looks like your password is invalid.');
        return await stop_spinner();
    }

    // -- Make sure the email is valid
    if (email_input.value.length === 0) {
        create_toast('error', 'Email', 'Oops! It looks like your email is invalid.');
        return await stop_spinner();
    }


    // -- Send the request to the server
    const res = await register(
        email_input.value,
        name_input.value,
        password_input.value
    )

    // -- Check if the request was successful
    if (res.code !== 200) {
        create_toast('error', 'Error', res.message);
        return await stop_spinner();
    }

    // -- Show the email verification panel
    const data = (res as RegisterSuccess).data;
    if (data.type === 'verified') {}

    else {
        const email_tokens = data as Register,
            new_email_input = document.querySelector('#resend-email') as HTMLInputElement,
            resend_button = document.querySelector('#resend') as HTMLButtonElement;

        new_email_input.value = email_input.value;

        show_panel('email_wait');
        email_verification(
            resend_button,
            email_tokens.verify_token,
            email_tokens.resend_token,
            () => new_email_input.value
        );
    }
}