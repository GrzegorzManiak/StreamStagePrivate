import { attach } from "../../click_handler";
import { recent, remove, send_verification } from "../api/email_verification";
import { create_toast } from '../../toasts';
import { open_panel } from './panels';
import { Pod, SecurityInfoSuccess, VerifyAccessSuccess, SecurityInfo} from "../index.d";
import { get_security_info } from "../api/security_info";

import create_linked_account from '../elements/oauth';
import create_login_history from '../elements/history';

// 
// Main entry point for the security panel
// 
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
        await click_handler(stop_spinner, button, 'email');
    });
}



//
// If a user wants to resend the verification email
// we will just store the old ones and terminate them
//
let resend_keys: string[] = [];
let panel_open = false;

// 
// This function will be called when the user clicks the button
// to send a verification email to their email address 
// 
async function click_handler(
    stop: () => void, 
    button: HTMLButtonElement,
    type: 'email' | 'tfa'
) {
    // -- Loop through the resend keys and terminate them
    for (const key of resend_keys) {
        const remove_res = await remove(key);
        if (remove_res.code !== 200) {
            create_toast('error', 'verification', remove_res.message);
        }

        // -- Remove the key from the array
        resend_keys = resend_keys.filter(k => k !== key);
        create_toast('success', 'verification', 'The previous verification email has been terminated');
    }

    // -- Send the verification request
    const res = await send_verification(type);

    // -- If its a 200, then show a success toast
    if (res.code !== 200) {
        create_toast('error', 'verification', 'There was an error sending the verification email: ' + res.message);
        return stop();
    }
    
    // -- The request was a success
    create_toast('success', 'Please check your email', 'We have sent you a verification email, It will be valid for 15 Minutes');


    // -- Get the request details 
    let { 
        access_key, 
        resend_key, 
        verify_key 
    } = (res as VerifyAccessSuccess).data;

    // -- Store the resend key
    resend_keys.push(resend_key);
    
    // -- Check if the email has been verified
    const verified = check_email_verification(() => verify_key);
    stop();

    // -- If the email has been verified
    verified.then(async() => {
        // -- Get the data
        const res = await get_security_info(access_key);

        // -- If the request was a success
        if (res.code !== 200 || !Object.keys(res).includes('data')) 
            return create_toast('error', 'Oops, there appears to be an error', res.message);
        
        // -- Else, Get the data
        const data = (res as SecurityInfoSuccess).data;
        console.log(data);
        fill_data(data);
        
        // -- Open the panel
        open_panel('security-verified');
    });
}

// -- This function will run every x seconds
//    to check if the email has been verified
async function check_email_verification(
    verify_token: () => string,
): Promise<boolean> {
    return new Promise(async (resolve, reject) => {
        const int = setInterval(async () => {
            const response = await recent(verify_token());
    
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


// data-panel-type='security-verified'
function fill_data(
    data: SecurityInfo
) {
    // -- Get the panel
    const panel = document.querySelector('[data-panel-type="security-verified"]');

    

    //
    // -- Extend session
    //
    const ES_ID = 'extend-verification-time-container',
        es_elm = panel.querySelector(`#${ES_ID}`) as HTMLDivElement;

    const btn = es_elm.querySelector('button') as HTMLButtonElement;
    console.log(btn);



    //
    // -- 2FA
    //
    const TFA_ID = 'two-factor-authentication-container',
        tfa_elm = panel.querySelector(`#${TFA_ID}`) as HTMLDivElement;
    console.log(tfa_elm);
    

    
    //
    // -- Linked Accounts
    //
    const LA_ID = 'linked-accounts-container',
        la_elm = panel.querySelector(`#${LA_ID}`) as HTMLDivElement;

    // #linked-accounts
    const linked_accounts = la_elm.querySelector('#linked-accounts') as HTMLDivElement;
    for (const account of data.service_providers) {
        const new_elm = create_linked_account(
            account,
            () => {}
        );

        linked_accounts.appendChild(new_elm);
    }


    //
    // -- Change Password
    //
    const CP_ID = 'change-password-container',
        cp_elm = panel.querySelector(`#${CP_ID}`) as HTMLDivElement;



    //
    // -- Change Email
    //  
    const CE_ID = 'change-email-container',
        ce_elm = panel.querySelector(`#${CE_ID}`) as HTMLDivElement;

    console.log(ce_elm);



    //
    // -- Login History
    //
    const LH_ID = 'login-history-container',
        lh_elm = panel.querySelector(`#${LH_ID}`) as HTMLDivElement;

    // #login-history
    const login_history = lh_elm.querySelector('#login-history') as HTMLDivElement;
    for (const login of data.login_history) {
        const new_elm = create_login_history(login);
        login_history.appendChild(new_elm);
    }



    //
    // -- Delete Account
    //
    const DA_ID = 'delete-account-container',
        da_elm = panel.querySelector(`#${DA_ID}`) as HTMLDivElement;

    console.log(da_elm);
}