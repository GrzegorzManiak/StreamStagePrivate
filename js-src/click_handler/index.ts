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
