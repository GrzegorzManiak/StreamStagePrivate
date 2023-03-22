import { create_toast } from '../common';

export function get_or_error<e>(element: HTMLElement, attribute: string): e {
    const value = element.getAttribute(attribute);
    if (!value) {
        create_toast('error', 'Configuration Error', `No ${attribute} found, please reload the page`);
        // -- Wait 3 seconds and reload the page
        setTimeout(() => {
            window.location.reload();
        }, 3000);
    }
    return value as unknown as e;
}

const config = document.getElementById('config');
export const configuration = {
    csrf_token: get_or_error<string>(config, 'data-csrf-token'),
    recent_verification: get_or_error<string>(config, 'data-recent-verification'),
    resend_verification: get_or_error<string>(config, 'data-resend-verification'),
}