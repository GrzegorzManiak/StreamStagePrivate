import {
    PanelType,
    Response,
} from '../index.d';
import { get_panel, hide_panel, panels, show_panel } from './panel_manager';
import { attach_to_input } from './password';

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

    // -- Handle response, hide the default panel
    hide_panel('defualt' as PanelType);

    // -- Show the panel
    show_panel('oauth' as PanelType);

    // -- Get the panel
    const panel = get_panel('oauth' as PanelType) 


    // -- Get the email input and set the value
    const email_input = panel.element.querySelector('input[name="email"]') as HTMLInputElement;
    email_input.value = response.user.email;

    // -- If the email is verified, hide the email input
    if (response.user.verified_email) {
        email_input.parentElement.style.display = 'none';
    }

    // -- Get the name input and set the value
    const name_input = panel.element.querySelector('input[name="username"]') as HTMLInputElement;
    name_input.value = response.user.name;

    // -- Get the password input 
    const password_input = panel.element.querySelector('input[name="password"]') as HTMLInputElement;
    attach_to_input(password_input);

    // -- Get the rp-password input
    const rp_password_input = panel.element.querySelector('input[name="rp-password"]') as HTMLInputElement;


    // -- Get the submit button
    const submit_button = panel.element.querySelector('button[type="submit"]') as HTMLButtonElement;

}