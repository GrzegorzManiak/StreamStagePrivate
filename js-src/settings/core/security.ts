import { PanelType, Pod, SecurityInfo, SecurityInfoSuccess, VerifyAccessSuccess} from "../index.d";
import create_linked_account, { attach_lister } from '../elements/oauth';
import { attach, handle_tfa_input } from "../../click_handler";
import { add_callback, get_active_pod, hide_pod, open_panel, show_pod } from './panels';
import { create_toast } from '../../toasts';

import create_login_history from '../elements/history';
import mfa from "../elements/mfa";
import { change_email, check_email_verification, close_session, extend_session, get_security_info, remove, send_verification, update_profile } from "../apis";
import { create_preference_toggles } from "../elements/security";
import { password_monitor, rp_password_monitor } from "../../authentication/core/validation";

const security_panels = [
    'security-preferences',
    'security-mfa',
    'security-linked-accounts',
    'security-password',
    'security-email',
    'security-history',
    'security-delete'
]

let verified = false;

/**
 * @param pod: Pod - The pod that this panel is attached to
 * 
 * @returns void
 * 
 * @description This function manages the security panel
 */
export function manage_security_panel(pod: Pod) {

    // -- Get the panel
    const panel = pod.panel.element,
        mfa_input = panel.querySelector('#mfa-input') as HTMLInputElement;

    // -- Get the verify access buttons
    const email_button = panel.querySelector('#send-verification-email') as HTMLButtonElement,
        tfa_button = panel.querySelector('#verify-tfa') as HTMLButtonElement;

    add_callback(async () => {
        if (!verified) return;

        // -- Get the timer panel
        const timer_panel = document.querySelector('#security-timer');

        // -- Get the current panel
        const pod = get_active_pod();

        // -- If we left the security panel
        if ( security_panels.indexOf(pod.type) === -1 && pod.type !== 'security'
        ) timer_panel.setAttribute('data-panel-status', 'hidden');
        else timer_panel.setAttribute('data-panel-status', '');
    });

    tfa_button.disabled = true;
    let mfa_code = '';
    handle_tfa_input(mfa_input, 
        (code) => {
            tfa_button.disabled = false;
            mfa_code = code;
        },
        () => tfa_button.disabled = true
    );


    // -- Add the click event listeners
    email_button.addEventListener('click', async () => email_click_handler(email_button));
    tfa_button.addEventListener('click', async () => await mfa_click_handler(tfa_button, () => mfa_code));
}



/**
 * @name resend_keys
 * @description This array stores the resend keys for
 *              when the user wants to resend the 
 *              verification email when entering the
 *              Security panel.
 * 
 *              They get looped ove and terminated every
 *              time the user clicks the button to send
 *              a new verification email.
 */
let resend_keys: string[] = [];



/**
 * @name terminate_resend_keys
 * @description This function terminates all the resend
 *              keys that are stored in the resend_keys
 *              array.
 * @returns Promise<void>
 */
export async function terminate_resend_keys() {
    return new Promise(async (resolve) => {
        for (const key of resend_keys) {
            remove(key).then(res => { if (res.code === 200) create_toast(
                'success',
                'verification',
                'The previous verification email has been terminated'
            )});
    
            // -- Remove the key from the array
            resend_keys = resend_keys.filter(k => k !== key);
        }
        
        // -- We're done
        return resolve(undefined);
    });
}



/**
 * @name email_click_handler
 * @param button: HTMLButtonElement - The button that was clicked
 * @returns Promise<void>
 * 
 * @description This function is called when the user clicks the
 *              button to send a verification email to their email   
 *              address, and awaits a response from the server 
 *              that specifies if the user has verified their email
 *              address or not.
 * 
 *              If the user has verified their email address, then
 *              the function will open the security panel.
 */
async function email_click_handler(
    button: HTMLButtonElement,
) {
    // -- Attach the spinner, terminate the resend keys, and send the verification request
    const stop_spinner = attach(button);
    await terminate_resend_keys();
    const res = await send_verification('email');

    // -- If its a 200, then show a success toast
    if (res.code !== 200) {
        create_toast(
            'error', 
            'verification', 
            'There was an error sending the verification email: ' + res.message
        );
        return stop_spinner();
    }
    
    // -- The request was a success
    create_toast(
        'success', 
        'Please check your email', 
        'We have sent you a verification email, It will be valid for 15 Minutes'
    );


    // -- Get the request details 
    let { access_key, resend_key, verify_key 
    } = (res as VerifyAccessSuccess).data;

    // -- Store the resend key
    resend_keys.push(resend_key);
    
    // -- Check if the email has been verified
    check_email_verification(() => verify_key).then(
        async() => open_security_panel(stop_spinner, access_key)
    );
}



/**
 * @name mfa_click_handler
 * @param button: HTMLButtonElement - The button that was clicked
 * @param get_code: () => string - A function that returns the mfa code
 *                                 from whatever the user has entered
 * @returns Promise<void>
 * 
 * @description This function is called when the user clicks the
 *              button to verify their mfa code, and awaits a response   
 *              from the server that specifies if the user has verified
 *              their mfa code or not.
 * 
 *              If the user has verified their mfa code, then the function
 *              will open the security panel.
 */
async function mfa_click_handler(
    button: HTMLButtonElement,
    get_code: () => string = () => ''
) {
    // -- Send the verification request, and attach the spinner
    const stop_spinner = attach(button);
    const res = await send_verification('tfa', get_code());

    // -- If its a 200, then show a success toast, 401 is invalid code
    if (res.code === 401) {
        create_toast(
            'error', 
            'verification', 
            'The code you entered is invalid'
        ); 
        return stop_spinner();
    }
    else if (res.code !== 200) {
        create_toast(
            'error', 
            'verification', 
            'There was an error verifying your code: ' + res.message
        );
        return stop_spinner();
    }
    
    // -- The request was a success
    create_toast(
        'success', 
        'verification', 
        'Your code has been verified'
    );

    // -- Get the access key, and open the security panel
    const { access_key } = (res as VerifyAccessSuccess).data;
    open_security_panel(stop_spinner, access_key);
}



/**
 * @name open_security_panel
 * @param stop: () => void - A function that stops the spinner
 *                           eg the mfa button spinner
 * @param access_key: string - The access key of the user (this is the 
 *                             key that the user verified their details for,
 *                             it is used to get sensitive information)
 * @returns Promise<void>
 * 
 * @description This function is called when the user has verified their
 *              email address or mfa code, and it will get the sensitive
 *              information from the server, and open the security panel.
 * 
 *              If the user has not verified their email address or mfa code,
 *              then this function if ran, will fail.
 */
async function open_security_panel(stop: () => void, access_key: string) {
    // -- Get the data
    const res = await get_security_info(access_key);
    stop();
    
    // -- If the request was a success
    if (res.code !== 200 || !Object.keys(res).includes('data')) 
        return create_toast('error', 'Oops, there appears to be an error', res.message);
    
    // -- Else, Get the data and open the security panel
    const data = (res as SecurityInfoSuccess).data;
    fill_data(data, access_key);
    // -- Show all the panels 
    for (let sec_panel in security_panels) {
        show_pod(security_panels[sec_panel] as PanelType);
    }
    open_panel('security-verified');
}



/**
 * @name fill_data
 * @param data: SecurityInfo - The security information
 * @param access_key: string - The access key of the user
 * @returns void
 * 
 * @description This function is called when the user has verified their
 *              email address or mfa code, and it will fill the security 
 *              panel with the sensitive information. 
 * 
 *              It automatically updates data every x seconds.
 */
function fill_data(
    data: SecurityInfo,
    access_key: string
) {
    // -- Get the timer panel
    const timer_panel = document.querySelector('#security-timer');
    timer_panel.setAttribute('data-panel-status', '');
    
    // -- Get the security panel
    const security_panel = document.querySelector('#security-panel');
    security_panel.setAttribute('data-panel-status', 'hidden');
    
    const panel = document;
    verified = true;

    //
    // -- Session Management
    //
    const ES_ID = 'extend-verification-time-container',
        es_elm = panel.querySelector(`#${ES_ID}`) as HTMLDivElement,
        btn = es_elm.querySelector('button') as HTMLButtonElement,
        timer = es_elm.querySelector('#extend-verification-time-timer') as HTMLHeadingElement;

    let time_left = 15 * 60 * 1000; // -- 15 minutes
    btn.onclick = async () => {
        const stop_spinner = attach(btn);
        const res = await extend_session(access_key);
        stop_spinner();

        if (res.code !== 200) return create_toast('error', 'Oops, there appears to be an error', res.message);
        create_toast('success', 'Success', 'Your session has been extended by 15 minutes');

        // -- Reset the timer
        time_left = 15 * 60 * 1000;
    };
    

    // -- Close session
    const close_session_btn = es_elm.querySelector('#close-secure-session') as HTMLButtonElement;



    //
    // -- 2FA
    //
    const TFA_ID = 'two-factor-authentication-container',
        tfa_elm = panel.querySelector(`#${TFA_ID}`) as HTMLDivElement;

    mfa(data, tfa_elm, access_key);

    

    //
    // -- Linked Accounts
    //
    const LA_ID = 'linked-accounts-container',
        la_elm = panel.querySelector(`#${LA_ID}`) as HTMLDivElement;

    attach_lister(la_elm);

    // #linked-accounts
    const linked_accounts = la_elm.querySelector('#linked-accounts') as HTMLDivElement;
    const update_providers = (data: SecurityInfo) => {
        // -- Clear the linked accounts
        linked_accounts.innerHTML = '';

        // -- Add the new linked accounts
        for (const account of data.service_providers) {
            const new_elm = create_linked_account(account, access_key);
            linked_accounts.appendChild(new_elm);
        }
    }
    update_providers(data);



    //
    // -- Change Password
    //
    const CP_ID = 'change-password-container',
        cp_elm = panel.querySelector(`#${CP_ID}`) as HTMLDivElement,
        requirements = cp_elm.querySelector('.requirements') as HTMLDivElement,
        password_errors = cp_elm.querySelector('.password-errors') as HTMLDivElement,
        change_password_btn = cp_elm.querySelector('#change-password') as HTMLButtonElement;

    // -- Inputs #cpass, #npass, #vpass
    const cpass = cp_elm.querySelector('#cpass') as HTMLInputElement,
        npass = cp_elm.querySelector('#npass') as HTMLInputElement,
        cfpass = cp_elm.querySelector('#cfpass') as HTMLInputElement;
    
    password_monitor(npass, password_errors);
    rp_password_monitor(npass, cfpass);
    npass.addEventListener('focus', () => requirements.style.display = 'block');
    npass.addEventListener('blur', () => {
        requirements.style.display = 'none';
        npass.removeAttribute('data-strength');
    });

    // -- Set the button
    change_password_btn.onclick = async () => {
        // -- Attach the spinner
        const stop_spinner = attach(change_password_btn);

        // -- Get the values
        const current_password = cpass.value,
            new_password = npass.value,
            confirm_password = cfpass.value;

        // -- Check if the passwords match
        if (new_password !== confirm_password) {
            stop_spinner();
            return create_toast('error', 'Oops, there appears to be an error', 'The passwords do not match');
        }
            
        // -- Send the request
        const res = await update_profile({
            token: access_key,
            old_password: current_password.trim(),
            password: new_password.trim()
        });

        // -- Check if the request was successful
        if (res.code !== 200) create_toast('error', 'Oops, there appears to be an error', res.message);
        else {
            create_toast('success', 'Success', 'Your password has been updated');
            await new Promise(resolve => setTimeout(resolve, 2000));
            document.location = '/';
        }
        return stop_spinner();
    };


    //
    // -- Change Email
    //  
    const CE_ID = 'change-email-container',
        ce_elm = panel.querySelector(`#${CE_ID}`) as HTMLDivElement;

    // #email, #change-email
    const email = ce_elm.querySelector('#email') as HTMLInputElement,
        change_email_btn = ce_elm.querySelector('#change-email') as HTMLButtonElement,
        current_email = ce_elm.querySelector('.current-email') as HTMLParagraphElement;
    current_email.innerText = 'Your current email is ' + data.email;

    // -- Set the button
    change_email_btn.onclick = async () => {
        // -- Attach the spinner
        const stop_spinner = attach(change_email_btn),
            new_email = email.value;


        // -- Send the request, make sure the email is valid
        const res = await change_email(access_key, new_email);
        if (res.code !== 200) {
            stop_spinner();
            return create_toast('error', 'Oops, there appears to be an error', res.message);
        }
        create_toast('success', 'Success', 'A verification email has been sent to your new email address');


        const data = (res as VerifyAccessSuccess).data;
        check_email_verification(() => data.verify_key, 3000, 15 * 60 * 1000,
        'Your email has been changed successfully!').then((success) => {
            stop_spinner();
            if (!success) create_toast('error', 'Oops, there appears to be an error', 'Your email has not been changed');
            else current_email.innerText = 'Your current email is ' + new_email;
        });
    }



    //
    // -- Login History
    //
    const LH_ID = 'login-history-container',
        lh_elm = panel.querySelector(`#${LH_ID}`) as HTMLDivElement;

    // #login-history
    const login_history = lh_elm.querySelector('#login-history') as HTMLDivElement;
    const update_history = (data: SecurityInfo) => {
        // -- Clear the login history
        login_history.innerHTML = '';

        for (const login of data.login_history) {
            const new_elm = create_login_history(login);
            login_history.appendChild(new_elm);
        }
    }
    update_history(data);



    //
    // -- Delete Account
    //
    const DA_ID = 'delete-account-container',
        da_elm = panel.querySelector(`#${DA_ID}`) as HTMLDivElement;

    

    //
    // -- Security preferences
    //
    const SP_ID = 'security-preferences-container',
        sp_elm = panel.querySelector(`#${SP_ID}`) as HTMLDivElement;

    // -- Toggles
    const toggles_elm = sp_elm.querySelector('.toggles') as HTMLDivElement;
    const update_toogles = (data: SecurityInfo) => {
        toggles_elm.innerHTML = '';
        const toggles = create_preference_toggles(data.security_preferences, async(pref: string, val: boolean) => {
            const res = await update_profile({ [pref]: val, token: access_key });
            if (res.code !== 200) return create_toast('error', 'Oops, there appears to be an error', res.message);
        });
        toggles.forEach((elm) => toggles_elm.appendChild(elm));
    }
    update_toogles(data);



    /**
     * @name timer_interval
     * @description This interval will update the timer
     * every second, this is the big timer on top of the 
     * page indicating how much time the user has left
     * to make changes to their account.
     */
    const timer_interval = setInterval(() => {
        // -- Update the timer
        time_left -= 1000;
        
        let min = Math.floor(time_left / 1000 / 60),
            sec = Math.floor(time_left / 1000) % 60;

        timer.innerText = `${min}:${sec < 10 ? '0' + sec : sec}`;

        // -- If the time is up
        if (time_left <= 0) {
            create_toast('error', 'Oops, there appears to be an error', 'Your session has expired, please refresh the page to continue');
            open_panel('security');
        }
    }, 1000);


    /**
     * @name close
     * @description Closes the security panel AND 
     * revokes the users PAK (access key) and clears
     * any remianing intervals and data
     */
    const close = () => {
        linked_accounts.innerHTML = '';
        login_history.innerHTML = '';

        show_pod('security');
        open_panel('security');
        clearInterval(timer_interval);
        clearInterval(data_interval);

        verified = false;
        timer_panel.setAttribute('data-panel-status', 'hidden');
        security_panel.setAttribute('data-panel-status', '');
        
        // -- Hide all the panels
        for (let sec_panel in security_panels) {
            hide_pod(security_panels[sec_panel] as PanelType, 'security');
        } 
    
    }


    /**
     * @name data_interval
     * @description Updates the data every 5 seconds
     * And checks if the users PAK is still valid
     */
    const data_interval = setInterval(async () => {
        const res = await get_security_info(access_key);
        if (res.code !== 200) {
            create_toast('error', 'Oops, there appears to be an error', res.message);
            return close();
        }

        // -- Get the data
        const data = (res as SecurityInfoSuccess).data;
        verified = true;

        // -- Update data
        update_providers(data);
        update_history(data);
        update_toogles(data);
    }, 5000);
    
    
    /**
     * @name close_session_btn
     * @description Closes the current session for the user 
     * It actually removes the access key from the database
     * so its completely useless, unlike refresing the page
     * where the access key is still valid.
     */
    close_session_btn.onclick = async () => {
        const stop_spinner = attach(close_session_btn),
            res = await close_session(access_key);

        if (res.code !== 200) {
            stop_spinner();
            return create_toast('error', 'Oops, there appears to be an error', res.message);
        }

        // -- Clear the data
        create_toast('success', 'Success', 'Your session has been closed');
        stop_spinner();
        close();
    };
}