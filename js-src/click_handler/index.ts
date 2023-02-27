// 
// All this function dose is that it changes the text of the button to a spinner
// whilst retaining the original text.
export function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}



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



export function construct_modal(
    title: string,
    message: string,
    buttons: boolean,
    custom: string = '',
) {
    const buttons_template = `
        <!-- Continue -->
        <button type="submit" class="btn yes btn-danger btn-lg w-100">
            Continue
        </button>


        <!-- Cancel button -->
        <button class="btn btn-secondary no btn-lg mt-3 w-100">
            Go back
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
                    class="modal-content bg-dark text-light p-5 rounded"
                    style="width: 500px;"
                >

                    <!-- Header -->
                    <div class="mb-5 justify-content-start header">
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
                    <div class="d-flex justify-content-lg-start justify-content-center flex-column buttons">
                        ${buttons ? buttons_template : ''}
                    </div>
                </div>
            </div>
        </div>
    `;
}



export function confirmation_modal(
    yes: () => void | Promise<void>,
    no: () => void | Promise<void>,
    message: string,
    title: string = 'Are you sure?',
) {
    // -- String template for the modal
    const modal = construct_modal(title, message, true);

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