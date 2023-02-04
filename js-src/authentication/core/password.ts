import { passwordStrength } from 'check-password-strength'

export const attach_to_input = (input: HTMLInputElement) => {
    let last_strength = '0';

    // -- Attach the event listener
    input.addEventListener('keyup', () => {
        // -- Get the password strength
        const strength = passwordStrength(input.value);
        last_strength = strength.id.toString();

        // -- Set the data-strength attribute
        input.setAttribute('data-strength', last_strength);
    });


    // -- if the input is unfocused, remove the data-strength attribute
    input.addEventListener('blur', () => {
        input.removeAttribute('data-strength');
    });

    // -- If the input is focused, set the data-strength attribute
    input.addEventListener('focus', () => {
        input.setAttribute('data-strength', last_strength);
    });
}