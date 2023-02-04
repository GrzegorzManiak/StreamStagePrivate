import { Panel, PanelType, Response } from '../index.d';
import { get_panel, hide_panel, show_panel } from '../core/panel_manager';
import { create_toast } from '../core/toasts';
import { name_monitor, password_monitor, rp_password_monitor, validate_name, validate_password } from '../core/validation';
import * as DOMPurify from 'dompurify';
import { register_with_oauth } from '../api/register';
import { login } from '../api/login';


// -- Handle instructions
const instruction_parser = (instructions: string): Response | null => {
    // -- Try decoding instructions
    try { return JSON.parse(atob(instructions)); }
    catch (error) { return null; }
};

function auth_token(token: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
        login(token).then((data) => {
            console.log(data.message, data);
    
            // -- If there was an error, show the error
            if (data?.status !== 'success') {
                create_toast('error', 'Login', 'There was some issue logging you in, ' + data.message);
                resolve(false);
            }
            else {
                // -- If we get here, we can submit the form
                create_toast('success', 'oAuth2 Login', 'You have successfully autenticated in with OAuth, please wait while we redirect you to the home page');
                
                // -- Redirect the user to the home page
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
            }
        });
    });
}

export const instruction_handler = async (instructions: string) => {
    // -- Parse instructions
    const response = instruction_parser(instructions);

    // -- If there is no response, return
    if (!response) return;
    if (response.message !== 'Success') {
        console.error(response.message);
        return;
    }   

    if (response.instructions.can_authenticate) 
        return auth_token(response.token);


    // -- Since the user has provided oauth
    // data, we can hide the login panel,
    // and show the oauth panel if they
    // need to fill in some more required
    // fields
    hide_panel('defualt' as PanelType);
    show_panel('oauth' as PanelType);

    // -- Tell the user that oauth was successful
    create_toast('success', 'oauth', 'You have successfully autenticated in with OAuth, please fill in the required fields');

    // -- Handle inputs
    handle_inputs(
        response, 
        get_panel('oauth' as PanelType)
    );
}


function handle_inputs(response: Response, panel: Panel) {
    // -- Get the email input and set the value
    const email_input = panel.element.querySelector('input[name="email"]') as HTMLInputElement;
    email_input.value = DOMPurify.sanitize(response.user.email);

    // -- If the email is verified, hide the email input
    if (response.user.verified_email)
        email_input.parentElement.style.display = 'none';
    

    // -- Get the name input and set the value
    const name_input = panel.element.querySelector('input[name="username"]') as HTMLInputElement;
    name_input.value =  DOMPurify.sanitize(response.user.name);
    name_monitor(name_input);


    // -- Get the password input 
    const password_input = panel.element.querySelector('input[name="password"]') as HTMLInputElement;
    password_monitor(password_input);


    // -- Get the rp-password input
    const rp_password_input = panel.element.querySelector('input[name="rp-password"]') as HTMLInputElement;
    rp_password_monitor(password_input, rp_password_input);

    // -- Get the submit button
    const submit_button = panel.element.querySelector('button[type="submit"]') as HTMLButtonElement;


    submit_button.addEventListener('click', async (event) => {
        // -- Validate all inputs
        const name_valid = validate_name(name_input.value);
        const password_valid = validate_password(password_input.value);


        // -- Make sure the passwords match
        if (password_input.value !== rp_password_input.value)
            return create_toast('error', 'Passwords', 'Oops! It looks like your passwords don\'t match.');
        
        // -- Make sure the name is valid
        if (name_valid.length > 0)
            return create_toast('error', 'Name', 'Oops! It looks like your name is invalid.');

        // -- Make sure the password is valid
        if (password_valid.length > 0)
            return create_toast('error', 'Password', 'Oops! It looks like your password is invalid.');


        // -- If the email is not verified, make sure the user
        // has entered a valid email
        if (!response.user.verified_email) {
            // -- Make sure the email is there, email validation
            //    will be done by just sending an email to the user
            if (email_input.value.length === 0)
                return create_toast('error', 'Email', 'Oops! It looks like you haven\'t entered an email.');
        }
        

        // -- Disable the button
        submit_button.disabled = true;

        // -- Make the request
        let register_attempt = register_with_oauth(
            response.token,
            password_input.value,
            name_input.value,
            email_input.value,
        );

        // -- Handle the response
        register_attempt.then(async (reg_req) => {
            // -- Check the status of the response
            if (reg_req.status === 'error') {
                submit_button.disabled = false;
                return create_toast('error', 'Error', reg_req.message);
            }

            // -- If we get here, we can submit the form
            create_toast('success', 'Account created!', 'Your account has been created! You will be redirected to the home page shortly.');
            
            // -- Get the token
            if (await auth_token(reg_req.token) == false) {
                submit_button.disabled = false;
                return create_toast('error', 'Error', 'There was some issue logging you in, please try again.');
            }

            else {
                // -- Redirect the user to the home page
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
            }

        });
    });
}