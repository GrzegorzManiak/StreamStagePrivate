// 
// All this function dose is that it changes the text of the button to a spinner
// whilst retaining the original text.
export function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 
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