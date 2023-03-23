import { Type, build_configuration } from '../api/config';
import { ToastType } from './index.d';


// -- Get the global configuration
export const configuration = build_configuration<{
    add_payment: string,
    get_payments: string,
    remove_payment: string,
}>({
    add_payment: new Type('data-add-payment', 'string'),
    get_payments: new Type('data-get-payments', 'string'),
    remove_payment: new Type('data-remove-payment', 'string'),
});



/**
 * @name sleep
 * 
 * @param ms: number - The number of milliseconds to sleep
 * @returns A promise that resolves after the specified number of milliseconds
 * 
 * @description This function sleeps for the specified number of milliseconds
 */
export function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}



/**
 * @name attach
 * 
 * @param button: HTMLButtonElement - The button to attach the spinner to
 * @returns A function that will revert the button to its original state
 * 
 * @description This function attaches a spinner to the button and disables
 *              the button, it returns a function that will revert the button    
 *              to its original state.
 */
export function attach(
    button: HTMLButtonElement,
): () => Promise<void> {
    // -- Disable the button
    button.disabled = true;

    // -- Set the 'loader-state' attribute to 'hide-text'
    button.setAttribute('loader-state', 'hide-text');

    // -- Return a function that will revert the button to its original state
    return () => {
        return new Promise(async (resolve) => {
            // -- Sleep for 1 second
            await sleep(1000);

            // -- Change the 'loader-state' attribute to 'show-text'
            button.setAttribute('loader-state', 'show-text');

            // -- Enable the button
            button.disabled = false;
            
            // -- Resolve the promise
            resolve();
        });
    };
}



/**
 * @name construct_modal
 * 
 * @param title: string - The title of the modal
 * @param message: string - The message of the modal
 * @param buttons: boolean - Whether or not to show the buttons (Continue, Cancel)
 * @param button: color - The color of the buttons (Continue, Cancel)
 * @param custom: string - Custom HTML to add to the modal (optional)
 * @returns A string template for the modal
 * 
 * @description This function constructs a string template for a modal
 *              that can be used to show a message to the user   
 */
export function construct_modal(
    title: string,
    message: string,
    buttons: boolean,
    color: 'danger' | 'success' | 'warning' | 'info' | 'secondary' | 'primary' | 'light' | 'dark',
    custom: string = '',
) {
    const buttons_template = `
        <!-- Continue -->
        <button type="submit" class="btn yes btn-${color} btn-lg w-75">
            Continue
        </button>

        <!-- Continue -->
        <button type="submit" class="btn no btn-danger btn-lg w-25 error">
            Cancel
        </button>
    `;



    // -- String template for the modal
    return `
        <div
            style="z-index: 9999; position: fixed; top: 0; left: 0; width: 100vw;
                height: 100vh; background-color: rgba(0, 0, 0, 0.5);">

            <!-- Modal -->
            <div class="modal d-flex justify-content-center align-items-center"
                style="z-index: 9999; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                background-color: rgba(0, 0, 0, 0.5);">

                <!-- Modal content -->
                <div 
                    class="modal-content bg-dark text-light rounded
                    p-xxl-5 p-xl-5 p-lg-5 p-md-3 p-sm-3 p-2"
                    style="width: 500px;"
                >

                    <!-- Header -->
                    <div class="mb-2 justify-content-start header">
                        <!-- Header -->
                        <h1 class="fw-bold ">${title}</h1>

                        <!-- Descriptiopn -->
                        <p class="text-muted">${message}</p>
                    </div>
                    
                    <!-- Custom -->
                    <div class="d-flex justify-content-lg-start justify-content-center flex-column custom">
                        ${custom ? custom : ''}
                    </div>
                    
                    <!-- Buttons -->
                    <div class="justify-content-lg-start justify-content-center d-flex buttons w-100 pop-up-buttons">
                        ${buttons ? buttons_template : ''}
                    </div>
                </div>
            </div>
        </div>
    `;
}



/**
 * @name confirmation_modal
 * 
 * @param yes: () => void | Promise<void> - The function to call if the user clicks 'Continue'
 * @param no: () => void | Promise<void> - The function to call if the user clicks 'Cancel'
 * @param message: string - The message of the modal
 * @param title: string - The title of the modal (optional)
 *  
 * @description This function creates a modal that asks the user to confirm
 *              an action, if the user clicks 'Continue' the yes function is
 *              called, if the user clicks 'Cancel' the no function is called.
 *              quite simple.
 */
export function confirmation_modal(
    yes: () => void | Promise<void>,
    no: () => void | Promise<void>,
    message: string,
    title: string = 'Are you sure?',
) {
    // -- String template for the modal
    const modal = construct_modal(title, message, true, 'danger');

    // -- Create a div element
    const div = document.createElement('div');

    // -- Set the innerHTML of the div to the modal
    div.innerHTML = modal;

    // -- Get the buttons
    const yes_btn = div.querySelector('.yes') as HTMLButtonElement,
        no_btn = div.querySelector('.no') as HTMLButtonElement;

    // -- Add the event listeners
    yes_btn.addEventListener('click', async() => {
        // -- Call the yes function
        yes();

        // -- Remove the modal
        div.remove();
    });

    no_btn.addEventListener('click', async() => {
        // -- Call the no function
        no();

        // -- Remove the modal
        div.remove();
    });

    // -- Append the modal to the body
    document.body.appendChild(div);
}



/**
 * @name handle_tfa_input
 * 
 * @param parent_elm: HTMLElement - The parent element of the inputs
 * @param complete: (code: string) => void - The function to call when the user has entered a valid code
 * @param invalid: () => void - The function to call when the user has entered an invalid code
 * 
 * @description This function handles the input of a TFA code
 */
export function handle_tfa_input(
    parent_elm: HTMLElement | Element,
    complete: (code: string) => void,
    invalid: () => void,
) {
    const inputs = 6;

    const check = () => {
        // -- Check if the code is valid
        const code = Array.from(parent_elm.querySelectorAll('input')).map((i) => i.value)
        if (code.length === inputs) complete(code.join(''));
        else invalid();
    };

    for (let i = 0; i < inputs; i++) {
        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('name', 'tfa');
        input.setAttribute('maxlength', '1');
        input.setAttribute('autocomplete', 'off');
        input.setAttribute('autocorrect', 'off');
        input.setAttribute('autocapitalize', 'off');
        input.setAttribute('spellcheck', 'false');
        input.setAttribute('pattern', '[0-9a-zA-Z]*');

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
            
            // -- Set the value to the first character
            elm.value = e.key.charAt(0);

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



/**
 * @name create_toast
 * 
 * @param type: ToastType - The type of toast to create EG, error, success, warning
 * @param title: string - The title of the toast
 * @param message: string - The message of the toast
 * @param close_after: number - The amount of time to wait before closing the toast
 * @param closed: () => void - The function to call when the toast is closed
 * 
 * @returns void
 * 
 * @description This function creates a toast and appends it to the DOM
 *              it also handles the removal of the toast after x seconds.
 *              This function is used to show the user that something
 *              has happened.
 */
export const create_toast = (
    type: ToastType, 
    title: string, 
    message: string,
    close_after: number = 5000,
    closed: () => void = () => {},
) => {
    // -- Lets get the root toasts element
    const toasts = document.getElementById('toasts');
    if (!toasts) throw new Error('No toasts element found');

    const toast = `
        <div 
            toast-type='${type}'
            class='
                toast
                d-flex
                align-items-center
                justify-content-start
            '
        >
            <!-- Icon, pinned to the top -->
            <div class='toast-icon col-1'>
                <i class="fa-regular fa-circle-check" icon='success'></i>
                <i class="fa-solid fa-triangle-exclamation" icon='warning'></i>
                <i class="fa-solid fa-exclamation" icon='error'></i>
                <i class="fa-solid fa-circle-info" icon='info'></i>
            </div>

            <!-- Content -->
            <div class='toast-content col-9'>
                <p class='toast-content-header m-0'>${title}</p>
                <p class='toast-content-text m-0'>${message}</p>
                <p class='toast-content-time m-0'>Now</p>
            </div>

            <!-- Close button -->
            <div class='toast-close col-2'>
                <i class="fa-solid fa-times"></i>
            </div>
        </div>
    `;

    // -- Add the toast to the toasts element
    const new_toast = document.createElement('div');
    new_toast.innerHTML = toast;

    // -- Get the close button and time
    const close_button = new_toast.querySelector('.toast-close'),
            time = new_toast.querySelector('.toast-content-time') as HTMLParagraphElement;


    const time_created = new Date();

    // -- For the life of the toast, update the time
    const time_interval = setInterval(() => {
        time.innerText = moment(time_created);
    }, 1000);


    // -- Add the close button event listener
    close_button.addEventListener('click', () => {
        unanimate_toast(new_toast, toasts);
        clearInterval(time_interval);
        closed();
    });

    // -- Close the toast after x seconds
    setTimeout(() => {
        unanimate_toast(new_toast, toasts);
        clearInterval(time_interval);
        closed();
    }, close_after);

    // -- Add the toast to the toasts element
    toasts.appendChild(new_toast);
}



/**
 * @name unanimate_toast
 * 
 * @param toast: HTMLDivElement - The toast to animate
 * 
 * @returns void
 * 
 * @description This function animates the toast out
 *              and then removes it from the DOM
 */
async function unanimate_toast(
    toast: HTMLDivElement,
    toasts: HTMLElement,
) {
    // -- We want to animate its opacity 
    const animation_length = 1000;

    // -- Add the animation class
    toast.classList.add('toast-out');
    const child = toast.children[0] as HTMLDivElement,
        computed_style = getComputedStyle(child),
        margin = computed_style.getPropertyValue('margin-bottom');

    const toast_height = toast.offsetHeight + parseInt(margin);

    // -- Animate the rest of the toasts
    const toasts_children = toasts.children;
    const toast_index = Array.from(toasts_children).indexOf(toast);

    // -- Check if the child is animating
    if (toast.style.animation) 
        toast.style.animation = '';

    // -- Animate the rest of the toasts
    for (let i = 0; i < toasts_children.length; i++) {
        const child = toasts_children[i] as HTMLDivElement;
        if (i <= toast_index) continue;
        if (child.classList.contains('toast-out')) continue;

        // --toast-adjust-height
        child.style.setProperty('--toast-adjust-height', `-${toast_height}px`);
        child.style.animation = `toast_adjust ${animation_length}ms ease-in-out`;
    }

    // -- Sleep for the animation length
    await sleep(animation_length);
    toast.classList.remove('toast-out');


    for (let i = 0; i < toasts_children.length; i++) {
        const child = toasts_children[i] as HTMLDivElement;
        if (i <= toast_index) continue;
        child.style.animation = '';
    }

    
    // -- Remove the toast from the DOM
    toast.remove();
}



/**
 * @name moment
 * 
 * @param date: Date - The date to format
 *
 * @returns string - The formatted date
 * 
 * @description This function formats a date to a
 *              more human-readable format
 *              
 *              For example, if the date is 5 minutes ago,
 *              it will return '5 minutes ago'    
 */ 
export function moment(date: Date): string {
    // -- Get the time difference in milliseconds
    const diff = (Date.now() - date.getTime()) / 1000;
  
    // -- Define the thresholds for different time intervals
    const thresholds = [
        { threshold: 0, label: 'Just now' }, // -- 1 second
        { threshold: 60 * 1000, label: 'A few seconds ago' }, // -- 1 minute
        { threshold: 60 * 60 * 1000, label: 'A few minutes ago' }, // -- 1 hour
        // -- Im not using the below two thresholds, but i added them anyway
        //    As i MIGHT use them for something else later
        { threshold: 24 * 60 * 60 * 1000, label: 'A few hours ago' }, // -- 1 day
        { threshold: 7 * 24 * 60 * 60 * 1000, label: 'A few days ago' }, // -- 1 week
        { threshold: Infinity, label: 'A while ago' }, // -- 1 week
    ];
  
    // -- Find the first threshold that the time difference is less than or equal to
    const { label } = thresholds.find(({ threshold }) => diff <= threshold) || thresholds[thresholds.length - 1];
    return label;
}