import { Panel, PanelType, Response } from '../index.d';
import { get_panel, hide_panel, show_panel } from './panel_manager';
import { name_monitor, password_monitor, rp_password_monitor } from './validation';
import * as DOMPurify from 'dompurify';


// -- Handle instructions
const instruction_parser = (instructions: string): Response | null => {
    // -- Try decoding instructions
    try { return JSON.parse(atob(instructions)); }
    catch (error) { return null; }
};


export const instruction_handler = (instructions: string) => {
    // -- Parse instructions
    const response = instruction_parser(instructions);

    // -- If there is no response, return
    if (!response) return;
    if (response.message !== 'Success') {
        console.error(response.message);
        return;
    }   

    // -- Since the user has provided oauth
    // data, we can hide the login panel,
    // and show the oauth panel if they
    // need to fill in some more required
    // fields
    hide_panel('defualt' as PanelType);
    show_panel('oauth' as PanelType);

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
}