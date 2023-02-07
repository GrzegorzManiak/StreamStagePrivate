import { Panel, PanelType, Response } from '../index.d';
import { get_panel, hide_all_panels_except, hide_panel, show_panel } from '../core/panel_manager';
import { ToastType, create_toast } from '../../toasts';
import { attach } from '../core/spinner';
import { recent, resend } from '../api/email';
import { login_url, sleep } from '..';


// -- This function will run every x seconds
//    to check if the email has been verified
async function check_email_verification(
    verify_token: string,
    button: HTMLButtonElement,
) {
    console.log(verify_token);
    return setInterval(async () => {
        const response = await recent(verify_token);

        // -- If the email has been verified
        if (response.code === 404) {} // -- Do nothing
        else if (response.code === 200) {
            // -- Login the user
            button.disabled = true;
            create_toast('success', 'Congratulations!', 'Your email has been verified, you\'ll be redirected to the home page in a few seconds.');
            await sleep(3000);
            window.location.href = login_url;
        }
        else {
            // -- Show the error
            create_toast('error', 'Error', response.message);
        }
    }, 3000);
}


export async function complete_verification(
    current_panel: PanelType,
    email: string,
    password: string,
    username: string,
    response: any
) {    
    create_toast(response.status, 'Registration', response.message);
    if (response.code !== 200) return;

    // -- Print out the token
    let resend_token = response.data.token,
        verify_token = response.data.verify_token;

    // -- Change the panel
    hide_all_panels_except('email-wait');
    
    // -- Get the resend button
    const resend_button = get_panel('email-wait').element.querySelector(
        'button[name="resend"]') as HTMLButtonElement;

    const email_input = get_panel('email-wait').element.querySelector(
        'input[name="email"]') as HTMLInputElement;
    email_input.value = email;


    // -- Start the verification checker
    check_email_verification(verify_token, resend_button);

    // -- Add the click handler
    resend_button.addEventListener('click', async () => {
        await handle_click(
            email,
            email_input.value,
            resend_button,
            resend_token,
            (token: string) => resend_token = token
        );
    });
}

async function handle_click(
    email: string,
    new_email: string,
    button: HTMLButtonElement,
    token: string,
    set_token: (token: string) => void
) {
    // -- Attach the spinner
    const stop_spinner = attach(button);

    // -- Check if the user set a new email
    let response = null;
    if (new_email === email) response = await resend(token);
    else response = await resend(token, new_email);

    // -- Handle the response
    // 306: Email already used
    // 200: Email sent
    // 302: Cooldown
    // 400: Error

    // -- Non fatal errors
    if (
        response.code === 306 ||
        response.code === 302 
    ) {
        create_toast(response.status as ToastType, 'Email', response.message);
        return await stop_spinner();
    } 
    
    // -- Fatal errors
    if (response.code !== 200) {
        create_toast(response.status as ToastType, 'Email', response.message);
        return await stop_spinner();
    }

    // -- Email sent
    create_toast(response.status as ToastType, 'Email', response.message);
    set_token(response.data.token);
    await stop_spinner();
    button.disabled = true;

    // -- Wait 1 minute
    return await sleep(60000).then(() => {
        button.disabled = false;
    });
}