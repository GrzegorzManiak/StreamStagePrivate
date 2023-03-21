import { LoginNone, LoginSuccess, PanelType } from "../index.d";
import { get_panel } from "../core/panel_manager";
import { create_toast } from '../../toasts';
import { attach } from "../../click_handler";
import { authenticate_token, login } from "../api";


export const login_handler = async () => {
    // -- Get the login panel
    const login_panel = get_panel('defualt' as PanelType);


    // -- Get the login fields
    const emailorname_input = login_panel.element.querySelector('input[name="emailorusername"]') as HTMLInputElement,
        password_input = login_panel.element.querySelector('input[name="password"]') as HTMLInputElement,
        button = login_panel.element.querySelector('button') as HTMLButtonElement;

    // -- Add the event listners to the inputs
    const check_inputs = () => {
        if (emailorname_input.value.trim() === '' || 
            password_input.value.trim() === ''
        ) button.disabled = true;
        else button.disabled = false;
    }

    emailorname_input.addEventListener('input', () => check_inputs());
    password_input.addEventListener('input', () => check_inputs());
    check_inputs();
    
    // -- Attach the event listener
    button.addEventListener('click', async () => {
        // -- Start the spinner
        const stop_spinner = attach(button);

        // -- Make the request
        await submit_details(
            button,
            emailorname_input.value.trim(),
            password_input.value.trim()
        );

        // -- Stop the spinner
        stop_spinner();
    });
}



async function submit_details(
    button: HTMLButtonElement,
    email_or_username: string,
    password: string,
) {
    // -- Start the spinner
    const stop_spinner = attach(button);

    // -- Make sure the values are not empty
    if (email_or_username === '' || password === '') {
        create_toast('error', 'login', "Please fill in all the fields");
        return stop_spinner();
    }

    // -- Make the request
    const response = await login(email_or_username, password);
    if (
        response.code !== 200 &&
        response.code !== 202
    ) {
        create_toast('error', 'login', response.message);
        return stop_spinner();
    }

    // -- A 202 response means that the user has
    //    to fill in some more details
    const data = (response as LoginSuccess);
    if (response.code === 202) {
        // if (data.data.mode === 'mfa') 
        // if (data.data.mode === 'email')
    }

    // -- 200
    else await submit_auth_token(
        button, (data.data as LoginNone).token);
}


async function submit_auth_token(
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