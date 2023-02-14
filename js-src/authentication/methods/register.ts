import { Panel, PanelType, Response } from '../index.d';
import { get_panel, hide_panel, show_panel } from '../core/panel_manager';
import { create_toast } from '../../toasts';
import { name_monitor, password_monitor, rp_password_monitor, validate_name, validate_password } from '../core/validation';
import * as DOMPurify from 'dompurify';
import { register } from '../api/register';
import { login_with_token } from '../api/login';
import { attach } from '../core/spinner';
import { complete_verification } from './verification';


export const register_handler = async () => {
    // -- Get the panel
    const panel = get_panel('register') as Panel;

    // 
    // -- Below code just sets up the input 
    //    verification stuff
    // 

    // -- Get the email input and set the value
    const email_input = panel.element.querySelector(
        'input[name="email"]') as HTMLInputElement;

     // -- Get the name input and set the value
     const name_input = panel.element.querySelector(
        'input[name="username"]') as HTMLInputElement;
    name_monitor(name_input);


    // -- Get the password input 
    const password_input = panel.element.querySelector(
        'input[name="password"]') as HTMLInputElement;
    password_monitor(password_input);


    // -- Get the rp-password input
    const rp_password_input = panel.element.querySelector(
        'input[name="rp-password"]') as HTMLInputElement;
    rp_password_monitor(password_input, rp_password_input);

    // -- Get the submit button
    const submit_button = panel.element.querySelector(
        'button[type="submit"]') as HTMLButtonElement;


    
    // 
    // -- Click handler, this is where the
    //    actual registration happens
    //
    submit_button.addEventListener('click', async () => {
        await handle_click(
            panel, 
            submit_button,
            name_input,
            email_input,
            password_input,
            rp_password_input
        );
    });
}


async function handle_click(
    panel: Panel,
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
        await stop_spinner();
        return;
    }
    
    // -- Make sure the name is valid
    if (name_valid.length > 0) {
        create_toast('error', 'Name', 'Oops! It looks like your name is invalid.');
        await stop_spinner();
        return;
    }

    // -- Make sure the password is valid
    if (password_valid.length > 0) {
        create_toast('error', 'Password', 'Oops! It looks like your password is invalid.');
        await stop_spinner();
        return;
    }

    // -- Make sure the email is valid
    if (email_input.value.length === 0) {
        create_toast('error', 'Email', 'Oops! It looks like your email is invalid.');
        await stop_spinner();
        return;
    }

    // 
    // -- Now, since all is good so far, we can make the request
    // 
    const response = await register(
        password_input.value,
        name_input.value,
        email_input.value
    );

    
    // -- Handle the response
    await complete_verification(
        email_input.value,
        response
    );

    // -- Stop the spinner
    await stop_spinner();
}