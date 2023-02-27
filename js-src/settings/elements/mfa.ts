import { attach, confirmation_modal, construct_modal } from '../../click_handler';
import { create_toast } from '../../toasts';
import { SecurityInfo, DefualtSuccess } from '../index.d';
import setup_tfa from '../api/setup_tfa';
import verify_tfa from '../api/verify_tfa';
import disable_tfa from '../api/disable_tfa';

export default (
    data: SecurityInfo,
    parent_elm: HTMLDivElement,
    access_key: string,
) => {
    const remove_tfa = parent_elm.querySelector('#remove-tfa') as HTMLButtonElement,
        add_tfa = parent_elm.querySelector('#add-tfa') as HTMLButtonElement;

    // -- Add remove listener
    remove_tfa.onclick = async () => {
        // -- Attach the spinner
        const stop_spinner = attach(remove_tfa);

        // -- Try to remove tfa
        confirmation_modal(
            async () => {
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
            'Are you sure you want to remove two factor authentication? This action cannot be undone.',
        );
    };

    // -- Add tfa listener
    add_tfa.onclick = async () => {
        // -- Attach the spinner
        const stop_spinner = attach(add_tfa);

        // -- Try to setup tfa
        const res = await setup_tfa(access_key);

        // -- Check if we got an error
        if (res.code !== 200) {
            // -- Stop the spinner
            stop_spinner();

            // -- Show the error
            create_toast('error', 'Oops, there appears to be an error', res.message);
            return;
        }

        // -- Else get the token
        const token = (res as DefualtSuccess).data.token as string;
        if (!token) {
            // -- Stop the spinner
            stop_spinner();

            // -- Show the error
            create_toast('error', 'Oops, there appears to be an error', 'No token was returned');
            return;
        }

        const tfa = construct_qr_url(token, 'StreamStage', data.email);

        const modal = construct_modal(
            'Add two factor authentication',
            'Scan the QR Code below with your authenticator app. If you are on mobile, click the link below the QR Code. Then enter the code below to complete the process.',
            true,
            `
                <img 
                    class="w-50 mx-auto d-block rounded"
                    src="${tfa.url}" 
                    alt="QR Code" 
                />

                <!-- Or click here to open -->
                <a
                    class="mt-3 text-center"
                    href="${tfa.otp}"
                    target="_blank"
                >
                    On mobile? Click here
                </a>

                <div class="form-group mt-3 mb-3 tfa-input d-flex gap-2 justify-content-center">
                </div>
            `
        );

        // -- Add the modal to a div
        const modal_div = document.createElement('div');
        modal_div.innerHTML = modal;

        // -- Add the modal to the DOM
        document.body.appendChild(modal_div);

        // -- Get the tfa input
        const tfa_input = modal_div.querySelector('.tfa-input') as HTMLDivElement;

        // -- Get the buttons
        const yes_btn = modal_div.querySelector('.yes') as HTMLButtonElement,
            no_btn = modal_div.querySelector('.no') as HTMLButtonElement;
        yes_btn.disabled = true;

        let otp = '';
        handle_tfa_input(tfa_input, (code) => {
            otp = code;
            yes_btn.disabled = false;
        }, () => {
            yes_btn.disabled = true;
        });
        
        // -- Add the event listeners
        yes_btn.addEventListener('click', async () => {
            const yes_stop = attach(yes_btn);
            const res = await verify_tfa(access_key, otp);

            // -- Check if we got an error
            if (res.code === 401) {
                // -- Stop the spinner
                yes_stop();

                // -- Show the error
                create_toast('error', 'Oops, there appears to be an error', 'The code you entered is invalid');
                return;
            }
            else if (res.code !== 200) {
                // -- Stop the spinner
                yes_stop();

                // -- Show the error
                create_toast('error', 'Oops, there appears to be an error', res.message);
                return;
            };

            // -- Alert the user
            create_toast('success', 'Success', 'Two factor authentication has been enabled');
            set_mfa(true);
            modal_div.remove();
            stop_spinner();
        });

        no_btn.addEventListener('click', () => {
            modal_div.remove();
            stop_spinner();
        });
    };
};

function construct_qr_url(
    secret: string,
    issuer: string,
    account: string,
): {
    url: string;
    otp: string;
} {
    // -- Construct the url
    const otp = `otpauth://totp/${issuer} (${account})?secret=${secret}&issuer=${issuer}`;
    const url = `https://chart.googleapis.com/chart?chs=250x250&chld=L|0&cht=qr&chl=${otp}`;

    return {
        url,
        otp,
    }
}

export function handle_tfa_input(
    parent_elm: HTMLElement,
    complete: (code: string) => void,
    invalid: () => void,
) {
    const check = () => {
        // -- Check if the code is valid
        const code = Array.from(parent_elm.querySelectorAll('input')).map((i) => i.value)
        if (code.length === inputs) {
            if (code.every((i) => !isNaN(parseInt(i)))) complete(code.join(''));
            else invalid();
        }
        else invalid();
    };

    const inputs = 6;

    for (let i = 0; i < inputs; i++) {
        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('name', 'tfa');
        input.setAttribute('maxlength', '1');
        input.setAttribute('autocomplete', 'off');
        input.setAttribute('autocorrect', 'off');
        input.setAttribute('autocapitalize', 'off');
        input.setAttribute('spellcheck', 'false');
        input.setAttribute('pattern', '[0-9]*');
        input.setAttribute('inputmode', 'numeric');

        input.style.caretColor = 'transparent';
        input.style.width = '3rem';

        input.classList.add('form-control');
        input.classList.add('text-center');
        input.classList.add('form-control-lg');
        input.classList.add('inp');

        // -- Add the event listener
        input.addEventListener('keyup', (e) => {
            const elm = e.target as HTMLInputElement;
            
            switch (e.key) {
                // -- Backspace
                case 'Backspace':
                    const prev = elm.previousElementSibling as HTMLInputElement;
                    if (prev) prev.focus();
                    check(); 
                    return;

                // -- Arrow keys
                case 'ArrowLeft':
                    const prev2 = elm.previousElementSibling as HTMLInputElement;
                    if (prev2) prev2.focus();
                    return;

                case 'ArrowRight':
                    const next2 = elm.nextElementSibling as HTMLInputElement;
                    if (next2) next2.focus();
                    return;
            }

            // -- Check if the value is a number
            if (isNaN(parseInt(e.key)))
                return elm.value = '';
            
            // -- Set the value to the first character
            elm.value = e.key;

            // -- Check if the code is valid
            check();    

            // -- Move to the next input
            const next = elm.nextElementSibling as HTMLInputElement;
            if (next) next.focus();
        });

        // -- Add the input to the parent
        parent_elm.appendChild(input);

        // -- Watch for paste
        input.addEventListener('paste', (e) => {
            e.preventDefault();
            const paste = (e.clipboardData.getData('text/plain') as string).slice(0, inputs);

            for (let i = 0; i < paste.length; i++) {
                const char = paste.charAt(i);
                if (isNaN(parseInt(char))) continue;

                const elm = parent_elm.querySelectorAll('input')[i] as HTMLInputElement;
                elm.value = char;
            }
        });
    }
}

function set_mfa(value: boolean){
    // -- Get all the elements with the data attribute
    const elements = document.querySelectorAll('[data-has-tfa]');

    // -- Loop through the elements
    for (let i = 0; i < elements.length; i++) {
        const elm = elements[i] as HTMLElement;

        // -- Set the attribute
        elm.setAttribute('data-has-tfa', value ? 'true' : 'false');
    }
}