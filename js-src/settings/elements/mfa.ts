import { attach, confirmation_modal, construct_modal, handle_tfa_input } from '../../click_handler';
import { SecurityInfo, DefualtSuccess } from '../index.d';
import { create_toast } from '../../toasts';
import disable_tfa from '../api/disable_tfa';
import verify_tfa from '../api/verify_tfa';
import setup_tfa from '../api/setup_tfa';



/**
 * @param data: SecurityInfo - The security info
 * @param parent_elm: HTMLDivElement - The parent element
 * @param access_key: string - The access key
 * 
 * @returns void
 * 
 * @description This function handles the removal and addition of mfa
 *              to the user's account.
 */
export default (
    data: SecurityInfo,
    parent_elm: HTMLDivElement,
    access_key: string,
) => {
    const remove_tfa = parent_elm.querySelector('#remove-tfa') as HTMLButtonElement,
        add_tfa = parent_elm.querySelector('#add-tfa') as HTMLButtonElement;

    // -- Add remove listener
    remove_tfa.onclick = async () => {
        remove_listner(remove_tfa, access_key);
    };

    // -- Add tfa listener
    add_tfa.onclick = async () => {
        add_listner(add_tfa, access_key, data);
    };
};



/**
 * @name remove_listner
 * 
 * @param button: HTMLButtonElement - The button
 * @param access_key: string - Data modifcation key
 * 
 * @returns void
 * 
 * @description This function handles the removal of mfa
 *              from the user's account, it also prompts
 *              the user to confirm the action before
 *              proceeding.
 */
function remove_listner(
    button: HTMLButtonElement,
    access_key: string,
) {
    // -- Attach the spinner
    const stop_spinner = attach(button);

    // -- Try to remove tfa
    confirmation_modal(async () => {
        // -- Try to remove tfa
        const res = await disable_tfa(access_key);

        // -- Check if we got an error
        if (res.code !== 200) {
            create_toast('error', 'Oops, there appears to be an error', res.message);
            return;
        }

        // -- Else show the success
        create_toast(
            'success',
            'Two factor authentication removed',
            'Successfully removed two factor authentication',
        );
        
        // -- Stop the spinner
        set_mfa(false);
        stop_spinner();
    },
    () => stop_spinner(),
    'Are you sure you want to remove two factor authentication? This action cannot be undone.');
}



/**
 * @name add_listner
 * 
 * @param button: HTMLButtonElement - The button
 * @param access_key: string - Data modifcation key
 * @param data: SecurityInfo - The security info
 * 
 * @returns void
 * 
 * @description This function handles the addition of mfa
 *              to the user's account, provides the user 
 *              with a qr code to scan with their authenticator
 *              or a link they can click, usally on mobile that
 *              will open the authenticator app.
 */ 
async function add_listner(
    button: HTMLButtonElement,
    access_key: string,
    data: SecurityInfo,
) {
    // -- Attach the spinner and start the request
    const stop_spinner = attach(button),
        res = await setup_tfa(access_key);

    // -- Check if we got an error
    if (res.code !== 200) {
        create_toast('error', 'Oops, there appears to be an error', res.message);
        return stop_spinner();
    }

    // -- Else get the token
    const token = (res as DefualtSuccess).data.token as string;
    if (!token) {
        create_toast('error', 'Oops, there appears to be an error', 'No token was returned');
        return stop_spinner();
    }


    // -- Construct the mfa url
    const tfa = construct_qr_url(token, 'StreamStage', data.email),
        modal = construct_modal(
        'Add two factor authentication',
        'Scan the QR Code below with your authenticator app. If you are on mobile, click the link below the QR Code. Then enter the code below to complete the process.',
        true,
        `<img class="w-50 mx-auto d-block rounded" src="${tfa.url}" alt="QR Code"/>
        <a class="mt-3 text-center" href="${tfa.otp}" target="_blank">On mobile? Click here</a>
        <div class="form-group mt-3 mb-3 tfa-input d-flex gap-2 justify-content-center"></div>`
    );

    // -- Add the modal to the body
    const modal_div = document.createElement('div');
    modal_div.innerHTML = modal;
    document.body.appendChild(modal_div);

    // -- Get the inpus
    const yes_btn = modal_div.querySelector('.yes') as HTMLButtonElement,
        no_btn = modal_div.querySelector('.no') as HTMLButtonElement,
        tfa_input = modal_div.querySelector('.tfa-input') as HTMLDivElement;

    // -- Disable the yes button
    yes_btn.disabled = true;

    // -- Handle the tfa input
    let otp = '';
    handle_tfa_input(tfa_input, (code) => {
        otp = code;
        yes_btn.disabled = false;
    }, () => yes_btn.disabled = true);

    
    //
    // -- Add MFA listener
    //
    yes_btn.addEventListener('click', async () => {
        const yes_stop = attach(yes_btn);
        const res = await verify_tfa(access_key, otp);

        // -- Check if we got an error
        if (res.code === 401) {
            create_toast('error', 'Oops, there appears to be an error', 'The code you entered is invalid');
            return yes_stop();
        }

        else if (res.code !== 200) {
            create_toast('error', 'Oops, there appears to be an error', res.message);
            return yes_stop();
        };

        // -- Alert the user
        create_toast('success', 'Success', 'Two factor authentication has been enabled');
        set_mfa(true);
        stop_spinner();
        modal_div.remove();
    });


    //
    // -- Add cancel MFA listener
    //
    no_btn.addEventListener('click', () => {
        stop_spinner();
        modal_div.remove();
    });
}



/**
 * @name construct_qr_url
 * 
 * @param secret: string - The secret key
 * @param issuer: string - The issuer aka us
 * @param account: string - The account, aka the user's email
 * 
 * @returns { url: string; otp: string; } - The url and otp string
 * 
 * @description This function constructs the url and otp string
 *              for the qr code and the link to the authenticator    
 *              app.
 */
function construct_qr_url(secret: string, issuer: string, account: string,
): { url: string; otp: string; } {
    const otp = `otpauth://totp/${issuer} (${account})?secret=${secret}&issuer=${issuer}`;
    const url = `https://chart.googleapis.com/chart?chs=250x250&chld=L|0&cht=qr&chl=${otp}`;
    return { url, otp }
}



/**
 * @name set_mfa
 * 
 * @param value: boolean - The value to set 
 * 
 * @returns void
 * 
 * @description This function sets the mfa value
 *              for all the elements with the data attribute 
 *              data-has-tfa, which enables / disables certain
 *              elements depending on if the user has mfa enabled.
 */
function set_mfa(value: boolean){
    // -- Get all the elements with the data attribute
    const elements = document.querySelectorAll('[data-has-tfa]');
    for (const element of Array.from(elements)) {
        element.setAttribute('data-has-tfa', value ? 'true' : 'false');
    }
}