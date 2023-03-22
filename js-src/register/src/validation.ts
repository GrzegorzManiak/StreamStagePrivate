export const validate_password = (password: string): Array<String> => {
    let errors = [];
    
    // -- Must be between 8 and 64 characters
    // -- Must contain at least one number
    // -- Must contain at least one uppercase letter
    // -- Must contain at least one lowercase letter
    // -- Must not contain any spaces

    if (password.length < 8 || password.length > 64) errors.push('length');
    if (!password.match(/\d/)) errors.push('number');
    if (!password.match(/[A-Z]/)) errors.push('uppercase');
    if (!password.match(/[a-z]/)) errors.push('lowercase');
    if (password.match(/\s/)) errors.push('spaces');

    return errors;
}

export const validate_name = (name: string): Array<String> => {
    let errors = [];

    // -- Must be between 3 and 20 characters
    // -- Must Start with a letter
    // -- Must only contain letters, numbers, and underscores
    // -- Must not contain two underscores in a row
    // -- Must not end with an underscore

    if (name.length < 3 || name.length > 20) errors.push('length');
    if (!name.match(/^[a-zA-Z]/)) errors.push('start');
    if (!name.match(/^\w+$/)) errors.push('characters');
    if (name.match(/__+/)) errors.push('double-underscore');
    if (name.match(/_$/)) errors.push('end-underscore');

    return errors
}



//
// This function is used to monitor the strength of a password
// and display the strength to the user in real time.
//
export const password_monitor = (
    input: HTMLInputElement,
    proxy: Element | null = null
) => {
    if (proxy === null) proxy = input;

    const validity = () => {
        let password = validate_password(input.value);
        let errors = ['length', 'number', 'uppercase', 'lowercase', 'spaces'];

        password.forEach((error) => {
            proxy.setAttribute(`data-error-${error}`, '');
        });

        // -- Remove any errors that are not present
        errors.forEach((error) => {
            if (!password.includes(error)) proxy.removeAttribute(`data-error-${error}`);
        });

        if (password.length === 0) return '3';
        if (password.length === 1) return '2';
        if (password.length === 2) return '1';
        if (password.length === 3) return '0';
        if (password.length === 4) return '0';
    };

    // -- Attach the event listener
    input.addEventListener('keyup', () => {
        input.setAttribute('data-strength', validity());
    });

    // -- if the input is unfocused, remove the data-strength attribute
    input.addEventListener('blur', () => {
        proxy.removeAttribute('data-strength');
    });

    // -- If the input is focused, set the data-strength attribute
    input.addEventListener('focus', () => {
        proxy.setAttribute('data-strength', validity());
    });

    // -- Detect browser autofill
    input.addEventListener('input', () => {
        if (input.value.length > 0) input.setAttribute('data-strength', validity());
    });
}



//
// This function is used to ensure that the name is valid and
// meets all criteria, and then sets the data-error-* attributes
// on the input element to show the user what is wrong with their
// name.
//
export const name_monitor = (input: HTMLInputElement) => {
    const validity = () => {
        let name = validate_name(input.value);
        let errors = ['length', 'start', 'characters', 'double-underscore', 'end-underscore'];

        name.forEach((error) => {
            input.setAttribute(`data-error-${error}`, '');
        });

        // -- Remove any errors that are not present
        errors.forEach((error) => {
            if (!name.includes(error)) input.removeAttribute(`data-error-${error}`);
        });
        
        if (name.length === 0) return '3';
    }


    // -- Attach the event listener
    input.addEventListener('keyup', () => {
        input.setAttribute('data-strength', validity());
    });

    // -- if the input is unfocused, remove the data-strength attribute
    input.addEventListener('blur', () => {
        input.removeAttribute('data-strength');
    });

    // -- If the input is focused, set the data-strength attribute
    input.addEventListener('focus', () => {
        input.setAttribute('data-strength', validity());
    });

    // -- Detect browser autofill
    input.addEventListener('input', () => {
        if (input.value.length > 0) input.setAttribute('data-strength', validity());
    });
}



// 
// This function monitors the password input and the repeat password input
// and ensures that they match.
// 
export const rp_password_monitor = (
    password_input: HTMLInputElement,
    rp_password_input: HTMLInputElement
) => {
    const passwords_match = () => {
        if (password_input.value === rp_password_input.value) {
            rp_password_input.setAttribute('data-strength', '3');
            return true;
        } else {
            rp_password_input.setAttribute('data-strength', '0');
            return false;
        }
    }


    // -- Attach the event listener
    rp_password_input.addEventListener('keyup', () => {
        passwords_match();
    });

    // -- if the input is unfocused, remove the data-strength attribute
    rp_password_input.addEventListener('blur', () => {
        rp_password_input.removeAttribute('data-strength');
    });

    // -- If the input is focused, set the data-strength attribute
    rp_password_input.addEventListener('focus', () => {
        passwords_match();
    });

    // -- Detect browser autofill
    rp_password_input.addEventListener('input', () => {
        if (rp_password_input.value.length > 0) passwords_match();
    });
}