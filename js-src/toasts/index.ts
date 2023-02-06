// -- Lets get the root toasts element
const toasts = document.getElementById('toasts');
if (!toasts) throw new Error('No toasts element found');

export type ToastType = 'error' | 'success' | 'warning';

// -- Create a toast
export const create_toast = (type: ToastType, title: string, message: string) => {
    // -- Create the toast element
    const toast = document.createElement('div');
    toast.classList.add('toast', 'show', 'mb-2');
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    // -- Create the toast header
    const toast_header = document.createElement('div');
    toast_header.classList.add('toast-header', 'rounded-2');

    // -- Create the badge
    const badge = document.createElement('span');
    badge.classList.add('badge', `bg-${type === 'error' ? 'danger' : type}`);
    badge.style.marginRight = '0.5rem';
    switch (type) {
        case 'error': badge.innerText = 'Error'; break;
        case 'success': badge.innerText = 'Success'; break;
        case 'warning': badge.innerText = 'Warning'; break;
    }

    // -- Create the toast title
    const toast_title = document.createElement('strong');
    toast_title.classList.add('me-auto');
    toast_title.innerText = title;

    // -- Create the close button
    const close_button = document.createElement('button');
    close_button.classList.add('btn-close');
    close_button.setAttribute('data-bs-dismiss', 'toast');
    close_button.setAttribute('aria-label', 'Close');

    close_button.addEventListener('click', () => {
        // -- Animate the toast out
        unanimate_toast(toast);
    });

    // -- Add the close button to the toast header
    toast_header.appendChild(badge);
    toast_header.appendChild(toast_title);
    toast_header.appendChild(close_button);

    // -- Create the toast body
    const toast_body = document.createElement('div');
    toast_body.classList.add('toast-body', 'rounded-2');
    toast_body.innerText = message;

    // -- Add the toast header and body to the toast
    toast.appendChild(toast_header);
    toast.appendChild(toast_body);

    // -- Add the toast to the toasts element
    toasts.appendChild(toast);

    // -- Animate the toast
    animate_toast(toast);

    // -- After 5 seconds, remove the toast
    setTimeout(() => {
        unanimate_toast(toast);
    }, 5000);
}


async function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}


async function animate_toast(toast: HTMLDivElement) {
    // -- We want to animate the height of the toast
    //    and its opacity
    const height = toast.offsetHeight;

    // -- Set the height and opacity to 0
    toast.style.height = '0px';
    toast.style.opacity = '0';

    // -- Show the toast
    toast.style.display = 'block';
    toast.classList.add('show');

    // -- Animate the height and opacity
    const animation_length = 500;
    
    // -- Animate the height
    while (toast.offsetHeight < height) {
        toast.style.height = `${toast.offsetHeight + 1}px`;
        toast.style.opacity = `${toast.offsetHeight / height}`;

        await sleep(animation_length / height);
    }
}

async function unanimate_toast(toast: HTMLDivElement) {
    // -- We want to animate its opacity 
    const animation_length = 500;

    // -- Animate the height
    while (Number(toast.style.opacity) > 0.1) {
        toast.style.opacity = `${Number(toast.style.opacity) - 0.01}`;
        await sleep(animation_length / 100);
    }

    // -- Hide the toast
    toast.style.display = 'none';
    toast.classList.remove('show');

    // -- Remove the toast from the DOM
    toast.remove();
}