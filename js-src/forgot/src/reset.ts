import { attach, create_toast } from "../../common";
import { rp_password_monitor, validate_password } from "../../register/src/validation";
import { change_pass } from "../api";

export async function reset_pass_handler(
    access_token: string,
) {
    // -- Get the password inputs 
    const password_input = document.querySelector('input[name="password"]') as HTMLInputElement,
        rp_password_input = document.querySelector('input[name="rp-password"]') as HTMLInputElement,
        reset_button = document.querySelector('#reset-btn') as HTMLButtonElement;

    rp_password_monitor(password_input, rp_password_input);

    // -- Add the event listners to the inputs
    const check_inputs = () => {
        if (password_input.value.trim() === '' || 
            rp_password_input.value.trim() === ''
        ) reset_button.disabled = true; 
        else reset_button.disabled = false;
    }

    password_input.addEventListener('input', () => check_inputs());
    rp_password_input.addEventListener('input', () => check_inputs());

    // -- Add the event listener to the button
    reset_button.addEventListener('click', async () => {
        const stop_spinner = attach(reset_button);
        const password_valid = validate_password(password_input.value);

        // -- Make sure the password is valid
        if (password_valid.length > 0) {
            create_toast('error', 'Password', 'Oops! It looks like your password is invalid.');
            return await stop_spinner();
        }

        // -- Make sure the passwords match
        if (password_input.value !== rp_password_input.value) {
            create_toast('error', 'Passwords', 'Oops! It looks like your passwords don\'t match.');
            return await stop_spinner();
        }

        // -- Attempt to make the request
        console.log(access_token);
        const res = await change_pass(
            access_token,
            password_input.value
        );

        // -- Handle the response
        if (res.code !== 200) {
            create_toast('error', 'Reset Password', res.message);
            return await stop_spinner();
        }

        // -- Redirect to the login page
        create_toast('success', 'Reset Password', res.message);
        await new Promise((resolve) => setTimeout(resolve, 2000));
        window.location.href = '/login';
    });
}