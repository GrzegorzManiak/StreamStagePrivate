import { attach } from "../../click_handler";
import { recent, send_verification } from "../api/email_verification";
import { create_toast } from '../../toasts';
import { Pod, VerifyAccessSuccess } from "../index.d";

export function manage_security_panel(pod: Pod) {
    console.log('Managing security panel');

    // -- Get the panel
    const panel = pod.panel.element;

    // -- Get the verify access button
    // #send-verification-email
    const button = panel.querySelector('#send-verification-email') as HTMLButtonElement;

    // -- Add the click event listener
    button.addEventListener('click', async () => {
        const stop_spinner = attach(button);
        await click_handler(stop_spinner, 'email');
    });
}

async function click_handler(stop: () => void, type: 'email' | 'tfa') {
    // -- Send the verification request
    const res = await send_verification(type);

    // -- If its a 200, then show a success toast
    if (res.code !== 200) {
        create_toast('error', 'verification', 'There was an error sending the verification email');
        return stop();
    }
    
    // -- The request was a success
    create_toast('success', 'Please check your email', 'We have sent you a verification email, It will be valid for 15 Minutes');


    // -- Get the request details 
    const { 
        access_key, 
        resend_key, 
        verify_key 
    } = (res as VerifyAccessSuccess).data;
    
    // -- Check if the email has been verified
    const verified = await check_email_verification(verify_key);
    if (verified === false) return stop();

    // -- Continue to show the panel
}

// -- This function will run every x seconds
//    to check if the email has been verified
async function check_email_verification(
    verify_token: string,
): Promise<boolean> {
    return new Promise(async (resolve, reject) => {
        const int = setInterval(async () => {
            const response = await recent(verify_token);
    
            // -- If the email has been verified
            if (response.code === 404) {} // -- Do nothing
            else if (response.code === 200) {
                // -- Login the user
                create_toast('success', 'Congratulations!', 'Your email has been verified, you\'ll be given access to your account in a few seconds.');
                clearInterval(int);
                resolve(true);
            }
            else {
                // -- Show the error
                create_toast('error', 'Error', response.message);
                clearInterval(int);
                reject(false);
            }
        }, 3000);
    
        // -- Stop the interval after 15 minutes
        setTimeout(() => {
            clearInterval(int);
        }, 15 * 60 * 1000);
    });
}
