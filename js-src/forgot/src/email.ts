import { show_panel } from '..';
import { ResendVerification } from '../../api/index.d';
import { check_email_verification, resend_verification } from '../../api';
import { attach, create_toast } from '../../common';
import { reset_pass_handler } from './reset';


export async function email_verification(
    resend_button: HTMLButtonElement,
    verify_token: string,
    resend_token: string,
    access_token: string,
): Promise<void> {
    // -- Get the clock element and the resned button
    const clock = document.querySelector('.clock') as HTMLDivElement,
        resend = document.querySelector('#email-resend-btn') as HTMLButtonElement;

    // -- Start the timer 
    let time = 60 * 15; // 15 minutes
    const timer = setInterval(() => {
        time -= 1;

        const min = Math.floor(time / 60),
            sec = (time % 60) < 10 ? `0${time % 60}` : time % 60;
        clock.innerText = `${min}:${sec}`;

        // -- If the timer is done, stop it
        if (time <= 0) {
            clearInterval(timer);
            clock.innerText = '0:00';
            resend.disabled = true;
            show_panel('forgot');

            // -- Show the toast
            create_toast('warning', 'Authentication', 'The verification code has expired');
        }
    }, 1000);



    // -- Start listening for the verification code
    check_email_verification(() => verify_token).then(async () => {
        
        // -- Stop the timer
        clearInterval(timer);
        clock.innerText = '0:00';
        show_panel('reset_pass');
        reset_pass_handler(access_token);
    });


    // -- Add the event listener to the resend button
    resend_button.addEventListener('click', async () => {
        const stop_spinner = attach(resend_button);
        const res = await resend_verification(resend_token);
        if (res.code !== 200) {
            create_toast('error', 'Authentication', 'Failed to resend the verification code');
            return stop_spinner();
        }

        create_toast('success', 'Authentication', 'The verification code has been resent');
        const data = (res as ResendVerification).data;
        verify_token = data.verify;
        resend_token = data.token;
        time =60 * 15;
        stop_spinner();
    });
}