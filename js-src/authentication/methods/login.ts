import { PanelType } from "../index.d";
import { get_panel } from "../core/panel_manager";
import { attach } from "../core/spinner";
import { create_toast } from '../../toasts';
import { login, login_with_token } from "../api/login";


export const login_handler = async () => {
    // -- Get the login panel
    const login_panel = get_panel('defualt' as PanelType);


    // -- Get the login fields
    const emailorname_input = login_panel.element.querySelector(
        'input[name="emailorusername"]') as HTMLInputElement;

    const password_input = login_panel.element.querySelector(
        'input[name="password"]') as HTMLInputElement;


    // -- Get the button
    const button = login_panel.element.querySelector(
        'button') as HTMLButtonElement;

    
    // -- Attach the event listener
    button.addEventListener('click', async () => {
        // -- Start the spinner
        const stop_spinner = attach(button);

        // -- Get the values
        const emailruser = emailorname_input.value,
            password = password_input.value;


        // -- Make sure the values are not empty
        if (emailruser === '') {
            create_toast('warning', 'login', 'Please enter an email or username');
            return await stop_spinner();
        }

        if (password === '') {
            create_toast('warning', 'login', 'Please enter a password');
            return await stop_spinner();
        }



        // -- Make the request
        const response = await login(emailruser, password);
        if (response.code !== 200) {
            create_toast('error', 'login', response.data.message);
            return stop_spinner();
        }

        // -- If the response is a success
        create_toast('success', 'login', response.data.message);
        const token = response.data.token;

        // -- Authenticate the user
        const response2 = await login_with_token(token);
        if (response2.code !== 200) {
            create_toast('error', 'login', response2.data.message);
            return stop_spinner();
        }

        create_toast('success', 'login', "You have successfully logged in, redirecting you to the dashboard");

        // -- Wait for 3 seconds
        setTimeout(() => {
            window.location.href = '/';
        }, 3000);
    });
}